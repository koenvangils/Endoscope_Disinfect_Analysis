import scopelib
import pandas as pd
import numpy as np

useinventorydata=False #Use inventory data for scope quantity (for example an Ultimo export). If false unique scope ID's from process manager export will be used.

#Input data
rawdata=scopelib.readdata('ProcessList_example.xls')
#ultimodump=pd.read_excel('Equipment_Instrument.xls', skiprows=1) #Ultimo inventory list scopes

year=2020

uniquescopes=pd.unique(rawdata[['Endoscooptype','Endoscooptype 2','Endoscooptype 3']].values.ravel('K'))
uniquescopes=np.delete(uniquescopes,np.where(uniquescopes=="-")) #Excluding empty values in the raw data (presented as '-'). 

if useinventorydata:
    for scope in uniquescopes:
        qtyoftype=(len(ultimodump[ultimodump['Typenr.'] == scope]))
        if qtyoftype > 0:
            scopelib.boxplot(rawdata,[scope],str(scope),year,qtyoftype)
else:
    for scope in uniquescopes:
        scopelib.boxplot(rawdata,[scope],str(scope),year)


##combine multiple scopes in one boxplot, for example combining comparable scopes.
#broncho=['BF-1T160', 'BF-1T180','BF-1TH190','BF-P180','BF-Q190','BF-UC180F']
#colon=['CF-H180AL','CF-H190L','CF-HQ190L','CF-Q180AL']
#colonped=['PCF-190L','PCF-H180AL','PCF-H190L']
#gastro=['GIF-H180','GIF-H180J','GIF-H185','GIF-H190','GIF-Q180','GIF-XP190N','GIF-XTQ160']

#scopelib.boxplot(rawdata,broncho,'grouped/Broncho'+' '+str(broncho),start,end,(len(ultimodump[ultimodump['Typenr.'].isin(broncho)])))
#scopelib.boxplot(rawdata,colon,'grouped/Colon'+' '+str(colon),start,end,(len(ultimodump[ultimodump['Typenr.'].isin(colon)])))
#scopelib.boxplot(rawdata,colonped,'grouped/Colonped'+' '+str(colonped),start,end,(len(ultimodump[ultimodump['Typenr.'].isin(colonped)])))
#scopelib.boxplot(rawdata,gastro,'grouped/Gastro'+' '+str(gastro),start,end,(len(ultimodump[ultimodump['Typenr.'].isin(gastro)])))

