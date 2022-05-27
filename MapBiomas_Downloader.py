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
from time import sleep
from functions_MapBiomas_Downloader import CreateDir, Polygonized
from tqdm import tqdm


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
        with tqdm(total=100) as progressbar:
            name = output_json['items'][count]['name']
            nome_arquivo = name.replace('/', '_')
            print(nome_arquivo)

            subDir = str(path) + '/' + str(year) + '/'

            progressbar.update(10)

            try:
                os.mkdir(subDir)
                # caminho_arquivo=str(os.getcwd())+'/'+nome_arquivo
            except OSError as err:
                if err.errno == errno.EEXIST:
                    print("Sub-Directory Alredy Exists")

            progressbar.update(40)

            file_path = subDir + nome_arquivo
            if os.path.isfile(file_path):
                print("file exists")
                sleep(3)

            else:
                print("file not exist, downloadig...")
                mediaLink = output_json['items'][count]['mediaLink']
                file_path, _ = urllib.request.urlretrieve(mediaLink, file_path)
                sleep(3)
                print('OK')

            progressbar.update(30)

            #Polygoniz .tif
            FileGpkgName = nome_arquivo.replace('.tif', '')
            print("Working in Polygoniz to GPKG")
            Polygonized(file_path, FileGpkgName, subDir)
            progressbar.update(20)
            sleep(2)
            year += 1
            count += 1


except IndexError as error:
    print('finished')
