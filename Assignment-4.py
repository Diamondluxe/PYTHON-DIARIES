#Question 1

def greet():
    print("Hello, Welcome to the Python Programming!")

greet()

#Question 2

def add_numbers(num1, num2):
    return num1+num2

result = add_numbers(10, 5)
print(result)

#Question 3

def largest(a,b):
    if a > b:
        return a
    else:
        return b
    
Large = largest(20, 35)
print(Large)

#Question 4

def check_even_odd(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"

check = check_even_odd(8)
print(check)

#Question 5

def rectangle_area(length, width):
    return length * width

area = rectangle_area(5, 4)
print(area)

#Bonus Challenge

def factorial(n):
    i = 1
    fact = 1
    while i <= n:
        fact = fact * i
        i += 1
    return fact

call = factorial(5)
print(call)

