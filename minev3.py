import random
import re
import time
from string import ascii_lowercase

#napraviti matricu, staviti random generiranje mina, kasnije staviti prilagodbe na duljinu i širinu tablice



def setuptablica(tablicasize, start, brojmina):
    emptytablica = [['0' for i in range(tablicasize)] for i in range(tablicasize)]

    mine = dodajmine(emptytablica, start, brojmina)

    for i, j in mine:
        emptytablica[i][j] = 'X'

    tablica = dodajbroj(emptytablica)

    return (tablica, mine)

#definiram funkciju koja daje oznake za retke i stupce te njihove margine
def showtablica(tablica):
    tablicasize = len(tablica)

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


def randomcelija(tablica):
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
    susjedne = susjednecelije(tablica, *start)

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


# pokazat ce trenutne celije, ako je celija vec bila prikazana zaustaviti ce funkciju;
#ako je celija prazna potrazit ce susjedne
def showcelije(tablica, trenutnacelija, redno, stupacno):
    if trenutnacelija[redno][stupacno] != ' ':
        return
    
    trenutnacelija[redno][stupacno] = tablica[redno][stupacno]

    if tablica[redno][stupacno] == '0':
        for r, c in susjednecelije(tablica, redno, stupacno):
            if trenutnacelija[r][c] != 'F':
                showcelije(tablica, trenutnacelija, r, c)

#treba jos nadopuniti kod i sve funkcije staviti u jednu cjelinu


def igrajponovo():
    choice = input('Želiš li još igrati? (da/ne): ')

    return choice.lower() == 'da'


def input1(inputstr, tablicasize, pomoc):
    celija = ()
    zastavica = False
    poruka = "Kriva celija. " + pomoc

    redoslijed = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[tablicasize - 1])
    input2 = re.match(redoslijed, inputstr)

    if inputstr == 'pomoc':
        poruka = pomoc

    elif input2:
        redno = int(input2.group(2)) - 1
        stupacno = ascii_lowercase.index(input2.group(1))
        zastavica = bool(input2.group(3))

        if -1 < redno < tablicasize:
            celija = (redno, stupacno)
            poruka = ''

    return {'celija': celija, 'zastavica': zastavica, 'poruka': poruka}


def igraj():
    print("Odaberi početno ('p'), srednje('s'), napredno('n') iskustvo igranja.")
    iskustvo =input('Upiši p/s/n:')
    tablicasize = int(input('Veličina tablice:'))
    while tablicasize < 2 or tablicasize > 26:
        tablicasize=int(input('Upiši veličinu tablice ponovo(2<n<=26):'))
    if iskustvo.lower() == 'p':
        brojmina = round(tablicasize**2/10)
    elif iskustvo.lower() == 's':
        brojmina = round(tablicasize**2/8)
    elif iskustvo.lower() == 'n':
        brojmina = round(tablicasize**2/6)
    else:
        brojmina = round(tablicasize**2/10)
    trenutnacelija = [[' ' for i in range(tablicasize)] for i in range(tablicasize)]

    tablica = []
    zastavice = []
    vrijeme = 0

    pomoc = ("Upiši slovo za stupac te broj za red (npr. a1; c4). "
    "Za staviti ili maknuti zastavicu staviti 'f' iza slova i broja koji oznacavaju stupac i redak (npr. a1f; c4f).")

    showtablica(trenutnacelija)
    print(pomoc + "Napisi 'pomoc' za ponovo prikazati ovu poruku.\n")

    while True:
        preostalemine = brojmina - len(zastavice)
        input3 = input('Unesi koordinate celije ({} preostalih mina): '.format(preostalemine))
        rezultat = input1(input3, tablicasize, pomoc + '\n')

        poruka = rezultat['poruka']
        celija = rezultat['celija']

        if celija:
            print('\n\n')
            redno, stupacno = celija
            trencel = trenutnacelija[redno][stupacno]
            zastavica = rezultat['zastavica']

            if not tablica:
                tablica, mine = setuptablica(tablicasize, celija, brojmina)
            if not vrijeme:
                vrijeme = time.time()

            if zastavica:
                #dodati zastavicu
                if trencel == ' ':
                    trenutnacelija[redno][stupacno] = 'F'
                    zastavice.append(celija)
               #makuti zastavicu
                elif trencel == 'F':
                    trenutnacelija[redno][stupacno] = ' '
                    zastavice.remove(celija)
                else:
                    poruka = 'Ne možeš tu staviti zastavicu.'

            # ako vec postoji zastavica, poslati poruku
            elif celija in zastavice:
                poruka = 'Već je tu zastavica'

            elif tablica[redno][stupacno] == 'X':
                print('Kraj igre\n')
                showtablica(tablica)
                if igrajponovo():
                    igraj()
                return

            elif trencel == ' ':
                showcelije(tablica, trenutnacelija, redno, stupacno)

            else:
                poruka = "Ta ćelija je već prikazana."

            if set(zastavice) == set(mine):
                minute, sekunde = divmod(int(time.time() - vrijeme), 60)
                print(
                    'Pobijedio/la si. '
                    'Trebalo ti je {} minuta i {} sekundi.\n'.format(minute,
                                                                      sekunde))
                showtablica(tablica)
                if igrajponovo():
                    igraj()
                return

        showtablica(trenutnacelija)
        print(poruka)

igraj()
