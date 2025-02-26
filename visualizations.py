import matplotlib.pyplot as plt
import pandas as pd


def showgraph(filename):
    df = pd.read_csv(filename)

    plt.figure(figsize=(8, 5))
    plt.scatter(df["compress_time"], df["percentage_reduction"], color="green", s=100)

    plt.xlabel("Compression Time (seconds)")
    plt.ylabel("Percentage Reduction")
    plt.title("Compression Time vs Percentage Reduction")

    # Label each point with its compressor name
    for i, txt in enumerate(df["compressor_name"]):
        plt.annotate(txt, (df["compress_time"][i], df["percentage_reduction"][i]), fontsize=10, xytext=(5,5), textcoords="offset points")

    plt.show() # if perm error, close csv file - stops from using.