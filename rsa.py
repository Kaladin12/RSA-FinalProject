import math, numpy
import fractions, re, string

def inverse_mod(a,m):
    a=a%m
    for i in range(0,m):
        if ((a*i)%m==1):
            return i
    return 1

def findPQ(N):
    primes = []
    for i in range(2,N-1,1):
        if N%i==0:
            primes.append(i)
    return primes

def findPhiOfN(primes):
    phi = (primes[0]-1)*(primes[1]-1)
    return phi

def findEncriptionKey(phi, N, clueASCII, plaintext):
    possibles = []
    for i in range(2, phi):
        possibles.append(i)
    e = 0
    newClue = []
    right=True
    for possible in possibles:
        if math.gcd(possible, phi)==1:
            for i in clueASCII:
                newClue.append((i**possible)%N)
            for i in newClue:
                if str(i) not in plaintext:
                    right=False
                    newClue=[]
                    break
                else:
                    right=True
            if right:
                e=possible
                break
    d = inverse_mod(e, phi)
    return [e,d]

def decipherText(plaintext, d, N):
    decipheredText=[]
    for letter in plaintext:
        decipheredText.append((int(letter)**d)%N)
    print(''.join(chr(i) for i in decipheredText))

text = numpy.loadtxt('mensaje.txt', delimiter=',', unpack=True, dtype=str)
words = text[0]
plainText = text[1]
plaintext = re.sub('['+string.punctuation+']', '', plainText).split() #obtenido de https://www.geeksforgeeks.org/python-extract-words-from-given-string/
clue = text[2]
clueASCII = [ord(char) for char in clue]
N = int(text[3])
#print(words, plainText, clue, N)
primes = findPQ(N)
phi = findPhiOfN(primes)
print(phi)
keys = findEncriptionKey(phi, N, clueASCII, plaintext)
decipherText(plaintext, keys[1], N)

