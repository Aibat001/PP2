# 4x + 2y = 94
# x + y = 35
# 4(35 - y) + 2y = 94
def solve(numheads, numlegs):
    chickens = (numheads * 4 - 94) / 2
    rabbits = 35 - chickens
    print(chickens, rabbits)

numheads = 35
numlegs = 94

result = solve(numheads, numlegs)