
import math
#-------------------------------------------------------------------72->
# v stands for vector, p/q to scale, d for direction
def log2(v, d, p=1, q=2):
    # a: lower bound b: current value  c: upper bound  
    a, b, c = v
    if (a == c): return v
    # total discrete choices
    n = c - a + 1
    # total d.c on left side to discard
    l = b - a + (1 if a != b else 0) # if they are same, we dont want to count
    # t.d.c on right side to discard
    r = c - b + (1 if c != b else 0) # them twice in discreate math
    # discard choices according to the direction
    a = a + max(0, l * d)
    c = c + min(0, r * d)
    if d == -1:
        c = max(a, c)
        a = min(a, c)
    else:
        a = min(a, c)
        c = max(a, c)
    debug = False
    if debug:
        print(f"left:{l}  right:{r}  a:{a}  c:{c}")
    # place b according to the scaling factor and between a, c
    n = c - a + 1
    b = math.floor(a + n * p / q)
    if debug:
        print(f"a:{a}  b:{b}  c:{c}")
    return (a, b, c)

def log2increase(v):
    return log2(v, 1, 1)

def log2decrease(v):
    return log2(v, -1, 1)

"""
reminders table to determine where to put the reminder from division result.
imagine we're operating on mod3 and we have 4 pixels to choose. how to group?
it is reasonable to think symmetrical
imagine 4 pixels as x-xx-x when its modulo 3 so its (0, 1, 0)
when its 5 pixels, xx-x-xx better so its (1, 0, 1)
if its 3 pixels it divides 3 perfect already so its (0, 0, 0)
and user 
selects index to choose the group of pixels.
"""
logrs = [
    [],
    [[0]],
    [
        (0, 0),
        (1, 0),
    ],
    [
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 1),
    ],
]
def logN(v, i, log=3):
    a, b, c = v
    if (a == c):
        return v

    n = c - a + 1    # n: total discreate choices of pixels
    s = max(1, log/n)# s: squish coefficient when n < log (aka pixels < choices)
    log = min(n, log)
    i = int(i//s) % log
    t = logrs[log][n % log]  # t: table
    d = n // log     # d: division
    t = [x+d for x in t]
    l = i       # left  sections to discard
    r = log - i - 1 # right sections to discard
    sl = sum(t[0:l])
    sr = sum(t[::-1][0:r])
    v = (a+sl, 0, c-sr)
    v = (v[0], (v[0]+v[2])//2, v[2])
    return v

def log3(v, i): return logN(v, i, 3)

log3((0,0,0), 0) # expect: (0, 0, 0)

log3((0,0,1), 0) # expect: (0, 0, 0)
log3((0,0,1), 1) # expect: (0, 0, 0)
log3((0,0,1), 2) # expect: (1, 1, 1)

log3((0,0,2), 0) # expect: (0, 0, 0)
log3((0,0,2), 1) # expect: (1, 1, 1)
log3((0,0,2), 2) # expect: (2, 2, 2)

log3((0,0,3), 0) # expect: (0, 0, 0)
log3((0,0,3), 1) # expect: (1, 1, 2)
log3((0,0,3), 2) # expect: (3, 3, 3)

log3((0,0,4), 0) # expect: (0, 0, 1)
log3((0,0,4), 1) # expect: (2, 2, 2)
log3((0,0,4), 2) # expect: (3, 3, 4)