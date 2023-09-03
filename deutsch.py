from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from tabulate import tabulate

def deutsch_query_gate(function):
    """
    Creates a unitary query gate from a given function f: {0,1} -> {0,1}

    Args:
        function (str): string representing one of the four possible functions
    Returns:
        gate (QuantumCircuit): quantum circuit representation of the query gate
    Raises:
        ValueError: if function is not 1, 2, 3, or 4
    Notes:
        -Uses QuantumCircuit package
    """
    if function not in ['1','2','3','4']:
        raise ValueError('Function must be 1, 2, 3, or 4')
    
    gate=QuantumCircuit(2)

    if function=='2':
        gate.cnot(0,1)
    elif function=='3':
        gate.x(1)
        gate.cnot(0,1)
    elif function=='4':
        gate.x(1)
    
    return gate


def run_deutsch_algorithm(function):
    """
    Runs the Deutsch algorithm on a quantum circuit for a specified function

    Args:
        function (str): string representing one of the four possible functions
    Returns:
        bit(int): 0 if function is constant, 1 if balanced
    Notes:
        -Uses QuantumCircuit package
    """
    qc=QuantumCircuit(2,1)
    qc.x(1)
    qc.h([0,1])

    qc.barrier()
    qc.compose(deutsch_query_gate(function), inplace=True)
    qc.barrier()

    qc.h(0)
    qc.measure(0,0)

    sim=AerSimulator()
    result=sim.run(qc,shots=1).result().get_counts()
    bit=int(list(result.keys())[0])

    return bit


def choose_function():
    """
    Presents the user with the choice of four possible functions f: {0,1} -> {0,1}

    Args:
        none
    Returns:
        user_choice (str): user's choice of function
    Notes:
        -Uses tabulate package
    """
    data1 = [[0, 0],
    [1, 0]]
    data2 = [[0, 0],
    [1, 1]]
    data3 = [[0, 1],
    [1, 0]]
    data4 = [[0, 1],
    [1, 1]]

    print(tabulate(data1, headers=["x", "f\N{SUBSCRIPT ONE}(x)"]))
    print('')
    print(tabulate(data2, headers=["x", "f\N{SUBSCRIPT TWO}(x)"]))
    print('')
    print(tabulate(data3, headers=["x", "f\N{SUBSCRIPT THREE}(x)"]))
    print('')
    print(tabulate(data4, headers=["x", "f\N{SUBSCRIPT FOUR}(x)"]))

    user_choice=input('Choose one of the four functions given above. Type "1", "2", "3", or "4": ')
    while user_choice not in ['1','2','3','4']:
        user_choice=input('Choose one of the four functions given above. Type "1", "2", "3", or "4": ')
    return user_choice


def constant_or_balanced(function):
    """
    Decides whether a gicen function is constant or balanced, based on the result of Deutsch's algortihm for that function

    Args:
        function (str): string representing one of the four possible functions
    Returns:
        (str): Description of function
    """
    if run_deutsch_algorithm(function)==0:
        return 'Your function is constant'
    if run_deutsch_algorithm(function)==1:
        return 'Your function is balanced'


print(constant_or_balanced(choose_function()))
