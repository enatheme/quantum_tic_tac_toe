import math

def number_of_winning_position(n: int) -> int:
    return int(2 * math.sqrt(n) + 2)

def generate_identity(n: int):
    m = []
    width = int(math.pow(2, n))
    for i in range(width):
        in_m = [0] * width
        in_m[i] = 1
        m.append(in_m)

    return m

# flip the target qubit if in the n control qubit, at least 1 is set to 1
def at_least_one_matrix(n: int):
    number_qubits = n + 1 # the target
    width = int(math.pow(2, number_qubits))
    m = generate_identity(number_qubits)
    
    # move the row to form a OR matrix
    j = 1
    for i in range(1 + int(width / 2), width):
        m[i], m[j] = m[j], m[i]
        j += 1

    return m

def check_even_play(n: int):
    assert(n % 2 == 0) # verify it is possible
    number_qubits = n + 1 # the target
    width = int(math.pow(2, number_qubits))
    m = generate_identity(number_qubits)

    # move the row to form a "even play" matrix
    j = 0
    control = 0
    for i in range(int(width / 2), width):
        # a little bit dirty, but flag if # 1 and 0 match
        if bin(control).count('1') == (n / 2):
            m[i], m[j] = m[j], m[i]
        j += 1
        control += 1

    return m


def check_one_more_zero(n: int):
    assert(n % 2 != 0) # verify it is possible
    number_qubits = n + 1 # the target
    width = int(math.pow(2, number_qubits))
    m = generate_identity(number_qubits)

    # move the row to form a "one more 0" matrix
    j = 0
    control = 0
    for i in range(int(width / 2), width):
        # a little bit dirty, but flag if # 0 is + 1 # 1 match
        if bin(control).count('1') == ((n  - 1)/ 2):
            m[i], m[j] = m[j], m[i]
        j += 1
        control += 1

    return m

def check_one_more_one(n: int):
    assert(n % 2 != 0) # verify it is possible
    number_qubits = n + 1 # the target
    width = int(math.pow(2, number_qubits))
    m = generate_identity(number_qubits)

    # move the row to form a "one more 1" matrix
    j = 0
    control = 0
    for i in range(int(width / 2), width):
        # a little bit dirty, but flag if # 1 is + 1 # 0 match
        if bin(control).count('1') == ((n + 1)/ 2):
            m[i], m[j] = m[j], m[i]
        j += 1
        control += 1

    return m


def is_valid(vector) -> bool:
    # check vector represent a square matrix
    if math.modf(math.sqrt(len(vector)))[0] > 0:
        raise Exception('Input vector does not represent a square matrix')
    count_0 = 0
    count_1 = 0
    for v in vector:
        if v == '0':
            count_0 += 1
        elif v == '1':
            count_1 += 1
        elif v == ' ':
            None
        else:
            raise Exception('Value is unknown')
    return (abs(count_0 - count_1) < 2)

def winner_list(width):
    winner_list = []
    # checking horizontal
    for i in range(0, width):
        temp_list = []
        for elem in range(0, width):
            temp_list.append(i + width * elem)
        winner_list.append(temp_list)

    # checking vertical
    for i in range(0, width):
        temp_list = []
        for elem in range(0, width):
            temp_list.append(i * width + elem)
        winner_list.append(temp_list)

    # checking diagonal "top left to bottom right"
    temp_list = []
    for i in range(0, width):
        temp_list.append(width * (i + 1) - (width - i))
    winner_list.append(temp_list)

    # checking diagonal "top right to bottom left"
    temp_list = []
    for i in range(0, width):
        temp_list.append(width * (i + 1) - i - 1)
    winner_list.append(temp_list)

    return winner_list

# expected that the vector is already accepted by is_valid
# the number of "winner" configuration are 2 sqrt(n) + 2
def is_winner(vector) -> bool:
    width = int(math.sqrt(len(vector)))
    # checking horizontal
    for i in range(0, width):
        is_winning = True
        for elem in range(0, width):
            if vector[i + width * elem] != '1':
                is_winning = False
        if is_winning:
            return True

    # checking vertical
    for i in range(0, width):
        is_winning = True
        for elem in range(0, width):
            if vector[i * width + elem] != '1':
                is_winning = False
        if is_winning:
            return True

    # checking diagonal "top left to bottom right"
    is_winning = True
    for i in range(0, width):
        if vector[i * i - 1] != '1':
            is_winning = False
    if is_winning:
        return True

    # checking diagonal "top right to bottom left"
    is_winning = True
    for i in range(0, width):
        if vector[width * i - i] != '1':
            is_winning = False
    if is_winning:
        return True
