def unique(list):
    arr = []
    for i in list:
        if i not in arr: arr.append(i)      
    print(arr)