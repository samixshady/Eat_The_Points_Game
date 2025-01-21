from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# 0 --> pacman
# 1 --> end goal
# 2,3,4,5,6 --> enemies
# 2,3,4 moves along x axis
# 5,6 moves along y axis
# 7-21 --> points
# 22,23 --> minus enemies

is_paused = False
score = 0
game_over = False
win = False
level = 1
Highscore= 0

grid10 = []
for i in range(-230,231):
    if i%10 == 0:
        grid10.append(i)
    else:
        pass

##Menu Parameters
START_GAME_MENU = 1
PAUSE_MENU = 2
RESET_GAME_MENU = 3
EXIT_MENU = 4
##Menu Parameters

center_x = [0,0,random.randint(-250,250),random.randint(-250,250),random.randint(-250,250),random.randint(-250,250),random.randint(-250,250),grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],random.randint(-250,250),random.randint(-250,250)]
center_y = [-230,190,random.randint(-250,250),random.randint(-250,250),random.randint(-250,250),random.randint(-250,250),random.randint(-250,250),grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],grid10[random.randint(0,46)],random.randint(-250,250),random.randint(-250,250)]
circle_radius = [20,10,20,20,20,20,20,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,20,20]
no_circle = 24
flag = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
mouth = 1

pause = 0
xspeed = 0.5
yspeed = 0.5
store_speed = 0
timer = 0
hard = 1

def zerozoneconverter(x,y,centerx,centery,zone): #modification for center works
    tempx = x-centerx
    tempy = y-centery
    if zone == 0:
        return x,y
    elif zone == 1:
        return tempy+centerx,tempx+centery
    elif zone == 2:
        tempx = tempx*-1
        return tempy+centerx,tempx+centery
    elif zone == 3:
        tempx = tempx*-1
        return tempx+centerx,tempy+centery
    elif zone == 4:
        tempx = tempx*-1
        tempy = tempy*-1
        return tempx+centerx,tempy+centery
    elif zone == 5:
        tempx = tempx*-1
        tempy = tempy*-1
        return tempy+centerx,tempx+centery
    elif zone == 6:
        tempy = tempy*-1
        return tempy+centerx,tempx+centery
    else:
        tempy = tempy*-1
        return tempx+centerx,tempy+centery

def zonedetector(x,y,centerx,centery): #modification for center done
    tempx = x-centerx
    tempy = y-centery
    if x>=centerx and y>=centery:
        if tempx>=tempy:
            return 0
        else:
            return 1
    elif x<centerx and y>=centery:
        if (-1*tempx)>tempy:
            return 3
        else:
            return 2
    elif x<centerx and y<centery:
        if (-1*tempx)>(-1*tempy):
            return 4
        else:
            return 5
    else:
        if tempx>(-1*tempy):
            return 7
        else:
            return 6

def otherzoneconverter(x,y,centerx,centery,desirezone): #modification for center done
    tempx = x
    tempy = y
    if desirezone == 0:
        return x,y
    elif desirezone == 1:
        tempx -= centerx
        tempy -= centery
        return tempy+centerx,tempx+centery
    elif desirezone == 2:
        tempx -= centerx
        tempy -= centery
        tempy = tempy *-1
        return tempy+centerx,tempx+centery
    elif desirezone == 3:
        tempx -= centerx
        tempy -= centery
        tempx = tempx*-1
        return tempx+centerx,tempy+centery
    elif desirezone == 4:
        tempx -= centerx
        tempy -= centery
        tempx = tempx*-1
        tempy = tempy*-1
        return tempx+centerx,tempy+centery
    elif desirezone == 5:
        tempx -= centerx
        tempy -= centery
        tempx = tempx*-1
        tempy = tempy*-1
        return tempy+centerx,tempx+centery
    elif desirezone == 6:
        tempx -= centerx
        tempy -= centery
        tempx = tempx*-1
        return tempy+centerx,tempx+centery
    else:
        tempx -= centerx
        tempy -= centery
        tempy = tempy*-1
        return tempx+centerx,tempy+centery

