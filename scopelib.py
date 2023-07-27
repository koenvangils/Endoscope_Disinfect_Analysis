import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

graphfontsize=9

def readdata(datafile):
    rawdata=pd.read_excel(datafile) #Process manager export Excel file
    rawdata=rawdata[rawdata['Proces-icoon']=='Succesvol afgerond'] #Only include succesful cleaning cycles
    rawdata['Processtart']=pd.to_datetime(rawdata['Processtart'],format="%d-%m-%Y %H:%M") #Convert date and time to datetime object
    rawdata['Processtart']=rawdata['Processtart'].dt.normalize()
    rawdata.sort_values(by=['Processtart'])
    return rawdata

def createfrequencytable(daterange,table1,table2,table3):
    frequencytable=[]
    for date in daterange:
        year=date.year
        weeknr=date.week
        weekday=date.strftime('%a')
        perdate=len(table1[table1['Processtart']==date])+len(table2[table2['Processtart']==date])+len(table3[table3['Processtart']==date])
        frequencytable.append([year,weeknr,weekday,perdate])
    frequencytablepandas=pd.DataFrame(frequencytable, columns = ['Year','Weeknr','Weekday','Frequency'])
    return frequencytablepandas

def freqperweekday(table,scopetype,year):
    table=table.loc[table['Processtart'].dt.year==year]
    daterange=pd.date_range(start=table['Processtart'].min(),end=table['Processtart'].max())
    table1, table2, table3 = (table[table[s].isin(scopetype)] for s in ('Endoscooptype','Endoscooptype 2','Endoscooptype 3'))
    IDsoftypeinlog=pd.concat([table1['Endoscoop ID'], table2['Endoscoop ID 2'], table3['Endoscoop ID 3']])
    IDsoftypeinlog.to_excel('test.xlsx')
    frequencytable=createfrequencytable(daterange,table1,table2,table3)
    return frequencytable,IDsoftypeinlog.nunique()

def boxplot(rawdata,scopetype,plotfile,year,qtyoftype=None):
    frequencytable,qtyoftypeinlog=freqperweekday(rawdata,scopetype,year)
    fig, ax = plt.subplots()
    sns.boxplot(data=frequencytable, x='Weekday', y='Frequency',whis=[0, 100],palette="vlag", showmeans=True, order=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
    sns.stripplot(data=frequencytable, x='Weekday', y='Frequency', size=3, order=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
    if qtyoftype:
        ax.set_title(plotfile.split('/')[-1]+'\nNr of scopes: '+str(qtyoftype)+' (Ultimo), '+str(qtyoftypeinlog)+' (Process Manager)\n Date range:'+str(start)+' - '+str(end),fontsize=graphfontsize) 
    else:
        qtyoftype=qtyoftypeinlog
        ax.set_title(plotfile.split('/')[-1]+'\nNr of scopes in log: '+str(qtyoftype)+'\n Year:'+str(year),fontsize=graphfontsize)
    ax.set_ylabel('Use frequency of this type')
    secax = ax.secondary_yaxis('right', functions=(lambda x: x / qtyoftype, lambda x: x * qtyoftype))
    secax.set_ylabel('Use frequency per endoscope of this type')

    plt.savefig(plotfile+'.png')
    plt.close()