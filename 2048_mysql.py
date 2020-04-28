import random, pygame, sys
from pygame.locals import *
from random import randint
import copy
import math
import re
import tkinter as tk
from tkinter import ttk
from mysqlhelper import MysqlHelper

# defining the window size and other different specifications of the window
FPS = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 700
name = '***'
score = 0
data = [['***',0],['***', 0],['***',0],['***',0],['***',0]]
datas = ([['***',0],['***', 0],['***',0],['***',0],['***',0]])
level = 1
boxsize = min(WINDOWWIDTH, WINDOWHEIGHT) // 4;
margin = 5
thickness = 0
# defining the RGB for various colours used
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
LIGHTSALMON = (255, 160, 122)
ORANGE = (221, 118, 7)
LIGHTORANGE = (227, 155, 78)
CORAL = (255, 127, 80)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 0, 150)
colorback = (189, 174, 158)
colorblank = (205, 193, 180)
colorlight = (249, 246, 242)
colordark = (119, 110, 101)

fontSize = [100, 85, 70, 55, 40]

dictcolor1 = {
    0: colorblank,
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 95, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (237, 190, 30),
    8192: (239, 180, 25)}

dictcolor2 = {
    2: colordark,
    4: colordark,
    8: colorlight,
    16: colorlight,
    32: colorlight,
    64: colorlight,
    128: colorlight,
    256: colorlight,
    512: colorlight,
    1024: colorlight,
    2048: colorlight,
    4096: colorlight,
    8192: colorlight}
BGCOLOR = LIGHTORANGE
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

TABLE = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

# 这是登录时候弹出的那个窗口的函数
def log():
    win = tk.Tk()
    win.title("LogIn")
    aLabel = ttk.Label(win, text="A Label")
    aLabel.grid(column=0, row=0)

    def clickMe():
      global name
      name = name1.get()
      print(name)
      win.destroy()
    action = ttk.Button(win, text="Login", command=clickMe)
    action.grid(column=1, row=1)

    ttk.Label(win, text="Enter a name:").grid(column=0, row=0)
    name1 = tk.StringVar()
    nameEntered = ttk.Entry(win, width=20, textvariable=name1)
    nameEntered.grid(column=0, row=1)
    win.mainloop()


def main():
    global FPSCLOCK, screen, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    # 设置屏幕
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('2048')

    showStartScreen()

    while True:
        runGame(TABLE)
        # gameover()


# 这是Button和函数关连的函数，即关于可以点击的Button的按钮
def createButton(text, x, y, width, height, font_size, action=None,):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # if click[0] == 1 and action != None:
    # 如果鼠标在Button范围内并且敲击了左键，执行
    if pygame.mouse.get_pressed()[0] and x + width > mouse[0] > x and y + height > mouse[1] > y:
        action()
    # 如果鼠标在Button范围内，变色
    elif x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, ORANGE, (x, y, width, height))
    # 如果鼠标不在Button范围内，不做任何变化
    else:
        pygame.draw.rect(screen, BGCOLOR, (x, y, width, height))


    smallText = pygame.font.Font('freesansbold.ttf', font_size)
    TextSurf = smallText.render(text, True, WHITE)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(TextSurf, TextRect)


# 显示开始页面
def showStartScreen():
    # the start screen
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('2048', True, WHITE, BGCOLOR)

    while True:
        screen.fill(BGCOLOR)
        # 返回一个旋转后的surface对象，默认是按照逆时针进行旋转的，当angle小于0时则代表的顺时针进行旋转
        display_rect = pygame.transform.rotate(titleSurf1, 0)
        rectangle = display_rect.get_rect()
        rectangle.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 8)
        screen.blit(display_rect, rectangle)

        createButton("Start", 80, 180, 480, 80, 50, start)
        createButton("RankingList", 80, 280, 480, 80, 50, leaderboard)
        createButton("LogIn", 80, 380, 480, 80, 50, login)
        createButton("LogOut", 80, 480, 480, 80, 50, logout)
        createButton("QUIT", 80, 580, 480, 80, 50, terminate)

        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# 敲击开始按钮后对应的start函数，即执行此函数
def start():
    while True:
        screen.fill(BGCOLOR)
        createButton("Easy", 80, 80, 480, 80, 50, easy)
        createButton("Medium ", 80, 240, 480, 80, 50, medium)
        createButton("Hard", 80, 400, 480, 80, 50, hard)

        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# 敲击简单按钮后对应的函数，即执行此函数
def easy():
    global level
    level = 3
    runGame(TABLE)

