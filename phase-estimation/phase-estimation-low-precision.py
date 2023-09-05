#instance of the phase estimation algorithm where θ is rounded to the nearest bit after the binary point (i.e nearest half)

#inputs: eigenstate |x⟩ and unitary operator U
#outputs: estimate of phase of eigenvalue of U [0 or 1/2]
#           thus eigenvalue = 1 or -1 [e^0 or e^(i*pi)]

# we will use a phase gate with eigenstate |1⟩
#   Rϕ |1⟩ = e^(iϕ) |1⟩ 
#   ϕ=2*pi*θ

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from math import pi

def phase_estimation(θ):
    """
    Runs the phase estimation algiorthm for the simple case where unitary gate U is a phase gate with eigenstate |1⟩.
    Low precision case: phase estimation is rounded to the nearest half.

    Args:
        θ (float): phase of the operation's eigenvalue λ such that λ=e^(2πiθ) 
    Returns:
        estimate (float): estimate of θ computed via phase estimation. Returns either 0.5 or 0.
    Raises:
        ValueError: if θ is not between 0 and 1
    """
    if not (0<=θ<=1):
        raise ValueError('θ must be between 0 and 1')

    qc=QuantumCircuit(2,1)
    qc.x(1)
    qc.barrier()
    qc.h(0)
    qc.cp(theta=2*pi*θ,
        control_qubit=0,
        target_qubit=1)
    qc.h(0)
    qc.measure(0,0)

    sim=AerSimulator()
    counts=sim.run(qc).result().get_counts()

    if max(counts, key=counts.get)=='1':
        estimate=0.5
    elif max(counts, key=counts.get)=='0':
        estimate=0
    
    return estimate