def midalgoSE(radius,centerx,centery,size,index,arr=[0,1,2,3,4,5,6,7]): #modification for center done
    global center_x,center_y,circle_radius,no_circle,flag
    x = 0
    y = radius
    d = 1.25-(radius)
    for i in arr:
        temp_x,temp_y = otherzoneconverter(x+centerx,y+centery,centerx,centery,i)
        draw_points(temp_x,temp_y,size)

    while x<=y:
        if d<0:
            d=d+2*x+3
            x=x+1
        else:
            d=d+2*x-(2*y)+5
            x=x+1
            y=y-1
        for i in arr:
            tempx,tempy = otherzoneconverter(x+centerx,y+centery,centerx,centery,i)
            draw_points(tempx,tempy,size)

def draw_points(x, y, s):
    glPointSize(s) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

##Menu Handler
def draw_menu():
    glColor3f(1, 1, 1)
    draw_menu_text(-80, 120, "Reach The Finish Line")
    draw_menu_text(-70, 100, "Press 'S' to Start")
    draw_menu_text(-70, 80, "Press 'P' to Pause")
    draw_menu_text(-70, 60, "Press 'R' to Reset")
    draw_menu_text(-70, 40, "Press 'ESC' to Exit")

def draw_menu_text(x, y,text):
    glRasterPos2f(x,y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18,ord(char))

def draw_text(x, y,text,score):
    text+=str(score)

    glRasterPos2f(x,y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18,ord(char))

def draw_text_empty(x, y,text):
    glRasterPos2f(x,y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18,ord(char))

def main_menu_handler(option):
    if option == EXIT_MENU:
        glutLeaveMainLoop()

def game_menu_handler(option):
    global is_paused, game_over, win
    if option == START_GAME_MENU:
        is_paused = False
        game_over = False
        win = False
        reset_game()
    elif option == PAUSE_MENU:
        is_paused = not is_paused
    elif option == RESET_GAME_MENU:
        reset_game()
    elif option == EXIT_MENU:
        glutLeaveMainLoop()

def main_menu_handler(option):
    if option == EXIT_MENU:
        glutLeaveMainLoop()

##Menu Handler

def midalgoNE(x0,y0,x1,y1,centerx,centery,size,arr): #modification for center done
    dx = x1-x0
    dy = y1-y0
    d=(2*dy)-dx
    incrE = 2*dy
    incrNE = 2*(dy-dx)
    x = x0
    y = y0
    for i in arr:
        temp_x,temp_y = otherzoneconverter(x,y,centerx,centery,i)
        draw_points(temp_x,temp_y,size)

    while x<x1:
        if d<=0:
            d=d+incrE
            x=x+1
        else:
            d=d+incrNE
            x=x+1
            y=y+1
        for i in arr:
            tempx,tempy = otherzoneconverter(x,y,centerx,centery,i)
            draw_points(tempx,tempy,size)        

