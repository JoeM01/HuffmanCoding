import time
import os
import importlib

#PRIMARY COMPRESSION HANDLER


def algorithm_compress(input_file, compressed_file, algorithm = None):
    module = importlib.import_module(algorithm) #importlib based off bulk compressor algorithm fields

    with open(input_file, 'rb') as file:
        data = file.read()

    start_time = time.time()
    compressed_data = module.compress(data) #assuming compressors follow consistent syntax
    compress_time = time.time() - start_time

    with open(compressed_file, 'wb') as file:
        file.write(compressed_data)

    original_size = os.path.getsize(input_file) 
    compressed_size = os.path.getsize(compressed_file)
    percentage_reduction = ((original_size - compressed_size) / original_size) * 100 
    compression_ratio = original_size / compressed_size 
    compressor_name = algorithm
    
    return{
        #'compressor_name': compressor_name,
        'compress_time': compress_time,
        'original_size': original_size,
        'compressed_size': compressed_size,
        'percentage_reduction': percentage_reduction,
        'compression_ratio': compression_ratio
    }


def algorithm_decompress(compressed_file, decompressed_file, algorithm = None):
    module = importlib.import_module(algorithm)
    with open(compressed_file, 'rb') as file:
        compressed_data = file.read()

    start_time = time.time()
    decompressed_data = module.decompress(compressed_data)
    decompress_time = time.time() - start_time

    with open(decompressed_file, 'wb') as file:
        file.write(decompressed_data) #write data to file var
    return{'decompress_time': decompress_time,}



def algorithm_compressor(input_file = None, compressed_File = None, decompressed_file = None, automated = False, algorithm = None): #to call in main
    try:

        if not automated:
            input_file = input("Enter the path of the input file: ")
            compressed_file = input("Enter the path of the compressed file: ")
            decompressed_file = input("Enter the path of the decompressed file: ")
        if automated:
            #input file specified in main
            file_name = os.path.basename(input_file)
            compressed_file = f"compression_outputs\\{algorithm}_{file_name}_compressed.bin" #organising file names, utilizing album and original name
            decompressed_file = f"compression_outputs\\{algorithm}_{file_name}_decompressed.txt"

        compressed = algorithm_compress(input_file, compressed_file, algorithm)
        decompressed = algorithm_decompress(compressed_file, decompressed_file, algorithm)

        results = {**compressed, **decompressed} #joins both dictionaries to utilize metric outputs of both.

        print(f"Original Size: {compressed['original_size']} bytes")
        print(f"Compressed Size: {compressed['compressed_size']} bytes")
        print(f"Compression Ratio: {compressed['compression_ratio']:.2f}")
        print(f"Time Taken to Compress: {compressed['compress_time']:.4f} seconds")
        print(f"Percentage Reduction: {compressed['percentage_reduction']:.2f}%")
        print(f"Decompressed! Time taken:{decompressed['decompress_time']:.4f} seconds")

        return results

    except FileNotFoundError as e:
        print(f"Error {e}")
