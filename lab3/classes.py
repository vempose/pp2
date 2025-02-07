class Person:
    def __init__(self, name = "Nothing"):
        self.name = name
    
    def getString(self):
        self.name = input("What's your name? ")
    
    def printString(self):
        print(self.name.upper())
    

class Shape:
    def area(self):
        return 0


class Square(Shape):
    def __init__(self, length = 0):
        self.length = length
    
    def area(self):
        return self.length ** 2


class Rectangle(Shape):
    def __init__(self, length = 0, width = 0):
        self.length = length
        self.width = width
    
    def area(self):
        return self.length * self.width


class Point():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def show(self):
        print(f"x = {self.x}, y = {self.y}")
        
    def move(self, x, y):
        self.x = x
        self.y = y
    
    def dist(self, point):
        return ((point.x - self.x)**2 + (point.y - self.y)**2)**0.5


class Account():
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"{amount} deposit made.")
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"{amount} withdraw made.")
        else:
            print("Insufficient funds!")


print("Square:")
some_square = Square(10)
print(some_square.area())
print()

print("Shape: ")
some_shape = Shape()
print(some_shape.area())
print()

print("Rectangle:")
rec = Rectangle(10, 20)
print(rec.area())
print()

print("Points:")
some_dot = Point(55, 75)
some_dot.show()
some_dot.move(1, 1)
some_dot.show()
other_dot = Point(3, 3)
print(some_dot.dist(other_dot))
print()

print("Bank:")
money = Account("me", 100)
money.deposit(100)
money.deposit(200)
money.withdraw(200)
print(money.balance)
money.withdraw(400)