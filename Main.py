import huffmanFinal
import compressorsMain
import visualizations as vs
import pandas as pd
import os


#TO DO
#Make calling compressors dynamic - DONE
#Export compression data to txt file on each run - DONE - CHANGED TO CVS, OLD METHOD IN OLD FOLDER.
#Visualize data(?) - matplot should now work as I've made the data actually return instead of just running the func

def bulkcompress(input_file, runs = 2):
    compressors = {
        #"ZLIB": zlibcompress.zlib_compressor,
        #"LZMA": lzmacompress.lzma_compressor,
        #"BZ2": bz2compress.bz2_compressor,
        "HUFFMAN": huffmanFinal.huffman_compressor, #simple, basic huffman
        "zlib": compressorsMain.algorithm_compressor, #LZ77/HUFFMAN(DEFLATE) 
        "lzma": compressorsMain.algorithm_compressor, #LZ-Markov Chain
        "bz2": compressorsMain.algorithm_compressor, #burrows wheeler, runlengthencode, movetofront, huffman
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
        save_results_to_csv(results)
    return results


def save_results_to_csv(results, filename="compression_outputs\\compression_results.csv"):
    df = pd.DataFrame.from_dict(results, orient="index") #construct data table
    
    df.index.name = "compressor_name"
    df.reset_index(inplace=True) # Names the blank index with comp names, panda uses the keys (names) as index. 

    df = df.round({"compression_ratio": 2, "compress_time": 4, "percentage_reduction": 2})
    #df.to_csv(filename)
    if os.path.exists(filename):
        df.to_csv(filename, mode="a", header=False, index=False)  # Append, no header
    else:
        df.to_csv(filename, index=False) #else create file, with header.
    print(f"Results saved to {filename}")

    return filename



#Indvidual Compressors with input-based file selection, and outputs of a file containing the data - For debugging individual compressors.
def choosecompressor():

    choice = int(input("Select your compressor: "))
    mode = ""

    if (choice == 1):
        mode = huffmanFinal.huffman_compressor()
    elif (choice == 2):
        mode = compressorsMain.algorithm_compressor(algorithm="zlib")
    elif (choice == 3):
        mode = compressorsMain.algorithm_compressor(algorithm="lzma")
    elif (choice== 4):
         mode = compressorsMain.algorithm_compressor(algorithm="bz2")
    return mode,

     


#Runnables --
if __name__ == "__main__":
    
    input_file = "Datasets\\alice29.txt"
    file_name="compression_outputs\\compression_results.csv"
    #compressed_data = "compressed_output"
    #decompressed_data = "decompressed_output"
    bulkcompress(input_file)
    #file = save_results_to_csv(results)

    vs.showgraph(file_name)