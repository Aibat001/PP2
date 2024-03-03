import pathlib
import os
from string import ascii_uppercase

path = '..'

# task 1
def listDirs(p):
    print([x.name for x in os.scandir(path = p) if x.is_dir()])


def listFiles(p):
    print([x.name for x in os.scandir(path = p) if x.is_file()])


def listDirsAndFiles(p):
    print([x.name for x in os.scandir(path = p)])
print("Task 1")
listDirs(path)
listFiles(path)
listDirsAndFiles(path)

# task 2
def check(p):
    exist_status = os.access(path = p, mode = os.F_OK)
    print(f'Existence : {exist_status}')
    read_status = os.access(path = p, mode = os.R_OK)
    print(f'Readibility : {read_status}')
    write_status = os.access(path = p, mode = os.W_OK)
    print(f'Writability : {write_status}')
    exec_status = os.access(path = p, mode = os.X_OK)
    print(f'Executability : {exec_status}')
print()
print('Task 2')
check(path)

# task 3
def test(p):
    exist_status = os.access(path = p, mode = os.F_OK)
    if exist_status:
        print(f'File: {os.path.basename(p)}')
        print(f'Directory: {os.path.dirname(p)}')
    else:
        print("The file does not exist")
print()
print("Task 3")
test('TSIS_6/demofile1.txt')

# task 4
def count(p):
    f = open(p, 'r')
    cnt = 0
    for i in f:
        cnt += 1
    return cnt
print()
print("Task 4")
print(f'Number of lines = {count("TSIS_6/demofile1.txt")}')

# task 5
def show(fname, l):
    f = open(fname, "a")
    f.write(str(l))
    f.close()

    f = open(fname, "r")
    print(f.read())
print()
print("Task 5")
l = str(input())
show('TSIS_6/demofile1.txt', l)

# task 6
def generateFiles():
    for char in ascii_uppercase:
        file = open(f'./files/{char}.txt', 'x')
        file.close()
print()
print("Task 6")
generateFiles()

# task 7
def copyContent(i, t):
    init_file = open(i, 'r')
    file_content = init_file.read()
    init_file.close()

    target_file = open(t, 'w')
    target_file.write(str(file_content))
    target_file.close()
    print('Successfully copied')

    target_file = open(t, 'r')
    print(target_file.read())
    target_file.close()
print()
print("Task 7")
copyContent('demofile1.txt', 'demofile2.txt')

# task 8
def delete(p):
    os.remove(p)
print()
print("Task 8")
delete("demofile2")