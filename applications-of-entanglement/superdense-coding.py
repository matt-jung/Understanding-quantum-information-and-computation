def superdense_coding(bits):
    """
    Carries out the superdense coding protocol for a given two-bit binary string

    Args:
        bits (str): two-digit binary string

    Returns:
        counts (dict): dictionary showing results of measurement on Bob's end

    Raises:
        TypeError: If bits is not a binary string
        ValueError: If bits is not two digits long.

    Notes:
        -Uses QuantumCircuit and AerSimulator packages
        -https://en.wikipedia.org/wiki/Superdense_coding
        -https://learn.qiskit.org/course/basics/entanglement-in-action#entanglement-16-0 
    """
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator

    if not isinstance(bits,str):
        raise TypeError('input must be a two-digit binary string')
    if not all(bit in '01' for bit in bits):
       raise TypeError('input must be a two-digit binary string') 
    if not len(bits)==2:
        raise ValueError('input must be a two-digit binary string')
    
    a=bits[0]
    b=bits[1]

    qc=QuantumCircuit(2)

    #Create entangled Bell state
    qc.h(0)
    qc.cnot(0,1)

    #Begin superdense coding protocol
    #Alice flips her qubit depending on which message she wants to send
    qc.barrier()
    if b=='1':
        qc.z(0)
    if a=='1':
        qc.x(0)

    #Alice's qubit is given to Bob
    qc.barrier()    
    qc.cnot(0,1)
    qc.h(0)

    qc.measure_all()

    sim=AerSimulator()
    counts=sim.run(qc).result().get_counts()
    return counts


bits=input('Give a two-digit binary string to send: ')
print(superdense_coding(bits))
