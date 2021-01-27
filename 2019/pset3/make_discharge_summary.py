#!/usr/bin/python
import numpy as np
import pandas as pd
import psycopg2
from scipy.stats import ks_2samp
import os, sys
import random
# from bs4 import BeautifulSoup 
mimicdir = datadir = '/Users/irenechen/Documents/mimic-data'
random.seed(22891)

# create a database connection
sqluser = 'iychen'
dbname = 'mimic'
schema_name = 'mimiciii'

# Connect to local postgres version of mimic
con = psycopg2.connect(dbname=dbname, user=sqluser)
cur = con.cursor()
cur.execute('SET search_path to ' + schema_name)



# notes on data extraction:
# - used first icu to find micu (total = 20859)
# - dropped patients with less than 48 hours (total = 11020)
# - dropped patients without age (age>300) total = 10322
# - 663 of whom are missing discharge summaries 
# (kept them, they will just have empty text)
# -dropped patients who died within 48 hours 
# - 7 patients with no icd9s dropped them. 


#============Discharge summaries 
dc_text_query = \
"""
SELECT fin.subject_id, fin.hadm_id, fin.icustay_id, string_agg(fin.text, ' ') as dc_chart
FROM (
  select ie.subject_id, ie.hadm_id, ie.icustay_id, 
  ne.text, ne.category, ne.description
  from icustays ie
  left join noteevents ne
  on ie.subject_id = ne.subject_id and ie.hadm_id = ne.hadm_id 
  and ne.category = 'Discharge summary' 
  where ie.first_careunit = 'MICU' 
 ) fin 
group by fin.subject_id, fin.hadm_id, fin.icustay_id 
order by fin.subject_id, fin.hadm_id, fin.icustay_id; 
"""


# you would think that every patient has a single dc summary, but there are "addendums" (check chart description)
# dc_sum[dc_sum.icustay_id.isin(dc_sum.icustay_id[dc_sum.icustay_id.duplicated()])].sort("icustay_id")

dc_sum = pd.read_sql_query(dc_text_query,con) 

# clean up the text 
dc_sum['dc_chart'] = dc_sum['dc_chart'].str.lower()
dc_sum['dc_chart'] = dc_sum['dc_chart'].str.replace('\n', '')
dc_sum['dc_chart'] = dc_sum['dc_chart'].str.replace('_', '')


#========function to extract the data from different time stamps 
def extract_chart(start_time, end_time, icu_group, con):
  chart_query = \
  """
  SELECT fin.subject_id, fin.hadm_id, fin.icustay_id, string_agg(fin.text, ' ') as chartext 
  FROM (
  select ie.subject_id, ie.hadm_id, ie.icustay_id, 
  ne.text, ne.category, ne.description
  from icustays ie
  left join noteevents ne
  on ie.subject_id = ne.subject_id and ie.hadm_id = ne.hadm_id 
  and ne.charttime between ie.intime + interval '%s' hour and ie.intime + interval '%s' hour
  where ie.first_careunit = '%s' 
  order by ie.subject_id, ie.hadm_id, ie.icustay_id, ne.charttime
  ) fin 
  group by fin.subject_id, fin.hadm_id, fin.icustay_id 
  order by fin.subject_id, fin.hadm_id, fin.icustay_id; 
  """ %(start_time, end_time, icu_group)

  char_data = pd.read_sql_query(chart_query,con) 
  # clean up the text 
  char_data['chartext'] = char_data['chartext'].str.lower()
  char_data['chartext'] = char_data['chartext'].str.replace('\n', '')
  char_data['chartext'] = char_data['chartext'].str.replace('_', '')

  return char_data


char_data0_12 = extract_chart('0', '12', 'MICU', con)
char_data12_24 = extract_chart('12', '24', 'MICU', con)
char_data24_36 = extract_chart('24', '36', 'MICU', con)
char_data36_48 = extract_chart('36', '48', 'MICU', con)


# checks 

# checks = """select ie.subject_id, ie.hadm_id, ie.icustay_id, ie.intime, ne.charttime,  ne.text
# from icustays ie
# left join noteevents ne 
# on ie.subject_id = ne.subject_id and ie.hadm_id = ne.hadm_id 
# where ie.icustay_id = '211552'
# order by ne.charttime
# """
# checks_ds = pd.read_sql_query(checks,con) 


