# Filename: encodeColumns.py
# Author: Khawm Mung
# Description: This script reads the columns of a spreadsheet and check if it does not have numerical encodings.
# Description: Columns with values defined in the dictionaries will be replaced with the numerical encodings from the dictionaries.

# import libraries and packages here
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import sys
import os
import json

# since we'll be working large csv files, it's a good idea to use chunks
chunk_size = 50 # adjust this based on available memory, pandas will read the csv file in chunks of 10000 rows

# throw a message if the user does not provide a csv file to read from
if len(sys.argv) < 2:
    print("Pleae provide a csv file to read from.")
    sys.exit()

filename = sys.argv[1] # get the filename from the command line argument

# TODOs: create a dictionary for the column values and pair them with encoded numericals
# initialize a dictionary for encoding
# initialize dictionaries for each columns
# repeat for each columns
action_taken = {
    'Loan originated': 1, 
    'Application approved but not accepted': 2, 
    'Application denied': 3, 
    'Application withdrawn by applicant': 4, 
    'File closed for incompleteness': 5, 
    'Purchased loan': 6, 
    'Preapproval request denied': 7, 
    'Preapproval request approved but not accepted': 8
}

purchaser_type = {
    'Not Applicable': 0, 
    'Fannie Mae': 1,
    'Ginnie Mae': 2,
    'Freddie Mae': 3,
    'Farmer Mae': 4,
    'Private securitizer': 5,
    'Commercial bank, savings bank, or savings association': 6,
    'Credit Union, mortgage company, or finance company': 71,
    'Life insurance company': 72,
    'Affiliate institution': 8,
    'Other type of purchaser': 9
}

preapproval = {
    'Preapproval requested': 1,
    'Preapproval not requested': 2
}

loan_type = {
    'Conventional': 1,
    'Federal Housing Administration': 2,
    'Veterans Affairs guaranteed': 3,
    'USDA Rural housing Service or Farm Service Agency guaranteed': 4
}

loan_purpose = {
    'Home purchase': 1,
    'Home improvement': 2,
    'Refinancing': 31,
    'Cash-out refinancing': 32,
    'Other purpose': 4,
    'Not Applicable': 5
}

lien_status = {
    'Secured by a first lien': 1,
    'Secured by a subordinate lien': 2
}

reverse_mortgage = {
    'Reverse mortgage': 1,
    'Not a reverse mortgage': 2,
    'Exempt': 1111
}

open_end_line_of_credit = {
    'Open-end line of credit': 1,
    'Not an open-end line of credit': 2,
    'Exempt': 1111
}

business_or_commercial_purpose = {
    'Primarily for a business or commercial purpose': 1,
    'Not primarily for a business or commercial purpose': 2,
    'Exempt': 1111
}

hoepa_status = {
    'High-cost mortgage': 1,
    'Not a high-cost mortgage': 2,
    'Not Applicable': 3
}

negative_amortization = {
    'Negative amortization': 1,
    'No negative amortization': 2,
    'Exempt': 1111
}

interest_only_payment = {
    'Interest only payments': 1,
    'No-interest only payments': 2,
    'Exempt': 1111
}

balloon_payment = {
    'Balloon payment': 1,
    'No balloon payment': 2,
    'Exempt': 1111
}

other_nonamortizing_features = {
    'Other non-fully amortizing features': 1,
    'No other non-fully amortizing features': 2,
    'Exempt': 1111
}

construction_method = {
    'Site-built': 1,
    'Manufactured home': 2
}

occupancy_type = {
    'Principal residence': 1,
    'Second residence': 2,
    'Investment property': 3
}

applicant_credit_score_type = {
    'Equifax Beacon 5.0': 1,
    'Experian Fair Isaac': 2,
    'FICO Risk Score Classic 04': 3,
    'FICO Risk Score Classic 98': 4,
    'VantageScore 2.0': 5,
    'VantageScore 3.0': 6,
    'More than one credit scoring model': 7,
    'Other credit scoring model': 8,
    'Not applicable': 9,
    'Exempt': 1111
}

