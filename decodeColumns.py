# Filename: decodeColumns.py
# Author: Khawm Mung
# Description: This script reads in a JSON file that contains the encoded dictionary of all the columns and decode them

import json

# load the json file containing all the encoding dictionaries
with open('all_encodings.json', 'r') as f:
    all_encoding_dicts = json.load(f)

# decoding the values in column1
column_name = 'column1'
encoding_dict = all_encoding_dicts.get(column_name, {})
decoded_values = [value for value in df[column_name].map(encoding_dict)]
