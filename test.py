import requests,os
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
from string import Template
import pprint
import io

pp = pprint.PrettyPrinter(indent=4)
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'obd.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

#service.files().delete(fileId='0B4n1_ERzWhI7c3RhcnRlcl9maWxl').execute()

root_results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name, mimeType)",q="name contains 'Folder'").execute()
#,q="name contains 'Folder1'"
pp.pprint(root_results)
id_parent_folder = root_results['files'][0]['id']

nameFolder = 'Result_707876543'

result = service.files().list(pageSize=10,fields="nextPageToken, files(id, name, mimeType,webViewLink)",q=Template("name contains '$nameFolder'").safe_substitute(nameFolder=nameFolder)).execute()

if(not result['files']):
    print('create catalog')
    folder_id = id_parent_folder
    file_metadata = {
        'name': nameFolder,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id]
    }
    result = service.files().create(body=file_metadata, fields='id').execute()

id_folder_save = result['files'][0]['id']

tmpFolder='tmp/'
file_path = tmpFolder+'google.ico'
pp.pprint(result['files'][0]['webViewLink'])
url = 'http://google.com/favicon.ico'
r = requests.get(url, allow_redirects=True)
f = open(file_path, 'wb')
f.write(r.content)
f.close()
name = 'google.ico'
file_path = file_path
file_metadata = {'name': name,'parents': [id_folder_save]}
media = MediaFileUpload(file_path, resumable=True)
r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
if(r['id']):
    media = None
    os.remove(file_path)


'''
folder_id = root_results['files'][0]['id']

file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': [folder_id]
}
r = service.files().create(body=file_metadata, fields='id').execute()
pp.pprint(r)
'''