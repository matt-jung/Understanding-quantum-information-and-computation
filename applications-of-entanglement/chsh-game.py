def quantum_strategy(x,y):
    """
    Runs the optimal quantum strategy for the CHSH game.

    Args:
        x (int): bit representing Alice's question
        y (int): bit representing Bob's question

    Returns:
        a (int): bit representing Alice's answer
        b (int): bit representing Bob's answer
    
    Raises:
        TypeError: if either x or y is not an integer
        ValueError: if either x or y is not in the set {0,1}
    
    Notes:
        -Uses QuantumCircuit, numpy, and AerSimulator packages
    """
    if not all(isinstance(i,int) for i in [x,y]):
        raise TypeError("x and y must both be integers")
    if not all(i in [0,1] for i in [x,y]):
        raise ValueError('x and y must both be either 0 or 1')

    from qiskit import QuantumCircuit
    from numpy import pi
    from qiskit_aer import AerSimulator

    qc=QuantumCircuit(2,2)
    
    #create entangled state
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    #Alice applies her gate
    if x==0:
        qc.ry(0,0)
    elif x==1:
        qc.ry(-pi/2,0)
    
    #Bob applies his gate
    if y==0:
        qc.ry(-pi/4,1)
    elif y==1:
        qc.ry(pi/4,1)

    qc.measure([0,1],[0,1])

    sim=AerSimulator()
    result=sim.run(qc,shots=1).result().get_counts()
    a=int(list(result.keys())[0][0])
    b=int(list(result.keys())[0][1])
    return a,b

def classical_strategy(x,y):
    """
    Runs the optimal classical strategy for the CHSH game.

    Args:
        x (int): bit representing Alice's question
        y (int): bit representing Bob's question

    Returns:
        a (int): bit representing Alice's answer
        b (int): bit representing Bob's answer

    Raises:
        TypeError: if either x or y is not an integer
        ValueError: if either x or y is not in the set {0,1}
    """
    if not all(isinstance(i,int) for i in [x,y]):
        raise TypeError("x and y must both be integers")
    if not all(i in [0,1] for i in [x,y]):
        raise ValueError('x and y must both be either 0 or 1')

    #Alice
    if x==0:
        a=0
    elif x==1:
        a=1
    #Bob
    if y==0:
        b=1
    elif y==1:
        b=0
    
    return a,b

def random_quantum_strategy(x,y):
    """
    Runs a random quantum strategy for the CHSH game.

    Args:
        x (int): bit representing Alice's question
        y (int): bit representing Bob's question

    Returns:
        a (int): bit representing Alice's answer
        b (int): bit representing Bob's answer
    
    Raises:
        TypeError: if either x or y is not an integer
        ValueError: if either x or y is not in the set {0,1}
    
    Notes:
        -Uses QuantumCircuit, numpy, random, and AerSimulator packages
    """
    if not all(isinstance(i,int) for i in [x,y]):
        raise TypeError("x and y must both be integers")
    if not all(i in [0,1] for i in [x,y]):
        raise ValueError('x and y must both be either 0 or 1')

    from qiskit import QuantumCircuit
    from numpy import pi
    import random
    from qiskit_aer import AerSimulator

    qc=QuantumCircuit(2,2)
    
    #create entangled state
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    #create random phases
    alice_phase=pi/8*random.randint(-8,8)
    bob_phase=pi/8*random.randint(-8,8)

    #Alice applies her gate
    qc.ry(alice_phase,0)
    
    #Bob applies his gate
    qc.ry(bob_phase,1)

    qc.measure([0,1],[0,1])

    sim=AerSimulator()
    result=sim.run(qc,shots=1).result().get_counts()
    a=int(list(result.keys())[0][0])
    b=int(list(result.keys())[0][1])

    return a,b

def random_classical_strategy(x,y):
    """
    Runs a random classical strategy for the CHSH game.

    Args:
        x (int): bit representing Alice's question
        y (int): bit representing Bob's question

    Returns:
        a (int): bit representing Alice's answer
        b (int): bit representing Bob's answer

    Raises:
        TypeError: if either x or y is not an integer
        ValueError: if either x or y is not in the set {0,1}

    Notes:
        -Uses random package
    """
    if not all(isinstance(i,int) for i in [x,y]):
        raise TypeError("x and y must both be integers")
    if not all(i in [0,1] for i in [x,y]):
        raise ValueError('x and y must both be either 0 or 1')
    
    import random

    a=random.randint(0,1)
    b=random.randint(0,1)

    return a,b



def chsh_game(strategy):
    """
    Runs the CHSH game with a given strategy.

    Args:
        strategy (str): strategy to run
    Returns:
        1 or 0 (int): 1 for a win, 0 for a loss

    Raises:
        TypeError: if strategy is not inputed as a string
        ValueError: if strategy is not quantum, classical, random_quantum or random_classical
    """
    strategy=strategy.lower()
    if not strategy in ['classical','quantum','random_quantum','random_classical']:
        raise ValueError('Strategy must either be quantum or classical.')
    if not isinstance(strategy,str):
        raise TypeError('Strategy must be given as a string.')

    import random
    referee_choices=[(0,0),(0,1),(1,0),(1,1)]
    (x,y)=referee_choices[random.randint(0, 3)]

    #Random strategy picks quantum or random with 50% chance
    if strategy=='random':
        strategy=['quantum','classical'][random.randint(0,1)]

    if strategy=='quantum':
        (a,b)=quantum_strategy(x,y)
    elif strategy=='classical':
        (a,b)=classical_strategy(x,y)
    elif strategy=='random_quantum':
        (a,b)=random_quantum_strategy(x,y)
    else:
        (a,b)=random_classical_strategy(x,y)

    if (a^b)==(x and y):
        return 1 #win
    else:
        return 0 #lose

def winning_chance(strategy):
    """
    Calculates the winning rate of a given CHSH game strategy

    Args:
        strategy (str): Strategy for the CHSH game
    Returns:
        win_message (str): Message giving the winning rate for chosen strategy

    Raises:
        TypeError: if strategy is not a string
        ValueError: if strategy is not quantumn, classical, or random
    """
    strategy=strategy.lower()
    if not strategy in ['classical','quantum','random_quantum','random_classical']:
        raise ValueError('Strategy must either be quantum or classical.')
    if not isinstance(strategy,str):
        raise TypeError('Strategy must be given as a string.')
    
    wins=0 
    for _ in range(1000):
        if chsh_game(strategy) == 1:
            wins+=1

    win_rate=(wins/1000)*100
    win_message='Out of 1000 games, Alice and Bob won '+str(win_rate)+'%% using the '+strategy+' strategy.'
    return(win_message)


strategy=input('Choose a strategy to use for the CHSH game. Type either "quantum", "classical", "random_quantum", or "random_classical" (without speech marks): ')
print(winning_chance(strategy))

