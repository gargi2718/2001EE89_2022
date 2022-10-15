#Help https://youtu.be/H37f_x4wAC0
import numpy as np
import pandas as pd
import openpyxl
from platform import python_version

#Part 2: Function to calculate time ranges of the longest subsequence count found in tit 3
def octant_longest_subsequence_count_with_range():
    try:
        df = pd.read_excel(
            r'C:\Users\Gargi\Desktop\2001EE89_2022\tut04\octant_output_4.xlsx')
    except ImportError:
        print("Wrong File")
    except :
        print("File already open or permission not given to use file")
    #declaring null columns to store values 
    df["   "]=''
    df["    "]=''
    df["     "]=''
    df["      "]=''
    df.at[0, "    "]="Count"
    df.at[0, "     "]="Longest_Subsequence_Length"
    df.at[0, "      "]="Count"
    k = [+1, -1, +2, -2, +3, -3, +4, -4]
    n = len(df)
    cr=2
    for i in k:
        count = 0
        max = 0
        counter = 0
        for j in range(0, n):
            if(j != n-1 and df.at[j, "Octant"] == i and df.at[j+1, "Octant"] == i):
                counter += 1

                if((counter+1) > max):
                    max = counter+1
                    count = 0
                if((counter+1) == max):
                    count += 1


            elif(j != n-1 and df.at[j, "Octant"] == i and df.at[j+1, "Octant"] != i and df.at[j-1, "Octant"] != i):
                if(max == 0):
                    max = 1
                if(max == 1):
                    count += 1


            elif(j == n-1 and df.at[j, "Octant"] == i):
                if(max == 0):
                    max = 1
                    count = 1


            else:
                counter = 0
                continue
        
        
        df.at[cr, "    "]=i
        df.at[cr, "     "]=max
        df.at[cr, "      "]=count
        cr+=1
        df.at[cr, "    "] = "Time"
        df.at[cr, "     "] = "To"
        df.at[cr, "      "] = "From"
        cr+=1
        counter=0
        
        for j in range(0,n-1):
            if(j != n-1 and df.at[j, "Octant"] == i and df.at[j+1, "Octant"] == i):
                counter += 1
                if((counter+1) == max):
                    t_from = df.at[j+1-max+1, "Time"]
                    t_to = df.at[j+1, "Time"]
                    df.at[cr, "     "]=t_from
                    df.at[cr,"      "]=t_to
                    cr+=1

            elif(j != n-1 and df.at[j, "Octant"] == i and df.at[j+1, "Octant"] != i and df.at[j-1, "Octant"] != i and max==1):
                t_from = df.at[j, "Time"]
                t_to = df.at[j, "Time"]
                df.at[cr, "     "] = t_from
                df.at[cr,"      "]=t_to
                cr+=1

            elif(j == n-1 and df.at[j, "Octant"] == i and max==1):
                t_from=df.at[j,"Time"]
                t_to=df.at[j,"Time"]
                df.at[cr, "     "] = t_from
                df.at[cr, "      "] = t_to
                cr+=1

            
            else:
                counter=0
                continue
            

    try:
        df.to_excel(
            'C:/Users/Gargi/Desktop/2001EE89_2022/tut04/octant_output_4.xlsx', index=False)
    except:
        print("Permission denied")




#Part 1 : Data Preprocessing 

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


def octant_identification():
    try:
        df = pd.read_excel(
            r'C:\Users\Gargi\Desktop\2001EE89_2022\tut04\input_octant_longest_subsequence_with_range.xlsx')
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
    df[" "] = ""
    try:
        df.to_excel(
            'C:/Users/Gargi/Desktop/2001EE89_2022/tut04/octant_output_4.xlsx', index=False)
    except:
        print("Permission denied")

#Part 2: longest subsequence count
def octant_longest_subsequence_count():
    try:
        df = pd.read_excel(
            r'C:\Users\Gargi\Desktop\2001EE89_2022\tut04\octant_output_4.xlsx')
    except ImportError:
        print("Wrong File Path")
    k = [+1, -1, +2, -2, +3, -3, +4, -4]
    n = len(df)

    df.at[0,"  "]="Count"
    df.at[0,"               "]="Longest Subsequence Length"
    df.at[0,"                   "]="Count"
    for i in range(8):
        df.at[i+1,"  "] = k[i]
    for i in k:
        count = 0
        max = 0
        counter = 0
        for j in range(0, n):
            if(j != n-1 and df.at[j, "Octant"] == i and df.at[j+1, "Octant"] == i):
                counter += 1

                if((counter+1) > max):
                    max = counter+1
                    count = 0
                if((counter+1) == max):
                    count += 1

            elif(j != n-1 and df.at[j, "Octant"] == i and df.at[j+1, "Octant"] != i and df.at[j-1, "Octant"] != i):
                if(max == 0):
                    max = 1
                if(max == 1):
                    count += 1

            elif(j == n-1 and df.at[j, "Octant"] == i):
                if(max == 0):
                    max = 1
                    count = 1

            else:
                counter = 0
                continue
        df.at[k.index(i)+1, "               "] = max
        df.at[k.index(i)+1, "                   "] = count

    try:
        df.to_excel(
            'C:/Users/Gargi/Desktop/2001EE89_2022/tut04/octant_output_4.xlsx', index=False)
    except PermissionError:
        print("File already open or permission denied")
    except:
        print("Permission denied")


ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

octant_identification()
octant_longest_subsequence_count()
octant_longest_subsequence_count_with_range()
