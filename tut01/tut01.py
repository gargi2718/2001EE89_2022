
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



def octant_identification(mod=5000):
   
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
    df.at[1,'']="User Input" # adding it the way it was in output file 
    df['Octant ID']='' #creating an empty column for storing ranges 
    
    df.at[1,'Octant ID']='MOD '+str(mod)
    print(df)
    k = [1, -1, 2, -2, 3, -3, 4, -4] #storing possible values of octant in a list

    #creating columns of possible octant values
    for col in k:
        df[col]=''
    df.at[0,'Octant ID']='Overall Count'

    #For calculating the overall counts of values in each octant 
    for i in k:
        df.at[0, i] = df['Octant'].value_counts()[i] #value_counts returns list containing the number if occurrences  of different values present in the column 


    count=2
    #for calculating ranges for summing the octants 



    df.to_csv('C:/Users/Gargi/Desktop/2001EE89_2022/tut01/octant_output.csv',index=None)
# calling function 
octant_identification()
from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


#octant_identification(mod)
