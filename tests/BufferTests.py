from utils import circularBuffer
from utils.circularBuffer import CircularBuffer

br = CircularBuffer(3)
input1 = [1,2,3]
input2 = [3,1,2]
input3 = [2,3,1]

inputTotal = [input1, input2, input3]

inputRealTotal = [inputTotal,inputTotal,inputTotal]
br.initQueue(inputRealTotal)
print(br.toString())
print(br.mean())
