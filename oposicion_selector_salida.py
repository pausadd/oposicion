"""
Incompleto idea separar calculo afinidades y su presentacion
"""

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
#for value, row, col in ordered_affinity: 
#   print(f"Value: {value}, Row: {row}, Column: {col}")

#exit() 

def selector_salidas(f1, f2, affinity, logfile):
    """ f1,f2 referencia a losficheros con los temas
        afinity la matriz de afinidades
        logfile esta por ver"""
    PCT=0.96
    while True:
        pctstr=input("int Numero de mejores relaciones entre temas de los dos temarios\n " + 
                    "0.xx porcentaje de afinidad a superar (def 0.96)\n" +
                    "'c' limpia el ficheo de log en C:\\temp\\oposicion_out_jaccard.txt\n" +
                    "t1xx saca los 20 temas del segundo temario mejor relacionados con el tema xx del primero\n" +
                    "t2xx hace lo mismo con los temas del segundo\n" + 
                    "'q' termina el programa:" )
        if pctstr == 'q': exit(0)
        elif pctstr == 'c':
            salida.close()
            salida = open(r'C:\temp\oposicion_out_jaccard.txt' , 'w', buffering=1, encoding='UTF8')
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