def display():
    global center_x, center_y, circle_radius, timer, score, game_over, win, is_paused, mouth, Highscore,level

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200,  0, 0, 0,  0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
   
    #x button
    glColor3f(1,0,0)
    midalgoNE(230,230,250,250,230,230,1,[0,2,4,6])
    #back button
    glColor3f(0,0,1)
    midalgoNE(-250,230,-230,250,-250,230,1,[0,7])
    midalgoNE(-250,230,-210,230,-210,230,1,[0])
    #pause button
    glColor3f(1,1,0)
    midalgoNE(-30,230,0,220,220,0,1,[5])
    midalgoNE(0,240,30,240,250,0,1,[5])
   
    if game_over:
        glColor3f(1, 0, 0)
        draw_text(-100, 0, "Game Over! Final Score: ", score)
        draw_text_empty(-170, -80, "Press '2' In-Game To Increase Speed By 2x", )
        glColor3f(0, 1, 0)
        draw_text(-40, -30, "Highscore ", Highscore)
        level=1
        draw_menu()
       # if game_over:

    elif win:
        glColor3f(0, 1, 0)
        draw_text(-130, 0, "YOU WIN, CONGRATS!! Score:", score)
        draw_text(-60, -60, "Current Level: " , level)
        draw_text_empty(-145, -90, "Press 'n' To Proceed To Next Level")
        draw_text_empty(-180, -120, "Press '2' In-Game To Increase Speed By 2x", )
        glColor3f(0, 1, 0)
        draw_text(-40, -30, "Highscore ", Highscore)
        draw_menu()
    elif is_paused:
        glColor3f(1, 1, 1)
        draw_text_empty(-50, 0, "Game Paused")
    else:
        # Draw end goal
        glColor3f(0, 1, 0)
        midalgoSE(circle_radius[1], center_x[1], center_y[1], 5, 1)
        midalgoSE(circle_radius[1] - 5, center_x[1], center_y[1], 5, 1)
        midalgoSE(circle_radius[1] - 9, center_x[1], center_y[1], 5, 1)

        # Draw pacman
        glColor3f(1, 1, 0)
        if mouth == 1:
            midalgoSE(circle_radius[0], center_x[0], center_y[0], 5, 0, [1,2,4,5,6,7])
            midalgoSE(circle_radius[0] - 5, center_x[0], center_y[0], 5, 0,[1,2,4,5,6,7])
            midalgoSE(circle_radius[0] - 10, center_x[0], center_y[0], 5, 0,[1,2,4,5,6,7])
            midalgoSE(circle_radius[0] - 15, center_x[0], center_y[0], 5, 0,[1,2,4,5,6,7])
            midalgoSE(circle_radius[0] - 19, center_x[0], center_y[0], 5, 0,[1,2,4,5,6,7])
            if circle_radius[0] > 24:
                midalgoSE(circle_radius[0] - 24, center_x[0], center_y[0], 5, 0,[1,2,4,5,6,7])
            if circle_radius[0] > 29:
                midalgoSE(circle_radius[0] - 29, center_x[0], center_y[0], 5, 0,[1,2,4,5,6,7])
            if circle_radius[0] > 34:
                midalgoSE(circle_radius[0] - 34, center_x[0], center_y[0], 5, 0,[1,2,4,5,6,7])          
        if mouth == 2:
            midalgoSE(circle_radius[0], center_x[0], center_y[0], 5, 0, [0,2,3,4,5,7])
            midalgoSE(circle_radius[0] - 5, center_x[0], center_y[0], 5, 0,[0,2,3,4,5,7])
            midalgoSE(circle_radius[0] - 10, center_x[0], center_y[0], 5, 0,[0,2,3,4,5,7])
            midalgoSE(circle_radius[0] - 15, center_x[0], center_y[0], 5, 0,[0,2,3,4,5,7])
            midalgoSE(circle_radius[0] - 19, center_x[0], center_y[0], 5, 0,[0,2,3,4,5,7])
            if circle_radius[0] > 24:
                midalgoSE(circle_radius[0] - 24, center_x[0], center_y[0], 5, 0, [0,2,3,4,5,7])
            if circle_radius[0] > 29:
                midalgoSE(circle_radius[0] - 29, center_x[0], center_y[0], 5, 0, [0,2,3,4,5,7])
            if circle_radius[0] > 34:
                midalgoSE(circle_radius[0] - 34, center_x[0], center_y[0], 5, 0, [0,2,3,4,5,7])  
        if mouth == 3:
            midalgoSE(circle_radius[0], center_x[0], center_y[0], 5, 0, [0,1,2,3,5,6])
            midalgoSE(circle_radius[0] - 5, center_x[0], center_y[0], 5, 0,[0,1,2,3,5,6])
            midalgoSE(circle_radius[0] - 10, center_x[0], center_y[0], 5, 0,[0,1,2,3,5,6])
            midalgoSE(circle_radius[0] - 15, center_x[0], center_y[0], 5, 0,[0,1,2,3,5,6])
            midalgoSE(circle_radius[0] - 19, center_x[0], center_y[0], 5, 0,[0,1,2,3,5,6])
            if circle_radius[0] > 24:
                midalgoSE(circle_radius[0] - 24, center_x[0], center_y[0], 5, 0,[0,1,2,3,5,6])
            if circle_radius[0] > 29:
                midalgoSE(circle_radius[0] - 29, center_x[0], center_y[0], 5, 0,[0,1,2,3,5,6])
            if circle_radius[0] > 34:
                midalgoSE(circle_radius[0] - 34, center_x[0], center_y[0], 5, 0,[0,1,2,3,5,6])  
        if mouth == 4:
            midalgoSE(circle_radius[0], center_x[0], center_y[0], 5, 0, [0,1,3,4,6,7])
            midalgoSE(circle_radius[0] - 5, center_x[0], center_y[0], 5, 0, [0,1,3,4,6,7])
            midalgoSE(circle_radius[0] - 10, center_x[0], center_y[0], 5, 0, [0,1,3,4,6,7])
            midalgoSE(circle_radius[0] - 15, center_x[0], center_y[0], 5, 0, [0,1,3,4,6,7])
            midalgoSE(circle_radius[0] - 19, center_x[0], center_y[0], 5, 0, [0,1,3,4,6,7])
            if circle_radius[0] > 24:
                midalgoSE(circle_radius[0] - 24, center_x[0], center_y[0], 5, 0,[0,1,3,4,6,7])
            if circle_radius[0] > 29:
                midalgoSE(circle_radius[0] - 29, center_x[0], center_y[0], 5, 0,[0,1,3,4,6,7])
            if circle_radius[0] > 34:
                midalgoSE(circle_radius[0] - 34, center_x[0], center_y[0], 5, 0,[0,1,3,4,6,7])  

        #points
        glColor3f(1,1,0)
        for i in range(7,22):
            midalgoSE(circle_radius[i],center_x[i],center_y[i],5,i)
            midalgoSE(circle_radius[i]-4,center_x[i],center_y[i],3,i)
       
        #minus enymies
        glColor4f(1,0,1,0)
        #minuseenem1
        midalgoSE(circle_radius[22],center_x[22],center_y[22],5,22)
        midalgoSE(circle_radius[22]-5,center_x[22],center_y[22],5,22)
        midalgoSE(circle_radius[22]-10,center_x[22],center_y[22],5,22)
        midalgoSE(circle_radius[22]-15,center_x[22],center_y[22],5,22)
        midalgoSE(circle_radius[22]-19,center_x[22],center_y[22],5,22)

        #minuseenem2
        midalgoSE(circle_radius[23],center_x[23],center_y[23],5,23)
        midalgoSE(circle_radius[23]-5,center_x[23],center_y[23],5,23)
        midalgoSE(circle_radius[23]-10,center_x[23],center_y[23],5,23)
        midalgoSE(circle_radius[23]-15,center_x[23],center_y[23],5,23)
        midalgoSE(circle_radius[23]-19,center_x[23],center_y[23],5,23)              

        #enemies
        glColor3f(1,0,0)
        #enemy1
        midalgoSE(circle_radius[2],center_x[2],center_y[2],5,2)
        midalgoSE(circle_radius[2]-5,center_x[2],center_y[2],5,2)
        midalgoSE(circle_radius[2]-10,center_x[2],center_y[2],5,2)
        midalgoSE(circle_radius[2]-15,center_x[2],center_y[2],5,2)
        midalgoSE(circle_radius[2]-19,center_x[2],center_y[2],5,2)

        #enemy2
        midalgoSE(circle_radius[3],center_x[3],center_y[3],5,3)
        midalgoSE(circle_radius[3]-5,center_x[3],center_y[3],5,3)
        midalgoSE(circle_radius[3]-10,center_x[3],center_y[3],5,3)
        midalgoSE(circle_radius[3]-15,center_x[3],center_y[3],5,3)
        midalgoSE(circle_radius[3]-19,center_x[3],center_y[3],5,3)

        #enemy3
        midalgoSE(circle_radius[4],center_x[4],center_y[4],5,4)
        midalgoSE(circle_radius[4]-5,center_x[4],center_y[4],5,4)
        midalgoSE(circle_radius[4]-10,center_x[4],center_y[4],5,4)
        midalgoSE(circle_radius[4]-15,center_x[4],center_y[4],5,4)
        midalgoSE(circle_radius[4]-19,center_x[4],center_y[4],5,4)

        #enemy4
        midalgoSE(circle_radius[5],center_x[5],center_y[5],5,5)
        midalgoSE(circle_radius[5]-5,center_x[5],center_y[5],5,5)
        midalgoSE(circle_radius[5]-10,center_x[5],center_y[5],5,5)
        midalgoSE(circle_radius[5]-15,center_x[5],center_y[5],5,5)
        midalgoSE(circle_radius[5]-19,center_x[5],center_y[5],5,5)

        #enemy5
        midalgoSE(circle_radius[6],center_x[6],center_y[6],5,6)
        midalgoSE(circle_radius[6]-5,center_x[6],center_y[6],5,6)
        midalgoSE(circle_radius[6]-10,center_x[6],center_y[6],5,6)
        midalgoSE(circle_radius[6]-15,center_x[6],center_y[6],5,6)
        midalgoSE(circle_radius[6]-19,center_x[6],center_y[6],5,6)
    glutSwapBuffers()

