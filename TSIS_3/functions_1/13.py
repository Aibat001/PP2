from random import randint

print("Hello! What is your name?")
word = str(input())
print("Well " + word + ", I am thinking of a number between 1 and 20.")
print("Take a guess.")
a = randint(0, 20)
num = a
f = 0
global cnt 
cnt = 0
while f <= 20:
    cnt += 1
    n = int(input())
    if n < num:
        print("Your guess is too low.")
        print("Take a guess.")
    elif n > num:
        print("Your guess is too high.")
        print("Take a guess.")
    elif a == num:
        print("Good job, " + word + "! You guessed my number in", cnt, "guesses!")
        break