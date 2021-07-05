from json import decoder
from os.path import isfile, join
import pandas as pd
import os
import collections
import json
import prepro
import math
import heapq

BLOCKSIZE = 3000

def countFrequency(arr):
    return collections.Counter(arr)

def getFiles(files, start, extension):
    lista = []
    for base, dirs, files in os.walk(files):
        for file in files:
            fich = join(base, file)
            if fich.endswith(extension):
                if start in fich:
                    lista.append(fich)
    return lista

#USAR BLOQUES DE INFORMACION DE TAMAÑO BLOCKSIZE
def createBlock(file):
    with open(file, encoding="utf8") as infile:
        aux = json.load(infile)
        for i in range(0, len(aux), BLOCKSIZE):
            with open('./block/'+ (os.path.splitext(os.path.basename(file))[0])+"-"+str(i//BLOCKSIZE)+".json", 'w') as outputFile:
                json.dump(aux[i:i+BLOCKSIZE], outputFile)
       

def blockIndex(file):
    diccionario={}
    dataFrame = pd.read_json(file)
    nombreArchivo=(os.path.splitext(os.path.basename(file))[0])
    for cont, row in dataFrame.iterrows():
        data = prepro.cleanText(row.values[2])
        frecuencia = countFrequency(data)
        for key, val in frecuencia.items():
            diccionarioAux = {}
            diccionarioAux["tf"]    = val
            diccionarioAux["tweet"] = row.values[0]
            if key in diccionario:
                diccionario[key].append(diccionarioAux)
            else:
                diccionario[key] = [diccionarioAux]
    if not os.path.isfile('./ofile/'+nombreArchivo+".json"):
        out = open('./ofile/'+nombreArchivo+".json", 'w')
    else:
        out = open('./ofile/'+nombreArchivo+".json", 'a')
    out.reconfigure(encoding='utf-8')
    sortedData = sorted(diccionario.items())
    result = ""
    for i, data in enumerate(sortedData):
        result += json.dumps(data, ensure_ascii = False)
        if i < len(sortedData)-1:
            result += "\n"
    print(result, file=out)

def createBlocks():
    files = getFiles("./data_elecciones", "tweets", ".json")
    for file in files:
        createBlock(file) 

def createBlockIndex():
    blocks = getFiles("./block/", "tweets", ".json")
    for file in blocks:
        blockIndex(file)