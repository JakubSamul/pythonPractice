def fib_seq(n):
    a = [1,1]
    c = 0
    while c < n-2:
        a.append(a[-1]+a[-2])
        c += 1
    return a

print(fib_seq(10))

