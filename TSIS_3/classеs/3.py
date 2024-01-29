class Rectangle():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def area(self):
        return self.a * self.b


ind1 = int(input())
ind2 = int(input())
rec = Rectangle(ind1, ind2)
print(rec.area())