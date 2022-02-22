import os
import sys
import boto3
import zipfile

from app.config.common import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME


session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
s3_client = session.client('s3')

def download_model():
    if os.path.exists('./models/legal_bert_small_smoothing-0.1'):
        return

    file_name = "legal_bert_small_smoothing-0.1.zip"

    try:

        with open('./models/legal_bert_small_smoothing-0.1.zip', 'wb') as data:
            s3_client.download_fileobj(BUCKET_NAME, file_name, data)

        print('File downloaded', flush=True)

        with zipfile.ZipFile('./models/legal_bert_small_smoothing-0.1.zip', 'r') as zip_ref:
            zip_ref.extractall('./models/')

        print('File unzipped', flush=True)
    except Exception:
        print("save failed ", sys.exc_info()[0])

    finally:
        os.remove('./models/legal_bert_small_smoothing-0.1.zip')

def download_datasets():
    datasets = ['df_metadata_annotated.pkl', 'df_clause_id_examples.pkl']
    try:
        for dataset in datasets:
            if os.path.exists(f'./datasets/{dataset}'):
                return
            with open(f'./datasets/{dataset}', 'wb') as data:
                s3_client.download_fileobj(BUCKET_NAME, dataset, data)

    except Exception:
        print("save failed ", sys.exc_info()[0])
