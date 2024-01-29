def spy_game(nums):
    for i in nums:
        if i == 7:
            num = nums[:nums.index(i)]
    if len(num) == len(nums):
        return False
    cnt = 0
    for j in num:
        if j == 0:
            cnt += 1
    if cnt >= 2:
        return True
    else:
        return False