def dsum(ic, jc):
    s = 1
    for i in range(1 + ic):
        for j in range(1 + jc):
                s*= (-1)**i
    return s