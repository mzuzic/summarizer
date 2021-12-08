import re

from sklearn.neighbors import KNeighborsClassifier
from app.models import clause_encoder
from app.datasets import df_clauses


def preprocess_clause(text):
    text = re.sub('\s+', ' ', text)

    return text.strip()


def train(clauses, labels):
    clauses = [preprocess_clause(clause) for clause in clauses]

    # Append negative examples
    clauses += df_clauses.text.tolist()
    labels += df_clauses.label.tolist()
    
    embeddings = clause_encoder.encode(clauses)

    knn = KNeighborsClassifier(
        n_neighbors=1,
        metric='cosine'
    )

    knn.fit(embeddings, labels)

    return knn
