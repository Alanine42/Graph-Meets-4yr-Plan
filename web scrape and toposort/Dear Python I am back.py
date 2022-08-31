import numpy as np

## OOP
class Student:
    def __init__(self, name, pid):
        ## CTOR
        self.name = name
        self.pid = pid

    def __str__(self):
        ## the toString() method
        return "Name: " + self.name + "\nPID: " + self.pid

    ## More magic methods
    def __len__(self):
        # define the the Student's length to be .... the name's length/
        return len(self.name)

    def __eq__(self, other):
        return self.pid == other.pid

    def __gt__(self, other):
        # return int(self.pid[1:]) > int(other.pid[1:])
        return self.pid > other.pid


# Instantiate class
alan = Student("Alan", "A16456107")
selina = Student("Selina", "A99999999")
print(alan, "likes", selina)
print(len(alan))
print("Are they the same student? ",alan == selina)
print("Rule: comparing 2 students <==> comparing the number section of their PID")
print("alan > selina (comparing pid)? : " , alan > selina)


## Lambda function
x = lambda a,b,c : a*b*c   # maps R^3 to R
print(x(4,5,6))



## List comprehension
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
# [expression for item in iterable if condition==True]
a_team = [f for f in fruits if "a" in f]
print(a_team)

seq = [x for x in range(10) ]
print(seq)