# 敲击中等按钮后对应的函数，即执行此函数
def medium():
    global level
    level = 2
    runGame(TABLE)

# 敲击中等按钮后对应的函数，即执行此函数
def hard():
    runGame(TABLE)

# 登出函数
def logout():
    global name
    name = "***"
    titleFont = pygame.font.Font('freesansbold.ttf', 40)
    titleSurf1 = titleFont.render('You log out', True, WHITE, BGCOLOR)
    while True:
        screen.fill(BGCOLOR)
        display_rect = pygame.transform.rotate(titleSurf1, 0)
        rectangle = display_rect.get_rect()
        rectangle.center = (WINDOWWIDTH / 2, WINDOWHEIGHT/2)
        screen.blit(display_rect, rectangle)
        showMainMenu()
        pygame.display.update()
        if checkForKeyPress():
            if len(pygame.event.get()) > 0:
                main()
        FPSCLOCK.tick(FPS)



# 在格子里随机填数的函数，有两个参数，第一个是TABLE，就是那整个盘子，第二个是等级，每个level下有不同生成的数不同
def randomfill(TABLE, level):
    # search for zero in the game table and randomly fill the places
    flatTABLE = sum(TABLE, [])
    if 0 not in flatTABLE:
        return TABLE
    empty = False
    w = 0
    while not empty:
        w = randint(0, 15)
        if TABLE[w // 4][w % 4] == 0:
            empty = True
    z = randint(1, 5)
    if level == 1:
        if z == 5:
            TABLE[w // 4][w % 4] = 4
        else:
            TABLE[w // 4][w % 4] = 2
    if level == 2:
        if z == 5:
            TABLE[w // 4][w % 4] = 16
        else:
            TABLE[w // 4][w % 4] = 8
    if level == 3:
        if z == 5:
            TABLE[w // 4][w % 4] = 64
        else:
            TABLE[w // 4][w % 4] = 32
    return TABLE

# 判断是否游戏结束
def gameOver(TABLE):
    # returns False if a box is empty or two boxes can be merged
    x = [-1, 0, 1, 0]
    y = [0, 1, 0, -1]
    for pi in range(4):
        for pj in range(4):
            if TABLE[pi][pj] == 0:
                return False
            for point in range(4):
                if pi + x[point] > -1 and pi + x[point] < 4 and pj + y[point] > -1 and pj + y[point] < 4 and TABLE[pi][
                    pj] == TABLE[pi + x[point]][pj + y[point]]:
                    return False
    return True

#游戏结束后显示的信息
def showGameOverMessage():
    # to show game over screen

    global data
    titleFont = pygame.font.Font('freesansbold.ttf', 60)
    titleSurf1 = titleFont.render('Game Over', True, WHITE, BGCOLOR)
    titleSurf2 = titleFont.render('Your Score:%d'% score, True, WHITE, BGCOLOR)
    showMainMenu()
    put_mysql()


    while True:
        screen.fill(BGCOLOR)
        display_rect = pygame.transform.rotate(titleSurf1, 0)
        rectangle = display_rect.get_rect()
        rectangle.center = (WINDOWWIDTH / 2 , WINDOWHEIGHT / 2 - 100)
        screen.blit(display_rect, rectangle)

        display_rect1 = pygame.transform.rotate(titleSurf2, 0)
        rectangle1 = display_rect1.get_rect()
        rectangle1.center = (WINDOWWIDTH / 2 - 30, WINDOWHEIGHT / 2 + 100)
        screen.blit(display_rect1, rectangle1)

        showMainMenu()
        pygame.display.update()
        if checkForKeyPress():
            if len(pygame.event.get()) > 0:
                global TABLE
                TABLE = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
                main()
        FPSCLOCK.tick(FPS)

#显示主界面
def showMainMenu():
    # to display main menu
    pressKeySurf = BASICFONT.render('Press a key for main menu', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 250, WINDOWHEIGHT - 30)
    screen.blit(pressKeySurf, pressKeyRect)

#检测键盘输入
def checkForKeyPress():
    # checking if a key is pressed or not
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

#画2048游戏界面
def show(TABLE):
    # showing the table
    screen.fill(colorback)
    myfont = pygame.font.SysFont("Arial", 60, bold=True)
    for i in range(4):
        for j in range(4):
            # ((x, y), (width, height))，表示的是所绘制矩形的区域，其中第一个元组(x, y)表示的是该矩形左上角的坐标，第二个元组 (width, height)表示的是矩形的宽度和高度
            pygame.draw.rect(screen, dictcolor1[TABLE[i][j]], (j * boxsize + margin,
                                                               i * boxsize + margin,
                                                               boxsize - 2 * margin,
                                                               boxsize - 2 * margin),
                             thickness)
            if TABLE[i][j] != 0:
                order = int(math.log10(TABLE[i][j]))
                myfont = pygame.font.SysFont("Arial", fontSize[order], bold=True)
                label = myfont.render("%4s" % (TABLE[i][j]), 1, dictcolor2[TABLE[i][j]])
                screen.blit(label, (j * boxsize + 3 * margin, i * boxsize + 9 * margin))


    pygame.display.update()

#运行游戏
def runGame(TABLE):
    TABLE = randomfill(TABLE, level)
    TABLE = randomfill(TABLE, level)
    show(TABLE)
    datas.append(TABLE)
    running = True

    while True:
        createButton("ReStart", 30, 650, 150, 40, 25, restart)
        createButton("OrderStep", 230, 650, 150, 40, 25, order_step)
        createButton("Cancel", 430, 650, 150, 40, 25, cancel)
        # if checkForKeyPress():
        #     pass
        #     pygame.event.get()
        #     return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                print("quit")
                pygame.quit();
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if running:
                    desired_key = None
                    if event.key == pygame.K_UP: desired_key = "w"
                    if event.key == pygame.K_DOWN: desired_key = "s"
                    if event.key == pygame.K_LEFT: desired_key = "a"
                    if event.key == pygame.K_RIGHT: desired_key = "d"

                    if desired_key is None:
                        continue

                    new_table = key(desired_key, copy.deepcopy(TABLE))
                    if new_table != TABLE:
                        global save_TABLE
                        save_TABLE = TABLE
                        TABLE = randomfill(new_table, level)
                        datas.append(TABLE)
                        show(TABLE)
                    if gameOver(TABLE):
                        showGameOverMessage()

# 键入上下左右执行相应函数
def key(DIRECTION, TABLE):
    if DIRECTION == 'w':
        for pi in range(1, 4):
            for pj in range(4):
                if TABLE[pi][pj] != 0: TABLE = moveup(pi, pj, TABLE)
    elif DIRECTION == 's':
        for pi in range(2, -1, -1):
            for pj in range(4):
                if TABLE[pi][pj] != 0: TABLE = movedown(pi, pj, TABLE)
    elif DIRECTION == 'a':
        for pj in range(1, 4):
            for pi in range(4):
                if TABLE[pi][pj] != 0: TABLE = moveleft(pi, pj, TABLE)
    elif DIRECTION == 'd':
        for pj in range(2, -1, -1):
            for pi in range(4):
                if TABLE[pi][pj] != 0: TABLE = moveright(pi, pj, TABLE)
    return TABLE

#向下走
def movedown(pi, pj, T):
    justcomb = False
    while pi < 3 and (T[pi + 1][pj] == 0 or (T[pi + 1][pj] == T[pi][pj] and not justcomb)):
        if T[pi + 1][pj] == 0:
            T[pi + 1][pj] = T[pi][pj]
        elif T[pi + 1][pj] == T[pi][pj]:
            T[pi + 1][pj] += T[pi][pj]
            justcomb = True
            global score
            score += 50
        T[pi][pj] = 0
        pi += 1
    return T

#向左走
def moveleft(pi, pj, T):
    justcomb = False
    while pj > 0 and (T[pi][pj - 1] == 0 or (T[pi][pj - 1] == T[pi][pj] and not justcomb)):
        if T[pi][pj - 1] == 0:
            T[pi][pj - 1] = T[pi][pj]
        elif T[pi][pj - 1] == T[pi][pj]:
            T[pi][pj - 1] += T[pi][pj]
            justcomb = True
            global score
            score += 66
        T[pi][pj] = 0
        pj -= 1
    return T

#向右走
def moveright(pi, pj, T):
    justcomb = False
    while pj < 3 and (T[pi][pj + 1] == 0 or (T[pi][pj + 1] == T[pi][pj] and not justcomb)):
        if T[pi][pj + 1] == 0:
            T[pi][pj + 1] = T[pi][pj]
        elif T[pi][pj + 1] == T[pi][pj]:
            T[pi][pj + 1] += T[pi][pj]
            justcomb = True
            global score
            score += 88
        T[pi][pj] = 0
        pj += 1
    return T

#向上走
def moveup(pi, pj, T):
    justcomb = False
    while pi > 0 and (T[pi - 1][pj] == 0 or (T[pi - 1][pj] == T[pi][pj] and not justcomb)):
        if T[pi - 1][pj] == 0:
            T[pi - 1][pj] = T[pi][pj]
        elif T[pi - 1][pj] == T[pi][pj]:
            T[pi - 1][pj] += T[pi][pj]
            justcomb = True
            global score
            score += 100
        T[pi][pj] = 0
        pi -= 1
    return T

# 这个是显示排行榜的时候，代码复制太多了，弄个函数，让代码少一点
def display(display_content, center_x, center_y):
    display_rect = pygame.transform.rotate(display_content, 0)
    rectangle = display_rect.get_rect()
    rectangle.center = (center_x, center_y)
    screen.blit(display_rect, rectangle)

#从mysql读取
def read_mysql():
    helper = MysqlHelper()
    helper.cursor.execute('select * from 2048_test order by score desc')
    C = helper.cursor.fetchall()
    if len(C) > 4:
        for i in range(5):
            for j in range(2):
                data[i][j] = C[i][j+1]
    else:
        for i in range(len(C)):
            for j in range(2):
                data[i][j] = C[i][j+1]

#放到mysql
def put_mysql():
    helper = MysqlHelper()
    # CREATE TABLE 2048_test(id int primary key auto_increment,name varchar(50),  score int) DEFAULT CHARSET = UTF8mb4;

    insert_sql = 'INSERT INTO 2048_test(name, score)VALUES(%s, %s)'
    shuju = (name, score)
    helper.execute_modify_sql(insert_sql, shuju)

#排行榜执行的函数
def leaderboard():

    read_mysql()
    titleFont = pygame.font.Font('freesansbold.ttf',40)
    titleSurf1 = titleFont.render('ranking list', True, WHITE, BGCOLOR)
    # global data
    name1 = titleFont.render('%s ' % data[0][0], True, WHITE, BGCOLOR)
    score1 = titleFont.render('%s' % data[0][1], True, WHITE, BGCOLOR)
    name2 = titleFont.render('%s ' % data[1][0], True, WHITE, BGCOLOR)
    score2 = titleFont.render('%s' % data[1][1], True, WHITE, BGCOLOR)
    name3 = titleFont.render('%s ' % data[2][0], True, WHITE, BGCOLOR)
    score3 = titleFont.render('%s' % data[2][1], True, WHITE, BGCOLOR)
    name4 = titleFont.render('%s ' % data[3][0], True, WHITE, BGCOLOR)
    score4 = titleFont.render('%s' % data[3][1], True, WHITE, BGCOLOR)
    name5 = titleFont.render('%s ' % data[4][0], True, WHITE, BGCOLOR)
    score5 = titleFont.render('%s' % data[4][1], True, WHITE, BGCOLOR)
    while True:
        screen.fill(BGCOLOR)

        display(titleSurf1, WINDOWWIDTH / 2, 80)
        display(name1, 200, 200)
        display(score1, 450, 200)
        display(name2, 200, 300)
        display(score2, 450, 300)
        display(name3, 200, 400)
        display(score3, 450, 400)
        display(name4, 200, 500)
        display(score4, 450, 500)
        display(name5, 200, 600)
        display(score5, 450, 600)


        showMainMenu()
        pygame.display.update()
        if checkForKeyPress():
            if len(pygame.event.get()) > 0:
                main()
        FPSCLOCK.tick(FPS)


# 登录的函数
def login():
    log()

    titleFont = pygame.font.Font('freesansbold.ttf', 40)
    titleSurf1 = titleFont.render('Your name: %s'%name, True, WHITE, BGCOLOR)
    while True:
        screen.fill(BGCOLOR)
        display_rect = pygame.transform.rotate(titleSurf1, 0)
        rectangle = display_rect.get_rect()
        rectangle.center = (WINDOWWIDTH / 2, WINDOWHEIGHT/2)
        screen.blit(display_rect, rectangle)

        showMainMenu()
        pygame.display.update()
        if checkForKeyPress():
            if len(pygame.event.get()) > 0:
                main()
        FPSCLOCK.tick(FPS)


# 重启函数
def restart():
    TABLE1 = TABLE = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    TABLE1 = randomfill(TABLE1, level)
    TABLE1 = randomfill(TABLE1, level)
    show(TABLE1)

# 上一步
def order_step():
    print(len(datas))
    if len(datas) == 6:
        pass
    # global save_TABLE
    else:
        # 把最后一步的界面删除
        # 显示上一个
        datas.pop(-1)
        show(datas[-1])
# 返回函数
def cancel():
    global TABLE
    TABLE = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    main()

# 结束函数
def terminate():
    pygame.quit()
    sys.exit()


main()