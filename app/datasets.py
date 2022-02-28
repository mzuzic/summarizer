import pandas as pd
from init_files_handler import download_datasets


FIELDS_DATASET = 'datasets/df_metadata_annotated.pkl'
CLAUSES_DATASET = 'datasets/df_clause_id_examples.pkl'  # Load from config?


def get_datasets():
    download_datasets()
    df_fields_annotated = pd.read_pickle(FIELDS_DATASET)
    df_clauses = pd.read_pickle(CLAUSES_DATASET)
    return df_fields_annotated, df_clauses


df_fields_annotated, df_clauses = get_datasets()
