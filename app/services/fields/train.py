# TRAINING

# TODO: USE SPATIAL INFORMATION (where inside the document is it included)

import numpy as np
import pickle
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier

from app.models import nlp
from app.datasets import df_fields_annotated
from app.constants import TOPN

from .utils.utils import is_valid_token


def get_contra_examples(ent_type, num=50):
    examples = []
    # examples are a list of tuples (ent_text, start_offset, clause_text, label)
    
    labels_to_extract = []
    if ent_type == 'DURATION':
        # pick up conga entities that belong to duration: TND
        labels_to_extract = ['TND']
    if ent_type == 'DATE':
        # pick up conga entities that belong to date: ASD, AED
        labels_to_extract = ['ASD', 'AED']
    if ent_type == 'MONEY':
        # pick up conga entities that belong to money: TAV
        labels_to_extract = ['TAV']
    
    if len(labels_to_extract) == 0:
        return []
        
    for idx, it in df_fields_annotated.iterrows():
        for i in range(1, 35):
            if f'Entity {i} type' in it:
                if it[f'Entity {i} type'] in labels_to_extract:
                    if pd.isna(it[f'Entity {i}']):
                        continue
                    j = it['Clause Text'].find(it[f'Entity {i}'])
                    examples.append({"ent_text": it[f'Entity {i}'],
                                     "start_offset": j,
                                     "clause_text": it['Clause Text'],
                                     "label": it['Label']
                                    })
    print(len(examples))
    return examples[:num]


def get_embeddings(support_list):
    # support_list is the same as examples in train()
    
    relevant_embeddings = list()
    ent_types = list()
    for support in support_list:
        ent_text = support['ent_text']
        start_offset = int(support['start_offset'])
        clause_text = support['clause_text']
        label = support['label']
        
        nlp_support = nlp(clause_text)
        tkns = [tkn for tkn in nlp_support]
                
        left_side = [tkn for tkn in tkns if tkn.idx < start_offset if is_valid_token(tkn)]
        if len(left_side) > TOPN:
            left_side = left_side[:-TOPN]
        right_side = [tkn for tkn in tkns if tkn.idx > start_offset + len(ent_text) if is_valid_token(tkn)]
        if len(right_side) > TOPN:
            right_side = right_side[:TOPN]
        
        left_vecs = list()
        right_vecs = list()
        for it in left_side:
            left_vecs.append(it.vector)
        
        for it in right_side:
            right_vecs.append(it.vector)
        
        final_embedding = np.mean(left_vecs, axis=0) + np.mean(right_vecs, axis=0)
        
        relevant_embeddings.append(final_embedding)
    return relevant_embeddings


def train(examples, label, ent_type):
    # ent_type - spacy entity type it is connected to (MONEY, INTEGER, DATE, DURATION)
    # we assume these are all from the same label - prefilter needed (per label)
    # examples are a list of tuples (ent_text, start_offset, clause_text, label)
    contra_examples = get_contra_examples(ent_type)
    
    support_embeddings = get_embeddings(examples)
    support_embeddings = [se for se in support_embeddings if not np.isnan(se).all()]
    contra_support_embeddings = get_embeddings(contra_examples)
    contra_support_embeddings = [se for se in contra_support_embeddings if not np.isnan(se).all()]
    
    X_train = support_embeddings + contra_support_embeddings
    y_train = [1]*len(support_embeddings) + [0]*len(contra_support_embeddings)

    knn = KNeighborsClassifier(n_neighbors=1, metric='cosine')
    knn.fit(X_train, y_train)
        
    return knn

def load_model(label, ent_type):
    with open(f'knn_{label}_{ent_type}.pkl', 'rb') as f:
        knn = pickle.load(f)
    return knn