def keyboardListener(key, x, y):
    global is_paused, center_x, center_y, circle_radius, no_circle, flag, score, game_over, win,level,hard

    if key == b' ':
        is_paused = not is_paused
    elif key == b'r' or key == b'R':
        reset_game()
    elif key == b'\x1b':  # 'Esc' key
        glutLeaveMainLoop()
    elif key == b's' or key == b'S':
        if game_over or win:
            reset_game()
    elif key == b'n' or key==b"N":
        if win:
            level=level+1
            next_level_reset_game()
    elif key == b'2':
        if hard == 1:
            hard = 2
        else:
            hard = 1

    glutPostRedisplay()

##Level System
def next_level_reset_game():
    global center_x, center_y, circle_radius, flag, score, game_over, win, xspeed, yspeed, mouth,level

    print(f"You Have Proceeded To Next Level",{level})
    # Reset pacman
    center_x[0] = 0
    center_y[0] = -230
    circle_radius[0] = 20
    mouth = 1

    # Reset end goal
    center_x[1] = 0
    center_y[1] = 190
    circle_radius[1] = 10

    # Reset points
    for i in range(7, 22):
        center_x[i] = grid10[random.randint(0, 46)]
        center_y[i] = grid10[random.randint(0, 46)]
        circle_radius[i] = 5

    # Reset enemies
    for i in range(2, 7):
        center_x[i] = random.randint(-250, 250)
        center_y[i] = random.randint(-250, 250)
        flag[i] = random.choice([0, 1])

    # Reset minus enemies
    center_x[22] = random.randint(-250, 250)
    center_y[22] = random.randint(-250, 250)
    center_x[23] = random.randint(-250, 250)
    center_y[23] = random.randint(-250, 250)

    # Reset speed and other variables
    xspeed = xspeed + 0.5
    yspeed = yspeed + 0.5
    game_over = False
    win = False
    glutPostRedisplay()