# for columns that have hyphens in the name just loosely match the column name to the dictionary object name
# for example: co_applicant_credit_score_type is the column name in the csv file, but the dict obj name is co_applicant_credit_score_type
co_applicant_credit_score_type = {
    'Equifax Beacon 5.0': 1,
    'Experian Fair Isaac': 2,
    'FICO Risk Score Classic 04': 3,
    'FICO Risk Score Classic 98': 4,
    'VantageScore 2.0': 5,
    'VantageScore 3.0': 6,
    'More than one credit scoring model': 7,
    'Other credit scoring model': 8,
    'Not applicable': 9,
    'No co-applicant': 10,
    'Exempt': 1111
}

applicant_ethnicity_1 = {
    'Hispanic or Latino': 1,
    'Mexican': 11,
    'Puerto Rican': 12,
    'Cuban': 13,
    'Other Hispanic or Latino': 14,
    'Not Hispanic or Latino': 2,
    'Information not provided by applicant in mail, internet, or telephone application': 3,
    'Not applicable': 4
}

co_applicant_ethnicity_1 = {
    'Hispanic or Latino': 1,
    'Mexican': 11,
    'Puerto Rican': 12,
    'Cuban': 13,
    'Other Hispanic or Latino': 14,
    'Not Hispanic or Latino': 2,
    'Information not provided by applicant in mail, internet, or telephone application': 3,
    'Not applicable': 4,
    'No co-applicant': 5
}

applicant_ethnicity_observed = {
    'Collected on the basis of visual observation or surname': 1,
    'Not collected on the basis of visual observation or surname': 2,
    'Not applicable': 3
}

co_applicant_ethnicity_observed = {
    'Collected on the basis of visual observation or surname': 1,
    'Not collected on the basis of visual observation or surname': 2,
    'Not applicable': 3,
    'No co-applicant': 4
}

applicant_race_1 = {
    'American Indian or Alaska Native': 1,
    'Asian': 2,
    'Asian Indian': 21,
    'Chinese': 22,
    'Filipino': 23,
    'Japanese': 24,
    'Korean': 25,
    'Vietnamese': 26,
    'Other Asian': 27,
    'Black or African American': 3,
    'Native Hawaiian or Other Pacific Islander': 4,
    'Native Hawaiian': 41,
    'Guamanian or Chamorro': 42,
    'Samoan': 43,
    'Other Pacific Islander': 44,
    'White': 5,
    'Information not provided by applicant in mail, internet, or telephone application': 6,
    'Not applicable': 7
}

co_applicant_race_1 = {
    'American Indian or Alaska Native': 1,
    'Asian': 2,
    'Asian Indian': 21,
    'Chinese': 22,
    'Filipino': 23,
    'Japanese': 24,
    'Korean': 25,
    'Vietnamese': 26,
    'Other Asian': 27,
    'Black or African American': 3,
    'Native Hawaiian or Other Pacific Islander': 4,
    'Native Hawaiian': 41,
    'Guamanian or Chamorro': 42,
    'Samoan': 43,
    'Other Pacific Islander': 44,
    'White': 5,
    'Information not provided by applicant in mail, internet, or telephone application': 6,
    'Not applicable': 7,
    'No co-applicant': 8
}

applicant_sex = {
    'Male': 1,
    'Female': 2,
    'Information not provided by applicant in mail, internet, or telephone application': 3,
    'Not applicable': 4,
    'Applicant selected both male and female': 6
}

co_applicant_sex = {
    'Male': 1,
    'Female': 2,
    'Information not provided by applicant in mail, internet, or telephone application': 3,
    'Not applicable': 4,
    'No co-applicant': 5,
    'Co-applicant selected both male and female': 6
}

submission_of_application = {
    'Submitted directly to your institution': 1,
    'Not submitted directly to your institution': 2,
    'Not applicable': 3,
    'Exempt': 1111
}

initially_payable_to_institution = {
    'Initially payable to your institution': 1,
    'Not initially payable to your institution': 2,
    'Not applicable': 3,
    'Exempt': 1111
}

