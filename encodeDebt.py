# Filename: encodeDebt.py
# Author: Khawm Mung
# Description: This script encodes the 'debt-to-income-ratio' column from categorical values to numerical values

# import libraries and packages here
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import sys
import os

# since we'll be working large csv files, it's a good idea to use chunks
chunk_size = 50 # adjust this based on available memory, pandas will read the csv file in chunks of 10000 rows

# throw a message if the user does not provide a csv file to read from
if len(sys.argv) < 2:
    print("Pleae provide a csv file to read from.")
    sys.exit()

filename = sys.argv[1] # get the filename from the command line argument

# dictionary for column encdoing
debt_to_income_ratio = {
    '<20%': 19, 
    '20%-<30%': 25, 
    '30%-<36%': 33, 
    '37%': 37, 
    '38%': 38, 
    '39%': 39, 
    '40%': 40, 
    '41%': 41,
    '42%': 42,
    '43%': 43,
    '44%': 44,
    '45%': 45,
    '46%': 46,
    '47%': 47,
    '48%': 48,
    '49%': 49,
    '50%-60%': 55,
    '60%': 60,
    '>60%': 61,
    'NA': -1,
    'Exempt': 1111
}

# create a modified dictionary to handle range values
range_dict = {key: value for key in debt_to_income_ratio for value in key.split('-')}

# define the output file name
base_name = os.path.basename(filename)
base_name = os.path.splitext(base_name)[0]
output_file = f"{base_name}_encoded_debt.csv"

chunk_number = 0 # keep track of the chunk number
first_chunk = True # keep track of the first chunk

# keep the default na values as empty strings
for chunk in pd.read_csv(filename, chunksize=chunk_size, keep_default_na=False, low_memory=False):
    chunk_number += 1
    print(f"Processing chunk {chunk_number}")

    # define custom function for mapping
    def map_values(value):
        return debt_to_income_ratio.get(value, value)

    # apply encoding to the columns
    chunk['debt_to_income_ratio'] = chunk['debt_to_income_ratio'].apply(map_values)
            
    # write the chunk to the output file
    if first_chunk:
        chunk.to_csv(output_file, index=False, mode='w')
        first_chunk = False
    else:
        chunk.to_csv(output_file, index=False, mode='a', header=False)