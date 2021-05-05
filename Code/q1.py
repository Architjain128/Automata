import os
import sys
import json

q,fi1,fi2 = sys.argv
f1 = open(fi1)
f2 = open(fi2,'w')
reg = json.load(f1)
reg = reg["regex"]
reg = reg.replace(" ","")

num_states = 0
state = []
alphabet = []
transitions = []
start_state = []
final_state = []
self_loops = []

def valid_id(a,st):
    if(a<len(st)):
        return True
    return False

def give_me_next_bracket(stri,s,ep):
    c = 1
    hys = '('
    for i in range(s+1,len(stri)):
        if stri[i]=='(':
            c+=1
            hys = '('
        if stri[i]==')':
            c-=1
            hys = ')'
        if(c==0 and hys==')'):
            return i
    return 0

def complete_my_assignment(mat,regex,s,e):
    global num_states,state
    if(s==-1):
        s = num_states
        num_states+=1
        state.append(str("q"+str(num_states-1)))
        mat.append([])
    if(e==-1):
        e = num_states
        num_states+=1
        state.append(str("q"+str(num_states-1)))
        mat.append([])
    s_pre = 0
    e_pre = 0
    pre = s
    i=0
    while i < len(regex):
        if regex[i] == '(':
            ii = i
            i = give_me_next_bracket(regex,ii+1,0)
            s_pre,e_pre = complete_my_assignment(mat,regex[ii+1:i],pre,-1)
            pre = e_pre
        elif regex[i]=='+':
            complete_my_assignment(mat,regex[i+1:],s,e)
            break
        elif regex[i]=='*':
            if s_pre == e_pre:
                if str("q"+str(pre)) not in self_loops:
                    self_loops.append(str("q"+str(pre)))
                mat[pre].append([regex[i-1],str("q"+str(pre))])
            else:
                mat[s_pre].append(['$',str("q"+str(e_pre))])
                mat[e_pre].append(['$',str("q"+str(s_pre))])
        else:
            if (valid_id(i+1,regex) and regex[i + 1]=='*'):
                i+=1
                continue
            e_pre = pre
            s_pre = pre
            nav = num_states
            num_states+=1
            state.append(str("q"+str(num_states-1)))
            mat.append([])
            mat[pre].append([regex[i],str("q"+str(nav))])
            pre = nav
        i+=1
    mat[pre].append(['$',str("q"+str(e))])
    return s,e

def final(n_f,mat):
    rery = []
    q = []
    for x in n_f:
        rery.append(x)
        q.append(x)
    
    while len(q) != 0:
        top = q[0]
        q.pop()
        
        for m in mat:
            if m[1]=='$' and m[2] == top and m[0] not in rery:
                rery.append(m[0])
                q.append(m[0])
    return rery

def formating(num_states,mat):
    temp=[]
    for i in range(0,num_states):
        for j in range(len(mat[i])):
            temp.append([str("q"+str(i)),mat[i][j][0],str(mat[i][j][1])])
    return temp

# define new start state
ns = ['q0']
# define new final state
nf=['q1']
# alphabet
rer = reg.replace("*","")
rer = rer.replace("+","")
rer = rer.replace("(","")
rer = rer.replace(")","")
for r in rer:
    if r not in alphabet:
        alphabet.append(r)
# bracket parsing
complete_my_assignment(transitions,reg,-1,-1)
print(self_loops) # conatins state having self loops
# transtion
dtransitions = formating(num_states,transitions)
# finding multiple end state
final_state = final(nf,dtransitions)

to_write = {
    "states": state,
    "letters": alphabet,
    "transition_matrix": dtransitions,
    "start_states": ns,
    "final_states": final_state
}

json.dump(to_write, f2)

f1.close()
f2.close()
