global str, binary_map_char

str = open('alice29.txt')
binary_map_char = {}


class Node:   
    def __init__(self, freq, data, left, right):  #initlizing the node object.
        self.freq = freq # freq is just total letter frequency
        self.data = data
        self.left = left
        self.right = right

#Generates huffman tree from an input dictionary.        

def generate_tree(charDict): #function that is called in 'encode'
    keyset = charDict.keys()
    prioQueue = [] # where nodes are stored in priority.
    for c in keyset: #for each char in keyset, create node.
        node = Node(charDict[c], c, None, None) # initializes node class, with frequencyset to charDict[c], data to c, left right as none.
        prioQueue.append(node)
        prioQueue = sorted(prioQueue, key= lambda x:x.freq) # Lambda is a nameless function, for when you only need it once or twice - sorted by smallest freq

    while len(prioQueue) > 1: #if 2 elements, merge
        first = prioQueue.pop(0) 
        second = prioQueue.pop(0) #pop first/smallest elements (pop 0)
        mergeNode = Node(first.freq + second.freq, '-', first, second) #REMEMBER its using node class, so freq, data is '-', left right are first second
        
        prioQueue.append(mergeNode)
        prioQueue = sorted(prioQueue, key= lambda x:x.freq) #Sorts by the second tuple in prioque - queue is ordered by 2nd's frequency

    return prioQueue.pop()



def set_binary_code(node, str):
    if not node is None: #if node is not 'none'
        if node.left is None and node.right is None: #check if left&right nodes are empty, then reached leaf (bottom char)
            binary_map_char[node.data] = str

        #left node
        str += '0'
        set_binary_code(node.left, str) #setting left node to 'str' (which is the binary map of the node data)
        str = str[:-1] #exclude last char as we will have an extra 0

        str += '1'
        set_binary_code(node.right, str)
        str = str[:-1]


#Encoding of chars--

def encode(str):
    charDict = {} #dictionary of all chars
    for c in str: #checks each character in string
        if not c in charDict: 
            charDict[c] = 1 # if not in mapping dict - add with count 1 
        else:
            charDict[c] += 1 #if already in, increase count by 1

    root = generate_tree(charDict) #root is return of this func

    set_binary_code(root, '') #calls this func

    print(' char | huffman code')
    for char in charDict:
        print(' %-4r |%12s' % (char, binary_map_char[char]))

    #print out entire binary code.
    s = '' 
    for c in str:
        s += binary_map_char[c]
    return s

print(encode(str))