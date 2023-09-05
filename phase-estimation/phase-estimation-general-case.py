def phase_estimation(phi,precision=3):
    """
    Runs QPE algorithm with chosen precision.

    Args:
        phi (float): phase of unitary gate U such that U |u⟩ = e^(2pi*i*phi) |u⟩,  where |u⟩ is an eigenstate of U.
        precision (int) level of precision in estimate (max 15)
    Returns:
        estimate (float): estimate for phi
    Raises:
        ValueError: if phi is not between 0 and 1
        TypeError: if precision is not an integer
        ValueError: if precision is not between 1 and 15   
    Notes:
        -uses qiskit and math packages
        -Unitary gate U is represented as a phase gate with eigenstate |1⟩
    """
    if not (0<=phi<=1):
        raise ValueError('phi must be between 0 and 1.')
    if not isinstance(precision,int):
        raise TypeError('precision must be an integer between 1 and 15 (inclusive)')
    if not (1<=precision<=15):
        raise ValueError('precision must be an integer between 1 and 15 (inclusive)')

    from qiskit import QuantumCircuit
    from math import pi
    from qiskit.circuit.library import QFT
    from qiskit.primitives import Sampler

    m=precision

    qc=QuantumCircuit(m+1,m)
    qc.x(m)
    qc.barrier()
    qc.h(range(m))

    for i in range(m):
        qc.cp(
            theta=2*pi*phi*(2**i),
            control_qubit=i,
            target_qubit=m
        )
    qc.barrier()

    qc.compose(
        QFT(m, inverse=True),
        inplace=True
    )
    qc.barrier()

    qc.measure(range(m),range(m))

    result = Sampler().run(qc).result()
    counts=result.quasi_dists[0]
    y=max(counts, key=counts.get)

    estimate=y/(2**m)
    return estimate

print(phase_estimation(phi=0.3,precision=15))
