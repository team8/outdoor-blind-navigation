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
print("The average is %s" % cb3.average())

cb4 = circularBuffer.CircularBuffer(3, np.array(1))
cb4.add(np.array([1, 2, 3]))
cb4.add(np.array([2, 3, 1]))
cb4.add(np.array([3, 1, 2]))
print("The median is %s" % cb4.median())
print("The average is %s" % cb4.average())

cb5 = circularBuffer.CircularBuffer(3, np.array(1))
cb5.add(np.array([1, None, 3]))
cb5.add(np.array([2, None, 1]))
cb5.add(np.array([3, 3, 2]))
print("The median is %s" % cb5.median())
print("The average is %s" % cb5.average())

cb6 = circularBuffer.CircularBuffer(3, [])
cb6.add([None])
print("The median is %s" % cb6.median())
print("The average is %s" % cb6.average())

cb7 = circularBuffer.CircularBuffer(3, [])
cb7.add([None, None, None])
cb7.add([3, 1, None])
cb7.add([2, None, 3])
print("The median is %s" % cb7.median())
print("The average is %s" % cb7.average())
print("The mode is %s" % cb7.mode())

