import statistics
import numpy as np

#Using an inefficient but easy to code implementation
class CircularBuffer:
    def __init__(self, capacity, noneOverridePercent =  0.8):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.minNumPercent = noneOverridePercent
        self.lastAccessed = False

    #Start out the buffer with given list listIn
    def initQueue(self, listIn):
        temp = listIn.copy()
        temp.reverse()
        for i in temp:
            self.add(i)

    #Push a new item onto the buffer
    def add(self, term):
        del self.queue[-1]
        self.queue.insert(0, term)
        self.lastAccessed = False

    #Writes out everything in the circularBuffer
    def toString(self):
        strOut = ""
        for i in self.queue:
            strOut += str(i)
        return strOut

    #Averages everything in the queue (can't take strings etc). If number of nones is greater than minNumPercent, it returns None
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

    #Sorts a copy of the buffer, then finds the median. Probably doesn't work on strings. If greater than minNumPercent, returns None
    def median(self, initIndex = 0, finIndex = None):
        finIndex = self.capacity if finIndex is None else finIndex
        temp = self.queue[initIndex:finIndex].copy()
        if temp.count(None) >= self.minNumPercent * self.capacity:
            return None
        else:
            temp = list(filter(None, temp))
            temp.sort()
            # if(self.capacity % 2 == 0):
                # return (temp[self.capacity // 2 + 1] + [self.capacity // 2]) / 2
            return temp[(finIndex - initIndex - 1)// 2 + 1]

    #Finds the thing with the most instances in the lisdt. Same as other 2, returns none if over minNumPercent
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

    def size(self):
        return len(self.queue)

    def getLast(self):
        self.lastAccessed = True
        return self.queue[0]

    def getList(self):
        return self.queue

    def getLastAccessed(self) -> bool:
        return self.lastAccessed
