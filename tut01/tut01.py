
import pandas as pd

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


   
    df = pd.read_csv(r'C:\Users\Gargi\Desktop\2001EE89_2022\tut01\octant_input.csv')

    '''For calculating the mean and storing it in columns'''
    df.at[0,'U Avg'] = df['U'].mean(axis=0)
    df.at[0,'V Avg'] = df['V'].mean(axis=0)
    df.at[0,'W Avg'] = df['W'].mean(axis=0)
    df['''U'= U - U avg'''] = df['U']-df.loc[0,'U Avg']
    df['''V'= V - V avg'''] = df['V']-df.loc[0,'V Avg']
    df['''W'= W - W avg'''] = df['W']-df.loc[0,'W Avg']
    n = len(df)
    df['Octant']=df["U"] # declaring Octant with dummy variables for now
    df = octant(df) # for calculating the octant and storing it in Octant column of the dataframe
    df[''] = '' #adding an empty column with empty values 


    df.to_csv('C:/Users/Gargi/Desktop/2001EE89_2022/tut01/octant_output.csv',index=None)
octant_identification()
from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


#octant_identification(mod)