#=======all notes after 48 hours 
chart_query = \
"""
SELECT fin.subject_id, fin.hadm_id, fin.icustay_id, string_agg(fin.text, ' ') as chartext 
FROM (
select ie.subject_id, ie.hadm_id, ie.icustay_id, 
ne.text, ne.category, ne.description
from icustays ie
left join noteevents ne
on ie.subject_id = ne.subject_id and ie.hadm_id = ne.hadm_id 
and ne.charttime between ie.intime + interval '48' hour and ie.outtime 
where ie.first_careunit = 'MICU' 
order by ie.subject_id, ie.hadm_id, ie.icustay_id, ne.charttime
) fin 
group by fin.subject_id, fin.hadm_id, fin.icustay_id 
order by fin.subject_id, fin.hadm_id, fin.icustay_id; 
""" 

char_data48p = pd.read_sql_query(chart_query,con) 
# clean up the text 
char_data48p['chartext'] = char_data48p['chartext'].str.lower()
char_data48p['chartext'] = char_data48p['chartext'].str.replace('\n', '')
char_data48p['chartext'] = char_data48p['chartext'].str.replace('_', '')


#=========icd9 dx 
dxquery = \
"""
select dx.subject_id, dx.hadm_id, ie.icustay_id, dx.icd9_code as icd_dx
from diagnoses_icd dx 
INNER JOIN icustays ie
    ON dx.hadm_id = ie.hadm_id
    and dx.subject_id = ie.subject_id

"""
icd_ds = pd.read_sql_query(dxquery,con) 

#----------useful clean up functions 
def clean_ccs(x):
  """
  Strips quotes and white space from ccs categories and icd9 
  """
  x = x.replace("'", "")
  x = x.strip()
  return x 


#----------Single level CCS categories
# This is aquired from the hcup website 
# https://www.hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp#download
ccs_single = pd.read_csv('single_level_ccs.csv')

# clean up 
ccs_single.drop(ccs_single.columns[1], 1, inplace = True)
ccs_single.columns = ['icd_dx', 'ccs_scat']

ccs_single = ccs_single.applymap(clean_ccs)

ccs_single = ccs_single[1:] # drop the no dx code 
#----multilevel ccs 
# ccs_multi = pd.read_csv('multi_level_ccs.csv')
# # only kept hte first three levels, the fourth is the icd itself
# ccs_multi.drop(ccs_multi.columns[[1, 3, 5, 7,8]], 1, inplace = True)
# ccs_multi.columns = ['icd_dx', 'ccs_mcat1', 'ccs_mcat2', 'ccs_mcat3']

# ccs_multi = ccs_multi.applymap(clean_ccs)


#-----elixhauser 
# to get the elixhauser list, went to R!
# library(icd)

# elix_df <- data.frame(icd_dx = matrix(unlist(quanElixComorbid), ncol = 1, byrow=T), 
# elix = rep(names(quanElixComorbid),unlist(lapply(quanElixComorbid, function(x) length(x))))
#   ,stringsAsFactors=FALSE)

# write.csv(elix_df, file = "/Users/maggiemakar/Dropbox (MIT)/Spring17MLHC/pset2/elix.csv", row.names = FALSE)
# elix = pd.read_csv('elix.csv')

#----merge with icd9 dataset 
# icd_ds = icd_ds.merge(ccs_single, on = 'icd_dx', how = 'left')
# icd_ds = icd_ds.merge(ccs_multi, on = 'icd_dx', how = 'left')
# icd_ds = icd_ds.merge(elix, on = 'icd_dx', how = 'left')


# check. Note that not all icds have an elixhauser category 
# TODO: check elix merge. 
# icd_ds.isnull().sum()

# think this discrepency is because elix lists all levels 
# of hierarchy assoced with the category 
# len(elix.icd_dx.unique())
# len(icd_ds.icd_dx[(icd_ds.elix.notnull())].unique())

#========get the "additional" dataset first. This is a 
# dataset that has all the dmeographics of the patient. 

# this query extracts the following:
#   Unique ids for the admission, patient and icu stay 
#   Patient gender 
#   admission & discharge times 
#   length of stay 
#   age 
#   ethnicity 
#   admission type 
#   in hospital death?
#   in icu death?
#   one year from admission death?
#   first hospital stay 
#   icu intime, icu outime 
#   los in icu 
#   first icu stay?

