import numpy as np
import pandas as pd
import json
from prepro import *
import build
from linecache import getline


def similitudCoseno(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def indicePalabra(palabra, objeto):
    l = 0
    r = objeto[1][1] - 1
    for l in range (0, r+1, 0):
        m = (l + r)//2
        lineaPrev = getline(objeto[1][0], m)
        if 0 != len(lineaPrev):
            lineaActual = json.loads(lineaPrev)
            first = list(lineaActual.keys())[0]
            if first == palabra:
                return lineaActual
            elif first < palabra:
                l = m + 1
            else:
                r = m - 1
        else:
            break
    return {palabra:{}}

def indiceBusqueda(palabra, file):
    lineaPrevia = []
    r = len(pd.read_json(file, lines = True)) - 1
    for l in range(0, r+1, 0):
        m = (l + r)//2
        lineaActual = json.loads(getline(file, m))
        first = list(lineaActual.keys())[0]
        if first == palabra:
            return lineaActual
        elif first < palabra:
            l = m + 1
        else:
            r = m - 1
        lineaPrevia = lineaActual
    return lineaPrevia

def puntaje(palabras, K, freq):
    cols = []
    for i in range(0, len(palabras), 1):
        for tweet in list(palabras[i][list(palabras[i].keys())[0]]["tweets"].keys()):
            if tweet not in cols:
                cols.append(tweet)
    idf  = {}
    data = {}
    for i in range(0, len(palabras), 1):
        first = list(palabras[i].keys())[0]
        idf[first]  = palabras[i][first]["idf"]
        data[first] = []
        for tweet in cols:
            if tweet not in palabras[i][first]["tweets"]:
                data[first].append(0)
            else:
                data[first].append(palabras[i][first]["tweets"][tweet]*idf[first])

def buscar(query, K):
    palabras = cleanText(query)
    freq     = build.countFrequency(palabras)
    resultPalabras = []
    listaAux = list(dict.fromkeys(palabras))
    for i in range(0, len(listaAux), 1):
        indPalabra = indicePalabra(listaAux[i], indiceBusqueda(listaAux[i], "ofile/ofile.json"))
        if {} != list(indPalabra.values())[0]:
            resultPalabras.append(indPalabra)
    return puntaje(resultPalabras, K, freq)