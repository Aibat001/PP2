def gen(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input())
evens = gen(n)
print(', '.join(str(even) for even in evens))