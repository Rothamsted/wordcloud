import json, urllib.request
import requests
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib

# import subprocess
# import sys
#
# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package, '--user'])
# req = ['matplotlib', 'pandas', 'numpy']
# [install(mod) for mod in req]

#Takes Username and password for use in the token.
api_host = "https://knetminer.com/beta/knetspace"  # The Host of the API
your_knetspace_username = "xhakanai"
your_knetspace_password = "verysecureknetpassword"
#Requests a session to the server.
session = requests.Session()
token = session.post(api_host + '/auth/jwt/', json={'username_or_email': your_knetspace_username, 'password': your_knetspace_password}).json() #This authenticates the session.
me = session.get(api_host + '/api/v1/me').json()

url = "https://knetminer.com/beta/knetspace/api/v1/networks/acf96c4d-74ff-4fb1-a65a-745c20d2981a/?format=json"
response = session.get(url) #This establishes a connection to the server.

if response.status_code ==  200:
    knetspace_json = response.json()
    print(knetspace_json) #This will then print the contents of the web token, i.e the Username, Email, etc, of the account connected the the URL.
    knetspace_json
    knetspace_json['graph'].keys() #Going through the json
    knetspace_json['graph']['allGraphData']['ondexmetadata'] #Going through parts of the json to find concepts and relations
    meta_data_dict = knetspace_json['graph']['allGraphData']['ondexmetadata'] #Turns out metadata has what is needed
    meta_data_keys = list(meta_data_dict.keys())
    concepts_dict, relationships_dict = {}, {}

    for i, v in enumerate(meta_data_dict.values()): #For interation in ondexmetadata, store it as a value
        print(meta_data_keys[i], v)
        if "concepts" in meta_data_keys[i]:
            concepts_dict[meta_data_keys[i]] = v
        if "relations" in meta_data_keys[i]:
            relationships_dict[meta_data_keys[i]] = v

    concept_type_dict, concept_count = {}, []
    concept_id_name = []
    for i in range(0, len(concepts_dict['concepts'])): #For interation within the range of the list and 0
        concept_count.append(concepts_dict['concepts'][i]['ofType'])
        concept_id_name.append([concepts_dict['concepts'][i]['ofType'], concepts_dict['concepts'][i]['value']])
        try:
            concept_type_dict[concepts_dict['concepts'][i]['id']] = concept_id_name[i]
        except:
            print(f"Failed for iteration {i}")
            pass

    relationships_type_dict, relations_count = {}, []
    relationships_id_name = []
    for i in range(0, len(relationships_dict['relations'])): #For interation within the range of the list and 0
        relations_count.append(relationships_dict['relations'][i]['ofType'])
        relationships_id_name.append([relationships_dict['relations'][i]['ofType'], relationships_dict['relations'][i]['toConcept']])
        try:
            relationships_type_dict[relationships_dict['relations'][i]['id']] = relationships_id_name[i]
        except:
            print(f"Failed for iteration {i}")
            pass

    concept_count = dict(Counter(concept_count))
    relations_count = dict(Counter(relations_count))
    relationships_dict

    # Getting relationship counts
    relationship_counts = []
    for i in range(0, len(relationships_dict['relations'])):
        from_concept = relationships_dict['relations'][i]['fromConcept'] # Variable from_concept is set to be equal to the strings between relations and fromConcept in the relations_dict
        to_concept = relationships_dict['relations'][i]['toConcept'] # Variable to_concept is set to be equal to the strings between relations and toConcept in the relations_dict
        for k in concept_type_dict.keys(): # For the Key in the concept_type_dict, if it is the same as to_concept, append the key 1. The same applies to from_concept
            if k == to_concept:
                if "<span style" not in concept_type_dict[to_concept][1]: # If <span style is found anywhere in the dictionary, remove it.
                    #print(k, concept_type_dict[k][1])
                    relationship_counts.append(concept_type_dict[k][1])
            if k == from_concept:
                if "<span style" not in concept_type_dict[from_concept][1]:
                    relationship_counts.append(concept_type_dict[k][1])

    print(dict(Counter(relationship_counts))) # Print the counter.
            # Put relationship counts into pandas data frame - it's a dict so figure out how to put a dict into a dataframe and what to name the columns

            # Then put into a word cloud using the resource sent with matplotlib


    relation_count_df = pd.DataFrame(dict(Counter(relationship_counts)))
    relation_count_df

    for i, toConcept in enumerate(relationships_dict):
        relationships_dict['relations'][i][toConcept] = +1

    concept_relation_count = {concept_type_dict:0}
    for i, v in enumerate(relationships_dict):
        print(v)


else:
    print(f"Response failed due to error code {response.status_code}")
