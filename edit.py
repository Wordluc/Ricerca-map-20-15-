import guizero
from math import  sqrt
import copy
import processing


class box:
    def __init__(self,x,y,identity_card,master,text_box,directs,option):
        self.step=guizero.PushButton(master,grid=[x,y],command=self.press,image='white.png')
        self.identity_card=identity_card
        self.text_box=text_box
        self.x=x
        self.y=y
        self.directs=directs
        self.option=option


    def press(self):
        if self.identity_card[self.directs.value]==1:
            self.option.text='On'
        else:
            self.option.text='Off'
        self.option.update_command(self.edit)
        self.text_box.value=self.identity_card

    def edit(self):
        if self.identity_card[self.directs.value]==1:
            self.option.text='Off'
            self.identity_card[self.directs.value]=0
            guizero.info(title='Modification performed',text=[' Deactivated',self.directs.value,])
        else:
            guizero.warn(title='Error modification',text=['It is impossible deactivated ',self.directs.value])
        self.text_box.value = self.identity_card



def location(symbol,matrix):
    #trova coordinate (x,y) di "symbol"
    for y in range(15):
        for x in range(20):
            if matrix[x,y]==symbol:
                return x,y

def control(T,n):
    #controlla se T è una coordinata accettabile
    if (T < n and T >= 0):
        return 1
    else:
        return 0


def analyze_possible(matrix,x,y,n):
    #analizza cella[x,y] e trova i vari passaggi possibili
    identity_card={'up':0,'down':0,'left':0,'right':0}
    yt = y + 1
    i = 0
    if control(yt, n)==1:
        if matrix[x,yt]==' ':
            identity_card['up']=1
            i += 1
    yt = y - 1
    if control(yt, n) == 1:
        if matrix[x, yt] == ' ':
            identity_card['down'] = 1
            i += 1
    xt = x + 1
    if control(xt, n) == 1:
        if matrix[xt, y] == ' ':
            identity_card['right'] = 1
            i += 1
    xt = x - 1
    if control(xt, n) == 1:
        if matrix[xt, y] == ' ':
            identity_card['left'] = 1
            i += 1
    identity_card['possible']=i
    return identity_card


def make_cards(matrix):
    #crea un carta d'identita per ogni cella
    identity_cards={}
    copy_matrix = copy.copy(matrix)
    #elimina in copy_matrix inizio(o) e fine(v)
    copy_matrix[location('o',matrix)] = ' '
    copy_matrix[location('v', matrix)] = ' '
    for y in range(20):
        for x in range(20):
           identity_cards[x,y]=analyze_possible(copy_matrix,x,y,n)#genera carte d'identita
    return identity_cards


def analyze_possible(matrix,x,y):
    #analizza cella[x,y] e trova i vari passaggi possibili
    identity_card={'up':0,'down':0,'left':0,'right':0}
    yt = y + 1
    i = 0
    if control(yt, 15)==1:
        if matrix[x,yt]==' ':
            identity_card['up']=1
            i += 1
    yt = y - 1
    if control(yt, 15) == 1:
        if matrix[x, yt] == ' ':
            identity_card['down'] = 1
            i += 1
    xt = x + 1
    if control(xt, 20) == 1:
        if matrix[xt, y] == ' ':
            identity_card['right'] = 1
            i += 1
    xt = x - 1
    if control(xt, 20) == 1:
        if matrix[xt, y] == ' ':
            identity_card['left'] = 1
            i += 1
    identity_card['possible']=i
    return identity_card


def make_cards(matrix):
    #crea un carta d'identita per ogni cella
    identity_cards={}
    copy_matrix = copy.copy(matrix)
    #elimina in copy_matrix inizio(o) e fine(v)
    copy_matrix[location('o',matrix)] = ' '
    copy_matrix[location('v', matrix)] = ' '
    for y in range(15):
        for x in range(20):
           identity_cards[x,y]=analyze_possible(copy_matrix,x,y)#genera carte d'identita
    return identity_cards


def save_(identity_cards,road,matrix,desktop):
    processing.start(matrix, copy_value(identity_cards,road), desktop)


def copy_value(identity_cards,road):
    for y in range(15):
        for x in range(20):
            identity_cards[x,y]=road[x,y].identity_card
    return  identity_cards

def edit_identity_cards(identity_cards,matrix,desktop):

    windows=guizero.Window(desktop,layout='grid',title='Edit',visible=False)
    road={}
    text_box=guizero.TextBox(windows,grid=[20,0],width=45,enabled=False)
    end = guizero.PushButton(windows, grid=[20, 1], text='End',command=lambda: save_(identity_cards, road, matrix, windows))
    directs=guizero.Combo(windows,options=["up", "down", "left","right"],grid=[20,2])
    option=guizero.PushButton(windows,grid=[20,4],text='Nome')

    y=14
    for i in range(15):
        for x in range(20):
            dictionary = {'X': 'black', 'o': 'green', ' ': 'white', 'v': 'yellow'}
            road[x,y]=box(x,i,identity_cards[x,y],windows,text_box,directs,option)
            road[x,y].step.bg=dictionary[matrix[x,y]]
        y-=1

    windows.show(wait=True)


def start(matrix,desktop):
    edit_identity_cards(make_cards(matrix),matrix,desktop)
