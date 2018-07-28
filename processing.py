import guizero
from math import  sqrt
import copy
import  end


def location(symbol, matrix):
    # trova coordinate (x,y) di "symbol"
    for y in range(15):
        for x in range(20):
            if matrix[x, y] == symbol:
                return x, y


def control_difference(ox,oy,vx,vy):
    # calcola la distanza x,y tra goal e fine
    XD = difference(ox,vx)
    YD = difference(oy,vy)
    return XD,YD

def difference(d,D):
    # calcola la distanza tra d - D>
    return int(sqrt((d-D)*(d-D)))


def set_priority(x, y, matrix):
    # calcola differenza
    XD, YD = control_difference(x, y, location('v', matrix)[0], location('v', matrix)[1])
    ox, oy = x, y
    vx, vy = location('v', matrix)
    priority = ['', '', '', '', '']
    for i in range(1, 3):
        # genera priorita
        if XD > YD:
            if ox < vx:
                priority[i] = 'right'
                priority[i + 2] = 'left'

            else:
                priority[i] = 'left'
                priority[i + 2] = 'right'
            XD = -1
        else:
            if oy > vy:
                priority[i] = 'down'
                priority[i + 2] = 'up'
            else:
                priority[i] = 'up'
                priority[i + 2] = 'down'
            YD = -1
    priority.remove('')

    return priority


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


def walk(matrix, identity_cards):
    x, y = location('o', matrix)
    identity_cards[x, y]['possible'] = 3
    xo, yo = x, y
    crossing = []
    step = []
    error = 0
    old_steps = ['fermo']
    crossing.append('fermo')
    xf, yf = location('v', matrix)
    tmatrix = copy.copy(matrix)
    while tmatrix[xf, yf] == 'v':
        action = 0
        priority = set_priority(x, y, matrix)
        for i in range(4):
            # controlla priorita
            if identity_cards[x, y][priority[i]] == 1:
                xt, yt = direct(priority[i], x, y)
                # controlla casella libera
                if tmatrix[xt, yt] == ' ' or tmatrix[xt, yt] == 'v':
                    tmatrix[xt, yt] = 'O'
                    if identity_cards[x, y]['possible'] > 2:
                        # salva coordinate e direzione degli incroci
                        crossing.append({'coordinate': [x, y], 'direct': priority[i]})
                    # avanzamento
                    x, y = xt, yt
                    action += 1
                    step.append(priority[i])
                    break
        if action == 0:
            error += 1
            tmatrix = copy.copy(matrix)
            x, y = xo, yo
            old_steps.append(step[:])
            step.clear()

            # controllo possibilita risoluzzione
            if old_steps[-1] == old_steps[-2]:
                guizero.warn(title='error', text='It is impossible go forward')
                return ['impossible']
            else:
                # prova modifica incrocio
                try:
                    xt, yt = crossing[-1]['coordinate'][0], crossing[-1]['coordinate'][1]
                    identity_cards[xt, yt][crossing[-1]['direct']] = 0
                    identity_cards[xt, yt]['possible'] -= 1
                except TypeError:
                    guizero.warn(title='Error', text='It is impossible go forward')
                    return ['impossible']
    guizero.info(title='', text=('Error number ', error))
    return step


def start(matrix,identity_cards,desktop):
    steps=walk(matrix,identity_cards)
    if steps[-1]!='impossible':
         end.start(steps,matrix,desktop,0)