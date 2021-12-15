import pandas as pd


FIELDS_DATASET = 'datasets/df_metadata_annotated.pkl'
CLAUSES_DATASET = 'datasets/df_clause_id_examples.pkl'  # Load from config?

df_fields_annotated = pd.read_pickle(FIELDS_DATASET)
df_clauses = pd.read_pickle(CLAUSES_DATASET)