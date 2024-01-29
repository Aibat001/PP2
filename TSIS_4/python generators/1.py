def gen(n):
    l = []
    for x in range(n + 1):
        l.append(x**2)
    return l

a = int(input())
print(gen(a))