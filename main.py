import pandas as pd
import numpy as np
import math as math

##################################################################
############################ Funkcje #############################
##################################################################

# Funkcja oblicza entropie na podstawie wzoru: -pi * log2 pi
# pi = n/N
def entropy(n, N):
    if N == 0:
        return 0
    else:
        p = n / N
        if p != 0:
            return -p * math.log(p, 2)
        else:
            return 0

# Funkcja podaje, w którym miejscu należy podzielić tabelę
def findMaxIndex(tab):
    maximum = max(map(max, tab))
    for i in range(0, len(tab)):
        for j in range(0, len(tab[i])):
            if tab[i][j] == maximum:
                index = [i, j]
                return index

# Funkcja sprawdza czy w danym wektorze wszystkie wartości są równe
def allEqual(iterator):
    return len(set(iterator)) <= 1

def tabs(level):
    text = " "
    for i in range(0, level):
        text += "\t"
    return text

##################################################################
################## Wczytanie danych z pliku csv ##################
##################################################################

database = pd.read_csv("data.csv")
del database['#']                                                       # Usuwam kolumnę z liczbą porządkową

budget = {'<1000': 0, '1000-3000': 1, '>3000': 2}                       # Zamieniam wartości tekstowe na wartości
transport = {'car': 0, 'train': 1, 'plane': 2}                          # liczbowe, odpowiadające danemu typowi
period = {'preseason': 0, 'season': 1, 'offseason': 2}
type = {'sightseeing': 0, 'rest': 1}
abundance = {'alone': 0, 'family': 1, 'couple': 2, 'friends': 3}
destinity = {'nowhere': 0, 'aboard': 1, 'country': 2}

database.budget = [budget[item] for item in database.budget]
database.transport = [transport[item] for item in database.transport]
database.period = [period[item] for item in database.period]
database.type = [type[item] for item in database.type]
database.abundance = [abundance[item] for item in database.abundance]
database.destinity = [destinity[item] for item in database.destinity]

table = pd.DataFrame(database).to_numpy()                               # Zamiana DataFrame (pandas) na array (numpy)


##################################################################
######################## Liczenie entropii #######################
##################################################################

def partEntropy(tab):
    N1 = sum(1 for item in tab[:, 5] if item == 0)                                        # N1 - konkluzja = nigdzie
    N2 = sum(1 for item in tab[:, 5] if item == 1)                                        # N2 - konkluzja = za granicą
    N3 = sum(1 for item in tab[:, 5] if item == 2)                                        # N3 - konkluzja = w kraju

    totalEntropy = entropy(N1, len(tab)) + entropy(N2, len(tab)) + entropy(N3, len(tab))   # Entropia całego układu

    uniTypes = [3, 3, 3, 2, 4, 3]

    informationGain = []
    for i in range(0, 5):
        n1 = []              # Ilość przykładów należących do danej klasy oraz o konkluzji - nigdzie
        n2 = []              # Ilość przykładów należących do danej klasy oraz o konkluzji - za granicą
        n3 = []              # Ilość przykładów należących do danej klasy oraz o konkluzji - w kraju
        for j in range(0, uniTypes[i]):
            n1.append(sum((tab[:, i] == j) & (tab[:, 5] == 0)))
            n2.append(sum((tab[:, i] == j) & (tab[:, 5] == 1)))
            n3.append(sum((tab[:, i] == j) & (tab[:, 5] == 2)))

        infGain = []
        for j in range(0, uniTypes[i]):
            if uniTypes[i] != 1:
                sumPlus = n1[j] + n2[j] + n3[j]                             # Ilość przykładów po potwierdzeniu warunku
                entPlus = entropy(n1[j], sumPlus) + \
                          entropy(n2[j], sumPlus) + \
                          entropy(n3[j], sumPlus)                           # Entropia po potwierdzeniu warunku

                sumMinus = len(tab) - sumPlus                               # Ilość przykładów po zaprzeczeniu warunku
                entMinus = entropy(N1 - n1[j], sumMinus) + \
                           entropy(N2 - n2[j], sumMinus) + \
                           entropy(N3 - n3[j], sumMinus)                    # Entropia po zaprzeczeniu warunku

                partEnt = sumPlus/len(tab) * entPlus + sumMinus/len(tab) * entMinus  # Łączna entropia po ocenie warunku
                infGain.append(totalEntropy - partEnt)                               # Zysk informacyjny
            else:
                infGain.append(0)

        informationGain.append(infGain)

    return informationGain


##################################################################
################### Tworzenie drzewa binarnego ###################
##################################################################

# Tablica przechowuje pytania dotyczące poszczególnych wyborów
questions = [["Czy budżet mniejszy od 1000 zł?",
              "Czy budżet pomiędzy 1000 a 3000 zł?",
              "Czy budżet powyżej 3000 zł?"],
             ["Czy podróżujemy samochodem?",
              "Czy podróżujemy pociagiem?",
              "Czy podróżujemy samolotem?"],
             ["Czy pobyt w okresie przedsezonowym?",
              "Czy pobyt w sezonie wakacyjnym?",
              "Czy pobyt po sezonie wakacyjnym?"],
             ["Czy wycieczka w celu zwiedzania?",
              "Czy wycieczka w celu odpoczynku?"],
             ["Czy wyjeżdzamy sami?",
              "Czy wyjeżdżamy z rodziną?",
              "Czy wyjeżdżamy z partnerem/partnerką?",
              "Czy wyjeżdżamy z przyjaciółmi?"]]

# Tablica zawiera konkluzję
conclusion = ["NIGDZIE NIE WYJEDZIEMY",
              "WYJEDZIEMY ZA GRANICĘ",
              "WAKACJE SPĘDZIMY W KRAJU"]

# Funkcja do budowania drzewa binarnego oparta o rekruencje
def binaryTree(tab, level):
    partialEntropy = partEntropy(tab)                               # Liczymy częściową entropię
    splitAxis = findMaxIndex(partialEntropy)                        # Wyznaczamy oś podziału

    print(questions[splitAxis[0]][splitAxis[1]])                    # Wypisujemy pytanie
    level += 1                                                      # Zwiększamy wcięcie w tekście

    partTab1 = []                                                   # Pierwsza tabela podziału (TAK)
    partTab2 = []                                                   # Druga tabela podziału (NIE)

    for i in range(0, len(tab)):
        if tab[i][splitAxis[0]] == splitAxis[1]:
            partTab1.append(tab[i])
        else:
            partTab2.append(tab[i])

    partTab1 = np.array(partTab1)
    partTab2 = np.array(partTab2)

    if not allEqual(partTab1[:, 5]):                                # Sprawdzamy czy w podzielonych tabelach konkluzja
        print(tabs(level), "Jeśli tak:")                            # jest jednorodna. Jeżeli tak, to wypisujemy ją,
        print(tabs(level), end=" ")                                 # w przeciwnym wypadku za pomocą rekurencji
        binaryTree(partTab1, level)                                 # tworzymy kolejny podział
    else:
        print(tabs(level), conclusion[partTab1[0][5]])
        level -= 1
    if not allEqual(partTab2[:, 5]):
        print(tabs(level), "Jeśli nie:")
        print(tabs(level), end=" ")
        binaryTree(partTab2, level)
    else:
        print(tabs(level), conclusion[partTab1[0][5]])
        level -= 1

binaryTree(table, 0)
