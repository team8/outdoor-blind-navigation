import circularBuffer
import numpy as np

cb = circularBuffer.CircularBuffer(3)

cb.add(1)
cb.add(2)
print("The size is %s" % cb.size)
cb.add(3)
print("The average is %s" % cb.average())
print("The median is %s" % cb.median())
print("The mode is %s" % cb.mode())
print("The head is currently %s" % cb.peek_head())
print("The tail is currently %s" % cb.peek_tail())
cb.add(4)
cb.add(5)
cb.add(6)
list = cb.return_list()
print("The size is %s" % cb.size)
print("The average is %s" % cb.average())
print("The median is %s" % cb.median())
print("The mode is %s" % cb.mode())
print("The head is currently %s" % cb.peek_head())
print("The tail is currently %s" % cb.peek_tail())
for x in range(len(list)):
    print("Element %s is " % x)
    print(list[x])


cb2 = circularBuffer.CircularBuffer(3, [])

cb2.add([1, 2, 3])
cb2.add([3, 1, 2])
print("The size is %s" % cb2.size)
cb2.add([2, 3, 1])
print("The average is %s" % cb2.average())
print("The median is %s" % cb2.median())
print("The mode is %s" % cb2.mode())
print("The head is currently %s" % cb2.peek_head())
print("The tail is currently %s" % cb2.peek_tail())

cb3 = circularBuffer.CircularBuffer(3, [])
cb3.add([])
print("The median is %s" % cb3.median())

cb4 = circularBuffer.CircularBuffer(3, np.array(1))
cb4.add(np.array([1, 2, 3]))
cb4.add(np.array([2, 3, 1]))
cb4.add(np.array([3, 1, 2]))
print("The mean is %s" % cb4.average())

