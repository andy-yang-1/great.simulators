import os
import sys
import json

def check(k, states, start_state, halt_state):
    if k < 2 or \
        not start_state in states or \
        not halt_state.issubset(states):
        exit(-1)


with open(sys.argv[1], "r") as f_source:
    lines = f_source.readlines()

# === set configurations of TM ===

## k : number of tapes
## states : list of all states
## start_state : initial state of TM
## halt_state : halt state of TM
k = int(lines[0].strip())
states = set(lines[1].strip().split(' '))
start_state = lines[2].strip()
halt_state = set(lines[3].strip().split(' '))
input_text = lines[4].strip().split()
print(k)
print(states)
print(start_state)
print(halt_state)

## trans : transition function
trans = dict()
now_line = 5
size = 1 << (k + 1)
while now_line < len(lines):
    now_line = now_line + 1
    now_state = lines[now_line].strip()
    print(now_line, now_state)
    ### check
    if not now_state in states:
        exit(-1)
    if now_state in halt_state:
        now_line = now_line + 1
        continue
    now_line = now_line + 1
    while now_line < len(lines) and not lines[now_line] == "\n":
        now_tape, write_tape, movement, trans_state = lines[now_line].strip().split(";")
        now_tape = now_tape.strip().split()
        write_tape = write_tape.strip().split()
        movement = movement.strip().split()
        trans_state = trans_state.strip()
        print(now_line, now_tape, write_tape, movement, trans_state)
        ### check
        if not trans_state in states or\
            not len(now_tape) == k or\
            not len(write_tape) == k - 1 or\
            not len(movement) == k:
            exit(-1)
        trans[(now_state, " ".join(now_tape))] = (trans_state, write_tape, movement)
        now_line = now_line + 1

## check whether the TM is valid
check(k, states, start_state, halt_state)
print(trans)

# === simulation start ===
class Tapes:
    def __init__(self, k, input_text):
        self.k = k
        self.p_tapes = [['*'] for i in range(k)]
        self.n_tapes = [['*'] for i in range(k)]
        self.p_tapes[0] = input_text

    def read(self, i, pos):
        pos, tape = (pos, self.p_tapes[i]) if pos >= 0 else (-pos, self.n_tapes[i])
        if pos >= len(tape):
            tape.append('*')
        return tape[pos]
    
    def write(self, i, pos, symbol):
        pos, tape = (pos, self.p_tapes[i]) if pos >= 0 else (-pos, self.n_tapes[i])
        tape[pos] = symbol

    def show(self):
        for i in range(k):
            print("".join(list(reversed(self.n_tapes[i][1:])) + list("|") + self.p_tapes[i]))

print('---SimulationProcess---')

tapes = Tapes(k, input_text)
now_state = start_state
headers = [0 for i in range(k)]
tapes.show()
print(now_state, headers)

now_step = 0
while not now_state in halt_state:
    now_tape = " ".join([tapes.read(i, headers[i]) for i in range(k)])
    if not trans.__contains__((now_state, now_tape)):
        exit(-1) 
    trans_state, write_tape, movement = trans[(now_state, now_tape)]

    now_state = trans_state
    for i in range(1, k):
        tapes.write(i, headers[i], write_tape[i-1])
    for i in range(k):
        if movement[i] == '<':
            delta = -1
        elif movement[i] == '-':
            delta = 0
        elif movement[i] == '>':
            delta = 1
        else:
            exit(-1)
        headers[i] = headers[i] + delta

    tapes.show()
    now_step += 1
    if now_step > 200:
        print(' Exceeding 200 Steps!', headers)
        break
    else:
        print(now_state, headers)

'''
example TM Language source file
2
q0 q1
q0
q1
1 1 1 0 0 1 1 1 0 0

q0
0 0 ; 0 ; > > ; q0
0 1 ; 0 ; > > ; q0
0 * ; 0 ; > > ; q0
1 0 ; 1 ; > > ; q0
1 1 ; 1 ; > > ; q0
1 * ; 1 ; > > ; q0
* 0 ; * ; - - ; q1
* 1 ; * ; - - ; q1
* * ; * ; - - ; q1

q1
'''