import statistics
import numpy as np


class CircularBuffer:
    def __init__(self, capacity, typeex=0):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.tail = -1
        self.head = 0
        self.type = typeex
        self.size = 0

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

    def __second_dimension_list(self):
        tmplist = []
        for x in range(self.__second_dimension_capacity()):
            if x is not None:
                tmplist.append([])
        if isinstance(self.type, np.ndarray):
            for x in self.queue:
                if x is not None:
                    for y in x:
                        element = list(x).index(y)
                        tmplist[element].extend([y])
        else:
            for x in self.queue:
                if x is not None:
                    for y in x:
                        element = x.index(y)
                        tmplist[element].extend([y])
        return tmplist

    def average(self):
        if isinstance(self.type, (float, int)):
            return statistics.mean(self.queue)
        elif isinstance(self.type, (list, np.ndarray)):
            tmp = self.__second_dimension_list()
            one_d_list = []
            for x in range(len(tmp)):
                innertmp = tmp[x]
                mean = statistics.mean(innertmp)
                one_d_list.append(mean)
            return one_d_list
        else:
            print("Incompatible data type")

    def median(self):
        if isinstance(self.type, (float, int)):
            return statistics.median(self.queue)
        elif isinstance(self.type, (list, np.ndarray)):
            tmp = self.__second_dimension_list()
            one_d_list = []
            for x in range(len(tmp)):
                innertmp = tmp[x]
                median = statistics.median(innertmp)
                one_d_list.append(median)
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
