import matplotlib.pyplot as plt
import pandas as pd
import os

def main():

    filename = 'dataset\enwikivoyage-20250220-stub-meta-current.xml'  # csv path
    dataset_type = 'XML'
    save_dir = "CSV-Visualizations/"
    
    # Load the CSV file and compute average metrics
    df_avg = load_csv(filename) 

    plot_scatter_ratio_time(df_avg, dataset_type, save_dir)
    plot_combined_bar_chart(df_avg, dataset_type, save_dir)


def load_csv(filename):
 
    #Load the CSV file, combined average metrics for each comp
    #return dataframe of average metrics
 
    df = pd.read_csv(filename)
    # Compute average metrics for each compressor across multiple runs
    df_avg = df.groupby('compressor_name').mean(numeric_only=True).reset_index()
    return df_avg

def plot_scatter_ratio_time(df, dataset_type, save_dir):
    #scatter plot for compression ratio vs. compression time.
    plt.figure(figsize=(10, 6))
    for i, row in df.iterrows():
        plt.scatter(row['compress_time'], row['compression_ratio'])
        plt.annotate(row['compressor_name'], (row['compress_time'], row['compression_ratio']))
    plt.xlabel('Compress Time (seconds)')
    plt.ylabel('Compression Ratio')
    plt.title(f'Compression Ratio vs. Compress Time for {dataset_type.upper()} Dataset')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f'{dataset_type}_ratio_vs_time.png'))
    plt.close()


def plot_combined_bar_chart(df, dataset_type, save_dir):
    #shows compress & decompress times for each algorithm for specified format
    bar_width = 0.35
    index = range(len(df))
    plt.figure(figsize=(12, 6))
    plt.bar(index, df['compress_time'], bar_width, label='Compress Time')
    plt.bar([i + bar_width for i in index], df['decompress_time'], bar_width, label='Decompress Time')
    plt.xlabel('Compressor')
    plt.ylabel('Time (seconds)')
    plt.title(f'Compression and Decompression Times for {dataset_type.upper()} Dataset')
    plt.xticks([i + bar_width / 2 for i in index], df['compressor_name'], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f'{dataset_type}_times.png'))
    plt.close()



main()