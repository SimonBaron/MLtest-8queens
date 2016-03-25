'''A bit of a go at building a ML program to solve the *8 Queens* problem'''

import random


class Arrangement(list):

    def qc(self): # specific to 8 queens, not general to N queens
        if len(self) != 8:
            return False
        if sorted(self) != range(1,9):
            return False
        return True

    def check(self):
        upper_diagonal = set([])
        lower_diagonal = set([])
        for x, y in enumerate(self):
            upper_diagonal = upper_diagonal | set([x-y])
            lower_diagonal = lower_diagonal | set([x+y])
        errors = 2*len(self) - len(upper_diagonal) - len(lower_diagonal)
        return errors

    def mutate(self):
        a, b = random.sample(range(2*len(self)), 2)
        if a < len(self) and b < len(self):
            hold = self[a]
            self[a] = self[b]
            self[b] = hold

    def reproduce(self, other):
        pivot = random.randint(0,7)
        child1 = self[:pivot] # these come out as lists
        child2 = other[:pivot]
        for i in self:
            if i not in child2:
                child2.append(i)
        for i in other:
            if i not in child1:
                child1.append(i)
        return [Arrangement(child1), Arrangement(child2)]


class Population:

    count = 0

    def __init__(self, N, memberlist = [], r = True):

        if r == True:
            self.members = [Arrangement(random.sample(range(1,9),8)) for i in range(N)]
        else:
            self.members = memberlist
        self.rank_all()
        self.N = N

    def check(self):
        for m in self.members:
            if m.check() == 0:
                return m

    def rank_all(self):
        self.ranked = {}
        for i in range(15):
            self.ranked[str(i)] = []
        for m in self.members:
            self.ranked[str(m.check())].append(m)
        for k in self.ranked.keys():
            if self.ranked[k] == []:
                del(self.ranked[k])

    def choose_n(self, n, best=True):
        choice = []
        need = n
        if best == True:
            order = sorted(self.ranked.keys())
        else:
            order = reversed(sorted(self.ranked.keys()))        
        for score in order:
            if need > 0:
                if len(self.ranked[score]) < need:
                    choice += (self.ranked[score])
                    need -= len(self.ranked[score])
                else:
                    k =  self.ranked[score]
                    choice += random.sample(k, need)
                    need = 0
        return choice

    def get_offspring(self):
        candidates = random.sample(self.members,5)
        self.subpop = Population(len(candidates), candidates, r=False)
        parents = self.subpop.choose_n(2)
        self.members += parents[0].reproduce(parents[1])
                

    def stats(self):
        self.rank_all()
        for i in sorted(self.ranked.keys()):
            print i, "\t", len(self.ranked[i])

    def generate(self, Cmax=1000):
        self.count = 0
        while self.count < Cmax:
            self.count += 1
            self.get_offspring()
            for m in self.members:
                if m.check() == 0:
                    return m, self.count
                m.mutate()
            self.rank_all()
            self.members = self.choose_n(self.N)
            #new = Population(self.N, self.members, r=False)

## testing and assessment

def average_count(population, iterations):
    count = []
    for i in range(iterations):
        testpop = Population(population)
        count.append(testpop.generate()[1])
    return float(sum(count))/len(count)
