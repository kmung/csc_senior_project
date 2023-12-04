# Filename: cleanup.py
# Author: Khawm Mung
# Description: This script cleans a csv file, remove blank columns and rows. It outputs the column headings to a new file.
# Input: recevies a csv file as a command-line argument

# import libraries and packages here
import argparse
import pandas as pd
from pandas import Series, DataFrame

# define command-line arguments
parser = argparse.ArgumentParser(description='Clean up a CSV file and output column headings')
parser.add_argument('input_file', type=str, help='path to input CSV file')

# parse command-line arguments
args = parser.parse_args()

# read in csv files
df = pd.read_csv(args.input_file, header=0) # header=0 assigns the first row of the file as the column headings

# remove blank rows
df.dropna(how='all', inplace=True) # inplace=True modifies the dataframe in place

# remove blank columns
df.dropna(axis=1, how='all', inplace=True)

# save cleaned data to a new file
cleaned_file = args.input_file.split('.')[0] + '_cleaned.csv'
df.to_csv(cleaned_file, index=False)

# save column headings to a new file titled column_headings.txt
headings_file = args.input_file.split('.')[0] + '_column_headings.txt'
with open(headings_file, 'w') as f:
    f.write('\n'.join(list(df.columns)))

