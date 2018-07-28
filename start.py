import guizero
from math import  sqrt
import edit

substitute='X'

class grid:
    def __init__(self,x,y,master,_imag,value,_dictionary):
       self.value=value
       self.dictionary=_dictionary
       self.button = guizero.PushButton(master,grid=[x,y],text='',image=_imag,command= self.input)
       self.button.bg = 'black'

    def input(self):
        global substitute
        self.value=substitute
        self.button.bg = self.dictionary[substitute]


def command(S,color):
    global substitute
    if S=='X':
        substitute= 'X'
        color.value='Wall'
    elif S==' ':
        substitute = ' '
        color.value = 'Road'
    elif S=='o':
        substitute = 'o'
        color.value = 'Start'
    elif S=='v':
        substitute = 'v'
        color.value = 'Goal'


def copy(_matrix):
    # crea matrice con valori di _matrix
    matrix={}
    y=14
    for i in range(15):
        for x in range(20):
            matrix[x,y]=_matrix[x,i].value
        y=y-1
    return matrix


def save(matrix,desktop):
    #controllo matrix
    control={'o':0,'v':0}
    i=0
    for y in range(15):
        for x in range(20):
            if matrix[x,y].value == 'o':
                  i=i+1
                  control['o'] +=1
            if matrix[x,y].value == 'v':
                  i=i+1
                  control['v'] += 1

    if control['v']==1 and control['o']==1:
        edit.start(copy(matrix),desktop)
    else:
        guizero.warn(title='error',text='You have forgot something')


def clean(matrice,dictionary):
    #pulisce matrice e colore celle
    for y in range(15):
        for x in range(20):
            matrice[x,y].value='X'
            matrice[x,y].button.bg=dictionary['X']



matrix = {}
dictionary = {'X': 'black', 'o': 'green', ' ': 'white', 'v': 'yellow'}

# GUI -->
desktop = guizero.App(title='Start',layout='grid',visible=False,)
picture='white.png'

# BUTTON
color=guizero.Text(desktop,grid=[20,0],text='Wall')
wall=guizero.PushButton(desktop,grid=[20,1],command=lambda:command('X',color),text='')
road=guizero.PushButton(desktop,grid=[20,2],command=lambda:command(' ',color),text='')
start=guizero.PushButton(desktop,grid=[20,3],command=lambda:command('o',color),text='')
goal=guizero.PushButton(desktop,grid=[20,4],command=lambda :command('v',color),text='')
end=guizero.PushButton(desktop,text='analyze',grid=[20,5],command=lambda:save(matrix,desktop))
cancel=guizero.PushButton(desktop,text='cancel',grid=[20,6],command=lambda:clean(matrix,dictionary))
wall.bg="#404040"
road.bg='white'
start.bg='green'
goal.bg='yellow'
# GUI <--

for iy in range(15):
    for ix in range(20):
        matrix[ix, iy] = grid(ix, iy, desktop, picture, 'X', dictionary)

desktop.show()
desktop.display()