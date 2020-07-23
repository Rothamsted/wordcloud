import json, urllib.request
import requests
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


import matplotlib.pyplot as plt
%matplotlib inline

Username = input("What's your Username?")
Password = input("What's your Password")
url = input("Enter a URL")
if url == "":
    url = "https://knetminer.com/beta/knetspace/api/v1/networks/acf96c4d-74ff-4fb1-a65a-745c20d2981a/?format=json"
api_host = "https://knetminer.com/beta/knetspace"  # The Host of the API
#your_knetspace_username = "xhakanai"  #Takes Username and password for use in the token.
#your_knetspace_password = "verysecureknetpassword" #Takes Username and password for use in the token.
session = requests.Session()  #Requests a session to the server.
token = session.post(api_host + '/auth/jwt/', json={'username_or_email': Username, 'password': Password}).json() #This authenticates the session.
me = session.get(api_host + '/api/v1/me').json()

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
    for i in range(0, len(concepts_dict['concepts'])):
        concept_count.append(concepts_dict['concepts'][i]['ofType'])
        concept_id_name.append([concepts_dict['concepts'][i]['ofType'], concepts_dict['concepts'][i]['value']])
        try:
            concept_type_dict[concepts_dict['concepts'][i]['id']] = concept_id_name[i]
        except:
            print(f"Failed for iteration {i}")
            pass

    relationships_type_dict, relations_count = {}, []
    relationships_id_name = []
    for i in range(0, len(relationships_dict['relations'])):
        relations_count.append(relationships_dict['relations'][i]['ofType'])
        relationships_id_name.append([relationships_dict['relations'][i]['ofType'], relationships_dict['relations'][i]['toConcept']])
        try:
            relationships_type_dict[relationships_dict['relations'][i]['id']] = relationships_id_name[i]
        except:
            print(f"Failed for iteration {i}")
            pass

    publications_dict = meta_data_dict['abstract']

    concept_count = dict(Counter(concept_count))
    relations_count = dict(Counter(relations_count))

    # Getting relationship counts
    relationship_counts = []
    for i in range(0, len(relationships_dict['relations'])):
        from_concept = relationships_dict['relations'][i]['fromConcept'] # Variable from_concept is set to be equal to the strings between relations and fromConcept in the relations_dict
        to_concept = relationships_dict['relations'][i]['toConcept'] # Variable to_concept is set to be equal to the strings between relations and toConcept in the relations_dict
        for k in concept_type_dict.keys(): # For the Key in the concept_type_dict, if it is the same as to_concept, append the key 1. The same applies to from_concept
            if k == to_concept:
                if "<span style" not in concept_type_dict[to_concept][1]: # If <span style is found anywhere in the dictionary, remove it.
                    relationship_counts.append(concept_type_dict[k][1])
            if k == from_concept:
                if "<span style" not in concept_type_dict[from_concept][1]:
                    relationship_counts.append(concept_type_dict[k][1])

    relationship_counter=(dict(Counter(relationship_counts)))

    df = pd.DataFrame(relationship_counter.items(), columns = ['Name','Count'])
    updated_df = df[df['Name'].apply(lambda x: "PMID" not in x)]

    stopwords = set(STOPWORDS)
    stopwords.update(["Proteins", "Genes", "Relations", "Concepts", "PMID", "Protein"])
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate('text')
    text = " ".join(name for name in updated_df.Name)
    wordcloud = WordCloud().generate(text)
    wordcloud = WordCloud(max_font_size=150, max_words=1000, background_color="black").generate(text)
    plt.figure(figsize=(30,15))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    wordcloud.to_file("wordcloud.png")
    plt.savefig('plot.png', dpi=300, bbox_inches='tight')
    plt.show()



else:
    print(f"Response failed due to error code {response.status_code}")
