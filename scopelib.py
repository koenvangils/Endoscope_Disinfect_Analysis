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
    rawdata.set_index('Processtart', inplace=True, drop=True) #Set date and time as Pandas dataframe index
    return rawdata

def correctdaterange(table,start,end):
    if start<table.index.min():
        start=table.index.min()
        print('Changed start date to first data point')
    if end>table.index.max():
        end=table.index.max()
        print('Changed end date to last data point')
    if start>end:
        start=end
        print('Start date can not be later than end date, no output.')
    return start,end

def createfrequencytable(daterange,table1,table2,table3):
    frequencytable=[[],[],[],[],[],[],[]]
    for date in daterange:
        weekday=date.dayofweek
        perdate=len(table1[table1.index.date==date.date()])+len(table2[table2.index.date==date.date()])+len(table3[table3.index.date==date.date()])
        frequencytable[weekday].append(perdate)
    frequencytablepandas=pd.DataFrame(frequencytable).transpose()
    frequencytablepandas.columns=['Mo','Tu','We','Th','Fr','Sa','Su']
    return frequencytablepandas

def freqperweekday(table,scopetype,start,end):
    table=table[(table.index >= start) & (table.index < end)]
    daterange=pd.date_range(start=start,end=end)
    table1, table2, table3 = (table[table[s].isin(scopetype)] for s in ('Endoscooptype','Endoscooptype 2','Endoscooptype 3'))
    IDsoftypeinlog=table1['Endoscoop ID'].astype('str')
    IDsoftypeinlog=IDsoftypeinlog.append(table2['Endoscoop ID 2']).astype('str')
    IDsoftypeinlog=IDsoftypeinlog.append(table3['Endoscoop ID 3']).astype('str')
    frequencytable=createfrequencytable(daterange,table1,table2,table3)
    return frequencytable,IDsoftypeinlog.nunique()

def freqperweekdayperuniquescope(table,serialnumber,start,end):
    table=table.loc[(table.index >= start) & (table.index < end)]
    daterange=pd.date_range(start=start,end=end)
    table1, table2, table3 = (table[table[s].isin(serialnumber)] for s in ('Serienr. endoscoop','Serienr. endoscoop 2','Serienr. endoscoop 3'))
    frequencytable=createfrequencytable(daterange,table1,table2,table3)
    return frequencytable

def freqperweekdayperuser(table,scopetype,user,start,end):
    table=table.loc[(table.index >= start) & (table.index < end)]
    daterange=pd.date_range(start=start,end=end)
    table1=table[table['Endoscooptype'].isin(scopetype)]
    table1=table1[table1['Specialistnaam'].isin(user)]
    table2=table[table['Endoscooptype 2'].isin(scopetype)]
    table2=table2[table2['Specialistnaam 2'].isin(user)]
    table3=table[table['Endoscooptype 3'].isin(scopetype)]
    table3=table3[table3['Specialistnaam 3'].isin(user)]
    frequencytable=createfrequencytable(daterange,table1,table2,table3)
    return frequencytable

def boxplot(rawdata,scopetype,plotfile,start,end,qtyoftype=None):
    start,end=correctdaterange(rawdata[rawdata['Endoscooptype'].isin(scopetype)],start,end)
    frequencytable,qtyoftypeinlog=freqperweekday(rawdata,scopetype,start,end)
    fig, ax = plt.subplots()
    ax.boxplot(frequencytable.fillna(0),showmeans=True,whis=[0,100],zorder=2)
    if qtyoftype:
        ax.set_title(plotfile.split('/')[-1]+'\nNr of scopes: '+str(qtyoftype)+' (Ultimo), '+str(qtyoftypeinlog)+' (Process Manager)\n Date range:'+str(start.date())+' - '+str(end.date()),fontsize=graphfontsize) 
    else:
        qtyoftype=qtyoftypeinlog
        ax.set_title(plotfile.split('/')[-1]+'\nNr of scopes in log: '+str(qtyoftype)+'\n Date range:'+str(start.date())+' - '+str(end.date()),fontsize=graphfontsize)
    ax.set_ylabel('Use frequency of this type')
    ax.set_xticklabels(frequencytable.columns)
    secax = ax.secondary_yaxis('right', functions=(lambda x: x / qtyoftype, lambda x: x * qtyoftype))
    secax.set_ylabel('Use frequency per endoscope of this type')

    plt.savefig(plotfile+'.png')
    plt.close()

def violinplot(rawdata,scopetype,plotfile,start,end,qtyoftype=None):
    start,end=correctdaterange(rawdata[rawdata['Endoscooptype'].isin(scopetype)],start,end)
    frequencytable,qtyoftypeinlog=freqperweekday(rawdata,scopetype,start,end)
    fig, ax = plt.subplots()
    sns.scatterplot(data=frequencytable.fillna(0).mean(),zorder=10)
    sns.violinplot(data=frequencytable.fillna(0),cut=0)
    if qtyoftype:
        ax.set_title(plotfile.split('/')[-1]+'\nNr of scopes: '+str(qtyoftype)+' (Ultimo), '+str(qtyoftypeinlog)+' (Process Manager)\n Date range:'+str(start.date())+' - '+str(end.date()),fontsize=graphfontsize) 
    else:
        qtyoftype=qtyoftypeinlog
        ax.set_title(plotfile.split('/')[-1]+'\nNr of scopes in log: '+str(qtyoftype)+'\n Date range:'+str(start.date())+' - '+str(end.date()),fontsize=graphfontsize)
    ax.set_ylabel('Use frequency of this type')
    secax = ax.secondary_yaxis('right', functions=(lambda x: x / qtyoftype, lambda x: x * qtyoftype))
    secax.set_ylabel('Use frequency per endoscope of this type')
    plt.savefig(plotfile+'_violin.png')
    plt.close()

def boxplotuniquescope(rawdata,serialnr,plotfile,start,end):
    start,end=correctdaterange(rawdata[rawdata['Serienr. endoscoop'].isin(serialnr)],start,end)
    frequencytable=freqperweekdayperuniquescope(rawdata,serialnr,start,end)
    fig, ax = plt.subplots()
    ax.boxplot(frequencytable.fillna(0),showmeans=True,whis=[0,100],zorder=2)
    ax.set_ylabel('Use frequency of this scope')
    ax.set_xticklabels(frequencytable.columns)
    plt.title(plotfile.split('/')[-1]+'\n'+str(start.date())+' - '+str(end.date()),fontsize=graphfontsize)
    plt.savefig(plotfile+'.png')
    plt.close()

def boxplotperuser(rawdata,scopetype,user,plotfile,start,end):
    start,end=correctdaterange(rawdata[rawdata['Specialistnaam'].isin(user)],start,end)
    frequencytable=freqperweekdayperuser(rawdata,scopetype,user,start,end)
    if np.max(np.max(frequencytable.fillna(0)))>0:
        fig,ax = plt.subplots()
        ax.boxplot(frequencytable.fillna(0),showmeans=True,whis=[0,100],zorder=2)
        ax.set_ylabel('Use frequency of this scope')
        ax.set_xticklabels(frequencytable.columns)        
        plt.title(plotfile.split('/')[-1]+'\n'+str(start.date())+' - '+str(end.date()),fontsize=graphfontsize)
        plt.savefig(plotfile+'.png')
        plt.close()
    else: pass
