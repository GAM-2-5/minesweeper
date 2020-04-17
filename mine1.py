import random
import re
import time
from string import ascii_lowercase

#napraviti matricu, staviti random generiranje mina, kasnije staviti prilagodbe na duljinu i širinu tablice



def setuptbalica(tablicasize, start, brojmina):
    emptytablica = [['0' for i in range(tablicasize)] for i in range(tablicasize)]

    mine = getmine(emptytablica, start, brojmina)

    for i, j in mine:
        emptytablica[i][j] = 'X'

    tablica = getnumbers(emptytablica)

    return (tablica, mine)

#definiram funkciju koja daje oznake za retke i stupce te njihove margine
def showtablica(tablica):
    gtablicasize = len(tablica)

    horizontalno = '   ' + (4 * tablicasize * '-') + '-'

    gornji = '     '

    for i in ascii_lowercase[:tablicasize]:
        gornji = gornji + i + '   '

    print(gornji + '\n' + horizontalno)


    for idx, i in enumerate(tablica):
        red = '{0:2} |'.format(idx + 1)

        for j in i:
            red = red + ' ' + j + ' |'

        print(red + '\n' + horizontalno)

    print('')


def reandomcelija(tablica):
    tablicasize = len(tablica)

    a = random.randint(0, tablicasize - 1)
    b = random.randint(0, tablicasize - 1)

    return (a, b)


def susjednecelije(tablica, redno, stupacno):
    tablicasize = len(tablica)
    susjedne = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < (redno + i) < tablicasize and -1 < (stupacno + j) < tablicasize:
                susjedne.append((redno + i, stupacno + j))

    return susjedne


def dodajmine(tablica, start, brojmina):
    mine = []
    susjende = susjednecelije(tablica, *start)

    for i in range(brojmina):
        celija = randomcelija(tablica)
        while celija == start or celija in mine or celija in susjedne:
            celija = randomcelija(tablica)
        mine.append(celija)

    return mine

# traze se susjedne mine odnosno koliko ih ima kako bi se mogli upisati brojevi
def dodajbroj(tablica):
    for redno, red in enumerate(tablica):
        for stupacno, celija in enumerate(red):
            if celija != 'X':
                vrijednost = [tablica[r][c] for r, c in susjednecelije(tablica, redno, stupacno)]
                tablica[redno][stupacno] = str(vrijednost.count('X'))

    return tablica


# pokazat ce trenutne celije, ako je celija vec bila prikazana zaustaviti ce funkciju; ako je celija prazna potrazit ce susjedne
def showcelije(tablica, trenutnacelija, redno, stupacno):
    if trenutnacelija[redno][stupacno] != ' ':
        return
    
    trenutnacelija[redno][stupacno] = tablica[redno][stupacno]

    if tablica[redno][stupacno] == '0':
        for r, c in susjednecelije(tablica, redno, stupacno):
            if trenutnacelija[r][c] != 'F':
                showcelije(tablica, trenutnacelija, r, c)


#treba jos nadopuniti kod i sve funkcije staviti u jednu cijelinu