denial_reason_1 = {
    'Debt-to-income ratio': 1,
    'Employment history': 2,
    'Credit history': 3,
    'Collateral': 4,
    'Insufficient cash (downpayment, closing costs)': 5,
    'Unverifiable information': 6,
    'Credit application incomplete': 7,
    'Mortgage insurance denied': 8,
    'Other': 9,
    'Not applicable': 10
}

denial_reason_2 = {
    'Debt-to-income ratio': 1,
    'Employment history': 2,
    'Credit history': 3,
    'Collateral': 4,
    'Insufficient cash (downpayment, closing costs)': 5,
    'Unverifiable information': 6,
    'Credit application incomplete': 7,
    'Mortgage insurance denied': 8,
    'Other': 9
}

denial_reason_3 = {
    'Debt-to-income ratio': 1,
    'Employment history': 2,
    'Credit history': 3,
    'Collateral': 4,
    'Insufficient cash (downpayment, closing costs)': 5,
    'Unverifiable information': 6,
    'Credit application incomplete': 7,
    'Mortgage insurance denied': 8,
    'Other': 9
}

denial_reason_4 = {
    'Debt-to-income ratio': 1,
    'Employment history': 2,
    'Credit history': 3,
    'Collateral': 4,
    'Insufficient cash (downpayment, closing costs)': 5,
    'Unverifiable information': 6,
    'Credit application incomplete': 7,
    'Mortgage insurance denied': 8,
    'Other': 9
}

denial_reason_5 = {
    'Debt-to-income ratio': 1,
    'Employment history': 2,
    'Credit history': 3,
    'Collateral': 4,
    'Insufficient cash (downpayment, closing costs)': 5,
    'Unverifiable information': 6,
    'Credit application incomplete': 7,
    'Mortgage insurance denied': 8,
    'Other': 9
}

# create a dictionary of dictionaries for the encodings
column_dictionaries = {
    'action_taken': action_taken,
    'purchaser_type': purchaser_type,
    'preapproval': preapproval,
    'loan_type': loan_type,
    'loan_purpose': loan_purpose,
    'lien_status': lien_status,
    'reverse_mortgage': reverse_mortgage,
    'open_end_line_of_credit': open_end_line_of_credit,
    'business_or_commercial_purpose': business_or_commercial_purpose,
    'hoepa_status': hoepa_status,
    'negative_amortization': negative_amortization,
    'interest_only_payment': interest_only_payment,
    'balloon_payment': balloon_payment,
    'other_nonamortizing_features': other_nonamortizing_features,
    'construction_method': construction_method,
    'occupancy_type': occupancy_type,
    'applicant_credit_score_type': applicant_credit_score_type,
    'co_applicant_credit_score_type': co_applicant_credit_score_type,
    'applicant_ethnicity-1': applicant_ethnicity_1,
    'co_applicant_ethnicity_1': co_applicant_ethnicity_1,
    'applicant_ethnicity_observed': applicant_ethnicity_observed,
    'co_applicant_ethnicity_observed': co_applicant_ethnicity_observed,
    'applicant_race-1': applicant_race_1,
    'co_applicant_race_1': co_applicant_race_1,
    'applicant_sex': applicant_sex,
    'co_applicant_sex': co_applicant_sex,
    'submission_of_application': submission_of_application,
    'initially_payable_to_institution': initially_payable_to_institution,
    'denial_reason-1': denial_reason_1,
    'denial_reason-2': denial_reason_2,
    'denial_reason-3': denial_reason_3,
    'denial_reason-4': denial_reason_4,
}

# define the output file name
base_name = os.path.basename(filename)
base_name = os.path.splitext(base_name)[0]
output_file = f"{base_name}_encoded_data.csv"

chunk_number = 0 # keep track of the chunk number
first_chunk = True # keep track of the first chunk

