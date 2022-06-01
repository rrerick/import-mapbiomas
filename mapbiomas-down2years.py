"""
MapBiomas_Down2years.py


    Feito para baixar e poligonizar os ano de 1985 e 2020 
"""

import errno
import urllib.request
import requests
import json
import os
from functionsmapbiomas import CreateDir, Polygonized
import sys

# Connec to url
url = requests.get(
    "https://storage.googleapis.com/storage/v1/b/mapbiomas-public/o/?delimiter=/&prefix=brasil/collection-6/lclu/coverage/")

ulr_text = url.text
output_json = json.loads(ulr_text)


# Create apropriate directory and dowloading
path = CreateDir()

try:
    year = 1985
    count = 1

    while year <= 2020:
        name = output_json['items'][count]['name']

        if '2020' in name or '1985' in name:
            nome_arquivo = name.replace('/', '_')
            print(nome_arquivo)
            subDir = str(path) + '/' + str(year) + '/'

            try:
                os.mkdir(subDir)
                # caminho_arquivo=str(os.getcwd())+'/'+nome_arquivo
            except OSError as err:
                if err.errno == errno.EEXIST:
                    print("Sub-Directory Alredy Exists")

            file_path = subDir + nome_arquivo
            if os.path.isfile(file_path):
                print("file exists")
            else:
                print("file not exist, downloading...")
                mediaLink = output_json['items'][count]['mediaLink']
                file_path, _ = urllib.request.urlretrieve(mediaLink, file_path)
                print('OK')

            #Polygoniz .tif
            FileGpkgName = nome_arquivo.replace('.tif', '')
            print("Working in Polygoniz to GPKG")
            fileISok=subDir + "ok.txt"

            if os.path.isfile (fileISok):
                print("%s '\t' polygonized" %name)
                year += 1
                count += 1
            else:
                os.chdir(subDir)
                with open('ok.txt', "w") as verification:
                    print("working...")
                    Polygonized(file_path, FileGpkgName, subDir)
                    year += 1
                    count += 1

        else:
            year += 1
            count += 1
            continue

except Exception as err:
    sys.exit("An Error has occurred\nExiting")
