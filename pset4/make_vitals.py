import numpy as np
import pandas as pd
import psycopg2
from scipy.stats import ks_2samp
import os 
import random

# Ouput directory to generate the files
mimicdir = '/Users/irenechen/Documents/mimic-data'

random.seed(22891)

# create a database connection
sqluser = 'iychen'
dbname = 'mimic'
schema_name = 'mimiciii'


# Connect to local postgres version of mimic
con = psycopg2.connect(dbname=dbname, user=sqluser)
cur = con.cursor()
cur.execute('SET search_path to ' + schema_name)

def get_demo():
    # Select adult patients admitted for longer than 48 hours
    denquery = \
    """
    -- This query extracts useful demographic/administrative information for patient ICU stays
    --DROP MATERIALIZED VIEW IF EXISTS icustay_detail CASCADE;
    --CREATE MATERIALIZED VIEW icustay_detail as
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

    #----drop patients with less than 48 hour 
    den['los_icu_hr'] = (den.outtime - den.intime).astype('timedelta64[h]')
    den = den[(den.los_icu_hr >= 48)]
    den = den[(den.age<300)]
    den.drop('los_icu_hr', 1, inplace = True)
    den.to_csv('demo.csv', index=False)
    
def get_24h():
    vithrquery = \
    """
    -- This query pivots the vital signs for the first 48 hours of a patient's stay
    -- Vital signs include heart rate, blood pressure, respiration rate, and temperature
    -- DROP MATERIALIZED VIEW IF EXISTS vitalsfirstday CASCADE;
    -- create materialized view vitalsfirstday as
    SELECT pvt.subject_id, pvt.hadm_id, pvt.icustay_id
    -- Easier names
    , min(case when VitalID = 1 then valuenum else null end) as HeartRate_Min
    , max(case when VitalID = 1 then valuenum else null end) as HeartRate_Max
    , avg(case when VitalID = 1 then valuenum else null end) as HeartRate_Mean
    , min(case when VitalID = 2 then valuenum else null end) as SysBP_Min
    , max(case when VitalID = 2 then valuenum else null end) as SysBP_Max
    , avg(case when VitalID = 2 then valuenum else null end) as SysBP_Mean
    , min(case when VitalID = 3 then valuenum else null end) as DiasBP_Min
    , max(case when VitalID = 3 then valuenum else null end) as DiasBP_Max
    , avg(case when VitalID = 3 then valuenum else null end) as DiasBP_Mean
    , min(case when VitalID = 4 then valuenum else null end) as MeanBP_Min
    , max(case when VitalID = 4 then valuenum else null end) as MeanBP_Max
    , avg(case when VitalID = 4 then valuenum else null end) as MeanBP_Mean
    , min(case when VitalID = 5 then valuenum else null end) as RespRate_Min
    , max(case when VitalID = 5 then valuenum else null end) as RespRate_Max
    , avg(case when VitalID = 5 then valuenum else null end) as RespRate_Mean
    , min(case when VitalID = 6 then valuenum else null end) as TempC_Min
    , max(case when VitalID = 6 then valuenum else null end) as TempC_Max
    , avg(case when VitalID = 6 then valuenum else null end) as TempC_Mean
    , min(case when VitalID = 7 then valuenum else null end) as SpO2_Min
    , max(case when VitalID = 7 then valuenum else null end) as SpO2_Max
    , avg(case when VitalID = 7 then valuenum else null end) as SpO2_Mean
    , min(case when VitalID = 8 then valuenum else null end) as Glucose_Min
    , max(case when VitalID = 8 then valuenum else null end) as Glucose_Max
    , avg(case when VitalID = 8 then valuenum else null end) as Glucose_Mean
    , hour
    -- , (ce.charttime - ie.intime) as hour_bucket
    FROM  (
      select ie.subject_id, ie.hadm_id, ie.icustay_id
      , case
        when itemid in (211,220045) and valuenum > 0 and valuenum < 300 then 1 -- HeartRate
        when itemid in (51,442,455,6701,220179,220050) and valuenum > 0 and valuenum < 400 then 2 -- SysBP
        when itemid in (8368,8440,8441,8555,220180,220051) and valuenum > 0 and valuenum < 300 then 3 -- DiasBP
        when itemid in (456,52,6702,443,220052,220181,225312) and valuenum > 0 and valuenum < 300 then 4 -- MeanBP
        when itemid in (615,618,220210,224690) and valuenum > 0 and valuenum < 70 then 5 -- RespRate
        when itemid in (223761,678) and valuenum > 70 and valuenum < 120  then 6 -- TempF, converted to degC in valuenum call
        when itemid in (223762,676) and valuenum > 10 and valuenum < 50  then 6 -- TempC
        when itemid in (646,220277) and valuenum > 0 and valuenum <= 100 then 7 -- SpO2
        when itemid in (807,811,1529,3745,3744,225664,220621,226537) and valuenum > 0 then 8 -- Glucose
        else null end as VitalID
          -- convert F to C
      , case when itemid in (223761,678) then (valuenum-32)/1.8 else valuenum end as valuenum
      , floor(extract(epoch from ce.charttime - ie.intime) / 3600) as hour
      from icustays ie
      left join chartevents ce
      on ie.subject_id = ce.subject_id and ie.hadm_id = ce.hadm_id and ie.icustay_id = ce.icustay_id
      and ce.charttime between ie.intime and ie.intime + interval '24' hour
      -- exclude rows marked as error
      and ce.error IS DISTINCT FROM 1
      where ce.itemid in
      (
      -- HEART RATE
      211, --"Heart Rate"
      220045, --"Heart Rate"
      -- Systolic/diastolic
      51, --	Arterial BP [Systolic]
      442, --	Manual BP [Systolic]
      455, --	NBP [Systolic]
      6701, --	Arterial BP #2 [Systolic]
      220179, --	Non Invasive Blood Pressure systolic
      220050, --	Arterial Blood Pressure systolic
      8368, --	Arterial BP [Diastolic]
      8440, --	Manual BP [Diastolic]
      8441, --	NBP [Diastolic]
      8555, --	Arterial BP #2 [Diastolic]
      220180, --	Non Invasive Blood Pressure diastolic
      220051, --	Arterial Blood Pressure diastolic
      -- MEAN ARTERIAL PRESSURE
      456, --"NBP Mean"
      52, --"Arterial BP Mean"
      6702, --	Arterial BP Mean #2
      443, --	Manual BP Mean(calc)
      220052, --"Arterial Blood Pressure mean"
      220181, --"Non Invasive Blood Pressure mean"
      225312, --"ART BP mean"
      -- RESPIRATORY RATE
      618,--	Respiratory Rate
      615,--	Resp Rate (Total)
      220210,--	Respiratory Rate
      224690, --	Respiratory Rate (Total)
      -- SPO2, peripheral
      646, 220277,
      -- GLUCOSE, both lab and fingerstick
      807,--	Fingerstick Glucose
      811,--	Glucose (70-105)
      1529,--	Glucose
      3745,--	BloodGlucose
      3744,--	Blood Glucose
      225664,--	Glucose finger stick
      220621,--	Glucose (serum)
      226537,--	Glucose (whole blood)
      -- TEMPERATURE
      223762, -- "Temperature Celsius"
      676,	-- "Temperature C"
      223761, -- "Temperature Fahrenheit"
      678 --	"Temperature F"
      )
    ) pvt
    group by pvt.subject_id, pvt.hadm_id, pvt.icustay_id, hour
    order by pvt.subject_id, pvt.hadm_id, pvt.icustay_id, hour;
    """

    vithr = pd.read_sql_query(vithrquery,con)
    vithr.to_csv('vitals_24h.csv', index=False)

def get_1d():
    vithrquery = \
    """
    -- This query pivots the vital signs for the first 48 hours of a patient's stay
    -- Vital signs include heart rate, blood pressure, respiration rate, and temperature
    -- DROP MATERIALIZED VIEW IF EXISTS vitalsfirstday CASCADE;
    -- create materialized view vitalsfirstday as
    SELECT pvt.subject_id, pvt.hadm_id, pvt.icustay_id
    -- Easier names
    , min(case when VitalID = 1 then valuenum else null end) as HeartRate_Min
    , max(case when VitalID = 1 then valuenum else null end) as HeartRate_Max
    , avg(case when VitalID = 1 then valuenum else null end) as HeartRate_Mean
    , min(case when VitalID = 2 then valuenum else null end) as SysBP_Min
    , max(case when VitalID = 2 then valuenum else null end) as SysBP_Max
    , avg(case when VitalID = 2 then valuenum else null end) as SysBP_Mean
    , min(case when VitalID = 3 then valuenum else null end) as DiasBP_Min
    , max(case when VitalID = 3 then valuenum else null end) as DiasBP_Max
    , avg(case when VitalID = 3 then valuenum else null end) as DiasBP_Mean
    , min(case when VitalID = 4 then valuenum else null end) as MeanBP_Min
    , max(case when VitalID = 4 then valuenum else null end) as MeanBP_Max
    , avg(case when VitalID = 4 then valuenum else null end) as MeanBP_Mean
    , min(case when VitalID = 5 then valuenum else null end) as RespRate_Min
    , max(case when VitalID = 5 then valuenum else null end) as RespRate_Max
    , avg(case when VitalID = 5 then valuenum else null end) as RespRate_Mean
    , min(case when VitalID = 6 then valuenum else null end) as TempC_Min
    , max(case when VitalID = 6 then valuenum else null end) as TempC_Max
    , avg(case when VitalID = 6 then valuenum else null end) as TempC_Mean
    , min(case when VitalID = 7 then valuenum else null end) as SpO2_Min
    , max(case when VitalID = 7 then valuenum else null end) as SpO2_Max
    , avg(case when VitalID = 7 then valuenum else null end) as SpO2_Mean
    , min(case when VitalID = 8 then valuenum else null end) as Glucose_Min
    , max(case when VitalID = 8 then valuenum else null end) as Glucose_Max
    , avg(case when VitalID = 8 then valuenum else null end) as Glucose_Mean
    -- , (ce.charttime - ie.intime) as hour_bucket
    FROM  (
      select ie.subject_id, ie.hadm_id, ie.icustay_id
      , case
        when itemid in (211,220045) and valuenum > 0 and valuenum < 300 then 1 -- HeartRate
        when itemid in (51,442,455,6701,220179,220050) and valuenum > 0 and valuenum < 400 then 2 -- SysBP
        when itemid in (8368,8440,8441,8555,220180,220051) and valuenum > 0 and valuenum < 300 then 3 -- DiasBP
        when itemid in (456,52,6702,443,220052,220181,225312) and valuenum > 0 and valuenum < 300 then 4 -- MeanBP
        when itemid in (615,618,220210,224690) and valuenum > 0 and valuenum < 70 then 5 -- RespRate
        when itemid in (223761,678) and valuenum > 70 and valuenum < 120  then 6 -- TempF, converted to degC in valuenum call
        when itemid in (223762,676) and valuenum > 10 and valuenum < 50  then 6 -- TempC
        when itemid in (646,220277) and valuenum > 0 and valuenum <= 100 then 7 -- SpO2
        when itemid in (807,811,1529,3745,3744,225664,220621,226537) and valuenum > 0 then 8 -- Glucose
        else null end as VitalID
          -- convert F to C
      , case when itemid in (223761,678) then (valuenum-32)/1.8 else valuenum end as valuenum
      , floor(extract(epoch from ce.charttime - ie.intime) / 3600) as hour
      from icustays ie
      left join chartevents ce
      on ie.subject_id = ce.subject_id and ie.hadm_id = ce.hadm_id and ie.icustay_id = ce.icustay_id
      and ce.charttime between ie.intime and ie.intime + interval '24' hour
      -- exclude rows marked as error
      and ce.error IS DISTINCT FROM 1
      where ce.itemid in
      (
      -- HEART RATE
      211, --"Heart Rate"
      220045, --"Heart Rate"
      -- Systolic/diastolic
      51, --	Arterial BP [Systolic]
      442, --	Manual BP [Systolic]
      455, --	NBP [Systolic]
      6701, --	Arterial BP #2 [Systolic]
      220179, --	Non Invasive Blood Pressure systolic
      220050, --	Arterial Blood Pressure systolic
      8368, --	Arterial BP [Diastolic]
      8440, --	Manual BP [Diastolic]
      8441, --	NBP [Diastolic]
      8555, --	Arterial BP #2 [Diastolic]
      220180, --	Non Invasive Blood Pressure diastolic
      220051, --	Arterial Blood Pressure diastolic
      -- MEAN ARTERIAL PRESSURE
      456, --"NBP Mean"
      52, --"Arterial BP Mean"
      6702, --	Arterial BP Mean #2
      443, --	Manual BP Mean(calc)
      220052, --"Arterial Blood Pressure mean"
      220181, --"Non Invasive Blood Pressure mean"
      225312, --"ART BP mean"
      -- RESPIRATORY RATE
      618,--	Respiratory Rate
      615,--	Resp Rate (Total)
      220210,--	Respiratory Rate
      224690, --	Respiratory Rate (Total)
      -- SPO2, peripheral
      646, 220277,
      -- GLUCOSE, both lab and fingerstick
      807,--	Fingerstick Glucose
      811,--	Glucose (70-105)
      1529,--	Glucose
      3745,--	BloodGlucose
      3744,--	Blood Glucose
      225664,--	Glucose finger stick
      220621,--	Glucose (serum)
      226537,--	Glucose (whole blood)
      -- TEMPERATURE
      223762, -- "Temperature Celsius"
      676,	-- "Temperature C"
      223761, -- "Temperature Fahrenheit"
      678 --	"Temperature F"
      )
    ) pvt
    group by pvt.subject_id, pvt.hadm_id, pvt.icustay_id
    order by pvt.subject_id, pvt.hadm_id, pvt.icustay_id;
    """


    vithr = pd.read_sql_query(vithrquery,con)
    vithr.to_csv('vitals_1d.csv', index=False)

def get_12h():
    vithrquery = \
    """
    -- This query pivots the vital signs for the first 48 hours of a patient's stay
    -- Vital signs include heart rate, blood pressure, respiration rate, and temperature
    -- DROP MATERIALIZED VIEW IF EXISTS vitalsfirstday CASCADE;
    -- create materialized view vitalsfirstday as
    SELECT pvt.subject_id, pvt.hadm_id, pvt.icustay_id
    -- Easier names
    , min(case when VitalID = 1 then valuenum else null end) as HeartRate_Min
    , max(case when VitalID = 1 then valuenum else null end) as HeartRate_Max
    , avg(case when VitalID = 1 then valuenum else null end) as HeartRate_Mean
    , min(case when VitalID = 2 then valuenum else null end) as SysBP_Min
    , max(case when VitalID = 2 then valuenum else null end) as SysBP_Max
    , avg(case when VitalID = 2 then valuenum else null end) as SysBP_Mean
    , min(case when VitalID = 3 then valuenum else null end) as DiasBP_Min
    , max(case when VitalID = 3 then valuenum else null end) as DiasBP_Max
    , avg(case when VitalID = 3 then valuenum else null end) as DiasBP_Mean
    , min(case when VitalID = 4 then valuenum else null end) as MeanBP_Min
    , max(case when VitalID = 4 then valuenum else null end) as MeanBP_Max
    , avg(case when VitalID = 4 then valuenum else null end) as MeanBP_Mean
    , min(case when VitalID = 5 then valuenum else null end) as RespRate_Min
    , max(case when VitalID = 5 then valuenum else null end) as RespRate_Max
    , avg(case when VitalID = 5 then valuenum else null end) as RespRate_Mean
    , min(case when VitalID = 6 then valuenum else null end) as TempC_Min
    , max(case when VitalID = 6 then valuenum else null end) as TempC_Max
    , avg(case when VitalID = 6 then valuenum else null end) as TempC_Mean
    , min(case when VitalID = 7 then valuenum else null end) as SpO2_Min
    , max(case when VitalID = 7 then valuenum else null end) as SpO2_Max
    , avg(case when VitalID = 7 then valuenum else null end) as SpO2_Mean
    , min(case when VitalID = 8 then valuenum else null end) as Glucose_Min
    , max(case when VitalID = 8 then valuenum else null end) as Glucose_Max
    , avg(case when VitalID = 8 then valuenum else null end) as Glucose_Mean
    -- , (ce.charttime - ie.intime) as hour_bucket
    FROM  (
      select ie.subject_id, ie.hadm_id, ie.icustay_id
      , case
        when itemid in (211,220045) and valuenum > 0 and valuenum < 300 then 1 -- HeartRate
        when itemid in (51,442,455,6701,220179,220050) and valuenum > 0 and valuenum < 400 then 2 -- SysBP
        when itemid in (8368,8440,8441,8555,220180,220051) and valuenum > 0 and valuenum < 300 then 3 -- DiasBP
        when itemid in (456,52,6702,443,220052,220181,225312) and valuenum > 0 and valuenum < 300 then 4 -- MeanBP
        when itemid in (615,618,220210,224690) and valuenum > 0 and valuenum < 70 then 5 -- RespRate
        when itemid in (223761,678) and valuenum > 70 and valuenum < 120  then 6 -- TempF, converted to degC in valuenum call
        when itemid in (223762,676) and valuenum > 10 and valuenum < 50  then 6 -- TempC
        when itemid in (646,220277) and valuenum > 0 and valuenum <= 100 then 7 -- SpO2
        when itemid in (807,811,1529,3745,3744,225664,220621,226537) and valuenum > 0 then 8 -- Glucose
        else null end as VitalID
          -- convert F to C
      , case when itemid in (223761,678) then (valuenum-32)/1.8 else valuenum end as valuenum
      , floor(extract(epoch from ce.charttime - ie.intime) / 3600) as hour
      from icustays ie
      left join chartevents ce
      on ie.subject_id = ce.subject_id and ie.hadm_id = ce.hadm_id and ie.icustay_id = ce.icustay_id
      and ce.charttime between ie.intime and ie.intime + interval '12' hour
      -- exclude rows marked as error
      and ce.error IS DISTINCT FROM 1
      where ce.itemid in
      (
      -- HEART RATE
      211, --"Heart Rate"
      220045, --"Heart Rate"
      -- Systolic/diastolic
      51, --	Arterial BP [Systolic]
      442, --	Manual BP [Systolic]
      455, --	NBP [Systolic]
      6701, --	Arterial BP #2 [Systolic]
      220179, --	Non Invasive Blood Pressure systolic
      220050, --	Arterial Blood Pressure systolic
      8368, --	Arterial BP [Diastolic]
      8440, --	Manual BP [Diastolic]
      8441, --	NBP [Diastolic]
      8555, --	Arterial BP #2 [Diastolic]
      220180, --	Non Invasive Blood Pressure diastolic
      220051, --	Arterial Blood Pressure diastolic
      -- MEAN ARTERIAL PRESSURE
      456, --"NBP Mean"
      52, --"Arterial BP Mean"
      6702, --	Arterial BP Mean #2
      443, --	Manual BP Mean(calc)
      220052, --"Arterial Blood Pressure mean"
      220181, --"Non Invasive Blood Pressure mean"
      225312, --"ART BP mean"
      -- RESPIRATORY RATE
      618,--	Respiratory Rate
      615,--	Resp Rate (Total)
      220210,--	Respiratory Rate
      224690, --	Respiratory Rate (Total)
      -- SPO2, peripheral
      646, 220277,
      -- GLUCOSE, both lab and fingerstick
      807,--	Fingerstick Glucose
      811,--	Glucose (70-105)
      1529,--	Glucose
      3745,--	BloodGlucose
      3744,--	Blood Glucose
      225664,--	Glucose finger stick
      220621,--	Glucose (serum)
      226537,--	Glucose (whole blood)
      -- TEMPERATURE
      223762, -- "Temperature Celsius"
      676,	-- "Temperature C"
      223761, -- "Temperature Fahrenheit"
      678 --	"Temperature F"
      )
    ) pvt
    group by pvt.subject_id, pvt.hadm_id, pvt.icustay_id
    order by pvt.subject_id, pvt.hadm_id, pvt.icustay_id;
    """

    vithr = pd.read_sql_query(vithrquery,con)
    vithr.to_csv('vitals_12h.csv', index=False)

get_24h()
get_demo()
# import pdb; pdb.set_trace()