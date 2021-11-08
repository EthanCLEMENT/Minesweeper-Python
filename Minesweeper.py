import tkinter as tk
import random
import numpy as np

class minesweeper:
    def __init__(self,rows,columns,size,mines):
        self.rows=rows
        self.columns=columns
        self.size=size
        self.mines=mines
        self.colors=["black","blue","blue","orange","orange","orange","red","red","red"] 
        
        #setting window
        self.window=tk.Tk()
        self.window.title("Minesweeper")
        
        self.canvas=tk.Canvas(self.window,width=self.columns*self.size,height=self.rows*self.size,background="white")
        self.canvas.grid(row=0,column=0)
        
        #define grid
        for i in range(self.columns):
            self.canvas.create_line(i*self.size,0,i*self.size,self.rows*self.size)
            
        for i in range(self.rows):
            self.canvas.create_line(0,i*self.size,self.columns*self.size,i*self.size)
        
        #label
        self.mine_label = tk.Label(self.window, text="Remaining mines : "+str(mines))
        self.mine_label.grid(row=1,column=0)
        
        #button
        self.canvas.bind("<Button-1>",self.mouse_click)
        self.grid()
    
    #returns the row and the column of square when we click on it
    def square(self,x,y):
        return y//self.size,x//self.size
    
    #returns the coordinates of a square when we click on it
    def coordinates(self,rows,columns):
        return columns*self.size,rows*self.size
    
    #initiates the grid and puts randomly mines in squares
    def grid(self): 
        #array that represents all the squares on the board. A negative number = mines 
        self.grid=np.zeros((self.columns,self.rows),dtype=int)
        self.unfound_squares=self.grid==0
        mines=self.mines
        #gameloop
        while mines>0:
            rows=random.randint(0,self.rows-1)
            columns=random.randint(0,self.columns-1)
            #making sure that 2 mines cannot be put in the same square 
            if self.grid[columns,rows]==0:
                self.grid[columns,rows]=-10
                #adds one in the adjacent squares of a mine
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        r=rows+i
                        c=columns+j
                        if 0<=r<self.rows and 0<=c<self.columns:
                            self.grid[c,r]+=1
                self.unfound_squares[columns,rows]=False
                mines-=1
    
    #keeps track of the clicks made by the player
    def mouse_click(self,event):
        rows,columns=self.square(event.x,event.y)
        x,y=self.coordinates(rows,columns)
        #if the player clicks on a mine
        if self.grid[columns,rows]<0:
            self.canvas.create_oval(x+5,y+5,x+self.size-5,y+self.size-5,fill="red",outline="orange",width=5)
            self.main_label.config(text="You lost !")
            self.canvas.unbind("<Button-1>")
        else:
            #if the player did not click on a mine
            self.canvas.create_text(x+self.size//2,y+self.size//2,text=str(self.grid[columns,rows]),fill=self.colors[self.grid[columns,rows]])
            self.unfound_squares[columns,rows]=False
            if self.grid[columns,rows]==0:
                self.expand_zone(rows,columns)
            if not np.any(self.unfound_squares):
                self.main_label.config(text="You won !")
                self.canvas.unbind("<Button-1>")
    
    #checks if the square is a 0. If yes displays all the squares around it
    def expand_zone(self,rows,columns):
        squares_found=[(rows,columns)]
        test=[]
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                r=rows+i
                c=columns+j
                if 0<=r<self.rows and 0<=c<self.columns and not (r,c) in squares_found:
                    test.append((r,c))
        while len(test)>0:
            square=test[0]
            squares_found.append(square)
            x,y=self.coordinates(square[0],square[1])
            self.canvas.create_text(x+self.size//2,y+self.size//2,text=str(self.grid[square[1],square[0]]),fill=self.colors[self.grid[square[1],square[0]]])
            self.unfound_squares[columns,rows]=False
            if self.grid[square[1],square[0]]==0:
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        r=square[0]+i
                        c=square[1]+j
                        if 0<=r<self.rows and 0<=c<self.columns and not (r,c) in squares_found:
                            test.append((r,c))
                            squares_found.append((r,c))
            test.remove(square)
            
main=minesweeper(8,12,30,12)
tk.mainloop()
