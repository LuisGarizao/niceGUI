import csv

#esta funcion recibe un entero positivo n y devuelve los primeros n numeros primos
def nPrimos(n):
    lista_primos=[] #aqui se almacenará la lista de primos
    num_actual=2 #empieza en 2 ya que 2 es el primer numero primo
    cont=0 #contador de divisores

    while len(lista_primos)<n:
        # este ciclo va desde el 1 hasta el numero actual+1
        # y el numero actual aumenta en cada iteracion del while

        # 2 es el primer primo asi que se agrega directamente
        if num_actual==2:
            lista_primos.append(num_actual)
        #si el numero es impar se evalua si este es primo
        if (num_actual%2!=0):
            # este ciclo va desde 1 hasta el 'numero_actual+1' con un salto de 2
            # esto para ignorar los indices pares ya que estos
            # no nos darian divisiones exactas
            for i in range(1 ,num_actual+1,2):
                #si el numero actual es divisible por el indice se suma 1 al contador
                if num_actual%i==0:
                    cont+=1
            
            # los primos solo son divisibles por 1 y ellos mismos
            # asi que si el numero es primo, el contador es 2
            if cont==2:
                # el numero se agrega a la lista
                lista_primos.append(num_actual)
            # reinicio del contador para la siguiente iteracion del while
            cont=0
        # aumento del contador el numero actual
        num_actual+=1

    return lista_primos

# esta funcion retorna los factores primos de un entero positivo
def factPrimos(num):
    listaPrimos = nPrimos(30) #lista de los 30 primeros numeros primos
    p = 0 #indice de la lista de primos
    fact = [] #lista de factores primos inicial
    factores = [] #lista de factores primos 'formateada'

    #obtención de los factores primos
    #mientras el numero a descomponer sea distinto de 1
    while num!=1:   
        try:
            # se comprueba si cada primo de la lista lo divide de forma exacta
            if num%listaPrimos[p]==0:
                # se divide el numero en dicho primo
                num/=listaPrimos[p]
                # y el numero primo se agrega a una lista
                fact.append(listaPrimos[p])
            # si el primo evaluado no cumple la condicion se pasa al siguiente de la lista
            else:
                p+=1
        # si la lista de primos no es suficiente se pide una lista mas larga
        except IndexError:
            listaPrimos=nPrimos(round(len(listaPrimos)*1.5))
    
    # pasando la lista de primos a un formato mas simple
    # usando la lista de factores primos previamente calculada
    for n in fact:
        # por cada elemento de la lista se crea una tupla 
        # de 2 elementos: el propio numero y su total de apariciones
        # esta tupla representa la notación de n^m de los factores primos
        f = (n, fact.count(n))
        #se comprueba si la tupla ya esta en la lista 'factores' y si no es el caso se agrega
        if f not in factores:
            factores.append(f)

    return factores

# funcion que retorna el minimo comun multiplo de una lista de numeros
def MCM(nums:list):

    factores=[] #lista que guarda los factores primos de los numeros recibidos
    # almacenando las listas de factores primos
    for num in nums:
        factores.append(factPrimos(num))

    # en esta lista se guardan los factores primos de mayor exponente (representados en tuplas)
    lista_factores=[] 
    try:
        # a traves de ciclos se manejan los indices para acceder a las tuplas 
        # que representan los factores y ponerlos en una lista ordenada
        for i in range(len(factores)):
            for j in range(len(factores[i])):
                factor=factores[i][j]
                #si el factor ya esta en la nueva lista no se agrega de nuevo
                if factor not in lista_factores:
                    lista_factores.append(factor) 
        # ordenando la lista 
        lista_factores.sort()

        # manipulación de la lista para que esta conserve unicamente los factores
        # de mayor exponente
        for i in range(len(lista_factores)):
            try:
                # si la base (indice 0) en la tupla actual es igual
                # a la de la siguiente, la actual se elimina ya que 
                # la siguiente tiene exponente mayor 
                if lista_factores[i][0] == lista_factores[i+1][0]:
                    lista_factores.pop(i)
            except IndexError:
                pass
    finally:
        # calculo del mcm multiplicando a los factores primos resultantes
        mcm=1
        for factor in lista_factores:
            mcm*=factor[0]**factor[1]
    return mcm

# funcion que retorna una lista de 10 posibles multiplicadores
def selectMult(m):
    # Guardamos las bases de los factores primos de m en una lista
    fP=factPrimos(m)
    P_i=[]
    for f in fP:
        P_i.append(f[0])

    # si m es divisible entre 4 se añade el 4 a la lista
    if 4 % m:
        P_i.append(4)
        
    # se calculan 10 valores posibles de a y se guardan en la lista 'aPosibles'
    aPosibles = []
    for i in range(10):
        a = 1 + MCM(P_i)*i
        aPosibles.append(a)
    return aPosibles

# funcion que retorna una lista de los posibles valores de C
def selectConst(m):
    # factores primos de m
    fP=factPrimos(m)
    P_i=[x[0] for x in fP] #lista de las bases
    e_i=[x[1]-1 for x in fP] # lista de los exponentes-1

    #calculo del euler(m) 
    euler_m=1
    for i in range(len(fP)):
        euler_m*=(P_i[i]**e_i[i])*(P_i[i]-1)
    
    #se obtiene una lista de euler numeros primos + la cantidad de factores primos de m
    cPosibles=nPrimos(euler_m+len(fP))
    #removemos los factores primos de m de la lista
    for num in P_i:
        cPosibles.remove(num)

    return cPosibles

# funcion del GLC
def glc(a,x0,c,m):
    xn=x0
    result= [] #en esta lista se guardan los resultados de cada iteración
    #
    for i in range(m):
        numero = (a*xn+c)%m # Xn+1
        uniform = numero/m # numero uniforme
        cociente,residuo = divmod((a*xn+c),m) #cociente y residuo de (𝑎𝑋𝑛+𝑐)/m
        xn1 = f"{cociente}+{numero}/{(m)}" #(𝑎𝑋𝑛+𝑐) 𝑚𝑜𝑑 m
        result.append([i,xn,xn1,numero,uniform]) #i:numero de iteración
        xn=numero
        # si el numero generado es igual a la semilla la funcion termina de inmediato
        if numero == x0:
            break
    return result


if __name__=="__main__":
    #solicitando semilla y m
    while True:
        try:
            x0=int(input("Ingrse el valor de la semilla: "))
            m=int(input("Ingrese m: "))# m>x0
            if not m>x0:
                raise Exception("La semilla debe ser menor que m.")
            else:
                break
        except Exception as E:
            print(f"algo salio mal [{E}]. reintente")

    # obteniendo las opciones para a y c
    list_A=selectMult(m)
    list_C=selectConst(m)
    print(f'Posibles valores de a:\n{list_A}\n\nPosibles valores de c:\n{list_C}\n')

    #solicitando multiplicador y constante aditiva
    while True:
        try:
            a=int(input("Seleccione un valor de a: "))
            c=int(input("Seleccione un valor de c: "))
            if not (a in list_A) and (c in list_C):
                raise Exception("un Valor no está en la lista")
            else:
                break
        except Exception as E:
            print(f"algo salio mal [{E}]. reintente")

    #ejecución
    resultado=glc(a,x0,c,m)
    with open('tabla.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(resultado)
    print("resultados generados con exito")
    # for i in range(len(resultado)):
    #     print(resultado[i])


