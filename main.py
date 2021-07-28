# ADAUGAREA TUTUROR FRAMEWORK-URILOR
# tkinter este un framework  specific limbajului Python ce permite dezvoltarea aplicatiilor cu interfata grafica

# Adaugarea fiecarui obiect din tkinter in namespace
import tkinter

from tkinter import *

# Permiterea accesarii mai multor font-uri, modificarea dimensiunii si stilul acestora.
from tkfontchooser import Font

# Permite utilizarea messagebox-urilor in aplicatiile Python
from tkinter import messagebox

# Functiile 'partial' permit specificarea numarului de date de intrare a unei functii.
from functools import partial

# adauga metode pentru generarea aleatoare a numerelor
import random

# Permite utilizarea sistemului de operare intr-o maniera dorita
import os

# Adaugarea unui mixer pentru a putea avea "Background music"
from pygame import mixer

# Adaugarea unui suport pentru introducerea si modificarea imaginilor
from PIL import ImageTk, Image

# Permite manipularea timpului
import time

# Initializarea si pornirea melodiei de pe meniul principal


def play_music():
    mixer.init()
    mixer.music.load("Opening.mp3")
    # Acest '-1' reprezinta faptul ca melodia se va repeta cat timp programul ruleaza
    mixer.music.play(-1)


# Initializarea diferitelor tipuri de ship-uri
ships = {"Aircraft Carrier": 4, "Battleship": 3,
         "Submarine": 2, "Destroyer": 1}

root = Tk()
game = Tk()

# Generarea titlului pentru joc cat si pentru meniul principal
game.wm_title("Battleships")
root.wm_title("Main Menu")

# Setarea background-ului de culoare violet pentru joc
game.configure(background='#856ff8')

# Setarea font-urilor pentru text
font1 = Font(family='Times', size=12, weight='bold')
font_big = Font(family='Times', size=16, weight='bold')
font_normal = Font(family='Times', size=10, weight='normal')

AI = False

# reseteaza programul


def restart_program():
    game.destroy()
    os.startfile("main.py")

# Genereaza un array bidimensional care reprezinta tabla unui jucator


def player_board():
    board = []
    t = []
    # Facem marginea de sus, care va fi reprezentata prin '#' si care va avea dimensiunea 12.
    t += (10+2) * ['# ']
    board.append(t)
    # Acum vom face liniile de pe tabla, care vor contine doar '~' in afara de prima si ultima pozitie a fiecarei linii, care reprezinta marginea tablei.
    rad = ['# ']
    for r in range(0, 10):
        rad.append("~ ")
    # Adaugam liniile in tabla
    rad.append('# ')
    for k in range(0, 10):
        board.append(list(rad))
    # Apoi, vom adauga marginea de jos, care, la fel ca si cea de sus, va avea doar '#'
    board.append(t)
    # returneaza o lista bi-dimensionala
    return board

# Genereaza barcile aleator pe tabla


def place_ship(ship, board):
    while True:
        checkcoords = []
        # Generarea coordonatelor
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        # Variabila care va determina daca barca va fi pusa pe orizontal sau vertical
        o = random.randint(0, 1)
        if o == 0:
            ori = "v"
        else:
            ori = "h"
        # Cazurile in care barcile depasesc dimensiunile tablei
        if ori == "v" and y + ships[ship] > 10:
            pass
        elif ori == "h" and x + ships[ship] > 10:
            pass
        else:
            if ori == "v":
                # Vom lua urmatoarea dimensiune a barcii si o vom adauga pe tabla din array-ul checkcoords
                for i in range(-1, (ships[ship] + 1)):
                    for j in range(-1, 2):
                        checkcoords.append(board[y + i][x + j])
                # Daca spatiul determinat pentru o barca nu este deja ocupatt de o alta barca, vom plasa barca noua in aceasta pozitie
                if ': ' not in checkcoords:
                    for i in range(ships[ship]):
                        board[y + i][x] = ': '
                    break
                # La fel ca si pentru pozitia verticala, doar ca verificam in cazul barcilor orizontale
            elif ori == "h":
                for i in range(-1, (ships[ship] + 1)):
                    for j in range(-1, 2):
                        checkcoords.append(board[y + j][x + i])
                if ': ' not in checkcoords:
                    for i in range(ships[ship]):
                        board[y][x + i] = ': '
                    break

