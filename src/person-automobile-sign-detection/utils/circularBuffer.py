import numpy as np

#Using an inefficient but easy to code implementation
class CircularBuffer:
    def __init__(self, capacity, minNumPercent =  0.5):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.minNumPercent = minNumPercent

    def initQueue(self, listIn):
        temp = listIn.copy()
        temp.reverse()
        for i in temp:
            self.add(i)

    def add(self, term):
        del self.queue[-1]
        self.queue.insert(0, term)

    def toString(self):
        strOut = ""
        for i in self.queue:
            strOut += str(i)
        return strOut

    def mean(self):
        temp = self.queue.copy()
        if temp.count(None) >= self.minNumPercent * self.capacity:
            return None
        else:
            temp = list(filter(None, temp))
        if(type(temp[0]) == list):
            return np.mean(temp, axis=0)
        else:
            temp = list(filter(None, temp))
            return sum(temp) / len(temp)

    def median(self):
        temp = self.queue.copy()
        if temp.count(None) >= self.minNumPercent * self.capacity:
            return None
        else:
            temp = list(filter(None, temp))
            temp.sort()
            if(self.capacity % 2 == 0):
                return temp[self.capacity // 2 + 1] + [self.capacity // 2] / 2
            return temp[self.capacity // 2 + 1]

    def mode(self):
        temp = self.queue.copy()
        if temp.count(None) >= self.minNumPercent * self.capacity:
            return None
        maxOccurrences = 0
        modeOut = None
        for i in temp:
            totalOfInstance = temp.count(i)
            if totalOfInstance > maxOccurrences:
                modeOut = i
                maxOccurrences = totalOfInstance
        return modeOut

    def consecutive_count(self, value):
        count = 0
        for i in range(-1, -(len(self.queue) - 1))
            if self.queue[i] == value:
                count += 1
            else:
                break
        return count





