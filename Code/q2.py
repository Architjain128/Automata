import os
import sys
import json
import copy

def num_to_bin(num,ln):
    sr = ""
    while num>0:
        sr = str(num%2) + sr
        num = num//2
    return sr.zfill(ln)

def superset(tik,sz):
    sts = []
    sts.append([])
    for i in range(1,sz):
        temp = [] 
        index = num_to_bin(i,len(tik))
        for j in range(0,len(index)):
            if(index[j]=='1'):
                temp.append(tik[j])
        temp.sort()
        sts.append(temp)
    return sts

def check_list(dic,a,b):
    key_to_lookup = a,b
    if key_to_lookup in dic:
        return dic[key_to_lookup] 
    else:
        return []

def sup(X,mat,al):
    tra = []
    X.sort()
    X.sort(key=len)
    for x in X:
        for a in al:
            tt = []
            for ax in x:
                tt = join_list(tt,check_list(mat,ax,a))
            temp = [x,a,tt]
            tra.append(temp)
    return tra

def set_transition(mat):
    dic = {}
    for x in mat:
        key_to_lookup = (x[0],x[1])
        if key_to_lookup in dic:
            dic[x[0],x[1]].append(x[2])
        else:
            dic[x[0],x[1]] = []
            dic[x[0],x[1]].append(x[2])
    return dic

def join_list(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list

def finalle(X,fin):
    X.sort()
    X.sort(key=len)
    temp = []
    for f in fin:
        for x in X:
            if (f in x) and (x not in temp):
                temp.append(x)
    return temp

fi1 = sys.argv[1]
fi2 = sys.argv[2]

f1 = open(fi1)
f2 = open(fi2, "w")

nfa = json.load(f1)
nstates = nfa["states"]
nletters = nfa["letters"]
ntransaction_matrix = nfa["transition_function"]
nstart_states = nfa["start_states"]
nfinal_states = nfa["final_states"]

dstates = []
dletters = []
dtransaction_matrix = []
dstart_states = []
dfinal_states = []

num_dstates = 2**len(nstates)
matrix = set_transition(ntransaction_matrix)

# start state
dstart_states = copy.deepcopy(nstart_states)
# letters 
dletters = copy.deepcopy(nletters)
# states
dstates = superset(nstates,num_dstates)
# transition
dtransaction_matrix = sup(dstates,matrix,dletters)
# final state
dfinal_states = finalle(dstates,nfinal_states)

to_write = {
    "states": dstates,
    "letters": dletters,
    "transition_matrix": dtransaction_matrix,
    "start_states": dstart_states,
    "final_states": dfinal_states
}

json.dump(to_write, f2)
f1.close()
f2.close()
