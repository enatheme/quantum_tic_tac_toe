import utils
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, assemble, Aer, transpile, execute, IBMQ
from qiskit.circuit import Gate
from qiskit.providers.aer import QasmSimulator
import matplotlib
import math
from typing import Union
import numpy as np

# InputVector purpose is to carry all information needed
class InputVector:
    def __init__(self, vector, start_player = '0'):
        self.size = len(vector)
        self.width = int(math.sqrt(self.size))
        self.payload = vector
        self.x_list = self.read_vector(vector, '1')
        self.o_list = self.read_vector(vector, '0')
        self.unknown_list = self.read_vector(vector, ' ')
        self.known_size = len(self.x_list) + len(self.o_list)
        self.unknown_size = len(self.unknown_list)

        self.winning_list = utils.winner_list(self.width)
        self.winning_list_size = len(self.winning_list)
        self.start_player = start_player

    def read_vector(self, vector, char):
        l = []
        for i, elem in enumerate(vector):
            if elem == char:
                l.append(i)
        return l

def init_grid(vector, to_gate: bool = False) -> Union[Gate, QuantumCircuit]:
    qc = QuantumCircuit(vector.size)
    for i in vector.x_list:
        qc.x(i)
    for i in vector.unknown_list:
        qc.h(i)
    if not to_gate:
        qc.barrier()

    if to_gate:
        return qc.to_gate(label = "state initialization")
    else:
        return qc

# the oracle consist in 4 parts
# - check all possible winning position (8 possibilities for a 3 x 3 tic tac toe)
# - OR on all above checks (at least a winning position is reachable)
# - all players play (no "I play all position" answer)
# - AND on the part 2 and 3
def oracle(vector, to_gate: bool = False) -> Union[Gate, QuantumCircuit]:
    qr_input = QuantumRegister(vector.size)
    qr_clauses = QuantumRegister(vector.winning_list_size)
    qr_at_least_a_clause = QuantumRegister(1)
    qr_valid_play = QuantumRegister(1)
    qr_kickback = QuantumRegister(1)
    qc = QuantumCircuit(qr_input, qr_clauses, qr_at_least_a_clause, qr_valid_play, qr_kickback)

    # 1st part
    for i, elem in enumerate(vector.winning_list):
        gate = winning_elem_detection(len(elem), str(i), to_gate)
        qc.append(gate, [*elem, vector.size + i])

    # 2nd part
    qc.append(at_least_a_clause(vector.winning_list_size, to_gate), [*qr_clauses, *qr_at_least_a_clause])
    # 3rd part
    qc.append(all_players_play_detection(vector, to_gate), [*vector.unknown_list, *qr_valid_play])
    # kickback - 4th part
    qc.mct([qr_at_least_a_clause, qr_valid_play], qr_kickback)
    # 3rd part invert
    qc.append(all_players_play_detection(vector, to_gate), [*vector.unknown_list, *qr_valid_play])
    # 2nd part invert
    qc.append(at_least_a_clause(vector.winning_list_size, to_gate), [*qr_clauses, *qr_at_least_a_clause])

    # 1st part invert
    for i, elem in enumerate(vector.winning_list):
        gate = winning_elem_detection(len(elem), str(i), to_gate)
        qc.append(gate, [*elem, vector.size + i])

    if not to_gate:
        qc.barrier()

    if to_gate:
        return qc.to_gate(label = 'oracle')
    else:
        return qc.decompose()

# check if a least a qubit in the input is set to 1 (a big OR)
def at_least_a_clause(nqubits: int, to_gate: bool = False) -> Union[Gate, QuantumCircuit]:
    qr_input = QuantumRegister(nqubits)
    qr_output = QuantumRegister(1)
    qc = QuantumCircuit(qr_input, qr_output)

    qc.unitary(utils.at_least_one_matrix(nqubits), [*qr_input, qr_output])

    if to_gate:
        return qc.to_gate(label = 'check at least a winning position')
    else:
        return qc

