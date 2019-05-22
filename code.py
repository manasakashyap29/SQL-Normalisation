############################################################
## project2.py - Code template for Project 2 - Normalization 
## Both for CS5421 and CS4221 students 
############################################################
from itertools import permutations,combinations
from copy import deepcopy
import random
import itertools
### IMPORTANT! Change this to your metric number for grading
student_no = 'A0178462W'

random.seed(123)

## Determine the closure of set of attribute S given the schema R and functional dependency F
def closure(R, F, S):
    omega = deepcopy(F)
    gamma = deepcopy(S)
    while True:
        flag = False
        for i in omega:
            if set(i[0]).issubset(set(gamma)):
                flag = True
                omega.remove(i)
                gamma = list(set(gamma).union(set(i[1])))
        if not flag:
            break
    gamma = sorted(gamma)
    return gamma

## Determine the all the attribute closure excluding superkeys that are not candidate keys given the schema R and functional dependency F

def all_closures(R,F):
    closures = []
    candidate_keys = []
    combination = []
    for i in range(1,len(R)+1):
        combination.extend(list(x) for x in combinations(R,i))
    for i in combination:
        flag = True
        a = closure(R,F,i)
        for key in candidate_keys:
           if set(i).issuperset(set(key)):
                flag = False
                break
        if flag:
           closures.append([i,a])
           if set(a) == set(R):
               candidate_keys.append(i)
    return closures

## Return the candidate keys of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS5421 students.
def candidate_keys(R, F): 
    return []

def calculate_sigma1(FD):
    sigma = []
    F = deepcopy(FD)
    for i in F:
        if len(i[1])>1: 
            for j in i[1]:
                sigma.append([i[0],[j]]) #separate each multiple attribute in RHS into different dependencies
        else:
            sigma.append(i)
    return sigma

def calculate_sigma2(R,sigma1):
    sigma2 = []
    for i in sigma1:
        i[0] = sorted(i[0])            
        if len(i[0]) > 1:
            for j in i[0]:  #loop through each attribute in LHS
                alpha = deepcopy(i[0])
                alpha.remove(j) #remove that particular attribute
                dep = closure(R,sigma1,alpha) #calculate closure and check if closure contains the attribute which was removed
                if set(j).issubset(dep):
                    i[0].remove(j)
            sigma2.append(i)
        else:
            sigma2.append(i) #if dependency is singleton add it straightaway
    return sigma2

def calculate_sigma3(R,sigma2):
    sigma3 = deepcopy(sigma2)
    for i in sigma2:
        F = deepcopy(sigma3)
        F.remove(i)
        dep = closure(R,F,i[0])
        if set(i[1]).issubset(set(dep)):
            sigma3.remove(i)
    return sigma3
    
## Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
def min_cover(R, FD): 
    sigma1 = calculate_sigma1(FD) # reduce to singletons
    sigma2 = calculate_sigma2(R,sigma1) #remove extraneous attribute on LHS
    sigma3 = calculate_sigma3(R,sigma2) #remove extraneous attribute on RHS
    return sigma3

## Return all minimal covers reachable from the functional dependencies of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS4221 students.
def min_covers(R, FD):
    covers =[]
    sigma1 = deepcopy(FD)
    singleton = [x for x in sigma1 if len(x[0]) ==1] #separate singletons
    multiattributes = [x for x in sigma1 if len(x[0]) >1] #and multiple attributes in LHS for easier computation of permutations
    multi_permutations = []
    for fd in multiattributes:
        fd_permutations = []
        lhs = permutations(fd[0],len(fd[0])) # permute the LHS eg: AB->C, BA->C
        for l in lhs:
            fd_permutations.append([list(l),fd[1]])
        multi_permutations.append(fd_permutations)
    
    combined_permutations = [list(x) for x in itertools.product(*multi_permutations)]
    permutations_to_run = min(len(combined_permutations),10)
    sampled_permutatioins = []
    if permutations_to_run < 10:
        sampled_permutations = combined_permutations 
    else:
        sampled_permutations = random.sample(combined_permutations,10)
    
    for fd in sampled_permutations:
        new_sigma1 =  []
        new_sigma1.extend(fd)
        new_sigma1.extend(singleton)
        sigma2_1 = calculate_sigma2(R,new_sigma1)      
        sigma2_2 = calculate_sigma1(sigma2_1)
       # checks for length. 
        if len(sigma2_2) <= 7:
            for sigma_instances in permutations(sigma2_2,len(sigma2_2)): # generate various orderings
                sigma3 = calculate_sigma3(R,list(sigma_instances))
                sorted_sigma3 = sorted(sigma3)
                if sorted_sigma3 not in covers:
                    covers.append(sorted_sigma3)
        else:
            random_iterations = 100
            sigma2_copy = deepcopy(sigma2_2)
            for i in range(random_iterations):
                random.shuffle(sigma2_copy) #generate various orderings of each dependency set
                sigma3 = calculate_sigma3(R,list(sigma2_copy))
                sorted_sigma3 = sorted(sigma3)
                if sorted_sigma3 not in covers:
                    covers.append(sorted_sigma3)
    return covers

## Return all minimal covers of a given schema R and functional dependencies F.
## NOTE: This function is not graded for CS4221 students.
def all_min_covers(R, FD):
    closures = all_closures(R,FD)
    closures1 = deepcopy(closures)
    closures2 = []
    for i in closures:
        if i[0]==i[1]: #remove trivial dependencies
            continue 
        for x in i[0]: #remove redundant attributes
            i[1].remove(x)
        closures2.append([i[0],i[1]])
    all_min = min_covers(R,closures2) #calculate min_covers on the minimised list
    return all_min

### Test case from the project
R = ['A', 'B', 'C', 'D']
FD = [[['A', 'B'], ['C']], [['C'], ['D']]]

print closure(R, FD, ['A'])
print closure(R, FD, ['A', 'B'])
print all_closures(R, FD)
print candidate_keys(R, FD)

R = ['A', 'B', 'C', 'D']
FD = [[['A'], ['B', 'C']],[['B'], ['C','D']], [['D'], ['B']],[['A','B','E'], ['F']]]
print (min_cover(R, FD)) 

R = ['A', 'B', 'C']
FD = [[['A', 'B'], ['C']],[['A'], ['B']], [['B'], ['A']]] 
print min_covers(R, FD) 
print all_min_covers(R, FD) 

## Tutorial questions
R = ['A', 'B', 'C', 'D', 'E']
FD = [[['A', 'B'],['C']], [['D'],['D', 'B']], [['B'],['E']], [['E'],['D']], [['A', 'B', 'D'],['A', 'B', 'C', 'D']]]
print min_cover(R, FD)
print min_covers(R, FD)
print all_min_covers(R, FD) 
