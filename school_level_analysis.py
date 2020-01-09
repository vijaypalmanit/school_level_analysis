import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

def getCSV ():
    global df
    
    import_file_path = filedialog.askopenfilename()
    df = pd.read_csv(import_file_path, skiprows=2)
    print (df.head())
    
browseButton_CSV = tk.Button(text="      Import CSV File     ", command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=browseButton_CSV)

root.mainloop()

print(df.iloc[1,])
print(df.columns)

df['date']=pd.to_datetime(df["date"])

df.insert(6,'comment','Non Zero')

def logic_comment(x,y):
    if x==1 and y==0:
        return 'Zero'
    elif x==1 and y>0:
        return 'Non Zero'
    else:
        return 'Non Zero'

df['comment'] = df.apply(lambda x: logic_comment(x['payment_number'],x['compass amount usd']),axis=1)


df2 = df[df['payment_number'].isin([1,2])].copy()

#set user_id with payment_number=2 with zero whose user_id with payment_number=1 are zero

lookup = df2.loc[(df2['payment_number']==1) & (df2['comment']=='Zero'),['user_id','comment']]

# since there are duplicate values you can check with lookup.groupby('user_id').filter(lambda x: len(x)>1).shape[0]
lookup=lookup.groupby('user_id')['comment'].agg('first')

print(df2.loc[df2['payment_number']==2,'comment'].head())

#--------------------------------------------------------------

df3=df2.copy()


df3.groupby(['comment','payment_number'])['user_id'].count()

df3.query('comment=="Zero" and payment_number==2')



df4=df3.merge(lookup,how='left',left_on='user_id',right_on='user_id',suffixes=('_main','_lookup'))


df4.loc[(df4['comment_lookup'].notna()) & (df4['payment_number']==2),'comment_main'] = df4.loc[(df4['comment_lookup'].notna()) & (df4['payment_number']==2),'comment_lookup']

df4 = df4.query('store_id != "111"')

df4.insert(1,'month','hello')

#-------------------------------------------
# this is dataframe consist of month ending for each business month eg. Business month May last from 2019-04-29 --- 2019-05-25 and so on....
df2=pd.DataFrame({'month_ending':['2019-04-28','2019-05-25','2019-06-29','2019-07-27','2019-08-24','2019-09-28','2019-10-26','2019-11-23','2019-12-28','2020-01-25','2020-02-22','2020-03-28','2020-05-02']})
df2['month_ending']=pd.to_datetime(df2['month_ending'])

bned_months=['May','June','July','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr']

df4['month'] = pd.cut(df4.date.astype(np.int64)//10**9,
                   bins=df2.month_ending.astype(np.int64)//10**9,
                   labels=bned_months)

#-------------------------------------------

#date=pd.to_datetime(d).date()

df4['date']=df4.date.dt.date

df4.groupby(['comment_main'])['user_id'].count()

df4.pivot_table(index='store_id',columns=['comment_main','payment_number'],values='user_id',fill_value=0,aggfunc='count')

df4.to_excel('D:\\Project\\project\\JIRA\\GB-395 create re-bill report\\New Data\\testing101.xlsx',index=False,columns=['date',
 'month','plan_source_cleaned', 'payment_number', 'user_id', 'subscriptionid', 'compass amount usd',
 'comment_main', 'store_id', 'store_name'])

# import os
# os.getcwd()