# based on the state of the board, detect if the number of plays are correct
def all_players_play_detection(vector, to_gate: bool = False) -> Union[Gate, QuantumCircuit]:
    qr_input = QuantumRegister(vector.unknown_size)
    qr_output = QuantumRegister(1)
    qc = QuantumCircuit(qr_input, qr_output)

    # even turn
    if vector.unknown_size % 2 == 0:
        qc.unitary(utils.check_even_play(vector.unknown_size), [*qr_input, qr_output])
    # odd turn with '0' started
    elif vector.start_player == '0':
        qc.unitary(utils.check_one_more_zero(vector.unknown_size), [*qr_input, qr_output])
    # odd turn with '1' started
    else:
        qc.unitary(utils.check_one_more_one(vector.unknown_size), [*qr_input, qr_output])

    if to_gate:
        return qc.to_gate(label = f'check all players played')
    else:
        return qc

# check if the position is winning
# it could be optimized by not checking 'impossible' position (where there is a 0 at the input state)
def winning_elem_detection(width: int, label: str, to_gate: bool = False) -> Union[Gate, QuantumCircuit]:
    in_qubits = QuantumRegister(width, name = 'input')
    out_qubits = QuantumRegister(1, name = 'output')
    qc = QuantumCircuit(in_qubits, out_qubits)
    qc.mct(in_qubits, out_qubits)

    if to_gate:
        return qc.to_gate(label = f'winning_detection {label}')
    else:
        return qc

# from qiskit textbook - general groover diffuser
def diffuser(nqubits: int, to_gate: bool = False) -> Union[Gate, QuantumCircuit]:
    qc = QuantumCircuit(nqubits)
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits):
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)  # multi-controlled-toffoli
    qc.h(nqubits-1)
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)
    # We will return the diffuser as a gate
    if to_gate:
        return qc.to_gate(label = "diffusing")
    else:
        return qc

def run_it(qc: QuantumCircuit, local_simulator: bool = True):
    backend = None
    if local_simulator:
        backend = Aer.get_backend('qasm_simulator')
    else:
        IBMQ.load_account()
        provider = IBMQ.get_provider('ibm-q')
        backend = provider.get_backend('ibmq_qasm_simulator')
    job = execute(qc, backend)
    return job

def q_ttt(vector, starting_player = '0', number_of_iteration: int = 1, to_gate: bool = False) -> QuantumCircuit:
    if not utils.is_valid(vector):
        raise Exception("Number of O and X are not correct")
    vec = InputVector(vector, starting_player)
    qr_input = QuantumRegister(vec.size, name = 'input')
    qr_ancilla = QuantumRegister(vec.winning_list_size + 2, name = 'winning clause')
    qr_extra = QuantumRegister(1, name = 'extra')
    cr = ClassicalRegister(vec.unknown_size)
    qc = QuantumCircuit(qr_input, qr_ancilla, qr_extra, cr)

    for qb in qr_extra:
        qc.initialize([1, -1]/np.sqrt(2), qb)
    qc.append(init_grid(vec, to_gate), qr_input)
    for i in range(number_of_iteration):
        qc.append(oracle(vec, to_gate), [*qr_input, *qr_ancilla, *qr_extra])
        qc.barrier()
        qc.append(diffuser(vec.unknown_size, to_gate), [*vec.unknown_list])
        qc.barrier()
    qc.measure([*vec.unknown_list], cr)

    return qc

def display(qc, decompose: bool = True, display_type: str = 'text'):
    if decompose:
        print(qc.decompose().draw(display_type))
    else:
        print(qc.draw(display_type))


def tic_tac_toe(vector) -> str:
    try:
        qc = q_ttt(vector, '1')
        display(qc)
        return run_it(qc, False).get_counts()
    except:
        raise

if __name__ == '__main__':
    vector = ['1', '0', '0', '1', ' ', ' ', ' ', ' ', '1']
    print(tic_tac_toe(vector))
