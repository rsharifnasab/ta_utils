from random import randint as rnd

def test_input_gen():

    min_n = 1
    max_n = 100
    P = rnd(min_n, max_n)
    Y = rnd(min_n, max_n)
    L = rnd(min_n, min(100,2*P-1))

    return f"{P} {L}\n{Y}\n"
