import statistics
import numpy as np


def median(list):
    sortedlist = sorted(list, key=lambda x: (x is None, x))
    n = len(sortedlist)
    if n == 0:
        raise Exception("no median for empty data")
    if n % 2 == 1:
        return sortedlist[n // 2]
    else:
        i = n // 2
        if sortedlist[i] and sortedlist[i - 1]:
            return (sortedlist[i - 1] + sortedlist[i]) / 2
        else:
            return None


def mean(list):
    newlist = []
    for x in list:
        if x is not None:
            newlist.append(x)
    if iter(newlist) is list:
        newlist = list(newlist)
    n = len(newlist)
    if n < 1:
        return None
    total = sum(newlist)
    return total / n


class CircularBuffer:
    def __init__(self, capacity, typeex=0):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.tail = -1
        self.head = 0
        self.type = typeex
        self.size = 0
        self.none_threshold = 5

    def __full(self):
        return self.size == self.capacity

    def __empty(self):
        return self.size == 0

    def add(self, item):
        if self.__full():
            removed = self.remove()
            self.tail = (self.tail + 1) % self.capacity
            self.queue[self.tail] = item
            self.size = self.size + 1
            return removed
        else:
            self.tail = (self.tail + 1) % self.capacity
            self.queue[self.tail] = item
            self.size = self.size + 1

    def remove(self):
        if self.__empty():
            print("Queue Empty")
        else:
            item = self.queue[self.head]
            self.head = (self.head + 1) % self.capacity
            self.size = self.size - 1
            return item

    def __second_dimension_capacity(self):
        if isinstance(self.type, np.ndarray):
            return len(self.queue)
        else:
            return len(self.queue[0])

    def __nonethreshold(self, inputlist):
        tmplist = []
        if isinstance(inputlist, np.ndarray):
            inputlist = list(inputlist)
        for x in range(self.__second_dimension_capacity()):
            if x is not None:
                tmplist.append([])
        if isinstance(self.type, np.ndarray):
            for x in (inputlist or []):
                if x is not None:
                    tmplist.append(x)
        else:
            for x in (inputlist or []):
                if x is not None:
                    tmplist.append(x)
        if tmplist and inputlist:
            noneamount = len(inputlist) - len(tmplist)
        elif inputlist:
            noneamount = len(inputlist)
        else:
            noneamount = 0
        if noneamount >= self.none_threshold:
            return False
        else:
            return True

    def __second_dimension_list(self):
        tmplist = []
        for x in range(self.__second_dimension_capacity()):
            tmplist.append([])
        if isinstance(self.type, np.ndarray):
            for x in self.queue:
                if self.__nonethreshold(x):
                    for y in x:
                        element = list(x).index(y)
                        tmplist[element].extend([y])
        else:
            for x in self.queue:
                if self.__nonethreshold(x):
                    for y in (x or []):
                        element = x.index(y)
                        tmplist[element].extend([y])
        return tmplist

    def average(self):
        if isinstance(self.type, (float, int)):
            return mean(self.queue)
        elif isinstance(self.type, (list, np.ndarray)):
            tmp = self.__second_dimension_list()
            one_d_list = []
            for x in range(len(tmp)):
                innertmp = tmp[x]
                newmean = mean(innertmp)
                one_d_list.append(newmean)
            return one_d_list
        else:
            print("Incompatible data type")

    def median(self):
        if isinstance(self.type, (float, int)):
            return median(self.queue)
        elif isinstance(self.type, (list, np.ndarray)):
            tmp = self.__second_dimension_list()
            one_d_list = []
            for x in range(len(tmp)):
                innertmp = tmp[x]
                innermedian = median(innertmp)
                one_d_list.append(innermedian)
            return one_d_list
        else:
            print("Incompatible data type")

    def mode(self):
        if isinstance(self.type, (float, int)):
            return statistics.mode(self.queue)
        elif isinstance(self.type, (list, np.ndarray)):
            tmp = self.__second_dimension_list()
            one_d_list = []
            for x in range(len(tmp)):
                innertmp = tmp[x]
                mode = statistics.mode(innertmp)
                one_d_list.append(mode)
            return one_d_list
        else:
            print("Incompatible data type")

    def return_list(self):
        return self.queue

    def size(self):
        return self.size

    def peek_head(self):
        return self.queue[self.head]

    def peek_tail(self):
        return self.queue[self.tail]