denquery = \
"""
--ie is the icustays table 
--adm is the admissions table 
SELECT ie.subject_id, ie.hadm_id, ie.icustay_id
, pat.gender
, adm.admittime, adm.dischtime, adm.diagnosis
, ROUND( (CAST(adm.dischtime AS DATE) - CAST(adm.admittime AS DATE)) , 4) AS los_hospital
, ROUND( (CAST(adm.admittime AS DATE) - CAST(pat.dob AS DATE))  / 365, 4) AS age
, adm.ethnicity, adm.ADMISSION_TYPE
--, adm.hospital_expire_flag
, CASE when adm.deathtime between adm.admittime and adm.dischtime THEN 1 ELSE 0 END AS mort_hosp
, CASE when adm.deathtime between ie.intime and ie.outtime THEN 1 ELSE 0 END AS mort_icu
, CASE when adm.deathtime between adm.admittime and adm.admittime + interval '365' day  THEN 1 ELSE 0 END AS mort_oneyr
, DENSE_RANK() OVER (PARTITION BY adm.subject_id ORDER BY adm.admittime) AS hospstay_seq
, CASE
    WHEN DENSE_RANK() OVER (PARTITION BY adm.subject_id ORDER BY adm.admittime) = 1 THEN 1
    ELSE 0 END AS first_hosp_stay
-- icu level factors
, ie.intime, ie.outtime
, ie.FIRST_CAREUNIT
, ROUND( (CAST(ie.outtime AS DATE) - CAST(ie.intime AS DATE)) , 4) AS los_icu
, DENSE_RANK() OVER (PARTITION BY ie.hadm_id ORDER BY ie.intime) AS icustay_seq

-- first ICU stay *for the current hospitalization*
, CASE
    WHEN DENSE_RANK() OVER (PARTITION BY ie.hadm_id ORDER BY ie.intime) = 1 THEN 1
    ELSE 0 END AS first_icu_stay

FROM icustays ie
INNER JOIN admissions adm
    ON ie.hadm_id = adm.hadm_id
INNER JOIN patients pat
    ON ie.subject_id = pat.subject_id
WHERE adm.has_chartevents_data = 1
ORDER BY ie.subject_id, adm.admittime, ie.intime;

"""

den = pd.read_sql_query(denquery,con)
#----Keep MICU only 
den = den[(den.first_careunit=='MICU')]

#----drop patients with less than 48 hour 
den['los_icu_hr'] = (den.outtime - den.intime).astype('timedelta64[h]')
den = den[(den.los_icu_hr >= 48)]
den = den[(den.age<300)]
den.drop('los_icu_hr', 1, inplace = True)

# clean ups 
den['gender'] = np.where(den['gender']=="M", 1, 0)

# no need to yell 
den.ethnicity = den.ethnicity.str.lower()
den.ethnicity.loc[(den.ethnicity.str.contains('^white'))] = 'white'
den.ethnicity.loc[(den.ethnicity.str.contains('^black'))] = 'black'
den.ethnicity.loc[(den.ethnicity.str.contains('^hisp')) | (den.ethnicity.str.contains('^latin'))] = 'hispanic'
den.ethnicity.loc[(den.ethnicity.str.contains('^asia'))] = 'asian'
den.ethnicity.loc[~(den.ethnicity.str.contains('|'.join(['white', 'black', 'hispanic', 'asian'])))] = 'other'

den = pd.concat([den, pd.get_dummies(den['ethnicity'], prefix='eth')], 1)
den = pd.concat([den, pd.get_dummies(den['admission_type'], prefix='admType')], 1)

den.drop(['diagnosis', 'hospstay_seq', 'los_icu','icustay_seq', 'admittime', 'dischtime','los_hospital', 'intime', 'outtime', 'ethnicity', 'admission_type', 'first_careunit'], 1, inplace =True) 

extra_vars = den.columns[3:]
msk = np.random.rand(len(den)) < 0.7
den['train'] = np.where(msk, 1, 0) 

# merge in icd9's and dx categories
den = den.merge(dc_sum, on = ['icustay_id', 'hadm_id', 'subject_id'], how = 'left') 

den.to_csv('discharge_summaries.csv', index=False)
# den = den.merge(char_data0_12, on = ['icustay_id', 'hadm_id', 'subject_id'], how = 'left') 
# den = den.merge(char_data12_24, on = ['icustay_id', 'hadm_id', 'subject_id'], how = 'left') 
# den = den.merge(char_data24_36, on = ['icustay_id', 'hadm_id', 'subject_id'], how = 'left') 
# den = den.merge(char_data36_48, on = ['icustay_id', 'hadm_id', 'subject_id'], how = 'left') 
# den = den.merge(char_data48p, on = ['icustay_id', 'hadm_id', 'subject_id'], how = 'left') 


import pdb; pdb.set_trace()
# den = den.merge(icd_ds, on = ['icustay_id', 'hadm_id', 'subject_id'], how = 'left') 


#============Section 1: 
