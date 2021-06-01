from time import sleep

lst = [0, 0, 0]
nums = [1,3,5,7,9,11,13,15]
l = len(nums)
total = 30

while True:
    a, b, c = nums[lst[0]], nums[lst[1]], nums[lst[2]]
    t = a + b + c

    print(f'{a} + {b} + {c} = {t}')

    if t == total:
        break

    if lst[0] == lst[1] == lst[2] == l - 1:
        break

    lst[0] += 1

    if lst[0] == 8:
        lst[0] = 0
        lst[1] += 1

    if lst[1] == 8:
        lst[1] = 0
        lst[2] += 1
        
    sleep(0.01)
    