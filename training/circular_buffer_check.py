import circularBuffer

cb = circularBuffer.CircularBuffer("num", 3)

cb.add(1)
cb.add(2)
print("The size is %s" % cb.size)
cb.add(3)
print("The average is %s" % cb.average())
print("The median is %s" % cb.median())
print("The head is currently %s" % cb.peek_head())
print("The tail is currently %s" % cb.peek_tail())
cb.add(4)
cb.add(5)
cb.add(6)
list = cb.return_list()
print("The size is %s" % cb.size)
print("The average is %s" % cb.average())
print("The median is %s" % cb.median())
print("The head is currently %s" % cb.peek_head())
print("The tail is currently %s" % cb.peek_tail())
for x in range(len(list)):
    print("Element %s is " % x)
    print(list[x])

