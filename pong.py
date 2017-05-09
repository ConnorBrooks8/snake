from Tkinter import *
import threading
import time
import random
#Size Variables
TIMESTEP=0.01

MINCOORDX=1
MINCOORDY=1
MAXCOORDX=500
MAXCOORDY=300

PADDLEWIDTH=5
PADDLELENGTH=50
PADDLEX=MINCOORDX+50
AIPADDLEX=MAXCOORDX-50

#Arrow Key Codes
RightKey='Right'
LeftKey='Left'
UpKey='Up'
DownKey='Down'

class Pong:

    def __init__(self,master):
        #Set Up main Frame and Canvas
        self.frame = Frame(master)
        self.frame.pack()
        self.frame.bind('<Key>',self.key)
        self.frame.focus_set()

        self.canvas = Canvas(master, width=MAXCOORDX, height=MAXCOORDY)
        self.canvas.pack()
        self.canvas.create_line(MINCOORDX,MINCOORDY,MINCOORDX,MAXCOORDY)
        self.canvas.create_line(MINCOORDX,MINCOORDY,MAXCOORDX,MINCOORDY)
        self.canvas.create_line(MINCOORDX,MAXCOORDY,MAXCOORDX,MAXCOORDY)
        self.canvas.create_line(MAXCOORDX,MINCOORDY,MAXCOORDX,MAXCOORDY)
        
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

        scorefile = open("highscorespong.txt","r")
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
        if event.keysym == UpKey:
            self.direction="up"
        if event.keysym == DownKey:
            self.direction="down"


    def startgame(self):

        self.updatehighscore()

        #reset game
        self.canvas.delete(ALL)
        
        self.score=0
        self.scorestring.set("Score: %d" % self.score)


        self.canvas.create_line(MINCOORDX,MINCOORDY,MINCOORDX,MAXCOORDY)
        self.canvas.create_line(MINCOORDX,MINCOORDY,MAXCOORDX,MINCOORDY)
        self.canvas.create_line(MINCOORDX,MAXCOORDY,MAXCOORDX,MAXCOORDY)
        self.canvas.create_line(MAXCOORDX,MINCOORDY,MAXCOORDX,MAXCOORDY)

        DefaultPaddlePos=1

        self.paddlePos=DefaultPaddlePos
        self.aiPaddlePos=DefaultPaddlePos
        self.direction="up"

        self.draw()



        self.quitgame=False

        threading.Thread(target=self.gameloop).start()


    def gameloop(self):
        while self.quitgame==False:
            
            self.move()
            self.draw()
            time.sleep(TIMESTEP)


    def move(self):
        if self.direction == "up":
            if self.paddlePos > MINCOORDY:
                self.paddlePos = self.paddlePos -1

        if self.direction == "down":
            if self.paddlePos < MAXCOORDY-PADDLELENGTH:
                self.paddlePos = self.paddlePos +1

    def draw(self):

        self.canvas.delete(ALL)
        self.canvas.create_line(MINCOORDX,MINCOORDY,MINCOORDX,MAXCOORDY)
        self.canvas.create_line(MINCOORDX,MINCOORDY,MAXCOORDX,MINCOORDY)
        self.canvas.create_line(MINCOORDX,MAXCOORDY,MAXCOORDX,MAXCOORDY)
        self.canvas.create_line(MAXCOORDX,MINCOORDY,MAXCOORDX,MAXCOORDY)


        
        
        self.canvas.create_rectangle(PADDLEX,self.paddlePos,PADDLEX+PADDLEWIDTH,self.paddlePos+PADDLELENGTH,fill="green",tag="paddle")

        self.canvas.create_rectangle(AIPADDLEX,self.aiPaddlePos,AIPADDLEX+PADDLEWIDTH,self.aiPaddlePos+PADDLELENGTH,fill="green",tag="paddle")


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
app = Pong(root)
root.mainloop()

