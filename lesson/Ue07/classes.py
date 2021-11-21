class Person:

    counter = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"I am {self.name} and {self.age} years old."

donald = Person("Donald", 74)
joe = Person("Joe", 78)

donald.counter = 3
print(donald)
print(donald.counter)

joe.counter = 5
print(joe)
print(joe.counter)

print(donald.counter)
print(Person.counter)