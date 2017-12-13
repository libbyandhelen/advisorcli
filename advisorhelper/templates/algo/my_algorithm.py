import random


class Algorithm:
    def __init__(self, lowerbound, upperbound):
        self.lowerbound = lowerbound
        self.upperbound = upperbound

    def get_suggestion(self):
        trail = []
        for i in range(len(self.lowerbound)):
            rand = random.random()
            trail.append(rand*(self.upperbound[i]-self.lowerbound[i])+self.lowerbound[i])
        return trail
