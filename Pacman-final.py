
import math
import turtle
from turtle import Turtle
import random
import time
import numpy as np

global game_state
game_state = "start"
global end
end = False
global started
started = False
global t3
t3 = 0
global notf 
notf = 0
FONT = ("Arial", 24, "bold")
turtle.color("pink")

wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Pacman")
wn.setup(800, 800)
wn.tracer(0)
global btngone
btngone = 0


images = ["rsz_ghost.gif", "rsz_ghost3.gif", "rsz_gh.gif", "rsz_gh2.gif", "rsz_pl3.gif", "rsz_coin1.gif", "rsz_wall.gif",
          "rsz_energy.gif","rsz_fruit2.gif","gameover.gif","win.gif","white.gif"]
for i in images:
    turtle.register_shape(i)

def start_game():

    global player
    player = Player()
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(200, 300)
    turtle.write("Score: {}".format(player.gold), font=FONT, align="left")


    a = 0
    setup_maze(levels[1])

    # keyboard
    turtle.listen()
    turtle.onkey(player.go_left, "Left")
    turtle.onkey(player.go_right, "Right")
    turtle.onkey(player.go_up, "Up")
    turtle.onkey(player.go_down, "Down")

    for e in enemies:
        e.mode = "chase"
        e.target(player.xcor(), player.ycor(), player)

        turtle.ontimer(e.move, t=1050)


class Graphics:
    def __init__(self):
        self.turtle = Turtle(visible=False)
        self.turtle.speed('fastest')

    def text_at_xy(self, x, y, text):
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.write(text, font=FONT)


class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)


