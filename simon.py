from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

def simon_oracle(string):
    """
    Creates a quantum circuit representation of an oracle function in Simon's algorithm with m=n.
    f: {0,1}^n -> {0,1}^n

    Args:
        string (str): binary string s such that f(x)=f(x XOR s) for all x in {0,1}^n
    Returns:
        oracle (QuantumCircuit): quantum circuit representation of oracle function
    Raises:
        TypeError: if string is not a string
        ValueError: if string is not binary
    """
    if not isinstance(string,str):
        raise TypeError('Input must be a valid binary string')
    if any(i not in ['0','1'] for i in string):
        raise ValueError('Input must be a valid binary string')
    
    n=len(string)

    oracle=QuantumCircuit(2*n)
    for i in range(n):
        oracle.cx(i,i+n)
    oracle.barrier()
    for i in range(n):
        if string[i]=='1':
            oracle.cx(0,n+i)
    
    return oracle


def simon_algorithm(string):
    """
    Runs simon's algorithm using a given string.

    Args:
        string (str): binary string s for oracle function
    Returns:
        strings (list): list of strings y that satisfy y.s=0, where a.b is the binary dot product
    Raises:
        TypeError: if string is not a string
        ValueError: if string is not binary
    Notes:
        -classical post-processing is still required to find s
    """
    if not isinstance(string,str):
        raise TypeError('Input must be a valid binary string')
    if any(i not in ['0','1'] for i in string):
        raise ValueError('Input must be a valid binary string')
    
    n=len(string)
    qc=QuantumCircuit(2*n,n)

    for i in range(n):
        qc.h(i)
    qc.barrier()

    oracle=simon_oracle(string)
    qc=qc.compose(oracle)
    qc.barrier()

    for i in range(n):
        qc.h(i)
        qc.measure(i,i)

    sim=AerSimulator()
    results=sim.run(qc).result().get_counts()

    strings=[i for i in results]
    
    return strings

print(simon_algorithm('101'))
