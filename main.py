from Tkinter import *
import threading
import time
#Define Some Variables
MINCOORD=1
MAXCOORD=100
RightKey='Right'
LeftKey='Left'
UpKey='Up'
DownKey='Down'
DefaultDirection= 'down'
DefaultHead=[10,10]

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

    def gameloop(self):
        while self.quit==False:
            self.move()
            time.sleep(0.1)

    def move(self):
        if self.direction=="right":
            self.head[0]=self.head[0]+10
            self.draw()
        if self.direction=="left":
            self.head[0]=self.head[0]-10
            self.draw()
        if self.direction=="up":
            self.head[1]=self.head[1]-10
            self.draw()
        if self.direction=="down":
            self.head[1]=self.head[1]+10
            self.draw()
    
    def draw(self):
        self.canvas.create_rectangle(self.head[0],self.head[1],self.head[0]+10,self.head[1]+10,fill="green")

    def startgame(self):
        #clear things
        self.direction= DefaultDirection
        self.head=DefaultHead
        self.quit=False

        threading.Thread(target=self.gameloop).start()

    def quit(self):
        self.quit = True
        self.frame.quit()

root = Tk()
app = Snake(root)
root.mainloop()
