#Convert Motec Log File into csv
#Take csv as input
import glob
import os
import numpy as np

"""Define the name of the file that needs to be analysed"""
motec_file = 'Silverstone-amr_v8_vantage_gt3-8-2023.03.31-08.09.18.csv'
motec_file2 = 'trial.csv'

"""Read the motec file line by line and create a list with each line as an item in the list"""
def raw_data(motec_file:str):

    with open(motec_file, 'r') as f:
        data_lines = [line.strip() for line in f]

    """Delete the contextual information and keep the track data"""
    content = data_lines[18:]

    return content

"""Reads the Motec File and returns the headers for each data type"""
def data_headers(motec_file:str)->list:

    with open(motec_file, 'r') as f:
        data_lines = [line.strip() for line in f]
    headers = data_lines[14]
    return headers

"""Reads the Motec File and returns the units for each data type"""
def data_units(motec_file:str)->list:

    with open(motec_file, 'r') as f:
        data_lines = [line.strip() for line in f]
    units = data_lines[15]
    return units





