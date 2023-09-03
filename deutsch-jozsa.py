from qiskit import QuantumCircuit
import random
from qiskit_aer import AerSimulator

def deutsch_jozsa_query_gate(n):
    """
    Creates a random query gate that is either constant or balanced with 50/50 chance

    Args:
        n (int): value of n for the Deutsch-Jozsa problem
    Returns:
        qc (QuantumCircuit): Quantum circuit representation of the query gate
    Raises:
        TypeError: if n is not an integer
        ValueError: if n is not greater than zero
    Notes:
        -Uses QuantumCircuit and random packages
    """
    if not isinstance(n,int):
        raise TypeError('n must be a positive integer.')
    if not (n>0):
        raise ValueError('n must be a positive integer.')


    qc=QuantumCircuit(n+1)

    #Function is constant 50% of the time.
    if random.randint(0,2):
        #further 50% f(x)=1 for all x
        if random.randint(0,2):
            qc.x(n)
        return qc

    #Function is balanced 50% of the time
    #choose random number out of 2**n possibilities
    binary_string = ''.join(random.choice('01') for _ in range(n))

    #apply x gates to oracle according to binary string
    for i in range(len(binary_string)):
        if list(reversed(binary_string))[i]=='1':
            qc.x(i)

    qc.barrier()
    #apply cnot gates to all qubits, with output qubit as control
    for qubit in range(n):
        qc.cx(qubit,n)
    
    qc.barrier()
    for i in range(len(binary_string)):
        if list(reversed(binary_string))[i]=='1':
            qc.x(i)
    
    return qc


def deutsch_jozsa_alorgithm(n):
    """
    Runs the Deutsch-Jozsa algorithm with a random query gate

    Args:
        n (int): value of n in the Deutsch-Jozsa problem
    Returns:
        qc (QuantumCircuit): circuit representation of the algorithm
        'Balanced' or 'Constant' (str): outcome of the algorithm
    Raises:
        TypeError: if n is not an integer
        ValueError: if n is not greater than zero
    Notes:
        -Uses QuantumCircuit, AerSimulator and random packages
    """
    if not isinstance(n,int):
        raise TypeError('n must be a positive integer.')
    if not (n>0):
        raise ValueError('n must be a positive integer.')
    
    qc=QuantumCircuit(n+1,n)

    qc.x(n)

    #H gate layer
    for qubit in range(n+1):
        qc.h(qubit)

    qc.barrier()
    qc=qc.compose(deutsch_jozsa_query_gate(n))
    qc.barrier()

    for qubit in range(n):
        qc.h(qubit)
        qc.measure(qubit,qubit)
    
    result = AerSimulator().run(qc,shots=1,memory=True).result()
    measurement = result.get_memory()

    if '1' in measurement[0]:
        return [qc,'Balanced']
    else:
        return [qc,'Constant']

algorithm=deutsch_jozsa_alorgithm(4)
print(algorithm[0].draw())
print(algorithm[1])