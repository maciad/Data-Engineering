#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# ### 2.1 Preparing data

# In[ ]:


params = pd.read_json('proj5_params.json', typ='series')


# In[ ]:


df = pd.read_csv('proj5_timeseries.csv', index_col=0, parse_dates=True)


# In[ ]:


new_cols = {}
for col in df.columns:
    new_col = re.sub(r'\W', '_', col.lower())
    new_cols[col] = new_col
    
df = df.rename(columns=new_cols)


# In[ ]:


df = df.asfreq(params.get('original_frequency'))


# In[ ]:


with open('proj5_ex01.pkl', 'wb') as f:
    pickle.dump(df, f)


# ### 2.2 Frequency adjustment

# In[ ]:


dff = df.asfreq(params.get('target_frequency'))


# In[ ]:


with open('proj5_ex02.pkl', 'wb') as f:
    pickle.dump(dff, f)


# ### 2.3 Downsampling

# In[ ]:


period_d = str(params.get('downsample_periods')) + params.get('downsample_units')
dfd = df.resample(period_d).sum(min_count=params.get('downsample_periods'))


# In[ ]:


with open('proj5_ex03.pkl', 'wb') as f:
    pickle.dump(dfd, f)


# ### 2.4 Upsampling

# In[ ]:


period_u = str(params.get('upsample_periods')) + params.get('upsample_units')


# In[ ]:


dfu = df.resample(period_u).interpolate(params.get('interpolation'), order=params.get('interpolation_order'))


# In[ ]:


original_frequency = pd.Timedelta(1, params.get('original_frequency'))
upsampled_frequency = pd.Timedelta(period_u)
dfu = dfu * upsampled_frequency / original_frequency


# In[ ]:


with open('proj5_ex04.pkl', 'wb') as f:
    pickle.dump(dfu, f)


# ### 2.5 Reshaping & alignment

# In[ ]:


# df2 = pd.read_csv('proj5_sensors.csv')
with open('proj5_sensors.pkl', 'rb') as file:
    df2 = pickle.load(file)


# In[ ]:


df2 = df2.pivot(columns='device_id', values='value')


# In[ ]:


freq = str(params.get('sensors_periods')) + params.get('sensors_units')
new_index = pd.date_range(
    start=df2.index.round(freq).min(),
    end=df2.index.round(freq).max(),
    freq=freq
)


# In[ ]:


df2 = df2.reindex(new_index.union(df2.index)).interpolate()
df2 = df2.reindex(new_index)


# In[ ]:


df2 = df2.dropna()


# In[ ]:


with open('proj5_ex05.pkl', 'wb') as f:
    pickle.dump(df2, f)

