#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import re
import pickle
import numpy as np
import json


# In[ ]:


df = pd.read_csv('lab1_ex01.csv')


# In[ ]:


names2 = pd.Series(df.columns, index=df.columns)
missing = (df.isnull().sum() / len(df))
types = df.dtypes.replace({'float64':'float', 'int64':'int', 'object':'other'})


# In[ ]:


df2 = pd.concat([names2, missing, types], axis=1).rename(columns={0:'name', 1:'missing', 2:'type'}).reset_index(drop=True)


# In[ ]:


df2.to_json('ex01_fields.json', default_handler=str, orient='records', indent=4)


# In[ ]:


count = df.count()
mean = df.mean(numeric_only=True)
std = df.std(numeric_only=True)
minv = df.min(numeric_only=True)
p25 = df.quantile(0.25, numeric_only=True)
p50 = df.quantile(0.5, numeric_only=True)
p75 = df.quantile(0.75, numeric_only=True)
maxv = df.max(numeric_only=True)


# In[ ]:


uniqued = {}
topd = {}
freqd = {}
for col in df.columns:
    if df[col].dtype != 'int64' and df[col].dtype != 'float64':
        topd[col] = df[col].value_counts().idxmax()
        freqd[col] = df[col].value_counts().max()
        uniqued[col] = df[col].nunique()
top = pd.Series(topd)
freq = pd.Series(freqd)
unique = pd.Series(uniqued)


# In[ ]:


names3 = {0.00:'count', 1.00:'mean', 2.00:'std', 3.00:'min', 0.25:'25%', 0.50:'50%', 0.75:'75%', 4.00:'max', 5.00:'unique', 6.00:'top', 7.00:'freq'}
df3 = pd.concat([count, mean, std, minv, p25, p50, p75, maxv, unique, top, freq], axis=1).rename(columns=names3)


# In[ ]:


df3.agg(lambda x: x.dropna().to_dict(), axis=1).to_json('ex02_stats.json', orient='index', indent=4 )


# In[ ]:


for col in df.columns:
    new_col = re.sub(r'(?![a-zA-Z0-9_ ]).', '', col)
    new_col = new_col.lower().replace(' ', '_')
    df.rename(columns={col:new_col}, inplace=True)


# In[ ]:


df.to_csv('ex03_columns.csv', index=False)


# In[ ]:


df.to_json('ex04_json.json', orient='records', indent=4)


# In[ ]:


df.to_excel('ex04_excel.xlsx', index=False)


# In[ ]:


with open('ex04_pickle.pkl', 'wb') as pick:
    pickle.dump(df, pick)


# In[ ]:


df4 = pd.read_pickle('lab1_ex05.pkl')
df4 = df4.iloc[:, 1:3]
df4 = df4.loc[df4.index.str.startswith('v')]
df4.replace(to_replace=[np.nan, None], value='' , inplace=True)
df4.to_markdown('ex05_table.md')


# In[ ]:


df5 = pd.read_json('lab1_ex06.json')
json_struct = json.loads(df5.to_json(orient='records'))
df_flat = pd.json_normalize(json_struct)
with open('ex06_pickle.pkl', 'wb') as pick:
    pickle.dump(df_flat, pick)