# Vom plasa barcile de dimensiuni diferite, + un numar diferit de barci


def place_all_ships(board):
    for ship in ships:
        for antal in range(0, (5 - ships[ship])):
            place_ship(ship, board)


# O fereastra care se va deschide la finalul jocului
def popupwindow(msg):
    # Permite reinsantierea jocului inca odata la cererea utilizatorului
    answer = messagebox.askquestion(
        "Game Over", msg + " Would you like to play again?")
    if answer == 'yes':
        restart_program()
    else:
        quit()


# Determina numarul de jucatori
def nr_players(number):
    global AI
    # Odata ce numarul de jucatori a fost stabilit, sunetul "Let the games begin" va incepe
    mixer.init()
    mixer.music.load("Begin.mp3")
    # Index-ul '0' determina rularea melodiei o singura data
    mixer.music.play(0)
    # Daca avem un singur jucator, label-ul pentru a doua tabla va fi Computer, deoarece ne vom juca cu calculatorul
    if number == 1:
        x = Label(game, text="Computer", font=font_normal,
                  fg="white", bg="#856ff8")
        AI = True
    else:
        # In cazul in care avem 2 jucatori, setam label-ul ca Player 2, pentru al doilea jucator
        x = Label(game, text="Player 2", font=font_normal,
                  fg="white", bg="#856ff8")
    x.place(x=720, y=347)
    # Vom avea un delay de 3 secunde, pentru a putea ramane pe meniul principal si a asculta sunetul mentionat anterior inainte de a se deshide jocul
    time.sleep(3)
    # Distrugem meniul principal
    root.destroy()
    # Deschidem fereastra jocului
    game.deiconify()


info = StringVar()
player2_or_AI = StringVar()
every_button = []

decision = 1


def music_on_off():
    global decision
    # Daca variabila decision are valoarea 1, semnifica ca utilizatorul doreste sa opreasca muzica
    if decision == 1:
        # Vom schimba valoarea variabilei in 2, pentru a putea accesa al doilea caz
        decision = 2
        mixer.music.stop()
        # Schimbam si textul butonului pentru muzica, pentru a marca faptul ca la urmatoarea apasare, muzica va porni
        music = Button(root, width=9, height=1, text="Music ON", font=font1, fg="white", activebackground="#856ff8",
                       bg="CadetBlue", command=lambda: music_on_off())
        music.place(x=690, y=400)
    elif decision == 2:
        decision = 1
        play_music()
        # Marcheaza faptul ca la urmatoarea apasare, se va opri muzica
        music = Button(root, width=9, height=1, text="Music OFF", font=font1, fg="white", activebackground="#856ff8",
                       bg="CadetBlue", command=lambda: music_on_off())
        music.place(x=690, y=400)

# Deschide textbox-ul cu instructiunile jocului


def instr_on_off():
    global text_box
    # Text-ul dorit
    Fact = "     Instructions\nThe game Battleships can either be played versus the computer, or versus a friend! The game contains multiple battleships of different sizes which will pe specified once the game starts, and the aim of the game is to shoot on your opponents bord in order to destroy all of their battleships. All battleships will be randomly generated and placed amongst the board. Once a part of a ship has been hit, the player can continue shooting whilst he keeps hitting other pieces, untill he misses. Have fun!"
    # Cream un text box
    text_box = Text(
        root,
        # Stabilim dimensiunile
        height=22,
        width=25,
        # Opreste separarea unui cuvant atunci cand apare o linie noua, si permite existenta cuvantului intreg.
        wrap=WORD,
        # Setarea fundalului
        bg="gray84"
    )
    text_box.pack(expand=True)
    # Adaugam in textbox text-ul stabilit si memorat in variabila 'Fact'
    text_box.insert('end', Fact)
    text_box.config(state='disabled')
    text_box.place(x=570, y=25)

# Ne intoarce la meniul principal


def back_to_main():
    game.destroy()
    os.startfile("main.py")

# Inchide programul


def on_closing():
    if messagebox.askyesno("Quit", "Do you want to quit?"):
        root.destroy()
        game.destroy()

# Crearea butoanelor si a labelurilor


