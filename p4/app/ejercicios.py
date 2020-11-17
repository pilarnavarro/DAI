#Ejercicio2
def ordena(matriz,algorithm):
    if algorithm=="burbuja":
        return "La matriz ordenada según el algoritmo de burbuja es " + burbuja(matriz)
    elif algorithm=="merge_sort" or algorithm=="merge":
        return "La matriz ordenada según el algoritmo de mezcla es " + mergeSort(matriz)
    else:
        return("No hay ninguna implementación para el algoritmo solicitado.")

def burbuja(matriz):
    for iter in range(len(matriz)):
        for j in range(0,len(matriz)-1):
            if matriz[j]>matriz[j+1]:
                matriz[j], matriz[j+1] = matriz[j+1], matriz[j]
    return str(matriz)

def mergeSort(matriz):
    if len(matriz)>1:
        mid = len(matriz)//2
        lefthalf = matriz[:mid]
        righthalf = matriz[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i,j,k=0,0,0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] <= righthalf[j]:
                matriz[k]=lefthalf[i]
                i=i+1
            else:
                matriz[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            matriz[k]=lefthalf[i]
            i=i+1; k=k+1

        while j < len(righthalf):
            matriz[k]=righthalf[j]
            j=j+1; k=k+1
    return str(matriz)

#-------------------------------------------------------------------
#Ejercicio3
import math

def criba(number):
    primes = []
    for i in range(2,number+1):
        primes.append(i)
    i = 2
    while(i <= int(math.sqrt(number))):
        if i in primes:
            for j in range(i*2, number+1, i):
                if j in primes:
                    primes.remove(j)
        i = i+1
    return str(primes)


#Ejercicio4
def fibonacci(number):
    result=fib(number)
    return str(result)

def fib(n):
    if n < 2:
        return n
    else:
        # fn = fn-1 + fn-2
        return fib(n-1) + fib(n-2)

#Ejercicio5

#Si la cadena introducida es vacía se genera una aleatoriamente
def balanceado(cadena):

    if cadena==None:
        cadena = [random.choice('[]') for _ in range(random.randint(1, 10))]

    pila = []
    balanceo = True
    i = 0
    while i < len(cadena) and balanceo:
        simbolo = cadena[i]
        if simbolo == "[":
            pila.append(simbolo)
        else:
            if len(pila)==0:
                balanceo= False
            else:
                pila.pop()
        i = i + 1

    if len(pila)==0 and balanceo:
        return True
    else:
        return False

#Ejercicio6
import re

'''
    Si el índice es 1 estamos en el primero de los casos pedidos
    en el ejercicio (palabra seguida de espacio y letra mayúscula).
    Si index=2 entonces buscamos direcciones de correo electrónico válidas
    Si index=3 buscamos números de tarjetas de crédito
'''
def regex(index,cadena):
    if index==1:
        match=re.findall(r'\b[a-zA-Z]+\s[A-Z]{1}\b',cadena)
    elif index==2:
        match=re.findall(r'\b[\w%+.-]+@[\w.-]+\.[a-z]{2,}\b',cadena)
    elif index==3:
        #match=re.findall(r'\b(\d{4}[\s-]){3}\d{4}\b',cadena)
        match=re.findall(r'\b\d{4}[-\s]\d{4}[-\s]\d{4}[-\s]\d{4}\b',cadena)
    else:
        return "Índice introducido incorrecto"
    
    if len(match)==0:
        return "No se ha encontrado ninguna subcadena con el patrón adecuado"
    return str(match)


