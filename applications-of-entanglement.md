# applications-of-entanglement
A showcase of various applications of entanglement in quantum computing, simulated using Qiskit:

## Superdense coding
[Superdense coding](https://en.wikipedia.org/wiki/Superdense_coding) works to transmit two classical bits of information using one qubit, at the cost of one "e-bit" of entanglement. The protocol is as follows:

Two qubits in the entangled Bell state $| \phi^+ \rangle$ are shared between Alice and Bob. Alice chooses which message to send to Bob by changing the phase of her qubit via $X$ and $Z$ gates, according to the following:

<p align="center">
$(I_B \otimes I_A) | \phi^+ \rangle = | \phi^+ \rangle$
</p>
<p align="center">
$(I_B \otimes Z_A) | \phi^+ \rangle = | \phi^- \rangle$
</p>
<p align="center">
$(I_B \otimes X_A) | \phi^+ \rangle = | \psi^+ \rangle$
</p>
<p align="center">
$(I_B \otimes X_A Z_A) | \phi^+ \rangle = | \psi^- \rangle$
</p>

where $I$ is the identity matrix and subscripts $A$ and $B$ refer to operations on Alice's and Bob's qubits.

Alice then gives her qubit to Bob, who applies a CNOT operation with qubit A as the control and qubit B as the target, then applies a Hadamard operation to qubit A. The state of the qubits is thus transformed into $| 00 \rangle$, $| 01 \rangle$, $| 10 \rangle$, or $| 11 \rangle$, depending on the state that Alice chose. Bob then measures the qubits, obtaining the two classical bits of information that Alice encoded. 


## The CHSH Game
The [CHSH game](https://en.wikipedia.org/wiki/CHSH_inequality#CHSH_game) is a game involving two players, Alice and Bob, who attempt to win by correctly answering the questions asked to them by a referee. The rules are as follows: 

- Alice and Bob are in two separate rooms, and cannot communicate with each other
- The referee's questions can either be in the form of a $0$ or a $1$
- The referee chooses a set of questions $(x,y)$ at random, asking question $x$ to Alice and $y$ to Bob
- Alice and Bob give answers $a$ and $b$ respectively, both in the form of a $0$ or a $1$
- They win if $a \oplus b = x \land y$, i.e. if $(x,y)=(1,1)$ they win if $a$ and $b$ are different, and in all other cases they win if $a$ and $b$ are the same.

The best classical strategy for this game has a 75% win rate, while the best quantum strategy has 85%. The quantum strategy involves Alice and Bob sharing a pair of qubits in the $| \phi^+ \rangle$ state, and rotating their respective qubits by different angles about the $y$-axis depending on which questions they are asked.
