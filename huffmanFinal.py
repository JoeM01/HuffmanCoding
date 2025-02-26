import time
import os

#root var is in relation to generated trees

#binary_map_char stores the char and its subsequent binary code.
#check set_binary_code for info - 

binary_code_storage = {}

#This huffman algorithm is only good for text files as it handles chars, there is potential to change it for images etc, but this method does not seem effective.

class Node:
    def __init__(self, freq, data, left=None, right=None):
        self.freq = freq
        self.data = data
        self.left = left
        self.right = right

def generate_tree(char_dict): #called in 'encode'
    prio_queue = []
    for char, freq in char_dict.items():
        prio_queue.append(Node(freq, char, None, None)) #loops through to return tuples for each, uses char_dict from encode {'a': 5, 'b': 2} becomes [('a', 5), ('b', 2)] 
        prio_queue.sort(key=lambda x: x.freq)
    

    while len(prio_queue) > 1:  #While queue has more than 1 item (root node)
        first = prio_queue.pop(0) #pop lowest freq and store as first
        second = prio_queue.pop(0) #pop 2ndlowest, store as second
        merge_node = Node(first.freq + second.freq, '-', first, second) #add 1st & 2nd freqs, blank for binarydata, 1 & 2 as left and right
        prio_queue.append(merge_node) #merge it back into queue
        prio_queue.sort(key=lambda x: x.freq) # Lambda is a nameless function, for when you only need it once or twice - sorted by smallest freq

    return prio_queue[0]

def set_binary_code(node, code):
    if node:
        if node.left is None and node.right is None: #checks if node has children (leaf node)
            binary_code_storage[node.data] = code #If traversed to the leaf, the node.data is the entire binary code it took to get there.
        else:
            set_binary_code(node.left, code + '0') #If not at leaf, keep traversing down adding a 0/1 depending on direction
            set_binary_code(node.right, code + '1')

#Encode for assigning frequency and calling treegen/binary code setting

def encode(input_bytes): #encode takes input bytes and tallies frequency, genning tree and codes via other funcs.
    byte_dict = {} 
    for byte in input_bytes: #looping 
        byte_dict[byte] = byte_dict.get(byte, 0) + 1 #add byte to dictionary, if it doesnt exist yet, add with freq of 0 - then increments by 1.
    
    root = generate_tree(byte_dict) # Generates a tree out of the input, stores it in root.
    
    set_binary_code(root, '') # Runs through the tree and adds binary codes - updating the binary_code_storage global
    
    encoded_str = ''.join(binary_code_storage[bit] for bit in input_bytes) #concats using join to combine all characters binary codes in a str into one.
    return encoded_str, root #root contains the tree itself, for decoding purposes

def decode(encoded_bytes, root): # ^^^
    decoded_bytes = bytearray() #empty container for decoded to be placed.
    node = root
    for bit in encoded_bytes:
        node = node.left if bit == '0' else node.right #traverses tree down binary codes
        if node.left is None and node.right is None:
            decoded_bytes.append(node.data) #if at leaf node, add it to decoded_bytes
            node = root #reset node back to root for loop.

    return decoded_bytes #returns the now populated decodedbytes

#Handles storing the information in binary, not just plaintext 1's & 0's
#Use with to open files, closes the file once the nest is complete.
#write_binary is essentially taking binary and converting it to an integer with base 2 which is proper.

def write_binary_to_file(encoded_str, output_file): 
    with open(output_file, 'wb') as file: 
        byte_array = bytearray()
        for i in range(0, len(encoded_str), 8): #range(start, stop, steps(8))
            byte = encoded_str[i:i+8] #each byte is a piece of the encoded string, with a len of 8
            byte_array.append(int(byte.ljust(8, '0'), 2)) #ljust is used to pad the end of a byte to a length of 8 using 0's. (end of str for eg)
        file.write(byte_array)                            #int (),2 - Stores it in in base 2, storing the bytes properly (0-255)

def read_binary_from_file(input_file):
    with open(input_file, 'rb') as file:    #Opens binary file using read binary 'rb'
        byte_array = bytearray(file.read())         #Stores bytes from file into bytearray, unsure if extra bytearray is needed
        return ''.join(f'{byte:08b}' for byte in byte_array) #Converts binary back into a string. {:08} - specifies pad to 8 bits, b specifies binary.

def file_compression(input_file, output_file):
    with open(input_file, 'rb') as file:
        input_bytes = file.read() #stores file

    start_time = time.time()
    encoded_str, root = encode(input_bytes) #calls encode using input_str, returns values into enc_str, root.
    compress_time = time.time() - start_time

    write_binary_to_file(encoded_str, output_file) #calls wbtf func, stores encoded binary str into output file as proper binary.

    original_size = os.path.getsize(input_file) #os import to get sizes for comparison
    compressed_size = os.path.getsize(output_file)

    percentage_reduction = ((original_size - compressed_size) / original_size) * 100 #should convert to percentage if formula is right
    compression_ratio = original_size / compressed_size #basic way to get compression ratio, needs work.

    results = {
        'original_size': original_size,
        'compressed_size': compressed_size,
        'compression_ratio': compression_ratio,
        'compress_time': compress_time,
        'percentage_reduction': percentage_reduction
    }
    #print(f"compress debug test {results}")
    return root, results #can return encoded str if needed for testing

def file_decompression(encoded_file, output_file, root):
    encoded_str = read_binary_from_file(encoded_file) #calls func which reads the binary and converts to string binary.

    start_time = time.time()
    decoded_str = decode(encoded_str, root) #traverses huffman tree and pieces chars together
    decode_time = time.time() - start_time

    with open(output_file, 'wb') as file: #standard write 
        file.write(decoded_str)

     #print("Compressed binary string:", encoded_str) - DEBUG TEST
    return decoded_str


def huffman_compressor(input_file = None, compressed_File = None, decompressed_file = None, automated = False): #reworked so it can be called in other files using imports.
    try:
        if not automated:
            input_file = input("Enter the path of the input file: ")
            compressed_file = input("Enter the path of the compressed file: ")
            decompressed_file = input("Enter the path of the decompressed file: ")
        if automated:
            #input file specified in main
            file_name = os.path.basename(input_file)
            compressed_file = f"compression_outputs\huffman_{file_name}_compressed.bin"
            decompressed_file = f"compression_outputs\huffman_{file_name}_decompressed.txt"

        root, compressed = file_compression(input_file, compressed_file) #root, compression filled from the returns in file_compression

        print(f"Original Size: {compressed['original_size']} bytes")
        print(f"Compressed Size: {compressed['compressed_size']} bytes")
        print(f"Compression Ratio: {compressed['compression_ratio']:.2f}")
        print(f"Time Taken to Compress: {compressed['compress_time']:.4f} seconds")
        print(f"Percentage Reduction: {compressed['percentage_reduction']:.2f}%")

        file_decompression(compressed_file, decompressed_file, root)
        print("Decompression complete! Ensure there is no data loss.") 
        return compressed #returns the encoded(results dictionary) from filecompression
    except FileNotFoundError as e:
        print(f"Error: {e}")




#huffman_compressor()