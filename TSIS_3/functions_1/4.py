def filter_prime():
    s = list(map(int, input().split()))
    for number in s:
        if number < 2:
            s.remove(number)
        elif number == 2:
            continue
        else:
            for i in range(2, number):
                if number % i == 0:
                    s.remove(number)

    return print(*s)