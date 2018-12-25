
# coding: utf-8

# # Global Terrorism Attacks - Predicting The Responsible Group

# **Table of Contents**
# <div id="toc"></div>

# ## Load data

# In[9]:




from collections import Counter
import pandas as pd
import csv
from sklearn import preprocessing
import os.path

import configparser
config = configparser.ConfigParser()
config.read('config.ini')
gtdConvertedFilename = 'gtd_converted.csv'

#if not os.path.isfile(gtdConvertedFilename):
#    get_ipython().run_line_magic('run', 'CreateCSVFile.py')

gtd = pd.read_csv(gtdConvertedFilename, encoding='latin1', low_memory=False)
gtd.tail(3)


# ## Examine Data

# In[10]:


target = gtd['gname']
gcount = Counter(target)
print('No. of groups = {}'.format(len(gcount)))
g1 = gcount.most_common(1)[0]
print('Most common group, {} = {:.4f}%'.format(g1[0], 100 * g1[1] / target.size))
gcount.most_common(5)


# ## Preprocessing

# ### Filter Groups

# In[11]:


from collections import Counter

group_count = Counter(gtd['gname'])
# Remove groups with 3 attacks or less
filtered_groups = [group for group, counter in group_count.items() if counter > 3]
# Remove 'Unknown'
filtered_groups.remove('Unknown')

gtd = gtd[gtd['gname'].isin(filtered_groups)]

gtd.shape


# ### Define Features

# In[12]:


if config.getboolean('Booleans', 'UseLessFeatures') == True:
    columns_to_keep = ['gname', 'iyear', 'country', 'attacktype1', 'weaptype1', 'targtype1']
else:
    columns_to_keep = ['gname', 'iyear', 'country', 'crit1', 'crit2', 'crit3', 'attacktype1', 'targtype1',
                       'targsubtype1','weaptype1', 'weapsubtype1', 'ransom']

gtd = gtd[columns_to_keep]
gtd.tail(3)


# ### Transform Target

# In[13]:


gtd.apply(preprocessing.LabelEncoder().fit_transform);


# ### Fill NaNs

# In[14]:


gtd=gtd.fillna(0) #TODO: 0?

gtd.tail(3)


# ## Save

# In[15]:


if config.getboolean('Booleans', 'UseLessFeatures') == True:
    csvFileName = 'gtd_processed_5features.csv'
else:
    csvFileName = 'gtd_processed_11features.csv'


# In[16]:


gtd.to_csv(csvFileName, encoding='utf-8', index=False)
