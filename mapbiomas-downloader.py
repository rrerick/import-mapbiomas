"""


1º) Descarregar as coberturas completas do Brasil de 2019 até 2020

Links de exemplo:
a) https://storage.googleapis.com/mapbiomas-public/brasil/collection-6/lclu/coverage/brasil_coverage_1985.tif
b) https://storage.googleapis.com/storage/v1/b/mapbiomas-public/o/?delimiter=/&prefix=brasil/collection-6/lclu/coverage/


VERSÃO :

    1 - Pegar o arquivo JSON (b) e conferir dos anos 2019 - 2020



"""
import errno
import urllib.request
import requests
import json
import os
import sys
from functions_MapBiomas_Downloader import CreateDir, Polygonized



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
        fileISok = subDir + "ok.txt"
        if os.path.isfile(fileISok):
            print("%s |\t| polygonized" % name)
            year += 1
            count += 1
        else:
            os.chdir(subDir)
            print("working...")
            Polygonized(file_path, FileGpkgName, subDir)
            year += 1
            count += 1

except Exception as err:
    print(err, '\n')
    err = str(err)
    if 'TIFFReadEncodedTile() failed' in err:
        print("The .tif file has an error \t It will be delete")
        os.remove(file_path)
        sys.exit("TRY AGAIN")
    else:
        sys.exit("An Error has occurred\nExiting")