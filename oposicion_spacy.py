
from unidecode import unidecode
import unicodedata
import datetime
import string

# spaCy is a library for advanced Natural Language Processing
import spacy

# Load Models: "python -m spacy download es_core_news_sm" for this  to work
# con _md no termina, muere sin error, cuanto dura dependiendo del tamaño de los ficheros, _sm va ok , _lg mal
# more details on models: https://spacy.io/models
# for spacy model, Load the SpaCy model
nlp = spacy.load('es_core_news_sm')

cedex = open(r'.\textos\cedex.txt' , encoding='UTF8' )
adif = open(r'.\textos\adif_noLineas.txt' , encoding='UTF8')
#cedex = open(r'.\textos\cedex_test.txt' , encoding='UTF8' )
#adif = open(r'.\textos\adif_noLineas_test.txt' , encoding='UTF8')

# readlines falla con acentos, hacer open()) con encoding
f1=cedex.readlines()
f2=adif.readlines()

#print output to file, buffer cada linea 
salida = open(r'.\textos\oposicion_out_spacy.txt' , 'w', buffering=1, encoding='UTF8')
def miPrint(s):
    print( s )
    salida.write(s + '\n')

def eliminar_signos_puntuacion(texto):
    # Crea una tabla de traducción para eliminar signos de puntuación
    tabla_traduccion = str.maketrans('', '', string.punctuation)
    texto_sin_puntuacion = texto.translate(tabla_traduccion)
    return texto_sin_puntuacion

d1=-1 #cedex
d2=-1 #adif
# lista vacia
#for affinity in (embedding_similarity):
affinity = [[]]
for str1 in f1:
    d1 = d1 + 1
    miPrint(str(datetime.datetime.now()) + "  Outer loop: " + str(d1))
    for str2 in f2:
        d2 = d2 + 1 
        str1 = eliminar_signos_puntuacion(str1)
        str2 = eliminar_signos_puntuacion(str2)
        #miPrint(str(datetime.datetime.now()) + "  Outer loop: " + str(d1) + "\t  Inner loop: " + str(d2))
        # aqui disponemos de los strings
        # proceso para spacy
        pstr1 = nlp(str1)
        pstr2 = nlp(str2)
        affinity[d1].append(pstr1.similarity(pstr2))
        if str1 == str2:
            miPrint('H'*20 + '  IGUALES = IGUALES  ' + 'H'*20)
            miPrint(' Contadores d1 y d2: ' + str(d1) + ' ' + str(d2) )
            miPrint(str1+ '\n' + str2)
            miPrint('H'*20 + 'H'*20)
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

PCT=0.96
while True:
    pctstr=input("int Numero de mejores relaciones entre temas de los dos temarios\n " + 
                 "0.xx porcentaje de afinidad a superar (def 0.96)\n" +
                 "'c' limpia el ficheo de log en C:\\temp\\oposicion_out_spacy.txt\n" +
                 "t1xx saca los 20 temas del segundo temario mejor relacionados con el tema xx del primero\n" +
                 "t2xx hace lo mismo con los temas del segundo\n" + 
                 "'q' termina el programa:" )
    if pctstr == 'q': exit(0)
    elif pctstr == 'c':
        salida.close()
        salida = open(r'.\textos\oposicion_out_spacy.txt' , 'w', buffering=1, encoding='UTF8')
    elif pctstr == '': pctstr=PCT
    elif pctstr[0:2] == 't1':
        # relacionadas con un tema concreto del primer fichero
        try:
            seleccion = int(pctstr[2:])
            numEntries = 10
            count = 1
            for value, row, col in ordered_affinity:
                #print(f"Value: {value}, Row: {row}, Column: {col}")
                if row == seleccion - 1:
                    miPrint(f"{count} ---- Elemento en ({row}, {col}): {affinity[row][col]} \n" 
                            + f1[row] + f2[col])
                    count += 1
                if count == numEntries +1 : break        
        except ValueError:
            pass
    elif pctstr[0:2] == 't2':
        # relacionadas con un tema concreto del segundo fichero
        try:
            seleccion = int(pctstr[2:])
            numEntries = 20
            count = 1
            for value, row, col in ordered_affinity:
                #print(f"Value: {value}, Row: {row}, Column: {col}")
                if row == seleccion - 1:
                    miPrint(f"{count} ---- Elemento en ({row}, {col}): {affinity[row][col]} \n" 
                            + f1[row] + f2[col])
                    count += 1
                if count == numEntries +1 : break        
        except ValueError:
            pass

    # entrada entero
    try:
        numEntries = int(pctstr)
        count = 1
        for value, row, col in ordered_affinity[:numEntries]:
            #print(f"Value: {value}, Row: {row}, Column: {col}")
            miPrint(f"{count} ---- Elemento en ({row}, {col}): {affinity[row][col]} \n" 
                    + f1[row] + f2[col])
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
