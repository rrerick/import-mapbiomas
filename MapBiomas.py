"""


1º) Descarregar as coberturas completas do Brasil de 2019 até 2020

Links de exemplo:
a) https://storage.googleapis.com/mapbiomas-public/brasil/collection-6/lclu/coverage/brasil_coverage_1985.tif
b) https://storage.googleapis.com/storage/v1/b/mapbiomas-public/o/?delimiter=/&prefix=brasil/collection-6/lclu/coverage/


VERSÃO :

    1 - Pegar o arquivo JSON (b) e conferir dos anos 2019 - 2020



"""
import errno
import requests
import json
import os
import sys
from MapBiomas_function import CreateDir, Polygonized, YearsInMapBiomas, download
from multiprocessing import Process


# Connec to url
url = requests.get(
    "https://storage.googleapis.com/storage/v1/b/mapbiomas-public/o/?delimiter=/&prefix=brasil/collection-6/lclu/coverage/")

ulr_text = url.text
output_json = json.loads(ulr_text)


# Create apropriate directory and dowloading
path = CreateDir()


def main():
    with open('years.txt', 'r') as arquivo:
        count_loop = 0
        requests_years = []
        infos = {}
        file_names = []

        for year in arquivo.readlines():
            print(year)
            time = year.replace('\n', '')

            correct_year = YearsInMapBiomas(time)
            print(correct_year, '\n')

            if correct_year == 'not':
                print("Any file in this year: %s" % (time))
                continue
            else:
                requests_years.append(correct_year)
                name = output_json['items'][correct_year]['name']
                print(name)
                file_name = name.replace('/', '_')
                file_names.append(file_name)
                print(file_name)

                subDir = str(path) + '/' + str(year) + '/'

                file_path = subDir + file_name
                count_loop += 1
                infos[correct_year] = [file_path, subDir, name]

                try:
                    os.mkdir(subDir)
                except OSError as err:
                    if err.errno == errno.EEXIST:
                        print("Sub-Directory Alredy Exists")

                if os.path.isfile(file_path):
                    print("file exists")
                    continue
                else:
                    print("file not exist, downloading...")
                    continue
    try:
        number_of_process = count_loop
        print("\nnumber of processes will be %i" % (number_of_process))

        processes = []
        for proc in range(number_of_process):

            if os.path.isfile(infos[requests_years[proc]][0]):
                print("file exists\n")
                continue

            else:
                print("Downloading %s" %(requests_years[proc]))
                p1 = Process(target=download, args=(
                    output_json, requests_years[proc], infos[requests_years[proc]][0]))
                processes.append(p1)
                p1.start()

        for p in processes:
            p.join()

        # Polygoniz
        print("Working in Polygoniz to GPKG")

        GPKGnames = []
        for pol in range(number_of_process):
            File1 = str(file_names[proc])
            FileGpkgName = File1.replace('.tif', '')
            GPKGnames.append(FileGpkgName)

        processes2 = []
        for pol in range(number_of_process):
            fileISok = infos[requests_years[pol]][1] + "ok.txt"
            print(fileISok)
            if os.path.isfile(fileISok):
                print("%s |\t| polygonized" % (infos[requests_years[pol]][2]))

            else:
                os.chdir(infos[requests_years[pol]][1])
                print("working...")

                p3=Process(target=Polygonized, args=(infos[requests_years[pol]][0], GPKGnames[pol], infos[requests_years[pol]][1]))
                processes2.append(p3)
                p3.start()


        for p1 in processes2:
            p1.join()

    except Exception as err:
        print(err, '\n')
        err = str(err)
        if 'TIFFReadEncodedTile() failed' in err:
            print("The .tif file has an error \t It will be delete")
            print("Trying Again...\n")
            os.remove(file_path)
            main()
        else:
            print(err)
            sys.exit("An Error Has Occurred\nExiting")


if __name__ == "__main__":
    main()
