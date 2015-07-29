from random import randint
from random import random
from random import sample

# Hybrid genetic-local search algorithm for Balanced Partitioning Problem (tournament selection and uniform crossover)

# 3 synthetic datasets to investigate
# n=24, m/n=0.8
#tnumbers = [8805, 233796, 266052, 288500, 329571, 386685, 444791, 496096, 516670, 558760, 560030, 593143, 611107, 759935, 763545, 775453, 780655, 832643, 851382, 860005, 872412, 875638, 910646, 963487]
# n=24, m/n=1.25
#tnumbers = [98474159, 144697516, 246593131, 305118089, 332788873, 424659277, 434057552, 451867054, 588600099, 663420606, 756703492, 806551936, 1011236450, 1267978346, 1558946719, 1605164879, 1616390394, 1627358918, 1736741111, 1998469071, 2005533775, 2017104959, 2105881047, 2131777488]
# n=200, m/n=0.15
tnumbers = [187033, 24548121, 35425304, 35541144, 54837427, 60702203, 60865477, 73573758, 80025720, 90876905, 94421190, 100340393, 106376548, 125176191, 147730896, 150645054, 157025924, 168295584, 181166193, 183538608, 238309283, 239370088, 244784543, 254253468, 261541886, 294755819, 296407156, 298381959, 306119600, 320787441, 327252107, 332887368, 336607338, 349439657, 350881143, 351227838, 353546915, 363545421, 379983147, 385109890, 408317063, 424581563, 427810023, 434599621, 453886680, 460369319, 462290052, 467079401, 484504581, 487118306, 493816253, 500398198, 520745999, 525504967, 535326009, 545974867, 552348533, 575147258, 578712810, 579135270, 583540738, 599523395, 603332987, 603809389, 604749352, 605309475, 608391222, 616489225, 624509382, 647181964, 647306876, 664642678, 671286656, 681470739, 682073665, 690127962, 695336783, 724272015, 765759802, 766465572, 771578697, 776739579, 810229902, 823089171, 829934280, 836045922, 842464194, 846613787, 848074372, 852105812, 865245874, 883923793, 888906823, 892028604, 902584245, 902878375, 911547132, 935212215, 950454944, 952578029, 967775433, 981703403, 1002035272, 1014709544, 1016954602, 1022239057, 1045983390, 1066488184, 1075083978, 1076787321, 1078603104, 1083923117, 1090259211, 1092919059, 1100636928, 1137809073, 1138650675, 1163176505, 1167536451, 1169195290, 1170744629, 1186288973, 1212837873, 1233000052, 1250752780, 1251617031, 1251768056, 1263600174, 1267609883, 1270459468, 1282762059, 1297340108, 1306068361, 1319695494, 1321367672, 1343055389, 1353760230, 1355551253, 1386046830, 1406948966, 1413395373, 1416675405, 1434105022, 1481051469, 1484959626, 1508325377, 1511982604, 1516844548, 1521857470, 1527408576, 1543748317, 1552903490, 1579281635, 1637692487, 1637837312, 1653381660, 1656229147, 1659717791, 1669516122, 1671976449, 1681423466, 1682938011, 1701226919, 1726785959, 1741499938, 1751683108, 1757690197, 1758608496, 1791976507, 1792973522, 1799059647, 1801539514, 1812725407, 1813319383, 1829742347, 1831758420, 1840635902, 1876771064, 1947515525, 1955058435, 1956127185, 1960284174, 1965241751, 1969133050, 1969625663, 2001067934, 2016494855, 2024133044, 2033033927, 2037006253, 2037251218, 2038448013, 2043216417, 2067519888, 2068229452, 2081969791, 2098077555, 2099123739, 2132568865, 2135004215]

sT=sum(tnumbers)
mST=sT % 2 # Is the sum of S odd or even?

n = len(tnumbers)
print 'n = '+ str(n)

bL = float(0)
for i in tnumbers:
    bL += i.bit_length()
#print bL
m = bL/n
print "m = " + str(m)
print "m/n = " + str(m/n)

# GA parameters
max_generations = 2000
K = 2 # tournament size
pX = 1 # Overall crossover rate
pU = 0.5 # Uniform crossover rate
pM = 1.1/float(n) # Mutation rate
P = 50 # Population size
E = 2 # number of Elites
t = 1 # no. of hill-climbing iterations in the inner algorithm
h = 3 # no. of gradient samples for Steepest Ascent Hill-Climbing

def hillClimb1(t,p0): # Random Ascent Hill-Climbing
    """Takes a list of lists and performs t hill-climbs on each member, returns modified list of lists"""
    p1=[]
    for b0 in p0:
        b1 = b0[:]
        for j in range(t):
            b2 = mutate(b1)         
            if fitness(b2) < fitness(b1):
                b1 = b2[:]
        p1.append(b1)
    return p1