def side_labels():
    # Determinarea tutror labelurilor si a butoanelor
    Label(game, text="Battleships", fg="white", bg="#856ff8",
          font=font_big).grid(row=0, column=10, columnspan=9)
    Label(game, textvariable=info, fg="white", bg="#856ff8",
          font=font1).grid(row=12, column=6, columnspan=18)
    Label(game, text="Good luck and have fun playing Battleships!",
          fg="purple", bg="#856ff8", font=font_normal).grid(row=10, column=1)

    for _ in range(10):
        Label(game, text="   ", bg="#856ff8").grid(row=_, column=0)
    b1 = Button(root, width=7, height=1, text="1 Player", font=font1, fg="white", activebackground="#856ff8",
                bg="CadetBlue", command=lambda: nr_players(1))
    b1.place(x=300, y=200)
    b2 = Button(root, width=7, height=1, text="2 Players", font=font1, fg="white", activebackground="#856ff8",
                bg="CadetBlue", command=lambda: nr_players(2))
    b2.place(x=400, y=200)
    Button(game, width=7, height=1, text="Exit", font=font1, fg="white", activebackground="#856ff8",
           bg="#856ff8", command=lambda: quit()).grid(row=11, column=25)
    Button(game, width=9, height=1, text="Main Menu", font=font1, fg="white", activebackground="#856ff8",
           bg="#856ff8", command=lambda: back_to_main()).grid(row=10, column=25)
    b3 = Button(root, width=7, height=1, text="Exit", font=font1, fg="white", activebackground="#856ff8",
                bg="CadetBlue", command=lambda: quit())
    b3.place(x=700, y=450)
    Button(game, width=7, height=1, text="Restart", font=font1, fg="white", activebackground="#856ff8",
           bg="#856ff8", command=lambda: restart_program())
    music = Button(root, width=9, height=1, text="Music OFF", font=font1, fg="white", activebackground="#856ff8",
                   bg="CadetBlue", command=lambda: music_on_off())
    music.place(x=690, y=400)
    title = Label(root, text="Welcome to Battleships",
                  font=font_big, fg="white", bg="CadetBlue")
    title.place(x=290, y=50)
    nr = Label(root, text="Please select the number of players:",
               font=font_big, fg="white", bg="CadetBlue")
    nr.place(x=230, y=150)
    instr = Button(root, width=9, height=1, text="Instructions", font=font1, fg="white", activebackground="#856ff8",
                   bg="CadetBlue", command=lambda: instr_on_off())
    instr.place(x=600, y=450)
    Label(game, text="Destroy all the boats to win", font=font_normal,
          fg="white", bg="#856ff8").grid(row=2, column=1)
    Label(game, text="1 Boat with 4 units", font=font_normal,
          fg="white", bg="#856ff8").grid(row=4, column=1)
    Label(game, text="2 Boats with 3 units", font=font_normal,
          fg="white", bg="#856ff8").grid(row=5, column=1)
    Label(game, text="3 Boats with 2 units", font=font_normal,
          fg="white", bg="#856ff8").grid(row=6, column=1)
    Label(game, text="4 Boats with 1 unit  ", font=font_normal,
          fg="white", bg="#856ff8").grid(row=7, column=1)
    # Permite inchiderea programului utilizand butonul X
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Nu permite maximizarea ferestrelor
    root.resizable(False, False)
    game.resizable(False, False)
    for _ in range(10):
        Label(game, text="   ", bg="#856ff8").grid(row=_, column=2)

    for _ in range(10):
        Label(game, width=20, text="   ", bg="#856ff8").grid(row=_, column=25)


score = 0

# Mutarile AI-ului