##Level System

##Reset Game
def reset_game():
    global center_x, center_y, circle_radius, flag, score, game_over, win, xspeed, yspeed, mouth

    # Reset pacman
    center_x[0] = 0
    center_y[0] = -230
    circle_radius[0] = 20
    mouth = 1

    # Reset end goal
    center_x[1] = 0
    center_y[1] = 190
    circle_radius[1] = 10

    # Reset points
    for i in range(7, 22):
        center_x[i] = grid10[random.randint(0, 46)]
        center_y[i] = grid10[random.randint(0, 46)]
        circle_radius[i] = 5

    # Reset enemies
    for i in range(2, 7):
        center_x[i] = random.randint(-250, 250)
        center_y[i] = random.randint(-250, 250)
        flag[i] = random.choice([0, 1])

    # Reset minus enemies
    center_x[22] = random.randint(-250, 250)
    center_y[22] = random.randint(-250, 250)
    center_x[23] = random.randint(-250, 250)
    center_y[23] = random.randint(-250, 250)

    # Reset speed and other variables
    score = 0
    game_over = False
    win = False
    xspeed = 0.5
    yspeed = 0.5
    glutPostRedisplay()
##Reset Game
def specialKeyListener(key, x, y):
    global center_x, center_y, is_paused, mouth
    if not is_paused:
        if key == GLUT_KEY_LEFT:
            if center_x[0] <= -230:
                pass
            else:
                center_x[0] -= 10
            mouth = 4
        elif key == GLUT_KEY_RIGHT:
            if center_x[0] >= 230:
                pass
            else:
                center_x[0] += 10
            mouth = 2
        elif key == GLUT_KEY_UP:
            if center_y[0] >= 230:
                pass
            else:
                center_y[0] += 10
            mouth = 1
        elif key == GLUT_KEY_DOWN:
            if center_y[0] <= -230:
                pass
            else:
                center_y[0] -= 10
            mouth = 3
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global center_x, center_y, circle_radius, no_circle, flag, is_paused

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            center_x.append(x - 250)
            center_y.append(250 - y)
            circle_radius.append(0)
            no_circle += 1
            flag.append(0)

    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
         print("Mouse Clicked at (", x, ",", y, ")")  
         if 0 <= x <= 50 and 0 <= y <= 50:
            reset_game()  # Clicked within the Back button area
         elif 240 <= x <= 260 and 0 <= y <= 40: ##Pause
             is_paused = not is_paused
         elif 450 <= x <= 490 and 0 <= y <= 50: ##Close
             glutLeaveMainLoop()
         #elif
         #glutPostRedisplay()
           
