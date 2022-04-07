import pandas
import math

# Wczytanie danych
data = pandas.read_csv("data.csv", header=0)

# p(x) * log2(p(x))
def entropy(n, N):
    p = n / N
    if(p != 0):
        return -p * math.log(p, 2)
    else:
        return 0

# Zmienna liczy warianty odpowiedzi dla danej kolumny
def getTypes(name):
    column = data[name]
    variants = []
    types = 1
    variants.append(column[0])
    for i in range(1, len(column)):
        check = 0
        for j in range(0, len(variants)):
            if(column[i] == variants[j]):
                check = 1
                break
        if(check == 0):
            variants.append(column[i])
            types += 1
    return int(types)

# Zamienia wartości tekstowe na liczbowe
def transform(name):
    column = data[name]
    variants = []
    types = 1
    variants.append(column[0])
    for i in range(1, len(column)):
        check = 0
        for j in range(0, len(variants)):
            if (column[i] == variants[j]):
                check = 1
                break
        if (check == 0):
            types += 1
            variants.append(column[i])

    tColumn = []
    for i in range(0, len(column)):
        for j in range(0, len(variants)):
            if(column[i] == variants[j]):
                tColumn.append(j)

    return tColumn


N1 = 0  # nigdzie
N3 = 0  # w kraju
N2 = 0  # za granicą

# Entropia dla całego układu: I = 1.43253376700698
destinity = data['destinity']
for i in range(0, len(destinity)):
    if(destinity[i] == "nowhere"):
        N1 += 1
    if (destinity[i] == "country"):
         N2 += 1
    if (destinity[i] == "aboard"):
        N3 += 1
ent = entropy(N1, 100) + entropy(N2, 100) + entropy(N3, 100)

table = []
table.append(transform('budget'))
table.append(transform('transport'))
table.append(transform('period'))
table.append(transform('type'))
table.append(transform('abundance'))
table.append(transform('destinity'))

types = []
types.append(getTypes('budget'))
types.append(getTypes('transport'))
types.append(getTypes('period'))
types.append(getTypes('type'))
types.append(getTypes('abundance'))
types.append(getTypes('destinity'))

# Warunek pierwszy: budżet
# 1. <1000
# 2. 1000-3000
# 3. >3000
def entBudget():
    n1 = 0 # <1000
    n2 = 0 # 1000-3000
    n3 = 0 # >3000
    n11 = 0 # <1000 i nigdzie
    n12 = 0 # <1000 i w kraju
    n13 = 0 # <1000 i za granicą
    n21 = 0 # 1000-3000 i nigdzie
    n22 = 0 # 1000-3000 i w kraju
    n23 = 0 # 1000-3000 i za granicą
    n31 = 0 # >3000 i nigdzie
    n32 = 0 # >3000 i w kraju
    n33 = 0 # >3000 i za granicą

    budget = data['budget']
    destinity = data['destinity']
    for i in range(0, len(budget)):
        if (budget[i] == "<1000"):
            n1 += 1
            if(destinity[i] == "nowhere"):
                n11 += 1
            if (destinity[i] == "country"):
                n12 += 1
            if (destinity[i] == "aboard"):
                n13 += 1
        if (budget[i] == "1000-3000"):
            n2 += 1
            if (destinity[i] == "nowhere"):
                n21 += 1
            if (destinity[i] == "country"):
                n22 += 1
            if (destinity[i] == "aboard"):
                n23 += 1
        if (budget[i] == ">3000"):
            n3 += 1
            if(destinity[i] == "nowhere"):
                n31 += 1
            if (destinity[i] == "country"):
                n32 += 1
            if (destinity[i] == "aboard"):
                n33 += 1
    I1p = entropy(n11, n1) + entropy(n12, n1) + entropy(n13, n1)
    I1m = entropy(N1-n11, n2+n3) + entropy(N2-n12, n2+n3) + entropy(N3-n13, n2+n3)
    E1 = n1/100 * I1p + (100-n1)/100 * I1m
    infProfit = ent - E1
    print(I1p)
    print(I1m)
    print(E1)
    print(infProfit)

def partEntropy():
    informationProfit = []
    for i in range(0, len(table) - 1):
        n = []
        nPart = []
        for j in range(0, types[i]):
            sum = 0
            nX = []
            nX.append(0)
            nX.append(0)
            nX.append(0)
            for k in range(0, 100):
                if(table[i][k] == j):
                    sum += 1
                    for l in range(0, 3):
                        if(table[5][k] == l):
                            nX[l] += 1

            nPart.append(nX)
            n.append(sum)

        for j in range(0, len(n)):
            Ip = entropy(nPart[j][0], N1) + entropy(nPart[j][1], N2) + entropy(nPart[j][2], N3)
            Im = entropy(n[j] - nPart[j][1] - nPart[j][2], 100 - N1) + \
                 entropy(n[j] - nPart[j][0] - nPart[j][2], 100 - N2) + \
                 entropy(n[j] - nPart[j][0] - nPart[j][1], 100 - N3)
            print(Ip)
            print(Im)

            E = (n[j]/100) * Ip + ((100 - n[j])/100) * Im
            infProfit = ent - E
            informationProfit.append(infProfit)
            print(n)
            print(nPart)
            print(infProfit)
            print()



    print(informationProfit)
    print(len(informationProfit))

partEntropy()
print(ent)

