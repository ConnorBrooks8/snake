from Tkinter import *
import threading
import time
import random
#Size Variables
MINCOORD=1
GRIDSPACE=15
SnakeWidth = 30
DotWidth = 10
MAXCOORD=GRIDSPACE*(SnakeWidth+1)+2
#Arrow Key Codes
RightKey='Right'
LeftKey='Left'
UpKey='Up'
DownKey='Down'

class Snake:

    def __init__(self,master):
        #Set Up main Frame and Canvas
        self.frame = Frame(master)
        self.frame.pack()
        self.frame.bind('<Key>',self.key)
        self.frame.focus_set()

        self.canvas = Canvas(master, width=MAXCOORD, height=MAXCOORD)
        self.canvas.pack()
        self.canvas.create_line(MINCOORD,MINCOORD,MINCOORD,MAXCOORD)
        self.canvas.create_line(MINCOORD,MINCOORD,MAXCOORD,MINCOORD)
        self.canvas.create_line(MINCOORD,MAXCOORD,MAXCOORD,MAXCOORD)
        self.canvas.create_line(MAXCOORD,MINCOORD,MAXCOORD,MAXCOORD)
        
        self.button = Button(self.frame, text="QUIT",fg="red",command=self.quit)
        self.button.pack(side=LEFT)

        self.start = Button(self.frame, text="Start",command=self.startgame)
        self.start.pack(side=LEFT)

        self.highscore = Button(self.frame, text="HighScores",command=self.highscore)
        self.highscore.pack(side=LEFT)


        self.score=0
        self.scorestring= StringVar()
        self.scorestring.set("Score: %d" % self.score)

        self.scorebutton = Label(self.frame, textvariable=self.scorestring)
        self.scorebutton.pack(side=LEFT)

        scorefile = open("highscores.txt","r")
        self.highscore=[]
        for i in range(10):
            rawline = scorefile.readline()
            rawscore = rawline.split(" ")
            hscore = [0,""]
            hscore[0] = int(rawscore[0])
            hscore[1] = rawscore[1].strip()
            self.highscore.append(hscore)
        scorefile.close()

        self.highscorestring=StringVar()
        self.highscorestring.set("Highscore: %d" % self.highscore[0][0])

        self.highlabel = Label(self.frame, textvariable=self.highscorestring)
        self.highlabel.pack(side=LEFT)

    def key(self,event):
        if event.keysym == RightKey:
            self.direction= "right"
        if event.keysym == LeftKey:
            self.direction="left"
        if event.keysym == UpKey:
            self.direction="up"
        if event.keysym == DownKey:
            self.direction="down"


    def startgame(self):

        DefaultDirection= 'right'
        DefaultHead=[(SnakeWidth+1)*3+2,(SnakeWidth+1)+2]
        DefaultEnd=[(SnakeWidth+1)+2,(SnakeWidth+1)+2]
        
        self.updatehighscore()

        #reset game
        self.canvas.delete(ALL)
        
        self.score=0
        self.scorestring.set("Score: %d" % self.score)

        self.canvas.create_line(MINCOORD,MINCOORD,MINCOORD,MAXCOORD)
        self.canvas.create_line(MINCOORD,MINCOORD,MAXCOORD,MINCOORD)
        self.canvas.create_line(MINCOORD,MAXCOORD,MAXCOORD,MAXCOORD)
        self.canvas.create_line(MAXCOORD,MINCOORD,MAXCOORD,MAXCOORD)

        self.direction= DefaultDirection
        self.head=DefaultHead
        self.end=DefaultEnd
        self.quitgame=False
        self.eat=False
        
        #Create Initial Snake
        self.item=self.canvas.create_rectangle(self.head[0],self.head[1],self.head[0]+SnakeWidth,self.head[1]+SnakeWidth,fill="green",tag=DefaultDirection)
        self.canvas.create_rectangle(self.head[0]-SnakeWidth,self.head[1],self.head[0],self.head[1]+SnakeWidth,fill="green",tag="right")
        self.canvas.create_rectangle(self.head[0]-(2*SnakeWidth),self.head[1],self.head[0]-SnakeWidth,self.head[1]+SnakeWidth,fill="green",tag="right")

        dotoverlap=True
        while dotoverlap==True:
            dotx = random.randint(MINCOORD,MAXCOORD-DotWidth)
            doty = random.randint(MINCOORD,MAXCOORD-DotWidth)
            dotoverlap = bool(self.canvas.find_overlapping(dotx,doty,dotx+DotWidth,doty+DotWidth))
 

        self.canvas.create_rectangle(dotx,doty,dotx+DotWidth,doty+DotWidth,fill='red',tag='dot')


        threading.Thread(target=self.gameloop).start()


    def gameloop(self):
        while self.quitgame==False:
            
            self.grow()
            if self.eat==False:
                self.delete()
            else:
                self.eat=False
            time.sleep(0.1)

    def grow(self): 
        
        if self.direction=="right":
            self.head[0]=self.head[0]+(SnakeWidth+1)
            self.canvas.itemconfig(self.item,tag='right')        
            self.eatcollide()
            self.draw()
        if self.direction=="left":
            self.head[0]=self.head[0]-(SnakeWidth+1)
            self.canvas.itemconfig(self.item,tag='left')
            self.eatcollide()
            self.draw()
        if self.direction=="up":
            self.head[1]=self.head[1]-(SnakeWidth+1)
            self.canvas.itemconfig(self.item,tag='up')
            self.eatcollide()
            self.draw()
        if self.direction=="down":
            self.head[1]=self.head[1]+(SnakeWidth+1)
            self.canvas.itemconfig(self.item,tag='down')
            self.eatcollide()
            self.draw()


    def eatcollide(self):
        overlap =self.canvas.find_overlapping(self.head[0],self.head[1],self.head[0]+SnakeWidth,self.head[1]+SnakeWidth) 
        for i in overlap:
            if bool(self.canvas.gettags(i))==True:
                if self.canvas.gettags(i)[0] == 'dot':
                    self.eat=True
                    self.canvas.delete(i)
                
                    dotoverlap=True
                    while dotoverlap==True:
                        dotx = random.randint(MINCOORD,MAXCOORD-DotWidth)
                        doty = random.randint(MINCOORD,MAXCOORD-DotWidth)
                    
                        dotoverlap = bool(self.canvas.find_overlapping(dotx,doty,dotx+DotWidth,doty+DotWidth))
        

                    self.score = self.score + 1
                    self.scorestring.set("Score: %d" % self.score)

                    if self.score > self.highscore:
                        self.highscore = self.score
                        self.highscorestring.set("Highscore: %d" % self.highscore[0][0])

                    self.canvas.create_rectangle(dotx,doty,dotx+DotWidth,doty+DotWidth,fill='red',tag='dot')
                else:
                    self.endgame()
            else:
                self.endgame()
        if self.head[0]>MAXCOORD-(SnakeWidth+1) or self.head[0]<MINCOORD or self.head[1]>MAXCOORD-(SnakeWidth+1) or self.head[1]<MINCOORD:
            self.endgame()
    def delete(self):
        endbox = self.canvas.find_closest(self.end[0],self.end[1])[0]

        if self.canvas.gettags(endbox)[0]=="right":
            self.end[0]=self.end[0]+(SnakeWidth+1)
        if self.canvas.gettags(endbox)[0]=="left":
            self.end[0]=self.end[0]-(SnakeWidth+1)
        if self.canvas.gettags(endbox)[0]=="up":
            self.end[1]=self.end[1]-(SnakeWidth+1)
        if self.canvas.gettags(endbox)[0]=="down":
            self.end[1]=self.end[1]+(SnakeWidth+1)

        self.canvas.delete(endbox)


    def draw(self): 
        self.item = self.canvas.create_rectangle(self.head[0],self.head[1],self.head[0]+SnakeWidth,self.head[1]+SnakeWidth,fill="green")

    def highscore(self):
        
        t = Toplevel(root)
        t.wm_title("Highscore")
        labels = []
        for i in range(10):
            labels.append(Label(t, text=(self.highscore[i][1] + ": " + str(self.highscore[i][0]))))
            labels[i].pack(side="top")
    
    def getkey(self, item):
        return item[0]
    
    def updatehighscore(self):
        if (self.score > self.highscore[9][0]):
            initials = raw_input("Enter your Initials: ")
            self.highscore.append([self.score, initials])
            print(self.highscore)
            self.highscore = sorted(self.highscore,key=self.getkey,reverse=True)[0:10]
            print(self.highscore)

        scorefile = open("highscores.txt","w")
        for i in range(10):
            scorefile.write(str(self.highscore[i][0]) + " " + self.highscore[i][1] + "\n")
        scorefile.close()
    def endgame(self):
        self.quitgame = True
        self.updatehighscore()

    def quit(self):
        self.endgame()
        
        time.sleep(1)
        self.frame.quit()


root = Tk()
app = Snake(root)
root.mainloop()