def check_collision(x1, y1, r1, x2, y2, r2):
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance < (r1 + r2)
def animate():
    glutPostRedisplay()
    global center_x, center_y, circle_radius, no_circle, xspeed, yspeed, score, game_over, win,hard,Highscore
    if not is_paused:
        if not game_over and not win:
            # points
            for i in range(7, 22):
                if check_collision(center_x[0], center_y[0], circle_radius[0], center_x[i], center_y[i],
                                   circle_radius[i]):
                    score += 1
                    print("Score:", score)
                    # Increase pacman radius by +5
                    circle_radius[0] += 1
                    center_x[i] += 1000
                    center_y[i] += 1000

            for i in range(2, 7):
                if check_collision(center_x[0], center_y[0], circle_radius[0], center_x[i], center_y[i],
                                   circle_radius[i]):
                    print("Game Over! Your final score:", score)
                    if score > Highscore:
                        Highscore = score
                        print("New Highscore is", Highscore)
                    else:
                        print("Highscore is", Highscore)
                    game_over = True

            if check_collision(center_x[0], center_y[0], circle_radius[0], center_x[1], center_y[1],
                                   circle_radius[1]):
                print("YOU WIN, CONGRATS!!")
                if score > Highscore:
                    Highscore = score
                    print("New Highscore is", Highscore)

                else:
                    print("Highscore is", Highscore)
                win = True

            for i in range(22, 24):
                if check_collision(center_x[0], center_y[0], circle_radius[0], center_x[i], center_y[i],
                                   circle_radius[i]):
                    score -= 1
                    print("Score:", score)
                    # Increase pacman radius by +5
                    circle_radius[0] += 1
                    center_x[i] += 1000
                    center_y[i] += 1000

            for i in range(2, 5):
                if flag[i] == 1:
                    center_x[i] -= xspeed*hard
                elif flag[i] == 0:
                    center_x[i] += xspeed*hard
                else:
                    pass

                if center_x[i] > 230:
                    flag[i] = 1
                elif center_x[i] < -230:
                    flag[i] = 0
                else:
                    pass

            for j in range(5, 7):
                if flag[j] == 1:
                    center_y[j] -= yspeed*hard
                elif flag[j] == 0:
                    center_y[j] += yspeed*hard
                else:
                    pass

                if center_y[j] > 230:
                    flag[j] = 1
                elif center_y[j] < -230:
                    flag[j] = 0
                else:
                    pass

            for i in range(22, 23):
                if flag[i] == 1:
                    center_x[i] -= xspeed*hard
                elif flag[i] == 0:
                    center_x[i] += xspeed*hard
                else:
                    pass

                if center_x[i] > 230:
                    flag[i] = 1
                elif center_x[i] < -230:
                    flag[i] = 0
                else:
                    pass

            for j in range(23,24):
                if flag[j] == 1:
                    center_y[j] -= yspeed*hard
                elif flag[j] == 0:
                    center_y[j] += yspeed*hard
                else:
                    pass

                if center_y[j] > 230:
                    flag[j] = 1
                elif center_y[j] < -230:
                    flag[j] = 0
                else:
                    pass
           
            for i in range(7,22):
                if circle_radius[i] == 5:
                    circle_radius[i] = 4
                else:
                    circle_radius[i] = 5

def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1,  1,  1000.0)

glutInit()
glutCreateMenu(main_menu_handler)
glutCreateMenu(game_menu_handler)
glutAddMenuEntry("Start Game", START_GAME_MENU)
glutAddMenuEntry("Pause", PAUSE_MENU)
glutAddMenuEntry("Reset Game", RESET_GAME_MENU)
glutAddMenuEntry("Exit", EXIT_MENU)
glutAttachMenu(GLUT_RIGHT_BUTTON)
glutInitWindowSize(500,600)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Reach the finish line!")
gluOrtho2D(-250, 250, -250, 350)
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()