def hillClimb2(t,h,p0): # Limited Sample Steepest Ascent Hill-Climbing
    """Takes a list of lists and performs t hill-climbs on each member (taking h gradient samples for Steepest Ascent),
    returns modified list of lists.
    This is an implementation of algorithm 17 from Essentials of Metaheuristics by Sean Luke"""
    p1=[]
    for b0 in p0:
        hcBest = b0[:]
        b1 = b0[:]
        for j in range(t):
            b2 = mutate(b1)
            for k in range(h-1):
                b3 = mutate(b1)
                if fitness(b3) < fitness(b2):
                    b2 = b3[:]
            b1 = b2[:]
            if fitness(b1) < fitness(hcBest):
                hcBest = b1[:]
        p1.append(hcBest)
    return p1

def mutate(b):
    """
    Takes a binary list and flips bits at a probability of pM, outputs another binary list.
    """
    x = b[:]
    for i in range(n):
        if pM > random():
            if b[i] == 0:
                x[i] = 1
            else:
                x[i] = 0
    return x

def unifXover(parentA, parentB):
    """
    Takes 2 binary lists and with probablity pX performs uniform crossover at probability pU to produce a list of 2 new binary lists.
    """
    childA = parentA[:]
    childB = parentB[:]
    if pX > random():
        for i in range(n):
            if pU > random():
                childA[i] = parentB[i]
                childB[i] = parentA[i]
    return [childA, childB]
        
def pList(s, bit):
    """ Takes a binary list and a bit value and returns the partition corresponding to that bit value """
    s1 = []
    for idx, val in enumerate(s):
        if val == bit:
            s1.append(tnumbers[idx])            
    return sorted(s1)

def fitness(s):
    """ Takes a binary list and returns a single number expressing fitness"""
    delta = 0
    for idx, val in enumerate(s):
        if val == 0:
            delta += tnumbers[idx]
        else:
            delta -= tnumbers[idx]
    return abs(delta)

def greedy(s):
    """ Takes a list of numbers and returns a binary list representing a partition by the greedy heuristic"""
    A = []
    B = []
    gL = []
    for i in sorted(s,reverse=True):
        if sum(A) < sum(B):
            A.append(i)
            gL.insert(0,0)
        else:
            B.append(i)
            gL.insert(0,1)
    return gL

def tournament_selection(pop, K):
    """
    Takes population list of binary lists and tournament size and returns a winning binary list.
    """
    tBest = 'None'
    for i in range(K):
        contestant = pop[randint(0, P-1)]
        if (tBest == 'None') or fitness(contestant) < fitness(tBest):
            tBest = contestant[:]
    return tBest

def initialize_population():
    """
    Generates a list of binary lists starting with the greedy heuristic and then adding random solutions.
    """
    popS = set() # Using a set to ensure all the starting population lists are unique
    popS.add(tuple(greedy(tnumbers)))
    while len(popS) < P:
        b0 = tuple(randint(0,1) for _ in range(n))
        popS.add(b0)
    return [list(elem) for elem in list(popS)] # Converts a set of tuples into a list of lists

def select_elites():
    """
    Selects the E best solutions from the population and returns them as a list of binary lists.
    """
    elites = []
    while len(elites) < E: # Keep choosing elites until there are E of them
        new_elites = popD[min(popD)] # These are the binary lists with the best fitness
        # If adding all the elites with this fitness would be too many, then discard the surplus at random
        while len(new_elites) > (E - len(elites)):
            new_elites.remove(sample(new_elites, 1)[0])
        elites.extend(new_elites)
        popD.pop(min(popD), None) # Remove the key with the value just added from popD{}
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
    return "min: "+str(min(popD))+", mean: "+str(popMean())+", max: "+str(max(popD))

def updateBest():
    """ Returns a list of the best fitness found, a binary list corresponding to that fitness and the
    current generation """
    return [min(popD), popD[min(popD)][0], s]

def rankedList():
    """Returns a list of each binary list and its fitness"""
    return [(fitness(i), i) for i in popL]
   
def rankedDict():
    """Make a dictionary where keys are fitness and values are lists of the binary lists with that fitness"""
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

    popL = hillClimb1(t,popL)
    #popL = hillClimb2(t,h,popL)

    # Assess fitness and record results
    popR = rankedList()
    popD = rankedDict()

    # Update current best
    if min(popD) < bestResults[0]:
        bestResults = updateBest()

    # Stop if optimum attained
    if ((mST == 0) and bestResults[0] == 0) or ((mST == 1) and bestResults[0] == 1):
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
        nextGen.extend([mutatedChildA, mutatedChildB])
               
    popL = nextGen[:]

print "\nBest solution found (on generation "+str(bestResults[2])+"/"+str(max_generations)+"): value="+str(bestResults[0])
#print pList(bestResults[1],0)
#print pList(bestResults[1],1)
