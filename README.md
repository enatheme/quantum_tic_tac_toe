# quantum_tic_tac_toe
Tic Tac Toe quantum solver

This project is part of the QOSF mentorship application.
The algorithm returns a winning play with the 'X' versus '0'.
It uses Grover's algorithm with Qiskit SDK.

Usage:
- q_tt(input_vector)
Where input_vector is a list of character with alphabet '0' (ennemi play), '1' (our play), ' ' (not played).
Exemple: ['1', '0', '0', '1', ' ', ' ', '0', ' ', ' ']
The list must be a valid tic tac toe grid.
Returns a quantum circuit.

 - display(qc)
Where qc is a quantum circuit.

 - run_it(qc)
Where qc is a quantum circuit. (quite slow, ~30 minutes on IBMQ simulator)

A usage example can be found in the Jupyter notebook
