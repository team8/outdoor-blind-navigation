import statistics


class CircularBuffer:
    def __init__(self, type, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.tail = -1
        self.head = 0
        self.type = type
        self.size = 0

    def full(self):
        return self.size == self.capacity

    def empty(self):
        return self.size == 0

    def add(self, item):
        if self.full():
            print(self.remove())
            self.tail = (self.tail + 1) % self.capacity
            self.queue[self.tail] = item
            self.size = self.size + 1
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

    def average(self):
        if self.type != "num":
            print("Incompatible data type")
        else:
            return statistics.mean(self.queue)

    def median(self):
        if self.type != "num":
            print("Incompatible data type")
        else:
            return statistics.median(self.queue)

    def return_list(self):
        return self.queue

    def size(self):
        return self.size

    def peek_head(self):
        return self.queue[self.head]

    def peek_tail(self):
        return self.queue[self.tail]
