import os
import math
import numpy as np
from collections import defaultdict

from app.model_repository import nlp
from app.constants import TOPN
from app.services.storage_service import storage_service

from .utils.utils import is_valid_token, is_duration, is_date, is_money
from .utils.spacy_utils import tokenize_sentence


def get_token_embedding(spacy_tkn, nlp_example):
    left_side = list()
    right_side = list()
    left_side = [it.vector for it in nlp_example[:spacy_tkn.i] if is_valid_token(it)]

    if len(left_side) > TOPN:
        left_side = left_side[:-TOPN]
        
    right_side = [it.vector for it in nlp_example[spacy_tkn.i+1:] if is_valid_token(it)][:TOPN]
    if len(right_side) > TOPN:
        right_side = right_side[:TOPN]

    if len(left_side) == 0 and len(right_side) == 0:
        return None
    if len(left_side) == 0:
        left_side = np.array([0]*len(right_side))
    if len(right_side) == 0:
        right_side = np.array([0]*len(left_side))

    return np.mean(left_side, axis=0) + np.mean(right_side, axis=0)


def batch_predict_proba_knn(input_embeddings, knn_model):
    preds = knn_model.kneighbors(input_embeddings, n_neighbors=1, return_distance=True)
    labels = knn_model.predict(input_embeddings)
    return preds, labels


def get_tkns_types(nlp_example):
    tkns_types = defaultdict(list) # list of spacy tkns marked with the NER type
    
    for tkn in nlp_example:
        if is_duration(tkn.text, tkn.pos_):
            tkns_types['DURATION'].append(tkn)
        elif is_date(tkn.text, tkn.pos_):
            tkns_types['DATE'].append(tkn)
        elif is_money(tkn.text, tkn.pos_):
            tkns_types['MONEY'].append(tkn)
            
    return tkns_types


def load_custom_field_models(all_custom_models):
    loaded_model_map = dict()

    for ent_type in all_custom_models:
        loaded_model_map[ent_type] = dict()
        for lbl in all_custom_models[ent_type]:
            storage_path = all_custom_models[ent_type][lbl]
            model = storage_service.download_ml_model(storage_path)
            loaded_model_map[ent_type][lbl] = model

    return loaded_model_map

THRESHOLD = 0.85

def get_custom_fields(nlp_example, model_map, clause_json):
    # then call tokenize_sentence on the nlp_example, to recombine
    # clause_json should contain clause_type and paragraph_index
    
    recombined_nlp_example = tokenize_sentence(nlp_example)
    tkns_types = get_tkns_types(recombined_nlp_example)
    
    result_map = defaultdict(list)
    
    for ent_type in tkns_types:
        if ent_type not in model_map:
            continue
            
        tkns = tkns_types[ent_type]
        tkn_embeddings = [get_token_embedding(tkn, nlp_example) for tkn in tkns]
        
        for custom_label in model_map[ent_type]:
            knn_model = model_map[ent_type][custom_label]
            
            tkn_sims, label_preds = batch_predict_proba_knn(tkn_embeddings, knn_model)
            
            similarities, n_neighbors_list = tkn_sims
            for idx, sim in enumerate(similarities):
                n_neighbors = n_neighbors_list[idx]
                tkn = tkns[idx]
                sim = 1 - sim
                if label_preds[idx] == 1:
                    result_map[custom_label].append((tkn.text, str(sim[0])))
    return result_map


def batch_predict_custom_fields(examples, all_custom_models):
    # all_custom_models are from the core_app, a map of all custom models trained per ent_type and label
    """
        {
            "DURATION": {
                "PT": "model_path_on_storage_service.pkl",
                "LC": "model_path_on_storage_service.pkl"
            },
            "MONEY": {
                "TIV": "model_path_on_storage_service.pkl",
                ...
            },
            ...
        }
    """
    nlp_examples = list(nlp.pipe(examples))

    # load all custom field type models from storage
    model_map = load_custom_field_models(all_custom_models)

    results = list()
    for nlp_example in nlp_examples:
        res = get_custom_fields(nlp_example, model_map, None)
        results.append(res)

    return results


