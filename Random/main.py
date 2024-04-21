import random
ok = []
while len(ok) < 6:
    for i in range(60):
        if len(ok) == 6:
            break
        a = random.randrange(1, 60)
        if i == a and i not in ok:
            ok.append(a)
ok.sort()
print(ok)
