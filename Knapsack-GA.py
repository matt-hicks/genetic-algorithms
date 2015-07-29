from random import randint
from random import random
from random import sample

# Genetic Algorithm for 0/1 Knapsack Problem (tournament selection and uniform crossover)

#knapfile = 'trivial3.txt'
#global_optimum = 13

#knapfile = 'easier7.txt'
#global_optimum = 200

#knapfile = 'easy20.txt'
#global_optimum = 726

knapfile = 'hard200.txt'

with open(knapfile, 'rU') as kfile:
    lines = kfile.readlines()
n = int(lines[0]) # Number of items
c = int(lines[n+1]) # Knapsack capacity
items = {int(line.split()[0]) : tuple(map(int, line.split()))[1:] for line in lines[1:n+1]} # Dict of possible items

# GA parameters
max_generations = 100
K = 2 # tournament size
pX = 1 # Overall crossover rate
pU = 0.5 # Uniform crossover rate
pM = 1.1/float(n) # Mutation rate
P = 50 # Population size
E = 2 # number of Elites

def mutate(human):
    """
    Takes a binary list and flips bits at a probability of pM, outputs another binary list.
    """
    xman = human[:]
    for i in range(n):
        if pM > random():
            if human[i] == 0:
                xman[i] = 1
            else:
                xman[i] = 0
    return xman

def unifXover(parentA, parentB):
    """
    Takes 2 binary lists and with probablity pX performs uniform crossover at probability pU to produce a list of 2 new binary lists.
    """
    childA = parentA[:]
    childB = parentB[:]
    if pX > random():
        for i in range(n):
            #if (1/float(n)) > random():
            if pU > random():
                childA[i] = parentB[i]
                childB[i] = parentA[i]
    return [childA, childB]
        
def packing_info(b):
    """
    Accepts a binary list denoting packed items and returns a list of their index numbers, total value and total weight.
    """
    indexes = []
    total_value = 0
    total_weight = 0
    for idx, val in enumerate(b):
        if val == 1:
            indexes.append(idx+1)
            total_value += items[idx+1][0]
            total_weight += items[idx+1][1]               
    return [indexes, total_value, total_weight]

def vFitness(b):
    """
    Accepts a binary list denoting packed items and returns their total value.
    """
    total_value = 0
    for idx, val in enumerate(b):
        if val == 1:
            total_value += items[idx+1][0]              
    return total_value

def wFitness(b):
    """
    Accepts a binary list denoting packed items and returns their total weight.
    """
    total_weight = 0
    for idx, val in enumerate(b):
        if val == 1:
            total_weight += items[idx+1][1]              
    return total_weight

def tournament_selection(pop, K):
    """
    Takes population list of binary lists and tournament size and returns a winning binary list.
    """
    tBest = 'None'
    for i in range(K):
        contestant = pop[randint(0, P-1)]
        if (tBest == 'None') or vFitness(contestant) > vFitness(tBest):
            tBest = contestant[:]
    return tBest

def initialize_population():
    """
    Generates a list of binary lists each representing a valid packing selection.
    """
    popS = set()
    while len(popS) < P:
        b0weight = c+1
        while b0weight > c: # the starting population only includes valid solutions
            b0 = tuple(randint(0,1) for _ in range(n))
            b0weight = wFitness(b0)
        popS.add(b0)
    return [list(elem) for elem in list(popS)] # Converts a set of tuples into a list of lists

def select_elites():
    """
    Selects the E best solutions from the population and returns them as a list of binary lists.
    """
    elites = []
    while len(elites) < E: # Keep choosing elites until there are E of them
        new_elites = popD[max(popD)] # These are the binary lists with the best fitness
        # If adding all the elites with this fitness would be too many, then discard the surplus at random
        while len(new_elites) > (E - len(elites)):
            new_elites.remove(sample(new_elites, 1)[0])
        elites.extend(new_elites)
        popD.pop(max(popD), None) # Remove the key with the value just added from popD{}
    return elites

def popMean():
    """
    Calculate the mean fitness of the current generation
    """
    t = 0
    for i in popR:
        t += i[0]
    return t/P

def report():
    return "max: "+str(max(popD))+", mean: "+str(popMean())+", min: "+str(min(popD))

def updateBest():
    return [max(popD), popD[max(popD)][0], s]

def rankedList():
    # Make a list of each binary list and its fitness
    return [(vFitness(i), i) for i in popL]
   
def rankedDict():
    # Make a dictionary where keys are fitness and values are tuples of the binary lists with that fitness
    popD = {}
    for item in popR:
        key = item[0]
        popD.setdefault(key, []).append(item[-1])
    return popD

# Create an initial population
popL = initialize_population()
popR = rankedList()
popD = rankedDict()
s = 0 # the generation counter
bestResults = updateBest()
print "Starting population - "+str(report())

while True:
    s += 1
    popR = rankedList()
    popD = rankedDict()

    # Update current best
    if max(popD) > bestResults[0]:
        bestResults = updateBest()

    # Stop if optimum attained (optimum only known if enumeration was possible)    
    if 'global_optimum' in globals():
        if bestResults[0] == global_optimum:
            print "Global Optimum reached after "+str(s)+" generations."
            break

    # Stop if time is up
    if s == max_generations:
        print "Stopped after "+str(s)+" generations."
        break
        
    # Give an update every 10% of total progress
    if s % (max_generations / 10) == 0:
        print "Best: "+str(bestResults[0])+", "+str(max_generations - s)+" generations remaining. Current population - "+str(report())
    
    # Start the child generation with E elites (direct copies from current generation)
    nextGen = select_elites()
        
    # Fill the next generation to size P, same size as the previous one
    while len(nextGen) < P:
        parentA = tournament_selection(popL, K) # Selection
        parentB = tournament_selection(popL, K)
        childrenAB = unifXover(parentA, parentB) # Crossover
        mutatedChildA = mutate(childrenAB[0]) # Mutation
        mutatedChildB = mutate(childrenAB[1])
        if (wFitness(mutatedChildA) <= c) and (wFitness(mutatedChildB) <= c): # Discard infeasible solutions
            nextGen.extend([mutatedChildA, mutatedChildB])
               
    popL = nextGen[:]

packing_info = packing_info(bestResults[1])
print "\nBest feasible solution found (on generation "+str(bestResults[2])+"/"+str(max_generations)+"): value="+str(packing_info[1])+", weight="+str(packing_info[2])+"/"+str(c)+"\n"+str(len(packing_info[0]))+"/"+str(n)+" items: "+str(packing_info[0])
