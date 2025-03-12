import matplotlib.pyplot as plt
import pandas as pd


def showgraph(filename):
    df = pd.read_csv(filename)
    
    #merges compressor names into one, with all results averaged.
    compressor_avg = df.groupby("compressor_name")[["compress_time", "percentage_reduction"]].mean()

    plt.figure(figsize=(8, 5))
    plt.scatter(compressor_avg["compress_time"], compressor_avg["percentage_reduction"], color="green", s=100)

    plt.xlabel("Compression Time (seconds)")
    plt.ylabel("Percentage Reduction")
    plt.title("Compression Time vs Percentage Reduction")

    # Label each point with its compressor name

    for compressor, row in compressor_avg.iterrows():
        plt.annotate(compressor, (row["compress_time"], row["percentage_reduction"]), fontsize=10, xytext=(5,5), textcoords="offset points")
    
    print(compressor_avg) #testing to see avg outputs

    plt.show() # if perm error, close csv file - stops from using.