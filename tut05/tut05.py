
import pandas as pd
import openpyxl
from datetime import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
import numpy as np
import scipy.stats as ss
from collections import OrderedDict

start_time = datetime.now()

#Help https://youtu.be/N6PBd4XdnEw
def octant_range_names(mod=5000):

    try:
        df = pd.read_excel(
            r'C:\Users\Gargi\Desktop\2001EE89_2022\tut05\output_octant.xlsx')
    except ImportError:
        print("Wrong File")
    octant_name_id_mapping = {"1": "Internal outward interaction", "-1": "External outward interaction", "2": "External Ejection",
                              "-2": "Internal Ejection", "3": "External inward interaction", "-3": "Internal inward interaction", "4": "Internal sweep", "-4": "External sweep"}

    for i in range(1,9,1):
            df["Rank "+ str(i)]=''
    df["Rank 1 Octant ID"]=''
    df["Rank 1 Octant Name"]=''

    rank(df,0)
    k=[1,-1,2,-2,3,-3,4,-4]
    n=int(30000/mod)
    cr=2
    for i in range(n):
        df=rank(df,cr)
        cr+=1
    cr+=2
    df.at[cr,1]="Octant ID"
    df.at[cr,-1]="Octant Name"
    df.at[cr,2]="Count of Rank 1 Mod values"
    for i in range(8):
        count=0
        df.at[cr+1+i,1]=k[i]
        df.at[cr+1+i,-1]=octant_name_id_mapping[str(k[i])]
        for j in range(n):
            if (df.at[2+j, "Rank 1 Octant ID"] == k[i]):
                count=count+1
               
        df.at[cr+1+i,2]=count
    try:
        df.to_excel(
            'C:/Users/Gargi/Desktop/2001EE89_2022/tut05/output_octant.xlsx', index=False)
    except:
        print("Permission denied")
        
# For getting the ranks of each value 
def rank(df,cr):
    octant_name_id_mapping = {"1": "Internal outward interaction", "-1": "External outward interaction", "2": "External Ejection",
                                  "-2": "Internal Ejection", "3": "External inward interaction", "-3": "Internal inward interaction", "4": "Internal sweep", "-4": "External sweep"}
    rank_def = {}
    k=[1,-1,2,-2,3,-3,4,-4]
    for i in k:
        rank_def[df.at[cr, i]] =i

    values_sorted=sorted(rank_def.keys(),reverse=True)
    
    for i in range(8):
        key=rank_def[values_sorted[i]]
        if(key>0):
            df.at[cr,"Rank "+str(key*2-1)]=i+1
        else:
            df.at[cr,"Rank "+str(key*(-2))]=i+1
    df.at[cr, 'Rank 1 Octant ID'] = rank_def[values_sorted[0]]
    df.at[cr, 'Rank 1 Octant Name'] = octant_name_id_mapping[str(rank_def[values_sorted[0]])]

    return df


#For part 1 i.e.  Data Pre-processing : Code same as that of tut 1 except handling excel file
#To identify the octant by using U',V',W' values in the dataframe

def octant(df):
    for index, row in df.iterrows():
        if(row['''U'= U - U avg'''] > 0):
            if(row['''V'= V - V avg'''] > 0):
                if(row['''W'= W - W avg'''] > 0):
                    row['Octant'] = +1
                else:
                    row['Octant'] = -1
            else:
                if(row['''W'= W - W avg'''] > 0):
                    row['Octant'] = +4
                else:
                    row['Octant'] = -4
        else:
            if(row['''V'= V - V avg'''] > 0):
                if(row['''W'= W - W avg'''] > 0):
                    row['Octant'] = +2
                else:
                    row['Octant'] = -2
            else:
                if(row['''W'= W - W avg'''] > 0):
                    row['Octant'] = +3
                else:
                    row['Octant'] = -3

    return df

#To calculate the no of rows(in a given range from start to stop) having a particular octant value


def no_of_counts(df, start, stop, octant_value):
    ci = 0  # counter variable
    for j in range(start, stop+1, 1):
        if(df.loc[j, "Octant"] == octant_value):
            ci = ci+1

    return ci

# Part 2 : Calculation of octant count in a given mod range


def octant_identification(mod=5000):
    try:
        df = pd.read_excel(
            r'C:\Users\Gargi\Desktop\2001EE89_2022\tut05\octant_input.xlsx')
    except ImportError:
        print("Wrong File")

    '''For calculating the mean and storing it in columns'''
    df.at[0, 'U Avg'] = df['U'].mean(axis=0)
    df.at[0, 'V Avg'] = df['V'].mean(axis=0)
    df.at[0, 'W Avg'] = df['W'].mean(axis=0)
    df['''U'= U - U avg'''] = df['U']-df.loc[0, 'U Avg']
    df['''V'= V - V avg'''] = df['V']-df.loc[0, 'V Avg']
    df['''W'= W - W avg'''] = df['W']-df.loc[0, 'W Avg']
    n = len(df)
    df['Octant'] = df["U"]  # declaring Octant with dummy variables for now
    # for calculating the octant and storing it in Octant column of the dataframe
    df = octant(df)
    df[' '] = ''  # adding an empty column with empty values
    df.at[1, ' '] = "User Input"  # adding it the way it was in output file
    df['Octant ID'] = ''  # creating an empty column for storing ranges

    df.at[1, 'Octant ID'] = 'MOD '+str(mod)

    # storing possible values of octant in a list
    k = [1, -1, 2, -2, 3, -3, 4, -4]

    #creating columns of possible octant values
    for col in k:
        df[col] = ''
    df.at[0, 'Octant ID'] = 'Overall Count'

    #For calculating the overall counts of values in each octant
    for i in k:
        # value_counts returns list containing the number if occurrences  of different values present in the column
        df.at[0, i] = df['Octant'].value_counts()[i]

    #the starting row for writing the counts in ranges
    count = 2

    #for calculating ranges for summing the octants
    begin = 0000
    end = mod-1

    # for calculating counts in the given ranges and storing it
    while (begin < n):

        df.at[count, "Octant ID"] = str(begin)+"-"+str(end)
        for i in k:
            df.at[count, i] = no_of_counts(df, begin, end, i)
        count = count+1
        if(end != n-1):
            begin = end+1
        if(end == n-1):
            break
        if(begin+mod-1 <= n-1):
            end = begin+mod-1
        elif(begin+mod-1 > n-1):
            end = n-1
    try:
        df.to_excel(
            'C:/Users/Gargi/Desktop/2001EE89_2022/tut05/output_octant.xlsx', index=False)
    except:
        print("Permission denied")


# calling function for Part 1 and Part 2
octant_identification()


#Part 3
mod = 5000
octant_range_names(mod)




from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")





#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
