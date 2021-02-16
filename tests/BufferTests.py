from utils import circularBuffer
from utils.circularBuffer import CircularBuffer

br = CircularBuffer(3)
input1 = [1,2,3]
input2 = [3,1,2]
input3 = [2,3,1]

inputTotal = [input1, input2, input3]

inputRealTotal = [inputTotal,inputTotal,inputTotal]


br2 = CircularBuffer(3)
input1 = [1,2,3]
input2 = [3,1,2]
input3 = [2,3,1]

inputTotal = [input1, input2, input3]

inputTotal2 = [input1, input2, [200,300,400]]

inputRealTotal = [inputTotal,None,inputTotal2]
br2.initQueue(inputRealTotal)
print(br2.toString())
print(br2.mean())

br2.add(None)


br3 = CircularBuffer(5)
br3.add(None)
print(br3.toString())

br3.add("Hello")
br3.add("Hello")
print(br3.toString())
br3.add(None)
br3.add("Test")
print(br3.toString())
print(br3.mode())

br3.add("Hello")
print(br3.mode())
