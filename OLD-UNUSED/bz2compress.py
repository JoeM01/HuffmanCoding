import bz2
import time
import os



def bz2_compress(input_file, compressed_file):
    with open(input_file, 'rb') as file:
        data = file.read()

    start_time = time.time()
    compressed_data = bz2.compress(data)
    compress_time = time.time() - start_time

    with open(compressed_file, 'wb') as file:
        file.write(compressed_data)

    original_size = os.path.getsize(input_file) 
    compressed_size = os.path.getsize(compressed_file)
    percentage_reduction = ((original_size - compressed_size) / original_size) * 100 
    compression_ratio = original_size / compressed_size 
    
    return{
        'compress_time': compress_time,
        'original_size': original_size,
        'compressed_size': compressed_size,
        'percentage_reduction': percentage_reduction,
        'compression_ratio': compression_ratio
    }


def bz2_decompress(compressed_file, decompressed_file):
    with open(compressed_file, 'rb') as file:
        compressed_data = file.read()

    decompressed_data = bz2.decompress(compressed_data)

    with open(decompressed_file, 'wb') as file:
        file.write(decompressed_data)



def bz2_compressor(input_file = None, compressed_File = None, decompressed_file = None, automated = False): #to call in main
    try:

        if not automated:
            input_file = input("Enter the path of the input file: ")
            compressed_file = input("Enter the path of the compressed file: ")
            decompressed_file = input("Enter the path of the decompressed file: ")
        if automated:
            #input file specified in main
            file_name = os.path.basename(input_file)
            compressed_file = f"compression_outputs\\bz2_{file_name}_compressed.bin"
            decompressed_file = f"compression_outputs\\bz2_{file_name}_decompressed.txt"

        compressed = bz2_compress(input_file, compressed_file)

        print(f"Original Size: {compressed['original_size']} bytes")
        print(f"Compressed Size: {compressed['compressed_size']} bytes")
        print(f"Compression Ratio: {compressed['compression_ratio']:.2f}")
        print(f"Time Taken to Compress: {compressed['compress_time']:.4f} seconds")
        print(f"Percentage Reduction: {compressed['percentage_reduction']:.2f}%")

        decompressed = bz2_decompress(compressed_file, decompressed_file)

        print(f"Decompressed!")
        return compressed

    except FileNotFoundError as e:
        print(f"Error {e}")
