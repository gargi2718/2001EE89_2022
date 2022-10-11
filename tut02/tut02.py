from platform import python_version

import openpyxl
import pandas as pd
import numpy as np

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
            r'C:\Users\Gargi\Desktop\2001EE89_2022\tut02\input_octant_transition_identify.xlsx')
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
            'C:/Users/Gargi/Desktop/2001EE89_2022/tut02/output_octant_transition_identify.xlsx', index=False)
    except:
        print("Permission denied")


# calling function for Part 1 and Part 2
octant_identification()


#Part 3: Calculating the transition count for 
def overall_transition_count():
    k = [1, -1, 2, -2, 3, -3, 4, -4]
    #counter to keep track of rows so that we can store our output in specific rows 
    crr = 10
    # for reading the file and handling exception for wrong file path
    try:
        df = pd.read_excel(
            r'C:\Users\Gargi\Desktop\2001EE89_2022\tut02\output_octant_transition_identify.xlsx')
    except ImportError:
        print("Wrong File Path. Please check path and try again!")

    n = len(df)
    #creating 3 columns for 
    df.at[crr, "Octant ID"] = "Overall Transition Count"
    df.at[crr+1,"Octant ID"]="To"
    df.at[crr+3, " "] = "From"
    for i in range(8):
        df.at[crr+2, k[i]] = k[i]
    for i in range(8):
        df.at[crr+3+k.index(k[i]), "Octant ID"] = k[i]
    for j in range(8):
        for i in range(8):
            df.at[crr+j+3,k[i]]=0

    for i in range(0, n-1):
        df.at[crr+3+k.index(df.at[i, "Octant"]), df.at[i+1, "Octant"]] +=1

    crr=crr+14
    try:
        df.to_excel(
            'C:/Users/Gargi/Desktop/2001EE89_2022/tut02/output_octant_transition_identify.xlsx', index=False)
    except:
        print("Permission denied")


def mod_transition_count(mod=5000):
    try:
        df = pd.read_excel(
            r'C:\Users\Gargi\Desktop\2001EE89_2022\tut02\output_octant_transition_identify.xlsx')
    except ImportError:
        print("Wrong File Path.Please check path and try again!")

    k = [1, -1, 2, -2, 3, -3, 4, -4]
    crr = 24
    n=len(df)
    begin=0000
    end=mod-1
    while(begin<n):
        # Storing titles for transition count of each index
        df.at[crr+1,"Octant ID"]=str(begin)+"-"+ str(end)
        df.at[crr, "Octant ID"] = "Mod Transition Count"
        df.at[crr+1, 1] = "To"
        df.at[crr+3, " "] = "From"
        #Storing column and row titles for mod transition count table 
        for i in range(8):
            df.at[crr+2,k[i]]=k[i]
        for i in range(8):
            df.at[crr+3+k.index(k[i]), "Octant ID"] = k[i]
        #Creating cells with null values to store counts later
        for j in range(8):
            for i in range(8):
                df.at[crr+j+3, k[i]] = 0
        #Counting transitions 
        for i in range(begin, end):
            df.at[crr+3+k.index(df.at[i, "Octant"]), df.at[i+1, "Octant"]] += 1
        crr+=14
        if(end != n-1):
            begin = end+1
        if(end == n-1):
            break
        if(begin+mod-1 <= n-1):
            end = begin+mod-1
        elif(begin+mod-1 > n-1):
            end = n-1

    #Writing to output file
    try:
        df.to_excel(
            'C:/Users/Gargi/Desktop/2001EE89_2022/tut02/output_octant_transition_identify.xlsx', index=False)
    except:
        print("Permission denied")

#Function calling for part 3
overall_transition_count()
mod_transition_count()


ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")



