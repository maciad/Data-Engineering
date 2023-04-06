#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import pickle
import json


# ### Ex 1

# In[ ]:


df1 = pd.read_json('proj3_data1.json')
df2 = pd.read_json('proj3_data2.json')
df3 = pd.read_json('proj3_data3.json')


# In[ ]:


df = pd.concat([df1, df2, df3]).reset_index(drop=True)


# In[ ]:


df.to_json('ex01_all_data.json')


# ### Ex 2

# In[ ]:


df_missing = df.isna().sum()


# In[ ]:


df_missing = df_missing[df_missing > 0].reset_index()


# In[ ]:


df_missing.to_csv('ex02_no_nulls.csv', index=False, header=False)


# ### Ex 3

# In[ ]:


df_params = pd.read_json('proj3_params.json', typ='series')


# In[ ]:


df['description'] = df[df_params['concat_columns']].apply(lambda x: ' '.join(x), axis=1)


# In[ ]:


df.to_json('ex03_descriptions.json')


# ### Ex 4

# In[ ]:


df4 = pd.read_json('proj3_more_data.json')


# In[ ]:


df5 = df.merge(df4, on=df_params['join_column'], how='left')


# In[ ]:


df5.to_json('ex04_joined.json')


# ### Ex 5

# In[ ]:


for i, row in df5.iterrows():
    desc = row['description'].replace(' ','_').lower()
    row.drop('description').to_json(f'ex05_{desc}.json')


# In[ ]:


for i, row in df5.astype({col: 'Int64' for col in df_params['int_columns']}).iterrows():
    desc = row['description'].replace(' ','_').lower()
    row.drop('description').to_json(f'ex05_int_{desc}.json')


# ### Ex 6

# In[ ]:


d = {}
for agg in df_params['aggregations']:
    d[f'{agg[1]}_{agg[0]}'] = df5.agg({agg[0]: agg[1]})[0]
with open('ex06_aggregations.json', 'w') as f:
    json.dump(d,f, indent=4)


# ### Ex 7

# In[ ]:


df6 = df5.groupby(df_params['grouping_column']).filter(lambda x: len(x) > 1)
df6 = df6.groupby(df_params['grouping_column']).mean(numeric_only=True)


# In[ ]:


df6.to_csv('ex07_groups.csv')


# ### Ex 8

# In[ ]:


df7 = df5.pivot_table(index=df_params['pivot_index'], columns=df_params['pivot_columns'],
          values=df_params['pivot_values'],aggfunc=max)


# In[ ]:


with open('ex08_pivot.pkl', 'wb') as f:
    pickle.dump(df7, f)


# In[ ]:


df8 = df5.melt(id_vars=df_params['id_vars'])


# In[ ]:


df8.to_csv('ex08_melt.csv', index=False)


# In[ ]:


df9 = pd.read_csv('proj3_statistics.csv')


# In[ ]:


df10 = pd.wide_to_long(df9, stubnames=df5[df_params['pivot_index']].unique(),
                       i='Country', j='year', sep='_').dropna(axis=1)


# In[ ]:


with open('ex08_stats.pkl', 'wb') as f:
    pickle.dump(df10, f)

