import math

n = int(input("Input number of sides: "))
l = int(input("Input the length of a side: "))
Area = l * l * math.sin((math.pi * (n - 2)) / n)
print("The area of the polygon is:", int(Area))