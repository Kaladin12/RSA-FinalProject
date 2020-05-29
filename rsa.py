import math, numpy
import fractions, re, string

def inverseMod(a,m): #reciclado de la practica del Teorema Chino del Residuo.
    a=a%m
    for i in range(0,m):
        if ((a*i)%m==1):
            return i
    return 1

def findPQ(N): #encuentra P y Q para determinada N
    primes = []
    for i in range(2,N-1,1):
        if N%i==0: #Como N solo tiene dos factores, basta con buscar que numerso generan modulo 0 con N
            primes.append(i)
    return primes #tanto P como Q

def findPhiOfN(primes):
    phi = (primes[0]-1)*(primes[1]-1) #Phi(N)=(P-1)(Q-1)
    return phi

def coprimes(phi):
    factors = []
    for k in range(2, phi): #Todos los enteros mayores a 2 y menores a Phi(N)
        if phi%k==0: #Si el entero tiene residuo 0, entonces verificar si es primo
            count=0
            for j in range(1,k): #desde 1 hasta el entero
                if k%j==0: #si tiene un factor en el rango
                    count+=1
            if count==1: #dado que los primos solo tienen una factor diferente de ellos mismos, entonces count debe ser 1 si k es primo
                factors.append(k)
    coprime=[]
    isCoprime = False
    for possibleCoprime in range(2, phi): #posibles coprimos entre 2 y phi
        for factor in factors:
            if possibleCoprime%factor==0: #busca si el posible coprimo tiene residuo 0 con algun factor de Phi
                isCoprime=False         #si es residuo 0 entonces no es coprimo porque comparte factor
                break
            else: #si no comparte factores entonces sigue siendo posible
                isCoprime=True
        if isCoprime==True: #si isCoprime es verdader, entonces el numero no posee factores comunes con Phi(N), por lo tanto es coprimo.
            coprime.append(possibleCoprime) #se agrega a la lista de posibles coprimos.
    return coprime

def findEncriptionKey(phi, N, clueASCII, plaintext):
    coprime = coprimes(phi)#manda a llamar a todos los coprimos con Phi(N)
    e = 0
    newClue = []
    right=True
    for possible in coprime:
        for i in clueASCII: 
            newClue.append((i**possible)%N) #eleva cada cifra del texto pista a la potencia del posible coprimo y obtiene su residuo modulo N
        for i in newClue:
            if str(i) not in plaintext: #si existe por lo menos uno de los resultados elevados a la potencia possible, entones no es la llave que buscamos
                right=False
                newClue=[]
                break
            else: #si existe en el texto cifrado entonces es verdadero
                right=True
        if right: #si right es verdadero, entonces todas las letras del texto pista estan en el texto cifrado, por lo tanto la llave es correcta.
            e=possible
            break
    d = inverseMod(e, phi) #se obtiene la llave privada a partir de la llave publica y phi
    return [e,d]

def decipherText(plaintext, d, N):
    decipheredText=[]
    for letter in plaintext:
        decipheredText.append((int(letter)**d)%N) #para cada letra en el texto cifrado se eleva a la potencia de la llave privada y se obtiene su residuo modulo N
    print(''.join(chr(i) for i in decipheredText))#descifrado convertido de ascii a texto

text = numpy.loadtxt('mensaje.txt', delimiter=',', unpack=True, dtype=str)
words = text[0] #cuantas palabras tiene el texto
plainText = text[1] #texto cifrado
plaintext = re.sub('['+string.punctuation+']', '', plainText).split() #obtenido de https://www.geeksforgeeks.org/python-extract-words-from-given-string/
clue = text[2] #pista
clueASCII = [ord(char) for char in clue] #funcion para convertir la pista de texto a ascii consultada en https://stackoverflow.com/questions/8452961/convert-string-to-ascii-value-python
N = int(text[3])#N otorgada en el txt
primes = findPQ(N) #buscar P y Q en base a N
phi = findPhiOfN(primes) #enuentra phi en base a los primos P y Q
print('Phi(N): ', phi)
keys = findEncriptionKey(phi, N, clueASCII, plaintext) #encuentra las llaves e y d.
decipherText(plaintext, keys[1], N) #decifra el texto en base a las llaves
print('Llave publica: ', keys[0], 'Llave privada: ', keys[1])

