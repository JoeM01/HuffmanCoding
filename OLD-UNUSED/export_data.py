import csv
import datetime

def export_bulkdata(results): # base txt, convert to csv?
     bulk_output = "compression_outputs\\bulk_data_log.csv" 

     with open(bulk_output, 'a') as file: #append with a, or figure out how to make a new file foreach
          file.write("\n")
          file.write("=" * 40 + "\n")
          file.write(f"\nResults for bulk compress @ {datetime.datetime.now()}\n") # get current timestamp
          file.write("-" * 40 + "\n")
          
          for name, compressor_func in results.items(): # gets name and function
               if not compressor_func:
                    file.write(f"Error getting {name} \n\n")
                    continue
               file.write(f"\n{name} Compressor:\n")
               file.write(f"Original Size: {compressor_func['original_size']}\n")
               file.write(f"Compressed Size: {compressor_func['compressed_size']}\n")
               file.write(f"Compression Ratio: {compressor_func['compression_ratio']:.2f}\n")
               file.write(f"Time Taken to Compress: {compressor_func['compress_time']:.4f}\n")
               file.write(f"Percentage Reduction: {compressor_func['percentage_reduction']:.2f}\n")


               #compressor_func from results