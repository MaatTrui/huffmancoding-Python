import time
from collections import deque
from math import ceil
with open('string.txt','rt') as file:
    string = file.read()

table = {}
class node:
    def __init__(self,char,freq,left=None,right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right =right
        self.huff = []
    
def generate(node, val =[]):
    global table
    val = val + node.huff
    if(node.left):
        generate(node.left,val)
    if(node.right):
        generate(node.right,val) 
    if(not node.left and not node.right):
        table[node.char] = val



def checkFrequency(string):
    freq ={}
    for a in string:
        if a in freq:
            freq[a]+= 1
        else:
            freq[a] = 1
    return freq


def encode(uncompressed,table):
    result = deque()
    compressed = 0
    pos = 0
    for a in uncompressed:
        for a in table[a]:
            if pos>7:
                result.append(bytes([compressed]))
                pos = 0
            if a:
                compressed |= 1 << pos
            else:
                compressed &= ~(1<<pos)
            pos += 1
    return result


start = time.time()
nodes = []  
freq = checkFrequency(string)
i = 0
for x in freq.keys():
    nodes.append(node(x,freq[x]))
while len(nodes) > 1 :
    nodes = sorted(nodes, key=lambda x: x.freq)
    left = nodes[0]
    right = nodes[1]
    left.huff.append(False)
    right.huff.append(True)
    nodes.append(node('', left.freq+right.freq, left,right))
    nodes.remove(left)
    nodes.remove(right)
    

generate(nodes[0])
hasil = encode(string, table)
with open('compressed.bin','wb') as file:
     while(hasil):
         file.write(hasil.popleft())
     file.close

with open('table.txt','wt') as file:
    c = str(len(table.keys())) + "\n"
    file.write(c)
    for a in list(table.keys()):
        file.write(str(a) + "\n")
    for i in list(table.keys()):
        for codes in table[i]:
            file.write(str(int(codes)))
        file.write("\n")
    file.close


print (time.time() - start, "seconds")