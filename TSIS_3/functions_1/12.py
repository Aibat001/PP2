def histogram(n):
    for i in n:
        for j in range(i):
            print("*", end="")
        print()


histogram([4, 9, 7])