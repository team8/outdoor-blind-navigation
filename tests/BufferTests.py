from utils import circularBuffer
from utils.circularBuffer import CircularBuffer

br = CircularBuffer(3)

testIn = [1,2,3]

br.initQueue(testIn)
print(br.toString())
br.add(3)
br.add(2)

print(br.toString())