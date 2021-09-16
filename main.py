# from table import *
from random import *
from tkinter import *

# ГЛОБАЛКИ
B = 15 # размер поля B*B
M = 30 # кол-во мин 
Clear = B*B-M # кол-во обычных ячеек
Table = [] # основная таблица данных
Buttons = [[0 for i in range(B)] for j in range(B)] # таблица кнопок

def init(): # инициализация с генерацией мин
    Temp = ["0"]*B*B
    for i in range(M):
        Temp[i] = "*"
    shuffle(Temp)
    for i in range(B):
        temp = []
        for j in range(B):
            temp.append(Temp[B*i+j])
        Table.append(temp)
    for i in range(B):
        for j in range(B):
            if Table[i][j] == "*":
                check_mine(i, j)
    show()

def check_mine(ii, jj): # изменение значений клеток
    for i in range(-1, 2):
        for j in range(-1, 2):
            if inTable(ii+i,jj+j) and Table[ii+i][jj+j] != "*":
                Table[ii+i][jj+j] = str(int(Table[ii+i][jj+j]) + 1)

def show(): # вывод таблицы на экран cmd
    for i in range(len(Table)):
        for j in range(len(Table)):
            print(Table[i][j], end=" ")
        print()
    print("-----------------------------------------")

def b_restart(): # перезапуск
    global Table
    global Clear
    Table = []
    restart["image"] = photo1
    Clear = B*B-M
    init()
    for i in range(B):
        for j in range(B):
            Buttons[i][j]["state"] = NORMAL
            Buttons[i][j]["relief"] = RAISED
            Buttons[i][j]["text"] = ""
            Buttons[i][j]["bg"] = "SystemButtonFace"

def inTable(i,j): # проверка в рамках таблицы
    return i>=0 and i<B and j>=0 and j<B

def ai_click(i,j): # автооткрывашка
    if Buttons[i][j]["state"] == DISABLED and Table[i][j] != "*":
        m_ = int(Table[i][j])
        for x in range(-1,2):
            for y in range(-1,2):
                if inTable(i+x,j+y):
                    if Buttons[i+x][j+y]["text"] == "?": #and Table[i+x][j+y] == "*":
                        m_ -= 1
        if m_ == 0:
            for x in range(-1,2):
                for y in range(-1,2):
                    if inTable(i+x,j+y): #and Table[i+x][j+y] != "*":
                        b_click(i+x,j+y)

def b_click_r(event,i,j): # клик правой
    if Buttons[i][j]["state"] == NORMAL and Buttons[i][j]["text"] == "":
        Buttons[i][j]["text"] = "?"
        for x in range(-1,2):
            for y in range(-1,2):
                if inTable(i+x,j+y):
                    ai_click(i+x,j+y)
    elif Buttons[i][j]["state"] == NORMAL and Buttons[i][j]["text"] == "?":
        Buttons[i][j]["text"] = ""

def b_click(i,j): # клик левой
    global Clear
    if Buttons[i][j]["state"] == NORMAL and Buttons[i][j]["text"] == "":
        Buttons[i][j]["state"] = DISABLED
        Buttons[i][j]["relief"] = FLAT#GROOVE
        if Table[i][j] == "0":
            Clear -= 1
            Buttons[i][j]["text"] = " "
            for x in range(-1,2):
                for y in range(-1,2):
                    if inTable(x+i,y+j) and Table[i+x][j+y] != "*":
                        b_click(i+x,j+y)
        elif Table[i][j] == "*":
            restart["image"] = photo2
            Buttons[i][j]["text"] = " "
            Buttons[i][j]["bg"] = "#CC1122"
            for i_ in range(B):
                for j_ in range(B):
                    Buttons[i_][j_]["state"] = DISABLED
                    Buttons[i_][j_]["relief"] = RIDGE
                    if Table[i_][j_] == "*":
                        Buttons[i_][j_]["bg"] = "#CC1122"
        else:
            Buttons[i][j]["text"] = Table[i][j]
            Clear -= 1
    if Clear == 0:
        Clear -= 1
        restart["image"] = photo3
        for i_ in range(B):
            for j_ in range(B):
                Buttons[i_][j_]["relief"] = RIDGE
                if Table[i_][j_] == "*":
                    Buttons[i_][j_]["bg"] = "#11CC22"
                    Buttons[i_][j_]["state"] = DISABLED

# print("------------------------------------------------")
root = Tk()
root.title("minrpg")
photo1 = PhotoImage(file="1")
photo2 = PhotoImage(file="2")
photo3 = PhotoImage(file="3")
restart = Button(root,image=photo1,command=b_restart)
restart.grid(row=0,column=0,columnspan=B)
init()
for i in range(B):
    for j in range(B):
        cmd = lambda x=i,y=j: b_click(x,y)
        Buttons[i][j] = Button(root,width=3,height=1,command=cmd,font="Helvetica 8 bold")
        cmd2 = lambda z=0,x=i,y=j: b_click_r(z,x,y)
        Buttons[i][j].bind('<Button-3>', cmd2)
        Buttons[i][j].grid(row=i+1,column=j)
root.mainloop()
