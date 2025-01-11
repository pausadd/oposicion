"""
No tiene porque ser el mejos a pesar del nombre
"""

from unidecode import unidecode
import unicodedata
import string
from sentence_transformers import SentenceTransformer, util
import datetime

def embedding_similarity(text1, text2):
    return 3
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight BERT model
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    return util.cos_sim(embeddings[0], embeddings[1]).item()

cedex = open(r'.\textos\cedex.txt' , encoding='UTF8' )
adif = open(r'.\textos\adif_noLineas.txt' , encoding='UTF8')
#cedex = open(r'.\textos\cedex_test.txt' , encoding='UTF8' )
#adif = open(r'.\textos\adif_noLineas_test.txt' , encoding='UTF8')

# readlines falla con acentos, hacer open()) con encoding
f1=cedex.readlines()
f2=adif.readlines()

#print output to file, buffer cada linea 
salida = open(r'.\textos\oposicion_oou.txt' , 'w', buffering=1, encoding='UTF8')
def miPrint(s):
    print( s )
    salida.write(s + '\n')

d1=-1 #cedex
d2=-1 #adif
# lista vacia
#for affinity in (embedding_similarity):
affinity = [[]]
for str1 in f1:
    d1 = d1 + 1
    print(str(datetime.datetime.now()) + "  Outer loop: " + str(d1))
    salida.write(str(datetime.datetime.now()) + "  Outer loop: " + str(d1) +"\n")
    for str2 in f2:
        d2 = d2 + 1 
        affinity[d1].append(embedding_similarity(str1 , str2))
        if str1 == str2:
            print(str1+ '\n' + str2)
            exit('H'*40 + 'IGUALES = IGUALES' + 'H'*40)
    affinity.append([])    
    d2 = -1


def matrix_to_ordered_list(matrix):
    # Create a list of tuples: (value, row, column)
    values_with_indices = [
        (matrix[i][j], i, j) for i in range(len(matrix)) for j in range(len(matrix[i]))
    ]
    # Sort the list by the first element of the tuple (the value) in descending order
    values_with_indices.sort(key=lambda x: x[0], reverse=True)
    return values_with_indices

# Get the ordered list in descending order
ordered_affinity = matrix_to_ordered_list(affinity)
for value, row, col in ordered_affinity:
    print(f"Value: {value}, Row: {row}, Column: {col}")

#exit() 

PCT=0.96
while True:
    pctstr=input("Numero de mejores marcas (int) " + 
                 "o porcentaje a superar (def 0.96)\n" +
                 "'c' limpia el ficheo de log en C:\\temp\\oposicion_out.txt\n" +
                 "'q' termina el programa:" )
    if pctstr == 'q': exit(0)
    elif pctstr == 'c':
        salida.close()
        salida = open(r'.\textos\oposicion_out.txt' , 'w', buffering=1, encoding='UTF8')
    elif pctstr == '': pctstr=PCT
    
    try:
        numEntries = int(pctstr)
        count = 1
        for value, row, col in ordered_affinity[:numEntries]:
            #print(f"Value: {value}, Row: {row}, Column: {col}")
            miPrint(f"{count} ---- Elemento en ({row}, {col}): {affinity[row][col]} \n" +
            f1[row] + f2[col])
            count += 1        
    except ValueError:
        pass
    
    try:
        pct=float(pctstr)
        # pct is ok, print results 
        #miPrint('-'*60)
        for i in range(len(affinity)):
            for j in range(len(affinity[i])):
                if affinity[i][j] >= pct:
                    miPrint(f"---- Elemento en ({i}, {j}): {affinity[i][j]}")
                    miPrint(f1[i])
                    miPrint(f2[j])            
        #print('-'*80)
    except ValueError as e:
        print(f"Intentalo de nuevo: {e}")

