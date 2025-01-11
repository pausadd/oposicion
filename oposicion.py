# Version basica

from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import Levenshtein
from unidecode import unidecode

import unicodedata
import string

def string_similarity(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

cedex = open(r'C:\temp\cedex.txt' , encoding='UTF8' )
adif = open(r'C:\temp\adif_noLineas.txt' , encoding='UTF8')
#adif = open()

# readlines falla con acentos, hacer open()) con encoding
f1=cedex.readlines()
f2=adif.readlines()

#"""
d1=-1
d2=-1
# lista vacia
affinitySeq = [[]]
affinityFuzz = [[]]
affinityLev = [[]]
#print(affinitySeq)
#print(len(f1) , len(f2))
for str1 in f1:
    d1 = d1 + 1
    for str2 in f2:
        d2 = d2 + 1 
        #print(d1,d2)
        affinitySeq[d1].append(string_similarity(str1 , str2))
        #print(affinitySeq)
        affinityFuzz[d1].append(fuzz.ratio(str1 , str2)/100)
        affinityLev[d1].append(Levenshtein.ratio(str1 , str2))
        if str1 == str2:
            print(str1+ '\n' + str2)
            exit('H'*80)
    affinitySeq.append([])    
    affinityFuzz.append([])    
    affinityLev.append([])    
    d2 = -1
print(len(affinitySeq))
if affinityLev == affinityFuzz: print("son iguales")

# print results 
for method in (affinitySeq,affinityFuzz,affinityLev):
    for i in range(len(method)):
        for j in range(len(method[i])):
            if method[i][j] >= 0.7:
                print(f"Elemento en ({i}, {j}): {method[i][j]}")
                print(f1[i-1])
                print(f2[j-1])

    print('-'*80)
#"""


def eliminar_signos_puntuacion(texto):
    # Crea una tabla de traducción para eliminar signos de puntuación
    tabla_traduccion = str.maketrans('', '', string.punctuation)
    texto_sin_puntuacion = texto.translate(tabla_traduccion)
    return texto_sin_puntuacion

def calcMiAffinity(s1, s2):
    affinity=0
    sp1 = s1.split()
    sp2 = s2.split()
    
    for i in range(len(sp1)):
        sp1[i] = eliminar_signos_puntuacion(sp1[i])
        # no contar y,de,el ... tren si
        if len(sp1[i]) >= 4:
            for j in range(len(sp2)):
                if sp1[i] == sp2[j]: affinity += 1
    return(affinity)

d1=-1   #cedex
d2=-1   #adif
# lista vacia
miAffinity = [[]]
for str1 in f1:
    d1 = d1 + 1
    for str2 in f2:
        d2 = d2 + 1 
        miAffinity[d1].append(calcMiAffinity(str1 , str2))
        if str1 == str2:
            print(str1+ '\n' + str2)
            exit('H'*80)
    miAffinity.append([])    
    d2 = -1

for i in range(len(miAffinity)):
    for j in range(len(miAffinity[i])):
        # filtrar por numero de palabras iguales
        if miAffinity[i][j] >= 5:
            print(f"Elemento en ({i}, {j}): {miAffinity[i][j]}")
            print(f1[i])
            print(f2[j])