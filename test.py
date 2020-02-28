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

name_root_folder = 'Folder' 

root_results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name, mimeType)",q=Template("name contains '$name_root_folder'").safe_substitute(name_root_folder=name_root_folder)).execute()
#pp.pprint(root_results)
id_root_folder = root_results['files'][0]['id']

def save_to_folder(name_folder_save):
    result = service.files().list(pageSize=10,fields="nextPageToken, files(id, name, mimeType,webViewLink)",q=Template("name contains '$name_folder_save'").safe_substitute(name_folder_save=name_folder_save)).execute()
    if(not result['files']):
        #create catalog
        file_metadata = {
            'name': name_folder_save,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [id_root_folder]
        }
        result = service.files().create(body=file_metadata, fields='id').execute()
    # id каталога для сохранения
    id_folder_save = result['files'][0]['id']
    # ссылка на каталог
    web_link = result['files'][0]['webViewLink']

    # получим список файлов в каталоге GoogleDrive, что бы не делать лишней работы
    list_files = service.files().list(pageSize=1000,fields="nextPageToken, files(id, name, mimeType, parents)",q=Template("'$id_parents_folder' in parents").safe_substitute(id_parents_folder=id_folder_save)).execute()
    control_list_file = []
    for file in list_files['files']:
        control_list_file.append(file['name'])
    ################################################################################
    return
    tmpFolder='tmp/'
    file_path = tmpFolder+'google.ico'
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
    return web_link
#################################

f_save = 'Result_707876543'
save_to_folder(f_save)



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