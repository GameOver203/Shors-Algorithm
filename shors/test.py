from Factoring import myShor

alg = myShor(6,3)

with open("text.txt", "a") as f:
    for i in range(2,100):
        print(alg.shor(i), file=f)

    
    