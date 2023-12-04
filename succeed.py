import pandas as pd
import sys
import os

chunk_size = 30  # adjust this based on available memory
filename = sys.argv[1]  # input file

base_name = os.path.basename(filename)
base_name = os.path.splitext(base_name)[0]
filtered_filename = f"{base_name}_success.csv"  # output file

# Use a flag to indicate whether the filtered file should be overwritten or appended to
first_chunk = True

for chunk in pd.read_csv(filename, chunksize=chunk_size, low_memory=False):
    filtered_chunk = chunk[chunk['action_taken'] == 1]
    
    if first_chunk:
        filtered_chunk.to_csv(filtered_filename, index=False, mode='w')
        first_chunk = False
    else:
        filtered_chunk.to_csv(filtered_filename, mode='a', header=False, index=False)