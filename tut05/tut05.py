
import pandas as pd
import openpyxl
from datetime import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
import numpy as np
import scipy.stats as ss

start_time = datetime.now()

#Help https://youtu.be/N6PBd4XdnEw
def octant_range_names(mod=5000):

    try:
        df = pd.read_excel(
            r'C:\Users\Gargi\Desktop\2001EE89_2022\tut05\output_octant.xlsx')
    except ImportError:
        print("Wrong File")
    possible_octant_names = ['Internal outward interaction',
                             'External outward interaction',
                             'External Ejection',
                             'Internal Ejection',
                             'External inward interaction',
                             'Internal inward interaction',
                             'Internal sweep',
                             'External sweep'
                             ]
    '''
        for i in range(1,9):
            df["Rank "+ str(i)]=''

        rank_def={}
        k=[1,-1,2,-2,3,-3,4,-4]
        for i in k:
            rank_def[i]=df.at[1,i]

        sorted_key_def = OrderedDict(sorted(rank_def.items()))
        
        octant_name_id_mapping = {"1":"Internal outward interaction", "-1":"External outward interaction", "2":"External Ejection", "-2":"Internal Ejection", "3":"External inward interaction", "-3":"Internal inward interaction", "4":"Internal sweep", "-4":"External sweep"}
'''   
    no_of_ranges = int(30000/mod)
    overall_count = []
    mod_count = np.zeros((no_of_ranges, 8))
    mod_ranking = []
    rank1 = []
 
    possible_octant_values = [1, -1, 2, -2, 3, -3, 4, -4]

    row_num = 0

    for i in range(8):
        overall_count.append(df.at[row_num,possible_octant_values[i]])
    row_num = row_num+2
    for i in range(no_of_ranges):
        for j in range(8):
            mod_count[i][j] = df[possible_octant_values[j]][row_num]
        mod_ranking.append(ss.rankdata(mod_count[i]))
        row_num = row_num + 1

    print(overall_count)
    print(mod_count)
    overall_ranking = ss.rankdata(overall_count)
    print(overall_ranking)
    print(mod_ranking)

    df['Rank 1'] = ''
    df['Rank 1'][no_of_ranges+2] = '1'
    df['Rank 2'] = ''
    df['Rank 2'][no_of_ranges+2] = '-1'
    df['Rank 3'] = ''
    df['Rank 3'][no_of_ranges+2] = '2'
    df['Rank 4'] = ''
    df['Rank 4'][no_of_ranges+2] = '-2'
    df['Rank 5'] = ''
    df['Rank 5'][no_of_ranges+2] = '3'
    df['Rank 6'] = ''
    df['Rank 6'][no_of_ranges+2] = '-3'
    df['Rank 7'] = ''
    df['Rank 7'][no_of_ranges+2] = '4'
    df['Rank 8'] = ''
    df['Rank 8'][no_of_ranges+2] = '-4'

    possible_ranks = ['Rank 1', 'Rank 2', 'Rank 3', 'Rank 4', 'Rank 5', 'Rank 6', 'Rank 7', 'Rank 8']

    row_num = 0
    for i in range(8):
        df[possible_ranks[i]][row_num] = 9-int(overall_ranking[i])
        if df[possible_ranks[i]][row_num]==1:
            rank1.append(i)
    row_num = row_num+2
    
    for i in range(no_of_ranges):
        for j in range(8):
            df[possible_ranks[j]][row_num] = 9 - int(mod_ranking[i][j])
            if df[possible_ranks[j]][row_num]==1:
                rank1.append(j)
        row_num = row_num + 1

    df['Rank 1 Octant ID'] = ''
    df['Rank 1 Octant name'] = ''

    df['Rank 1 Octant ID'][0] = possible_octant_values[rank1[0]]
    df['Rank 1 Octant name'][0] = possible_octant_names[rank1[0]]

    row_num = 2

    for i in range(no_of_ranges):
        df['Rank 1 Octant ID'][row_num] = possible_octant_values[rank1[i+1]]
        df['Rank 1 Octant name'][row_num] = possible_octant_names[rank1[i+1]]
        row_num = row_num+1

    row_num = row_num+3

    columns_to_use = ['1', '-1', '2']

    df[columns_to_use[0]][row_num] = 'Octant ID'
    df[columns_to_use[1]][row_num] = 'Octant Name'
    df[columns_to_use[2]][row_num] = 'Rank 1 Mod Values'
    row_num = row_num+1

    for i in range(8):
        df[columns_to_use[0]][row_num] = possible_octant_values[i]
        df[columns_to_use[1]][row_num] = possible_octant_names[i]
        df[columns_to_use[2]][row_num] = rank1[1:no_of_ranges+1].count(i)
        row_num = row_num+1
    
###Code

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

octant_range_names()



from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


#mod=5000 
#octant_range_names(mod)



#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
