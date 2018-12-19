"""
This program implements the Enhanced RSA algorithm for cryptography.
It randomly selects four prime numbers from a set of prime numbers (txt file of prime numbers) and 
uses them to produce the public and private keys. Using the keys, it can 
either encrypt or decrypt messages.
"""

import random

def gcd(a, b):
    """
    Performs the Euclidean algorithm and returns the gcd of a and b
    """
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)


def xgcd(a, b):
    """
    Performs the extended Euclidean algorithm
    Returns the gcd, coefficient of a, and coefficient of b
    """
    x, old_x = 0, 1
    y, old_y = 1, 0

    while (b != 0):
        quotient = a // b             #divide with integral result
        a, b = b, a - quotient * b    
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y

    return a, old_x, old_y

def chooseE(totient):
    """
    Chooses a random number, 1 < e < totient, and checks whether or not it is 
    coprime with the totient, that is, gcd(e, totient) = 1
    """
    while (True):
        e = random.randrange(2, totient)

        if (gcd(e, totient) == 1):
            return e

def knnalgo(message,sprime2,prime3,prime4):
    #applies knn algorithm to find r1 

    randx = random.randint(100, 500)

    
    fo = open('primes-to-100k.txt', 'r')         # open the stored txt file of prime numbers in a python list
    lines = fo.read().splitlines()
    fo.close()

    
    prime1 = int(lines[randx])                   # store the changed prime number in this variable


    
    l = prime1 * prime2 * prime3 * prime4        # compute l, totient, j again
    totient = (prime1 - 1) * (prime2 - 1) * (prime3 - 1) * (prime4 - 1)
    j = chooseE(totient)

    
    
    gcd1, x, y = xgcd(j, totient)                # compute k, 1 < k < totient such that jk = 1 (mod totient)
                                                 # j and k are inverses (mod totient)
     
    if (x < 0):                                  # make sure k is positive
        k = x + totient
    else:
        k = x
    

        ascii_val = []
        r1 = []

        for i in range(0, len(message)):         # stores the ascii values of individual character
                ascii_val.append(ord(message[i]))

        for i in range(0,len(message)):          #fastexponentiation
            t2 = iterative(ascii_val[i],k,l)
            r1.append(t2)

        return r1 


def chooseKeys():
    """
    Selects four random prime numbers from a list of prime numbers which has 
    values that go up to 100k. It creates a text file and stores the two 
    numbers there where they can be used later. Using the prime numbers, 
    it also computes and stores the public and private keys in two separate 
    files.
    """

     
    
    rand1 = random.randint(100, 500)                # choose four random numbers within the range of lines where
    rand2 = random.randint(100, 500)                # the prime numbers are not too small and not too big
    rand3 = random.randint(100, 500)
    rand4 = random.randint(100, 500)

    
    


   
    fo = open('primes-to-100k.txt', 'r')            # store the txt file of prime numbers in a python list
    lines = fo.read().splitlines()
    fo.close()

    
    prime1 = int(lines[rand1])                      # store our prime numbers in these variables
    prime2 = int(lines[rand2])
    prime3 = int(lines[rand3])
    prime4 = int(lines[rand4])


    
    l = prime1 * prime2 * prime3 * prime4           # compute l, totient, j
    totient = (prime1 - 1) * (prime2 - 1) * (prime3 - 1) * (prime4 - 1)
    j = chooseE(totient)


    
    
    gcd1, x, y = xgcd(j, totient)                   # compute k, 1 < k < totient such that jk = 1 (mod totient)
                                                    # j and k are inverses (mod totient)
     
    if (x < 0):
        k = x + totient                             # make sure k is positive
    else:
        k = x  

    
    
    n = random.randint(100,300)                     # write the public key:j and n to a file
    o = random.randint(100,300)
    
    f_public = open('public_keys.txt', 'w')
    f_public.write(str(l) + '\n')
    f_public.write(str(j) + '\n')
    f_public.write(str(n) + '\n')
    f_public.write(str(o) + '\n')
    f_public.write(str(prime1) + '\n')
    f_public.write(str(prime2) + '\n')
    f_public.write(str(prime3) + '\n')
    f_public.write(str(prime4) + '\n')
    f_public.close()

    f_private = open('private_keys.txt', 'w')       # write the private keys:k and n to a file
    f_private.write(str(l) + '\n')
    f_private.write(str(k) + '\n')
    f_private.write(str(n) + '\n')
    f_private.write(str(o) + '\n')
    f_private.write(str(prime1) + '\n')
    f_private.write(str(prime2) + '\n')
    f_private.write(str(prime3) + '\n')
    f_private.write(str(prime4) + '\n')
    f_private.close()

    g = gcd(o,totient)    

    while g != 1:
        o = random.randint(100,300)
        g = gcd(o,totient)

    
    p = random.randint(100,300)                         #calculate p and q
    q = p*j

