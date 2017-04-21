from Tkinter import *
import threading
import time
import random
#Define Some Variables
MINCOORD=1
MAXCOORD=122
RightKey='Right'
LeftKey='Left'
UpKey='Up'
DownKey='Down'
DefaultDirection= 'right'
DefaultHead=[34,12]
DefaultEnd=[16,16]

class Snake:

    def __init__(self,master):

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
        #clear things
        self.direction= DefaultDirection
        self.head=DefaultHead
        self.end=DefaultEnd
        self.quit=False
        self.eat=False

        self.item=self.canvas.create_rectangle(self.head[0],self.head[1],self.head[0]+10,self.head[1]+10,fill="green",tag=DefaultDirection)

        self.canvas.create_rectangle(self.head[0]-10,self.head[1],self.head[0],self.head[1]+10,fill="green",tag="right")

        self.canvas.create_rectangle(self.head[0]-20,self.head[1],self.head[0]-10,self.head[1]+10,fill="green",tag="right")

        dotx = random.randint(MINCOORD,MAXCOORD-3)
        doty = random.randint(MINCOORD,MAXCOORD-3)
        self.canvas.create_rectangle(dotx,doty,dotx+3,doty+3,tag='dot')

        threading.Thread(target=self.gameloop).start()


    def gameloop(self):
        while self.quit==False:
            
            self.grow()
            self.eatcollide()
            if self.eat==False:
                self.delete()
            else:
                self.eat=False
            time.sleep(0.5)

    def grow(self): 
        
        if self.direction=="right":
            self.head[0]=self.head[0]+11
            self.canvas.itemconfig(self.item,tag='right')
            self.draw()
        if self.direction=="left":
            self.head[0]=self.head[0]-11
            self.canvas.itemconfig(self.item,tag='left')
            self.draw()
        if self.direction=="up":
            self.head[1]=self.head[1]-11
            self.canvas.itemconfig(self.item,tag='up')
            self.draw()
        if self.direction=="down":
            self.head[1]=self.head[1]+11
            self.canvas.itemconfig(self.item,tag='down')
            self.draw()


    def eatcollide(self):
        overlap =self.canvas.find_overlapping(self.head[0],self.head[1],self.head[0]+10,self.head[1]+10) 
        for i in overlap:
            for j in self.canvas.gettags(i):
                if j == 'dot':
                    self.eat=True
                    self.canvas.delete(i)
                    dotx = random.randint(MINCOORD,MAXCOORD-3)
                    doty = random.randint(MINCOORD,MAXCOORD-3)
                    self.canvas.create_rectangle(dotx,doty,dotx+3,doty+3,tag='dot')
        if self.head[0]>MAXCOORD-11 or self.head[0]<MINCOORD or self.head[1]>MAXCOORD-11 or self.head[1]<MINCOORD:
            self.quit()
    def delete(self):
        endd = self.canvas.find_closest(self.end[0],self.end[1])[0]

        if self.canvas.gettags(endd)[0]=="right":
            self.end[0]=self.end[0]+11
        if self.canvas.gettags(endd)[0]=="left":
            self.end[0]=self.end[0]-11
        if self.canvas.gettags(endd)[0]=="up":
            self.end[1]=self.end[1]-11
        if self.canvas.gettags(endd)[0]=="down":
            self.end[1]=self.end[1]+11

        self.canvas.delete(endd)


    def draw(self): 
        self.item = self.canvas.create_rectangle(self.head[0],self.head[1],self.head[0]+10,self.head[1]+10,fill="green")

    def quit(self):
        self.quit = True
        time.sleep(1)
        self.frame.quit()

root = Tk()
app = Snake(root)
root.mainloop()