def ai_shoots(y_coord, x_coord, player_1_board, ai_score):
    global score
    # Daca scorul este 20 pentru AI, acesta a castigat
    if score == 20:
        popupwindow("The computer has won.")
    # Daca AI-ul a lovit o parte din barca, scorul se va incrementa
    if player_1_board[y_coord][x_coord] == ': ':
        score = score + 1
        player_1_board[y_coord][x_coord] = 'X '
        # Vom marca aceasta parte a barcii care a fost lovit prin culoarea rosu si un X
        every_button[0][y_coord - 1][x_coord -
                                     1].configure(text="X", fg="black", bg="red3")
        # Verificam daca mai exista vreo parte a unei barci in stanga barcii lovite
        if player_1_board[y_coord - 1][x_coord] == ': ':
            # Reapelam functia pentru a marca noua parte gasita si pentru a cauta incontinuu daca exista alte parti ale  unei barci
            ai_shoots(y_coord - 1, x_coord, player_1_board, ai_score)
        # Verificam daca mai exista vreo parte a unei barci in dreapta barcii lovite
        elif player_1_board[y_coord + 1][x_coord] == ': ':
            ai_shoots(y_coord + 1, x_coord, player_1_board, ai_score)
        # Verificam daca mai exista vreo parte a unei barci sub barca lovita
        elif player_1_board[y_coord][x_coord - 1] == ': ':
            ai_shoots(y_coord, x_coord - 1, player_1_board, ai_score)
        # Verificam daca mai exista vreo parte a unei barci deasupra barca lovita
        elif player_1_board[y_coord][x_coord + 1] == ': ':
            ai_shoots(y_coord, x_coord + 1, player_1_board, ai_score)
        else:
            # Altfel, generam aleator niste coordonate, unde AI-ul va impusca
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            ai_shoots(y, x, player_1_board, ai_score)
    elif player_1_board[y_coord][x_coord] == 'X ' or player_1_board[y_coord][x_coord] == 'O ':
        # Daca pozitia la care utilizatorul incerce sa impuste a fost deja lovita, incercam o noua pozitie.
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        ai_shoots(y, x, player_1_board, ai_score)
    else:
        # Daca nu nimereste vreo barca, butonul se schimba in 'O'
        player_1_board[y_coord][x_coord] = 'O '
        every_button[0][y_coord - 1][x_coord -
                                     1].configure(text="O", fg="white")


player_score_1 = 0
player_score_2 = 0
# Verifica daca utilizatorul a lovit sau a omis o barca


def hit_or_miss(a, b, board, all_buttons, info, player, player_1_hits, player_2_hits, ai_score, board2):
    global AI
    global player_score_2
    global player_score_1

    # Initializam un textbox, unde vom afisa un mesaj corespunzator
    text_box = Text(
        game,
        height=2,
        width=30,
        wrap=WORD,
        bg="#856ff8"
    )
    text_box.place(x=25, y=250)

    # Daca utilizatorul impusca la o parte care deja a fost lovita
    if board[a + 1][b + 1] == 'O ' or board[a + 1][b + 1] == 'X ':
        # Vom asculta un sunet de metal
        mixer.init()
        mixer.music.load("Metal.mp3")
        mixer.music.play(0)
        # Vom insera in textbox un mesaj care indica ca acel loc deja a fost lovit
        Fact = "You have already fired there! "
        text_box.insert('end', Fact)
        text_box.config(state='disabled')
        # Daca utilizatorul loveste o parte din barca
    elif board[a + 1][b + 1] == ': ':
        # Vom asculta un sunet de explozie
        mixer.init()
        mixer.music.load("Explosion.mp3")
        mixer.music.play(0)
        # Vom insera in textbox un mesaj care indica ca am nimerit o parte din barca
        Fact = "A hit, nice shot! "
        text_box.insert('end', Fact)
        text_box.config(state='disabled')
        board[a + 1][b + 1] = 'X '
        # Marcam partea lovita
        all_buttons[a][b].configure(
            text="X", fg="black", bg="red3", activebackground="red3")
        # Incrementam contorul care indica cate parti a unei barci au fost lovite
        if player == "player 1":
            player_score_1 += 1
        else:
            player_score_2 += 1
    else:
        # Pentru cazul in care am omis lovirea unei barci
        # Vom asculta un sunet de 'splash'
        mixer.init()
        mixer.music.load("Splash.mp3")
        mixer.music.play(0)
        # Inseram in textbox un mesaj care indica ca am omis
        Fact = "Seems like you missed that one!"
        text_box.insert('end', Fact)
        text_box.config(state='disabled')
        board[a + 1][b + 1] = 'O '
        all_buttons[a][b].configure(
            text="O", fg="White", activeforeground="white")
        # Este randul AI-ului
        if AI:
            # Generam niste coordonate aleatoare
            x = random.randint(0, 10)
            y = random.randint(0, 10)
            ai_shoots(y, x, board2, ai_score)
    # Daca scorul unui jucator este 20, am lovit toate barcile si am castigat
    if player_score_1 == 20 or player_score_2 == 20:
        if player == "player 1":
            player = "player 2"
        elif player == "player 2":
            player = "player 1"
        popupwindow(player + " has won!")

