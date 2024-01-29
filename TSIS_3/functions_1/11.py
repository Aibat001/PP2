def palindrome(word):
    for i in range(len(word)):
        if word[i] != word[-(i + 1)]:
            print("NO")
            break
        else:
            print("YES")
            break

word = input()
print(palindrome(word))