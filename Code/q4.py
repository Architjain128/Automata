import copy
import sys
import json

fi1 = sys.argv[1]
fi2 = sys.argv[2]

f1 = open(fi1)
f2 = open(fi2, "w")

dfa = json.load(f1)
dstates = dfa["states"]
dletters = dfa["letters"]
dtransaction_matrix = dfa["transition_function"]
dstart_states = dfa["start_states"]
dfinal_states = dfa["final_states"]

def init(a):
    tra = []
    temp1=[]
    temp2=[]
    stet = {}
    for i in a:
        for j in dtransaction_matrix:
            if(j[0]==i):
                temp = j
                fl = 1
                if i not in dfinal_states:
                    fl = 0
                    if i not in temp1:
                        temp1.append(i)
                else:
                    fl=1
                    if i not in temp2:
                        temp2.append(i)
                tra.append([temp,fl])
                stet[str(j[0])]=fl
    return tra,temp1,temp2,stet

def init_part(a,b):
    re = []
    for i in range(b):
        tt = []
        for j in range(a):
            tt.append(-1)
        re.append(tt)
    return re

def give_me_states(a,b):
    re = []
    for n in a:
        for m in b:
            if m in n:
                re.append(n)
                break
    return re

def give_me_transition_fun(a):
    re = []
    for n in a:
        for m in dletters:
            for l in dtransaction_matrix:
                if(l[0] in n) and (l[1]==m):
                    for o in a:
                        if(l[2] in o):
                            re.append([n,m,o])
                    break
    return re

# finding tree rooted at start state in Directed forest
tree = [0]*len(dstates)
sts = []
q =[]
for x in dstart_states:
    sts.append(x)
    q.append(x)

while len(q)!=0:
    temp = q[0]
    q.remove(temp)
    for x in dtransaction_matrix:
        if (x[0]==temp) and (x[2] not in sts):
            sts.append(x[2])
            q.append(x[2])

for i in dstates:
    if i in sts:
        tree[dstates.index(i)]=1

# transition table state*alphabet 
trt = {}
for i in dstates:
    tt = []
    for j in dletters:
        st = ""
        for n in dtransaction_matrix:
            if(n[0]==i and n[1]==j):
                st=str(n[2])
        tt.append(st)
    trt[str(i)] = tt

# divide states in two set in starting
tra,temp1,temp2,stet = init(sts)

# refining the states
P=[]
P.append(temp2)
P.append(temp1)
p1=[]
pp=[[],[]]
pp2=[]
stet_dash = {}
num_set = 2
p1 = copy.deepcopy(P)
fl = False
while True:
    if(p1==pp2) or fl:
        break 
    for d in dstates:
            for e in p1:
                if(d in e):
                    stet_dash[str(d)]=p1.index(e)
    pp2 = p1
    fl = False
    pp = [[] for i in range(len(p1))]
    for w in p1:
        j = 0
        zz = init_part(len(dletters),len(w))
        for j in range(len(w)):
            for n in dtransaction_matrix:
                if n[0]==w[j]:
                    for k in range(len(p1)):
                        if n[2] in p1[k]:
                            zz[j][dletters.index(n[1])] = k
        tj =1
        ck = 0
        ly = len(w)
        fl = False
        for j in range(1,ly):
            # pp[p1.index(w)]=copy.deepcopy(zz[j])
            # for m in dletters:
            if zz[0]!= zz[j]:
                if fl:
                    p1[len(p1)-1].append(w[tj])
                    w.pop(tj)
                    tj-=1
                else:
                    p1.append([w[tj]])
                    w.pop(tj)
                    tj-=1
                    fl=True
            tj+=1

# print(stet)  # stet contains initial groups of all states
# print(stet_dash)  # stet_dash contains final groups of all states

# new start_states
ns = give_me_states(p1,dstart_states)

# new final_states
nf = give_me_states(p1,dfinal_states)

# new transition_function
tr = give_me_transition_fun(p1)

to_write = {
    "states": p1,
    "letters": dletters,
    "transition_matrix": tr,
    "start_states": ns,
    "final_states": nf
}

json.dump(to_write, f2)
f1.close()
f2.close()