# Creem tabla si determinam numarul de jucatori


def side(player, allbuttons):
    # Cream tabla cu barcile jucatorului 1
    if player == "player 1":
        # Tabla va avea 10 linii si 10 coloane
        for row in range(10):
            for column in range(10):
                allbuttons[row][column].grid(row=1 + row, column=4 + column)
        # Adaugam un label care marcheaza faptul ca aceasta tabla contine barcile jucatorului 1
        label2 = Label(game, text="Player 1", font=font1,
                       fg="white", bg="#856ff8")
        label2.grid(row=11, column=4, columnspan=10)
    else:
        # Creem tabla destinata Computer-ului sau pentru jucatorul 2
        # Tabla va avea 10 linii si 10 coloane
        for row in range(10):
            for column in range(10):
                allbuttons[row][column].grid(row=1 + row, column=15 + column)
        # Adaugam un label care indica daca a doua tabla contine barcile computer-ului sau a jucatorului 2
        label3 = Label(game, textvariable=player2_or_AI,
                       font=font1, fg="white", bg="#856ff8")
        label3.grid(row=11, column=15, columnspan=10)


# Facem functionale toate patratele tablelor. Aceastea vor fi tratate ca si butoane
def board_buttons(board, info, player, player_1_hits, player_2_hits, ai_score, board2):
    allbuttons = []
    a = 0
    for i in range(10):
        b = 0
        # Creem un array gol pentru stocarea datelor referitoare la fiecare buton, anume: numarul specific fiecarui buton
        buttons = []
        for j in range(10):
            # Folosim functia 'partial' pentru fiecare buton in parte care permite derviarea unei functii cu n parametrii in una cu mai putine parametrii
            button = Button(game, width=2, height=1, font=font1, bg="sky blue", activebackground="sky blue", command=partial(
                hit_or_miss, a, b, board, allbuttons, info, player, player_1_hits, player_2_hits, ai_score, board2))
            # Adaugam datele butoanelor in array
            buttons.append(button)
            b += 1
        # Adaugam datele intr-o lista apoi intr-o noua variabila
        allbuttons.append(list(buttons))
        a += 1
        # Adaugam toate datele intr-un array principal
    every_button.append(allbuttons)
    side(player, allbuttons)

# Determinam spatiul aflat dintre cele doua table


def middle_board_space():
    for _ in range(10):
        Label(game, text="   ", bg="#856ff8").grid(row=1 + _, column=14)

# Cream design-ul paginii principale


def mainMenu():
    global game
    # Scriem titlul jocului principal
    game.title("Battleships")
    root.geometry('800x500')
    # Folosim o poza ca si fundalul pentru pagina principala
    image1 = Image.open("Battleships.png")
    test = ImageTk.PhotoImage(image1)

    label1 = tkinter.Label(image=test)
    label1.image = test
    # Pozitionam poza
    label1.place(x=0, y=0)


# Functia principala
def main():
    # Apelam pagina principala
    mainMenu()
    # Ascundem pagina cu jocul principal
    game.withdraw()
    # Setarea numarului de lovituri
    player_1_hits = 0
    player_2_hits = 0
    ai_hits = 0
    # Dam drumul la muzica
    play_music()
    # initializam tablele jucatorilor
    player_1_board = player_board()
    player_2_board = player_board()
    # Adaugam avioanele jucatorilor pe table
    place_all_ships(player_1_board)
    place_all_ships(player_2_board)

    info = StringVar()
    side_labels()

    # Creem butoanele specifice fiecarei table, si punem toate label-urile si butoanele necesare
    board_buttons(player_1_board, info, "player 1", player_1_hits,
                  player_2_hits, ai_hits, player_2_board)
    middle_board_space()
    board_buttons(player_1_board, info, "player 2", player_1_hits,
                  player_2_hits, ai_hits, player_2_board)


# Apelam functia principala
main()
# Permite executarea aplicatiei de tkinter, aceasta fiind executata in continuu (loop).
root.mainloop()