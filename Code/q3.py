import sys
import json
import copy


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

def self_loop(a,mat):
    fl = 0
    fr = 0
    for n in mat:
        if i==n[0]:
            fl+=1
        elif i==n[2]:
            fr+=1
    return fl,fr

def merge_ex(mat,s):
    st = ""
    fl = False
    for m in mat:
        st = st + str(m[1]) + '+'
        fl=True
    if(fl):
        return st[:-1]
    return st

def star(a,b,s):
    global dtransaction_matrix
    st = s
    fl =False
    i = len(st)
    for n in a:
        for m in b:
            if i==0:
                dtransaction_matrix.append([n[0],str(str(n[1])+str(m[1])),m[2]])
            elif i==1:
                dtransaction_matrix.append([n[0],str(str(n[1])+str(st) +'*'+ str(m[1])),m[2]])
            else:
                dtransaction_matrix.append([n[0],str(str(n[1])+'(' +str(st) +')*'+ str(m[1])),m[2]])

def remove_redundent_state(a):
    global dtransaction_matrix
    for x in a:
        if x in dtransaction_matrix:
            dtransaction_matrix.remove(x)

# define new states
d_st = [["start"]]
d_fl = [["final"]]
new_states= copy.deepcopy(dstates)
new_states.append("start")
new_states.append("final")

#  add new start state
for x in dstart_states:
    dtransaction_matrix.append(["start","$",x])

#  add new final state
for x in dfinal_states:
    dtransaction_matrix.append([x,"$","final"])

temp = []
for i in dstates:
    temp.append([i,self_loop(i,dtransaction_matrix)])

ans=''
while True:
    if len(dtransaction_matrix)==1 or len(dstates)==0:
        break
    incoming = []
    outgoing = []
    pseudo = []
    for m in dtransaction_matrix:
        if temp[0][0]==m[0] or temp[0][0]==m[2]:
            if temp[0][0]==m[0] and temp[0][0]!=m[2] :
                outgoing.append(m)
            elif temp[0][0]!=m[0] and temp[0][0]==m[2] :
                incoming.append(m)
            else:
                pseudo.append(m)
    ans=''
    ans = merge_ex(pseudo,ans)
    star(incoming,outgoing,ans)
    remove_redundent_state(pseudo)
    remove_redundent_state(incoming)
    remove_redundent_state(outgoing)
    dstates.remove(temp[0][0])
    temp=[]
    for i in dstates:
        temp.append([i,self_loop(i,dtransaction_matrix)])

ans = merge_ex(dtransaction_matrix,ans)

to_write = {
    "regex": ans,
}

json.dump(to_write, f2)
f1.close()
f2.close()
