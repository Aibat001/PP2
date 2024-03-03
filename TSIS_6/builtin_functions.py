import functools
import time
import re
import math


# task 1
def multi_nums():
    list = map(int, input().split())
    res = functools.reduce(lambda a, b: a * b, list)
    print(res)


# task 2
def count_letters():
    str = input()
    lwr_pt = re.compile("[a-z]")
    upp_pt = re.compile("[A-Z]")
    lwr = lwr_pt.findall(str)
    upp = upp_pt.findall(str)
    print(f'Num of lower chars = {len(lwr)}, Num of upper chars = {len(upp)}')


# task 3
def isPalindrome(s):
    if s == str.join('', list(reversed(s))):
        print('Is palindrome')
    else:
        print('Not palindrome')


# task 4
def del_string(n, ms):
    print(time.time())
    time.sleep(ms / 1000)
    print(f'Square root of {n} after {ms} milliseconds is {math.sqrt(n)}')
    print(time.time())


# task 5
def isAllTrue(tuple):
    return all(tuple)

def main():
    true = (2, "wordle", True)
    false = (0, "wow", True)
    print(isAllTrue(true))
    print(isAllTrue(false))

if __name__ == '__main__':
    main()