class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("rsz_pl3.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self):
        # self.goto(self.xcor(), self.ycor() + 24)
        move_to_x = player.xcor()
        move_to_y = player.ycor() + 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = player.xcor() - 24
        move_to_y = player.ycor()
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = player.xcor() + 24
        move_to_y = player.ycor()
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if (distance < 5):
            return True
        else:
            return False


class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("rsz_coin1.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

class Fruit(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("rsz_fruit2.gif")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 1000
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


class Energy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("rsz_energy.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


class Enemy(turtle.Turtle):
    def __init__(self, x, y, ghst, shp, mde="chase"):
        turtle.Turtle.__init__(self)
        self.shape(shp)
        self.color("white")
        self.penup()
        self.speed(0)
        self.gold = 200
        self.goto(x, y)
        self.prevx = [0, 0]
        self.prevy = [0, 0]
        self.nextx = []
        self.nexty = []
        self.targetx = 0
        self.targety = 0
        self.mode = mde
        self.ghost = ghst

    def dist(self, x1, y1, x2, y2):
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def target(self, x, y, other):
        if (self.mode == "chase"):
            if (self.ghost == 1):
                self.targetx = other.xcor()
                self.targety = other.ycor()
            if (self.ghost == 2):
                if (self.dist(self.xcor(), self.ycor(), other.xcor(), other.ycor()) < 800 * 24):
                    self.targetx = other.xcor()
                    self.targety = other.ycor()
                else:
                    self.targetx = random.randrange(-1200, 1200)
                    self.targety = random.randrange(-1200, 1200)

        if (self.mode == "frightened"):
            self.targetx = -other.xcor()
            self.targety = -other.ycor()

        ##@rifat start
        ## just defineing the positin for rounding at 15 second
        ##rsz_gh2.gif ghost rounding around the (240,-216) point
        ##rsz_gh1.gif ghost rounding around the (-192,-216) point

        if (self.mode == "scattered"):
            if self.ghost == 1:
                self.targetx = -192
                self.targety = -216
            else:
                self.targetx = 192
                self.targety = -216
        ##@rifat
        
    def move(self):
        global t3
        global notf
        if done == 1:
            self.goto(self.xcor(), self.ycor())
        else:
            self.nextx = []
            self.nexty = []
            dx = 0
            dy = 24
            self.nextx.append(self.xcor() + dx)
            self.nexty.append(self.ycor() + dy)

            dx = 0
            dy = -24
            self.nextx.append(self.xcor() + dx)
            self.nexty.append(self.ycor() + dy)

            dx = -24
            dy = 0
            self.nextx.append(self.xcor() + dx)
            self.nexty.append(self.ycor() + dy)

            dx = 24
            dy = 0
            self.nextx.append(self.xcor() + dx)
            self.nexty.append(self.ycor() + dy)

            minm = 9999999
            movex = 90
            movey = 80
            i = -1
           
            while (i <= 3):
                i = i + 1
                if (i >= len(self.nextx)):
                    break
                

                if (self.nextx[i], self.nexty[i]) in walls:
                    continue
                elif (self.nextx[i] == self.prevx[self.ghost - 1] and self.nexty[i] == self.prevy[self.ghost - 1]):
                    continue
                distance = self.dist(self.nextx[i], self.nexty[i], self.targetx, self.targety)
                if (distance < minm):
                    minm = self.dist(self.nextx[i], self.nexty[i], self.targetx, self.targety)
                    movex = self.nextx[i]
                    movey = self.nexty[i]

            self.prevx[self.ghost - 1] = self.xcor()
            self.prevy[self.ghost - 1] = self.ycor()
            self.goto(movex, movey)

            if self.mode == "frightened":
                print("In fright")
                t1 = time.clock() - t0
                t3 = 999
                if t1 >= 15:
                    notf = 1
                    if self.ghost == 1:
                        self.shape("rsz_gh.gif")
                    elif self.ghost == 2:
                        self.shape("rsz_gh2.gif")
                    self.mode = "chase"
                    t3 = 0
            elif self.mode != "frightened":
                print("In scattered")
                t3 += 1
                if t3 < 50:
                    self.mode = "scattered"
                    self.shape("rsz_ghost3.gif")
                elif t3 >50:
                    self.mode = "chase"
                    if self.ghost == 1:
                        self.shape("rsz_gh.gif")
                    else:
                        self.shape("rsz_gh2.gif")
                elif t3 > 150:
                    t3 = 0
                    #turtle.ontimer(self.move, t=400)
                    

            ##@rifat  end      

            # move in interval
            turtle.ontimer(self.move, t=random.randint(300, 500))

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

    wn.update()





def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)
            if (character == "X"):
                pen.goto(screen_x, screen_y)
                pen.shape("rsz_wall.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))  # add as tuple/pair
            if (character == "P"):
                player.goto(screen_x, screen_y)
            if (character == 'T'):
                treasures.append(Treasure(screen_x, screen_y))
            if (character == 'I'):
                enemies.append(Enemy(screen_x, screen_y, 1, "rsz_gh.gif", "chase"))
            if (character == 'B'):
                enemies.append(Enemy(screen_x, screen_y, 2, "rsz_gh2.gif", "chase"))
            if (character == 'E'):
                energies.append(Energy(screen_x, screen_y))
            if (character == 'F'):
                fruits.append(Fruit(screen_x, screen_y))


def btnclk(x, y):
    global done
    global game_state
    global started
    global end
    global btngone
    btngone = 1
    print(x,y)
    if x < 50 and x > -21 and y < -210 and y > -235:
        turtle.Screen().bye()
    elif x < 85 and x > -50 and y < -240 and y > -270:
        game_state = "start"
        started = False
        end = False
        turtle.clear()
        turtle.clear()
    


def buttons():
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(-30, -230)
    turtle.pendown()
    turtle.begin_fill()
    turtle.fillcolor('red')
    turtle.fd(80)
    turtle.left(90)
    turtle.fd(30)
    turtle.left(90)
    turtle.fd(80)
    turtle.left(90)
    turtle.fd(30)
    turtle.left(90)
    turtle.end_fill()

    turtle.color("black")
    turtle.write("  QUIT", font=("Arial", 15, "bold"))

    turtle.hideturtle()
    turtle.penup()
    turtle.goto(-50, -40-230)
    turtle.pendown()
    turtle.begin_fill()
    turtle.fillcolor('red')
    turtle.fd(130)
    turtle.left(90)
    turtle.fd(30)
    turtle.left(90)
    turtle.fd(130)
    turtle.left(90)
    turtle.fd(30)
    turtle.left(90)
    turtle.end_fill()

    turtle.color("black")
    turtle.write(" RESTART", font=("Arial", 15, "bold"))
    
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(-100, 350)
    turtle.write("Final  Score: {}".format(player.gold), font=FONT, align="left")

    turtle.onscreenclick(btnclk)


# main loop
global done
done = 0
global levels
levels = [""]
global level_1
level_1 =     ["XXXXXXXXXXXXXXXXXXXXXXXXXXX",
               "XP                       BX",
               "X                         X",
               "X  XX    XXXXXXXXX    XX  X",
               "X  XX     XXXXXXXT    XX  X",
               "X    XX   XXXXXXX  XX     X",
               "X    XX    XXXXXE  XX     X",
               "X  X   XX    X    XX   X  X",
               "X  XX  XX    X    XX  XX  X",
               "X  XXX    T          XXX  X",
               "X  XXXE              XXX  X",
               "X  XXXXXX    X    XXXXXX  X",
               "X  XXX               XXX  X",
               "X  XXX          T    XXX  X",
               "X  XX  XX    X    XX  XX  X",
               "X  X   XX    X    XX   X  X",
               "X   TXX    XXXXX    XX    X",
               "X    XX   XXXXXXX   XX    X",
               "X         XXXXXXX         X",
               "X  XX    XXXXXXXXX  XX   FX",
               "X  XX               XX    X",
               "X        I                X",
               "XXXXXXXXXXXXXXXXXXXXXXXXXXX", ]
levels.append(level_1)

# add treasures
global treasures
treasures = []
global player
global enemies
enemies = []
global energies
energies = []
global fruits
fruits = []
global pen
pen = Pen()
global t0
t0 = 0
global walls
walls = []
a = 0
##@rifat
b = 0
t2 = 0
max_distance =196600




while True:
    if game_state == "start":
        if started == False:
            if btngone == 1:
                turtle.clear()
                btngone = 0
                wn.bgpic("white.gif")
            started = True
            start_game()

        # Stop screen updates
        wn.tracer(0)
        # turtle.clear()
        for treasure in treasures:
            if player.is_collision(treasure):
                #turtle.clear()

                player.gold += treasure.gold
                print(player.gold)
                treasure.destroy()
                treasures.remove(treasure)
                turtle.clear()
                turtle.penup()
                turtle.goto(200, 300)
                turtle.hideturtle()
                turtle.write("Score: {}".format(player.gold), font=FONT, align="left")

        for e in enemies:

            if player.is_collision(e):
                if e.mode == "chase":
                    game_state = "game over"
                    break
                elif e.mode == "frightened":
                    e.destroy()
            #print("######## :",enemies[0].xcor(),enemies[0].ycor())
            e.target(player.xcor(), player.ycor(), player)

        for energy in energies:
            if player.is_collision(energy):
                energy.destroy()
                for e in enemies:
                    e.shape("rsz_ghost.gif")
                    e.mode = "frightened"
                    print("fright start")
                    t0 = time.clock()
                    

        """#@Rifat Scattered start

        ###take the ghost position for array with just accessing array address
        first_ghost_x=enemies[0].xcor();
        first_ghost_y=enemies[0].ycor();
        second_ghost_x=enemies[1].xcor();
        second_ghost_y=enemies[1].ycor();
        distance_between = (first_ghost_x-second_ghost_x)**2 + (first_ghost_y - second_ghost_y)**2

        #print (" rifat : ",enemies[1].xcor(),enemies[1].ycor())
        #if (enemies[1].xcor()== -72 and enemies[1].ycor() == -216) or (enemies[0].xcor()== -48 and enemies[0].ycor() == -216) :
        ## define max_distance=196600
        if distance_between > max_distance:
            #print (" rifat : ",enemies[1].xcor(),enemies[1].ycor())
            enemies[1].mode = "scattered"
            enemies[0].mode = "scattered"
            #turtle.ontimer(enemies[1].move, t=250)
            if b ==0:
                t2 = time.clock()
                b = 1

        #@Rifat Scattered end"""


        for fruit in fruits:
            if player.is_collision(fruit):
                game_state = "win"
                break

    # Update screen
    elif game_state == "game over" or game_state == "win":
        # turtle.done()
        if game_state == "game over":
            wn.bgpic("gameover.gif")
        else:
            wn.bgpic("win.gif")
        if not end:
            end = True
            pen.clear()
            turtle.clear()
            player.hideturtle()
            for e in enemies:
                e.destroy()
            for t in treasures:
                t.destroy()
            for energy in energies:
                energy.destroy()
            for fruit in fruits:
                fruit.destroy()

        for e in enemies:
            e.goto(e.xcor(), e.ycor())
        buttons()

    wn.update()
