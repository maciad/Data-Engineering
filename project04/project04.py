#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import geopandas as gpd
import pandas as pd
import pyrosm
import pickle
import contextily as cx
import matplotlib.pyplot as plt


# In[ ]:


params = pd.read_json('proj4_params.json', typ='series')


# ### 1

# In[ ]:


gdf_lamps = gpd.read_file('proj4_points.geojson').to_crs(epsg=2180)


# In[ ]:


gdf_buf = gdf_lamps.copy()
gdf_buf['geometry'] = gdf_buf.geometry.buffer(100)
joined_df = gpd.sjoin(gdf_lamps, gdf_buf)


# In[ ]:


count_df = joined_df.groupby(gdf_lamps[params['id_column']]).size().reset_index(name='count')


# In[ ]:


count_df.to_csv('proj4_ex01_counts.csv', index=False)


# In[ ]:


gdf_lamps_4326 = gdf_lamps.to_crs(epsg=4326)


# In[ ]:


gdf_lamps_4326['lat'] = gdf_lamps_4326.geometry.y
gdf_lamps_4326['lon'] = gdf_lamps_4326.geometry.x


# In[ ]:


gdf_lamps_4326[[params['id_column'],'lat','lon']].to_csv('proj4_ex01_coords.csv', index=False)


# ### 2

# In[ ]:


osm = pyrosm.OSM(pyrosm.get_data(params['city'].lower()))


# In[ ]:


gdf_driving = osm.get_network(network_type='driving').to_crs(epsg=2180)


# In[ ]:


gdf_driving_primary = gdf_driving[gdf_driving['highway'] == 'primary']


# In[ ]:


gdf_driving_primary_columns = gdf_driving_primary[['id', 'name', 'geometry']]


# In[ ]:


gdf_driving_primary_columns.rename(columns={'id': 'osm_id'}).to_file(
    "proj4_ex02_primary_roads.geojson", driver="GeoJSON"
)


# ### 3

# In[ ]:


gdf_lamps['buffer_geom'] = gdf_lamps.geometry.buffer(50)


# In[ ]:


df_joins = gpd.sjoin(
    gdf_driving_primary_columns,
    gdf_lamps.set_geometry('buffer_geom'),
    predicate='intersects',
    how='left'
)


# In[ ]:


lamp_counts = df_joins.groupby('name').agg({'lamp_id': 'count'}).rename(
    columns={'lamp_id': 'point_count'}
)


# In[ ]:


lamp_counts.to_csv('proj4_ex03_streets_points.csv')


# ### 4

# In[ ]:


gdf_countries = gpd.read_file('proj4_countries.geojson').to_crs(epsg=3857)


# In[ ]:


gdf_countries['geometry'] = gdf_countries['geometry'].boundary


# In[ ]:


with open('proj4_ex04_gdf.pkl', 'wb') as f:
    pickle.dump(gdf_countries, f)


# In[ ]:


for index, row in gdf_countries.iterrows():
    ax = gdf_countries[gdf_countries['name'] == row['name']].plot()
    cx.add_basemap(ax)
    plt.savefig(f"proj4_ex04_{row['name'].lower()}.png")
    plt.close()

