import argparse
import pandas as pd
import psycopg2
import csv

from pymetamap import MetaMap
import pickle
import matplotlib.pyplot as plt
import numpy as np

sqluser = 'iychen'
dbname = 'mimic'
schema_name = 'mimiciii'

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-N', type=int, 
                    help='number of data points to use')
args = parser.parse_args()

datadir = '/Users/irenechen/Documents/mimic-data'

# Connect to postgres with a copy of the MIMIC-III database
con = psycopg2.connect(dbname=dbname, user=sqluser)

# the below statement is prepended to queries to ensure they select from the right schema
query_schema = 'set search_path to ' + schema_name + ';'

mm = MetaMap.get_instance('/afs/csail.mit.edu/group/clinicalml/shared/mimic_folder/timeline/public_mm/bin/metamap18')
    
df = pd.read_csv('../pset2/discharge_summaries.csv')

N = args.N

csvfile = open('dc_%d.csv' % args.N, 'wb')
fieldnames = ['index', 'pos_info', 'mm', 'trigger', 'semtypes', 'patientid', 'preferred_name', 'score', 'location', 'tree_codes', 'cui']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

def cui_to_dict(cui,k):
    results = dict()
    results['index'] = cui.index
    results['mm'] = cui.mm
    results['score'] = cui.score
    results['preferred_name'] = cui.preferred_name
    results['cui'] = cui.cui
    results['semtypes'] = cui.semtypes
    results['trigger'] = cui.trigger
    results['location'] = cui.location
    results['pos_info'] = cui.pos_info
    results['tree_codes'] = cui.tree_codes
    return results

all_cuis = list()
all_errors = list()
# for i in xrange(N):
total_N = len(df)

rand_ids = np.random.choice(total_N,N,replace=False)
print 'only using %d notes' % len(rand_ids)
sents = [df.iloc[i]['dc_chart'] for i in rand_ids]

processes = 500
chunk_total = len(sents)

chunks_idx =[(((chunk_total*(i-1))/processes),((chunk_total*i)/processes)) for i in range(1,processes+1) ]
print chunks_idx
for (start, stop) in chunks_idx:
    sents_subset = sents[start:stop]
    ids_subset = rand_ids[start:stop]
    concepts,error = mm.extract_concepts(sents_subset, ids_subset)

    for j, concept in enumerate(concepts):
        try:
            cui = cui_to_dict(concept,j)
            writer.writerow(cui)
            csvfile.flush()
            print 'wrote row'
    #         all_cuis.append(cui)
        except:
            all_errors.append(j)

df3 = pd.DataFrame(all_errors)
df3.to_csv('../pset3/dc_errors_%d.csv' % N)