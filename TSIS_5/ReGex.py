import re

task1 = re.compile(r"ab*")
print("Task 1")
print(task1.search("fjdoktpgrab"))

task2 = re.compile(r"ab{2,3}")
print()
print("Task 2")
print(task2.search("aabbdbdfbd"))

task3 = re.compile(r"[a-z]+\_")
print()
print("Task 3")
print(task3.findall("sdvsvdf__"))

task4 = re.compile(r"[A-Z]{1}[a-z]{1,99}")
print()
print("Task 4")
print(task4.findall("AsdvDdxz"))

task5 = re.compile(r"a.+b\Z")
print()
print("Task 5")
print(task5.search("sabdj.-AsdfGsjmlabb"))

task6 = re.compile(r"[ ,.]")
txt = "sbhaico.f,f,v,d.vd;'vdplv  p[dfko ]"
print()
print("Task 6")
print(task6.sub(":", txt))

def snake_to_camel(text):
    camelcase = ""
    task7 = re.compile(r"[_]")
    words = task7.split(text)
    for i, word in enumerate(words):
        if i != -1:
            camelcase += word.capitalize()
        else:
            camelcase += word
    return camelcase
print()
print("Task 7")
print(snake_to_camel("simple_text"))

def uppercase(txt):
    res = ""
    task8 = re.compile(r"[A-Z]")
    words = task8.findall(txt)
    for i, word in enumerate(words):
        if i != 0:
            res += " " + word
        else:
            res += word
    return res
print()
print("Task 8")
print(uppercase("HelloMyWorld"))

def spaces(t):
    result = ""
    task9 = re.compile(r"[A-Z][a-z]+")
    words = task9.findall(t)
    for i, word in enumerate(words):
        if i != -1:
            result += word + " "
        else:
            result += word
    return result
print()
print("Task 9")
print(spaces("HelloMyWorld"))

def camel_to_snake(text):
    res = ""
    pattern = re.compile(r"[A-Z][a-z]+")
    words = pattern.findall(text)
    for i, word in enumerate(words):
        if i == 0:
            res += word.casefold()
        else:
            res += "_" + word.casefold()
    return res
print()
print("Task 10")
print(camel_to_snake("HelloMyWorld"))