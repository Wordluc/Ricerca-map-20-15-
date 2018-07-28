import guizero
import copy
from math import  sqrt


n_steps=0
xd=0
yd=0

def location(symbol, matrix):
    # trova coordinate (x,y) di "symbol"
    for y in range(15):
        for x in range(20):
            if matrix[x, y] == symbol:
                return x, y


def direct(priority, x, y):
    if priority == 'up':
        y += 1
    elif priority == 'down':
        y -= 1
    elif priority == 'right':
        x += 1
    else:
        x -= 1
    return x, y


def control(T,n):
    #controlla se T è una coordinata accettabile
    if (T < n and T >= 0):
        return 1
    else:
        return 0


def control_difference(ox,oy,vx,vy):
    # calcola la distanza x,y tra goal e fine
    XD = difference(ox,vx)
    YD = difference(oy,vy)
    return XD,YD

def difference(d,D):
    # calcola la distanza tra d - D>
    return int(sqrt((d-D)*(d-D)))


def forward(step,road,n,windows):
    global n_steps
    global xd
    global yd
    n-=1
    if n_steps!=n+1 :

        xd, yd = direct(step[n_steps], xd, yd)
        road[xd, yd].bg = 'green'
        guizero.Text(windows,grid=[xd,14-yd],text=n_steps+1,bg='green')
        n_steps += 1
    else:
        if guizero.yesno(title='',text='You want to go out?')==1:
            windows.destroy()


def visualize(matrix,steps,image,desktop,n_step):
    windows=guizero.Window(desktop,layout='grid',visible=False,title='End')
    dictionary = {'X': 'black', 'o': 'green', ' ': 'white', 'v': 'yellow'}
    global n_steps
    n_steps=n_step
    global xd
    global yd
    y=14
    xd,yd=location('o',matrix)
    road={}
    for iy in range(15):
        for ix in range(20):
            road[ix,iy]=guizero.Picture(windows,image=image,grid=[ix,y])
            road[ix,iy].bg=dictionary[matrix[ix,iy]]
        y-=1
    windows.show(wait=True)
    guizero.PushButton(windows, text='Go forward', grid=[(ix + 1), 0], command=lambda: forward(steps, road, int(len(steps)), windows))


def start(steps,matrix,desktop,n_step):
    visualize(matrix,steps,'white.png',desktop,n_step)