# keep the default na values as empty strings
for chunk in pd.read_csv(filename, chunksize=chunk_size, keep_default_na=False, low_memory=False):
    chunk_number += 1
    print(f"Processing chunk {chunk_number}")

    # apply encoding to the columns
    for column in chunk.columns:
        # Replace empty cells with -1
        #chunk[column] = chunk[column].astype(int).replace({'': '-1'})

        # replace nan values with -1 for applicant_ethnicity_1
        #column['applicant_ethnicity_1']

        # Check if the column values are strings and a dictionary exists for the column
        if chunk[column].dtype == 'object' and column in column_dictionaries:
            # map the values to the dictionary
            if column == 'action_taken':
                chunk[column] = chunk[column].replace(action_taken)
            elif column == 'purchaser_type':
                chunk[column] = chunk[column].replace(purchaser_type)
            elif column == 'preapproval':
                chunk[column] = chunk[column].replace(preapproval)
            elif column == 'loan_type':
                chunk[column] = chunk[column].replace(loan_type)
            elif column == 'loan_purpose':
                chunk[column] = chunk[column].replace(loan_purpose)
            elif column == 'lien_status':
                chunk[column] = chunk[column].replace(lien_status)
            elif column == 'reverse_mortgage':
                chunk[column] = chunk[column].replace(reverse_mortgage)
            elif column == 'open_end_line_of_credit':
                chunk[column] = chunk[column].replace(open_end_line_of_credit)
            elif column == 'business_or_commercial_purpose':
                chunk[column] = chunk[column].replace(business_or_commercial_purpose)
            elif column == 'hoepa_status':
                chunk[column] = chunk[column].replace(hoepa_status)
            elif column == 'negative_amortization':
                chunk[column] = chunk[column].replace(negative_amortization)
            elif column == 'interest_only_payment':
                chunk[column] = chunk[column].replace(interest_only_payment)
            elif column == 'balloon_payment':
                chunk[column] = chunk[column].replace(balloon_payment)
            elif column == 'other_nonamortizing_features':
                chunk[column] = chunk[column].replace(other_nonamortizing_features)
            elif column == 'construction_method':
                chunk[column] = chunk[column].replace(construction_method)
            elif column == 'occupancy_type':
                chunk[column] = chunk[column].replace(occupancy_type)
            elif column == 'applicant_credit_score_type':
                chunk[column] = chunk[column].replace(applicant_credit_score_type)
            elif column == 'co_applicant_credit_score_type':
                chunk[column] = chunk[column].replace(co_applicant_credit_score_type)
            elif column == 'applicant_ethnicity-1':
                chunk[column] = chunk[column].replace(applicant_ethnicity_1)
            elif column == 'co_applicant_ethnicity_1':
                chunk[column] = chunk[column].replace(co_applicant_ethnicity_1)
            elif column == 'applicant_ethnicity_observed':
                chunk[column] = chunk[column].replace(applicant_ethnicity_observed)
            elif column == 'co_applicant_ethnicity_observed':
                chunk[column] = chunk[column].replace(co_applicant_ethnicity_observed)
            elif column == 'applicant_race-1':
                chunk[column] = chunk[column].replace(applicant_race_1)
            elif column == 'co_applicant_race_1':
                chunk[column] = chunk[column].replace(co_applicant_race_1)
            elif column == 'applicant_sex':
                chunk[column] = chunk[column].replace(applicant_sex)
            elif column == 'co_applicant_sex':
                chunk[column] = chunk[column].replace(co_applicant_sex)
            elif column == 'submission_of_application':
                chunk[column] = chunk[column].replace(submission_of_application)
            elif column == 'initially_payable_to_institution':
                chunk[column] = chunk[column].replace(initially_payable_to_institution)
            elif column == 'denial_reason-1':
                chunk[column] = chunk[column].replace(denial_reason_1)
            elif column == 'denial_reason-2':
                chunk[column] = chunk[column].replace(denial_reason_2)
            elif column == 'denial_reason-3':
                chunk[column] = chunk[column].replace(denial_reason_3)
            elif column == 'denial_reason-4':
                chunk[column] = chunk[column].replace(denial_reason_4)

    # write the chunk to the output file
    if first_chunk:
        chunk.to_csv(output_file, index=False, mode='w')
        first_chunk = False
    else:
        chunk.to_csv(output_file, index=False, mode='a', header=False)