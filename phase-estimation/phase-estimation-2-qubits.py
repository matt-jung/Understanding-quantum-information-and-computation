#again, we will use a phase gate with eigenstate |1⟩
#   Rϕ |1⟩ = e^(iϕ) |1⟩ 
#   ϕ=2*pi*θ
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from math import pi
from qiskit_aer import AerSimulator


def phase_estimation(theta):
    """
    Estimates theta via phase estimation algorithm with two control qubits. Estimate is rounded to the nearest 1/4.

    Args:
        theta (float): phase of Rϕ gate such that Rϕ |1⟩ = e^(i*2*pi*theta) |1⟩
    Returns:
        estimate (float): estimate of theta computed via QPE, rounded to nearest 0.25
    Raises:
        ValueError: if theta is not between 0 and 1
    Notes:
        -for some reason, AerSimulator only runs the circuit if I decompose before running. I tried to decompose only the QFT, but couldn't.
    """
    if not (0<=theta<=1):
        raise ValueError('theta must be between 0 and 1')

    qc=QuantumCircuit(3,2)
    qc.x(2)
    qc.barrier()
    qc.h([0,1])

    #apply control-U to taget state
    qc.cp(2*pi*theta,
          control_qubit=0,
          target_qubit=2)
    
    #apply control-U^2 to target state
    qc.cp(2*pi*(2*theta),
          control_qubit=1,
          target_qubit=2)
    
    #apply QFT to top register
    qft = QFT(num_qubits=2).to_gate()
    qft_inv=qft.inverse()
    qc.append(qft_inv, qargs=[0, 1])
   
   #for some reason AerSim only works if I decompose the circuit
    qc=qc.decompose(reps=2)
    qc.measure([0,1],[0,1])

    sim=AerSimulator()
    counts=sim.run(qc).result().get_counts()

    #convert measurement to integer form
    y=max(counts, key=counts.get)
    y=int(y,2)

    estimate=y/4
    return estimate
