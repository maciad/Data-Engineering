#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import pickle
import re


# ### Ex 1

# In[2]:


init_df = pd.read_csv('proj2_data.csv', sep='|', decimal=',')


# In[3]:


with open('proj2_ex01.pkl', 'wb') as file1:
    pickle.dump(init_df, file1)


# ### Ex 2

# In[4]:


grades = {'niedostateczny': 1,'mierny': 2, 'dostateczny': 3,
          'dobry': 4, 'bardzo dobry': 5} 


# In[5]:


df2 = init_df.copy()
df2['task_grade'] = init_df['task_grade'].map(grades)
df2['final_grade'] = init_df['final_grade'].map(grades)


# In[6]:


with open('proj2_ex02.pkl', 'wb') as file2:
    pickle.dump(df2, file2)


# ### Ex 3

# In[7]:


df3 = init_df.copy()


# In[8]:


df3['task_grade'] = df3['task_grade'].astype('category')
df3['final_grade'] = df3['final_grade'].astype('category')


# In[9]:


df3['task_grade'] = df3['task_grade'].cat.set_categories(
    ['niedostateczny', 'mierny', 'dostateczny', 'dobry', 'bardzo dobry'])
df3['final_grade'] = df3['final_grade'].cat.set_categories(
    ['niedostateczny', 'mierny', 'dostateczny', 'dobry', 'bardzo dobry'])


# In[10]:


with open('proj2_ex03.pkl', 'wb') as file3:
    pickle.dump(df3, file3)


# ### Ex 4

# In[11]:


df4 = init_df.copy()
df4.drop(df4.select_dtypes(include=['int64', 'float64']), axis=1, inplace=True)


# In[12]:


for col in df4.columns:
    if df4[col].dtype == 'object':
        df4[col] = df4[col].str.extract(r'([-]?\d+[,\.]?\d*)', expand=False)
        df4[col] = df4[col].str.replace(',', '.')
        df4[col] = df4[col].astype('float64')
df4.dropna(inplace=True, how='all', axis=1)


# In[13]:


with open('proj2_ex04.pkl', 'wb') as file:
    pickle.dump(df4, file)


# ### Ex 5

# In[14]:


forbidden = ['niedostateczny', 'mierny', 'dostateczny', 'dobry', 'bardzo dobry']
i = 1

for col in init_df.columns:
    max_uniq = init_df[col].value_counts().max()
    if (init_df[col].dtype == 'object' and 
            init_df[col].str.contains(r'^[a-z]+$', regex=True).all() and
            max_uniq < 10 and 
            not init_df[col].isin(forbidden).any()):
        df5 =  pd.get_dummies(init_df[col])
        with open(f'proj2_ex05_{i}.pkl', 'wb') as file:
            pickle.dump(df5, file)
        i += 1

