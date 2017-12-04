from elasticsearch import Elasticsearch
from google.cloud import storage
import os, re, json, certifi

def upload_to_elastic():
  es = start_bonsai()
  for filename in os.listdir('./image_question'):
    [exam_info_path, question_info_path, question_image_path, solution_image_path] = get_paths(filename)

    data = {}
    data['q_img'] = upload_to_gcs(question_image_path.split('/')[-1], question_image_path)
    data['s_img'] = upload_to_gcs(solution_image_path.split('/')[-1], solution_image_path)
    print '%s uploaded successfully to GCS' % filename

    update_json(data, exam_info_path)
    update_json(data, question_info_path)
    es.index(index='exam', doc_type='question', body=json.dumps(data))
    print 'JSON uploaded successfully to ES'

def upload_to_gcs(destination_blob_name, filepath):
  storage_client = storage.Client.from_service_account_json('forager-upload.json')
  bucket = storage_client.get_bucket('forager-qa-images')
  blob = bucket.blob(destination_blob_name)
  blob.upload_from_filename(filepath)
  return destination_blob_name

def clear_elastic():
  es = start_bonsai()
  es.indices.delete(index='exam', ignore=[400, 404])

##### HELPERS #####
def get_paths(path):
  exam_info_path = './info_exam/' + '_'.join(path.split('_')[:-1]) + '.json'
  question_info_path = './info_question/' + replace_last(path, '.PNG', '.json')
  question_image_path = './image_question/' + path
  solution_image_path = './image_solution/' + replace_last(path, 'q', 's')
  return [exam_info_path, question_info_path, question_image_path, solution_image_path]

def replace_last(src_str, replace_what, replace_with):
  head, _sep, tail = src_str.rpartition(replace_what)
  return head + replace_with + tail

def update_json(curr_json, path_to_json):
  with open(path_to_json) as json_file:
    curr_json.update(json.load(json_file))

def start_elastic():
  return Elasticsearch([{'host': 'localhost', 'port': 9200}])

def start_bonsai():
  bonsai = os.environ['BONSAI_URL']
  auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
  host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')
  es_header = [{'host': host, 'port': 443, 'use_ssl': True, 'http_auth': (auth[0],auth[1])}]
  return Elasticsearch(es_header)

#clear_elastic()
upload_to_elastic()