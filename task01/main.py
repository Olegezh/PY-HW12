# 1. Cоздайте класс студента.
# - Используя дескрипторы проверяйте ФИО на первую заглавную букву и наличие только букв.
# - Названия предметов должны загружаться из файла CSV при создании экземпляра. Другие предметы в экземпляре недопустимы.
# - Для каждого предмета можно хранить оценки (от 2 до 5) и результаты тестов (от 0 до 100).
# - Также экземпляр должен сообщать средний балл по тестам для каждого предмета и по оценкам всех предметов вместе взятых.

import csv
class Name_Validate:

    def __init__(self, st_name = None):
        self.st_name = st_name

    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.param_name, value)

    def validate(self, value):
        if not value.istitle():
            raise TypeError(f'Имя или фамилия {value} должны начинаться с заглавной буквы')

class Student:
    _course_exams = {}
    _course_tests = {}

    _first_name = Name_Validate()
    _second_name = Name_Validate()

    def __init__(self, first_name, second_name):
        self._first_name = first_name
        self._second_name = second_name
        self._courses_load()

    def __str__(self):
        return f' студент {self.get_full_name} \n {list(self._course_exams.keys())}'
    @property
    def get_full_name(self):
        return f'{self._first_name} {self._second_name}'

    def _courses_load(self):
        with open('courses.csv', 'r', encoding='utf-8') as csv_file:
            courses = csv.reader(csv_file, delimiter="\n")
            for course in courses:
                self._course_exams[course[0]] = []
                self._course_tests[course[0]] = []

    def add_exam_result(self, course_name, value):
        if course_name not in self._course_exams.keys():
            raise ValueError(f'у студента {self.get_full_name} нет такого курса')
        if value <2 or value >5:
            raise ValueError(f'оценка за экзамен должна быть от 2 до 5')
        self._course_exams[course_name].append(value)

    def get_exam_result(self, course_name):
        if course_name not in self._course_exams.keys():
            raise ValueError(f'у студента {self.get_full_name} нет такого курса')
        if len(self._course_exams[course_name])!= 0:
            aver_res = sum(self._course_exams[course_name][i] for i in range(len(self._course_exams[course_name])))/len(self._course_exams[course_name])
        else:
            aver_res = -999

        return aver_res

    def get_total_exam_result(self):
        aver_res = 0
        count = 0
        for item in self._course_exams.keys():
            if self.get_exam_result(item) != -999:
                aver_res += self.get_exam_result(item)
                count +=1
        aver_res = aver_res / count
        return aver_res

    def add_test_result(self, course_name, value):
        if course_name not in self._course_tests.keys():
            raise ValueError(f'у студента {self.get_full_name} нет такого курса')
        if value < 1 or value > 100:
            raise ValueError(f'оценка за тест должна быть от 1 до 100')
        self._course_tests[course_name].append(value)

    def get_test_result(self, course_name):
        if course_name not in self._course_tests.keys():
            raise ValueError(f'у студента {self.get_full_name} нет такого курса')
        if len(self._course_tests[course_name])!= 0:
            aver_res = sum(self._course_tests[course_name][i] for i in range(len(self._course_tests[course_name])))/len(self._course_tests[course_name])
        else:
            aver_res = -999
        return aver_res

    def get_total_test_result(self):
        aver_res = 0
        count = 0
        for item in self._course_tests.keys():
            if self.get_test_result(item) != -999:
                aver_res += self.get_test_result(item)
                count +=1
        aver_res = aver_res / count
        return aver_res


def print_res(stu, type_ , course):
    if type_ == "exam":
        print(f'Студент {stu.get_full_name} имеет среднюю оценку за экзамены по предмету {course} = {stu.get_exam_result(course)}')
    if type_ == "test":
        print(f'Студент {stu.get_full_name} имеет среднюю оценку за тесты по предмету {course} = {stu.get_test_result(course)}')


stu1 = Student('Иван', 'Иванов')
print(stu1)

course = "Математика"
stu1.add_exam_result(course, 5)
stu1.add_exam_result(course, 4)
print_res(stu1, "exam", course)

stu1.add_test_result(course, 50)
stu1.add_test_result(course, 60)
print_res(stu1, "test", course)

course = "История"
stu1.add_exam_result(course, 3)
stu1.add_exam_result(course, 4)
print_res(stu1, "exam", course)

course = "Литература"
stu1.add_test_result(course , 99)
stu1.add_test_result(course , 77)
print_res(stu1, "test", course)


print(f'Студент {stu1.get_full_name} имеет среднюю оценку  по экзаменам за все предметы = {stu1.get_total_exam_result()}')
print(f'Студент {stu1.get_full_name} имеет среднюю оценку по тестам за все предметы = {stu1.get_total_test_result()}')
