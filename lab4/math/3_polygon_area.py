from math import tan, pi


n = int(input("Input number of sides: "))
a = float(input("Input the length of a side: "))

apothem = a / (2*tan(pi/n))
area = (n*a*apothem) / 2

print("The area of the polygon is:", area)