def iterative(x,y,p):
    # calculates x^y mod p : fast exponentiation 

    res = 1                 
    x = x%p            
        
    while y > 0:
         temp = y%2
         if temp:              
            res = (res*x)%p 
         
      
         y = y>>1      
         x = (x*x)%p
        

    return res
    

def verify_encrypt(r2,o,e,r1,l):
    # verification of the process
    h = []
    for i in range(0,len(r1)):
        x = iterative(r2[i],o,l)               # calculates r2[i]^o mod l
        y = iterative(e[i],r1[i],l)            # calculates e[i]^r1[i] mod l
        x = (x*y)%l
        h.append(x)
    return h


def encrypt(message, file_name1 = 'public_keys.txt',file_name2 = 'private_keys.txt'):
    """
    Encrypts a message (string) by raising each character's ASCII value to the 
    power of j*k and taking the modulus of l. Returns a array of numbers.
    file_name refers to file where the public key is located. 
    """

    try:
        fo1 = open(file_name1, 'r')
        fo2 = open(file_name2, 'r')
    # check for the possibility that the user tries to encrypt something
    # using a public key that is not found
    except FileNotFoundError:
        print('That file is not found.')
    else:
        l = int(fo1.readline())
        j = int(fo1.readline())
        n = int(fo1.readline())
        o = int(fo1.readline())
        prime1 = int(fo1.readline())
        prime2 = int(fo1.readline())
        prime3 = int(fo1.readline())
        prime4 = int(fo1.readline())
        fo1.close()

        l1= int(fo2.readline())
        k = int(fo2.readline())
        fo2.close()


        ascii_val = []
        e = []
        r1 = []
        r2 = []
        r11 = []


        for i in range(0, len(message)):
            # add ciphertext to the list if the max block size is reached
            # reset ciphertext so we can continue adding ASCII codes
                ascii_val.append(ord(message[i]))

        # encrypt all of the numbers by taking it to the power of e
        # and modding it by n
        for i in range(0,len(message)):
            pw = (j*k)
            t2 = iterative(ascii_val[i],pw,l)
            e.append(t2)
        
        for i in range(0,len(message)):
            t2 = iterative(ascii_val[i],k,l)
            r1.append(t2)

        flag=0
        for i in range(0,len(message)):
            if ascii_val[i] == r1[i]:
                flag=1
                r11 = knnalgo(message ,prime2,prime3,prime4) 

        if flag ==1:
            for i in range(0,len(message)):
                r1[i] = r11[i]

        for i in range(0,len(message)):
            temp = iterative(n, r1[i],l)
            t2 = (ascii_val[i]*temp)%l
            r2.append(t2)

        h = verify_encrypt(r2,o,e,r1,l)    

        return r1,h

def decrypt(r1):
    """
    Decrypts a string of numbers by raising each number to the power of j and 
    taking the modulus of l. Returns the message as a string.
    """

    fo = open('public_keys.txt', 'r')
    fo1 = open('private_keys.txt', 'r')
    l = int(fo.readline())
    j = int(fo.readline())

    fo.close()

    h = []
    h1 = []
    tmp = ""
    msg = ""
    for i in range(0,len(r1)):
        t2 = iterative(r1[i],j,l)
        h.append(t2)
        h1.append(t2)
        h[i]= chr(h[i])
        msg += h[i]
    
    y = 1
    for i in range(0,len(r1)):
        h1[i] = (h1[i]*y)%l

    return msg , h1


def main():

    chooseKeys()

    message = input('enter the message: \n')
    r1,h = encrypt(message)
    print('The encrypted message is : \n')
    print(r1)
    print('\n')
    print("verification-encrypted h: ")
    print(h)
    print('\n')
    msg,h1 = decrypt(r1)
    print("verification-decrypted h: ")
    print(h)
    print('\n')
    print("The decrypted message is: \n")
    print(msg)
main()    


