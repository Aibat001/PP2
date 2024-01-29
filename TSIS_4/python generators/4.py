def gen(a, b):
    num = int()
    for i in range(a, b + 1):
            yield i**2

a = int(input())
b = int(input())
interval = gen(a, b)
print(", ".join(str(x) for x in interval))