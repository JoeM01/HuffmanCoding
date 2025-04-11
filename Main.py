import huffman
import compressorsMain
import visualizations as vs
import pandas as pd
import os
import datetime


def bulkcompress(input_file, runs = 1):
    compressors = {
        "huffman": huffman.huffman_compressor, #basic huffman coding
        "zlib": compressorsMain.algorithm_compressor, #LZ77/HUFFMAN(DEFLATE) - Built off gzip algorithm
        "lzma": compressorsMain.algorithm_compressor, #LZ-Markov Chain - 7zip
        "bz2": compressorsMain.algorithm_compressor, #BWT, RLE, MTF, huffman
        "gzip": compressorsMain.algorithm_compressor, # gzip, deflate   
    }

    results = {}
    for run in range(runs):
        for name, compressor_func in compressors.items():
            print(f"RUNNING {name} COMPRESSOR... (Run {run+1})")
            print("-------------------------------")
            try:
                results[name] = compressor_func(input_file=input_file, automated=True, algorithm=name,)
            except TypeError:
                results[name] = compressor_func(input_file=input_file, automated=True,)
            print("-------------------------------")
                #print(results) #debug to ensure results are stored properly
        csv_results = save_results_to_csv(results, input_file)
    return csv_results


def save_results_to_csv(results, input_file):
    time = datetime.datetime.now().strftime("%d-%m")
    input_ext = input_file.split(".")[-1]
    filename = f"CSV-Visualizations\\compression_results_{input_ext}_{time}.csv"

    df = pd.DataFrame.from_dict(results, orient="index") #construct data table
    
    df.index.name = "compressor_name"
    df.reset_index(inplace=True) # Names the blank index with comp names, panda uses the keys (names) as index. 

    df = df.round({"compression_ratio": 2, "compress_time": 4, "decompress_time": 4, "percentage_reduction": 2})
    #df.to_csv(filename)
    if os.path.exists(filename):
        df.to_csv(filename, mode="a", header=False, index=False)  # Append, no header
    else:
        df.to_csv(filename, index=False) #else create file, with header.
    print(f"Results saved to {filename}")

    return filename



#For debugging individual compressors.
def choosecompressor():
    choice = int(input("Select your input file: "))
    mode = ""

    if (choice == 1):
        mode = huffman.huffman_compressor()
    elif (choice == 2):
        mode = compressorsMain.algorithm_compressor(algorithm="zlib")
    elif (choice == 3):
        mode = compressorsMain.algorithm_compressor(algorithm="lzma")
    elif (choice== 4):
        mode = compressorsMain.algorithm_compressor(algorithm="bz2")
    return mode

     


#Runnables --

    
input_file = "Datasets\\enwikivoyage-20250220-stub-meta-current.xml"
csvresults = bulkcompress(input_file) #Return results stored in var

vs.showgraph(csvresults) #used then for visualizations