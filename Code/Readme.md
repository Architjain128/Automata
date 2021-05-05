# Regex to NFA
## How to run
```
    > python3 q1.py ./input.json ./output.json
```
## Explanation
+ set start state as `q0` (only one start state)
+ set final state as `q1` (only one final state initially)
+ finding alphabets by replacing all `*`, `+` ,`(` ,`)` and ` ` and remaing unique element in string
+ I have written a recurcive function to parse given string according to correct bracket sequence and on returning it will check for `*` and `+` and geenrate new states according to counter named `num_states` and add transition funtion related to it in temp martix which was latter parsed in required format for dumping
+ For start state it assummed it will only be one in all cases
+ I implrmrnted modified BFS in function `final` started form current final state `q1` to check for multiple end states and add them if exists in final state in dump.


# NFA to DFA
## How to run
```
    > python3 q2.py ./input.json ./output.json
```
## Explanation
+ `start states` and `alphabets` are same as input (assunmed)
+ `states` are powerset of all states
+ for `transition function` firstly i stored all transition posittion according to inputed function in a 2D list and then for all state i take union of all list corresponding to each state in set as there new transition positions 
+ `final state` all states in powerset conating any of input final states are incoorperated in final state of dump


# DFA to Regex
## How to run
```
    > python3 q3.py ./input.json ./output.json
```
## Explanation
+ In starting i have added `start` as a start state containg trnsactions from [`start`,`$`,for all start states in input]
+ I have also added `final` as a final state containg trnsactions from [for all final states in input,`$`,`final`]
+ one by one i remove a state from input transition state as well as from input state and keeping a conut on incoming and outgoing arrows for each state and checking for selfloops
+ If it has self loop add its ` (incoming alphabet) + (selfloop alphabet) + '*' + (outgoing alphabet) `
+ If no selfloops add its ` (incoming alphabet) + (outgoing alphabet) `
+ Repeat previous 3 steps till input transition function has only one element or all input state are removed
+ then transition state from `start` to `final` is the required expression

# Minimize DFA
## How to run
```
    > python3 q4.py ./input.json ./output.json
```
## Explanation
+ `alphabets` are same as input
+ My approach to remove unreachable state is treating all states in input as nodes in a forest connected with directed edges and then finding a tree rooted at start state by implementing a modified BFS
+ I formed a dictionary named `trt` which is storing a list corresponding to all states containing there transition postion by ith alphabet for refining 
+ I used a infinte loop breaking when there is no change in set `p1` and `pp2` where p1 containing current pseudo* equivalent states and pp2 is previous value of p1 by doing this i split `p1` in different state if transition postions of all pairs present in it are non-equivalent and state index is maintained in a dictionary named `stet_dash`
+ For eqivalence check i used temporary array storing index of transition position from all aplhabets
+ For new `start state` and new `final state` i used `give_me_states` function which iterates over `p1` and return all states in it which are present in input start/final state
+ For new `transition function` i itreate over all set in `p1` and input transaction matrix and parse require rows from input

> + *Here pseudo means the may or may not be final state but assuming they are
> + Here transtion postion is transition value of a state for a alphabet

> Link to the <a href="https://1drv.ms/u/s!At2KpJlL7sPThjdlO_iq1hoa-VQ8?e=fVhqsy">video</a>
