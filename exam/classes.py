class Person:
    
    def __init__(self, name, age) -> None:
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = value

    def __repr__(self) -> str:
        return f"{self.name} ({self.age} years old)"

class Student(Person):
    
    def __init__(self, name, age, studentId) -> None:
        super().__init__(name, age)
        self._studentId = studentId

    @property
    def studentId(self):
        return self._studentId

    @studentId.setter
    def studentId(self, value):
        self._studentId = value

    def __repr__(self) -> str:
        return self.studentId + " - " + super().__repr__()

    @classmethod
    def classname(cls):
        return cls.__name__

    @staticmethod
    def staticstuff():
        return "Fian oasch"

s = Student("Andi", 25, "S1910307106")
print(Student.classname())
print(Student.staticstuff())
print(s)