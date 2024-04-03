#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
import sqlite3
import pandas as pd


# In[ ]:


con = sqlite3.connect("proj6_readings.sqlite")
cur = con.cursor()


# ### 2.1 Basic counting

# In[ ]:


query = '''SELECT COUNT(DISTINCT detector_id) FROM readings'''


# In[ ]:


df = pd.read_sql(query, con)
df


# In[ ]:


df.to_pickle('proj6_ex01_detector_no.pkl')


# ### 2.2 Some stats

# In[ ]:


query_2 = '''SELECT detector_id, count(count), min(starttime), max(starttime)
             FROM readings
             GROUP BY detector_id'''


# In[ ]:


df2 = pd.read_sql(query_2, con)


# In[ ]:


df2


# In[ ]:


df2.to_pickle('proj6_ex02_detector_stat.pkl')


# ### 2.3 Moving Window

# In[ ]:


query_3 = '''SELECT 
                detector_id,
                count,
                lag(count) OVER (PARTITION BY detector_id ORDER BY starttime) as prev_count
            FROM readings
            WHERE detector_id = 146
            LIMIT 500'''


# In[ ]:


df3 = pd.read_sql(query_3, con)


# In[ ]:


df3


# In[ ]:


df3.to_pickle('proj6_ex03_detector_146_lag.pkl')


# ### 2.4 Window

# In[ ]:


query_4 = '''SELECT detector_id,
               count,
               SUM(count) OVER (PARTITION BY detector_id ORDER BY starttime ROWS BETWEEN CURRENT ROW AND 10 FOLLOWING) AS window_sum
            FROM readings
            WHERE detector_id = 146
            LIMIT 500'''


# In[ ]:


df4 = pd.read_sql(query_4, con)


# In[ ]:


df4


# In[ ]:


df4.to_pickle('proj6_ex04_detector_146_sum.pkl')


# In[ ]:


con.close()

