import statistics


def list_multi_dimension(list, elem, r=False):
    for row, i in enumerate(list):
        try:
            column = i.index(elem)
        except ValueError:
            continue
        if r:
            return row, column
        else:
            return column
    return -1


class CircularBuffer:
    def __init__(self, capacity, typeex=0):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.tail = -1
        self.head = 0
        self.type = typeex
        self.size = 0

    def full(self):
        return self.size == self.capacity

    def empty(self):
        return self.size == 0

    def add(self, item):
        if self.full():
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
        if self.empty():
            print("Queue Empty")
        else:
            item = self.queue[self.head]
            self.head = (self.head + 1) % self.capacity
            self.size = self.size - 1
            return item

    def second_dimension_capacity(self):
        return len(self.queue[0])

    def second_dimension_list(self):
        tmplist = []
        for x in range(self.second_dimension_capacity()):
            tmplist.append([])
        tmp = self.queue
        for x in self.queue:
            for y in x:
                tmplist[list_multi_dimension(tmp, y)].extend([y])
        return tmplist

    def average(self):
        if isinstance(self.type, (float, int)):
            return statistics.mean(self.queue)
        elif isinstance(self.type, list):
            tmp = self.second_dimension_list()
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
        elif isinstance(self.type, list):
            tmp = self.second_dimension_list()
            one_d_list = []
            for x in range(len(tmp)):
                innertmp = tmp[x]
                median = statistics.median(innertmp)
                one_d_list.append(median)
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
