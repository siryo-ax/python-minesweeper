from tkinter import *
from tkinter.messagebox import *
from random import randint
from time import time

titlescreen = Tk()
titlescreen.title("Minesweeper")
titlescreen.geometry("300x300")
titlescreen.resizable(False,False)
titlescreen.iconbitmap("assets/mine.ico")
c0 = PhotoImage(file = "assets/c0.png")
c1 = PhotoImage(file = "assets/c1.png")
c2 = PhotoImage(file = "assets/c2.png")
c3 = PhotoImage(file = "assets/c3.png")
c4 = PhotoImage(file = "assets/c4.png")
c5 = PhotoImage(file = "assets/c5.png")
c6 = PhotoImage(file = "assets/c6.png")
c7 = PhotoImage(file = "assets/c7.png")
c8 = PhotoImage(file = "assets/c8.png")
blank = PhotoImage(file = "assets/blank.png")
cflag = PhotoImage(file = "assets/flag.png")
mine = PhotoImage(file = "assets/mine.png")

def gameover(win,t0,squares,grid_dim,game_window) :
    """
    End the game

    Args:
        win (bool)
        t0 (int): time value when the game started
        squares (list): 'objects' squares
        game_window (tk)
    """
    t1 = time()
    
    #To prevent the player from interacting with the 'playground' after the end of the game 
    #Doesn't work, I don't know why yet
    """
    for x in range(grid_dim):
        for y in range(grid_dim) :
            if squares[x][y]!=None :
                squares[x][y].unbind("<Button-1>")
                squares[x][y].unbind("<Button-2>")
                squares[x][y].unbind("<Button-3>")
            else : 
                pass
                """
    if win == True :
        showinfo("Game Over","You Won !\nTime : " + str(round(t1-t0)) + " seconds")
    else :
        showinfo("Game Over","You Lost...")
    game_window.destroy()
    titlescreen.deiconify()
        
        

def dig0(x,y,grid_limit,mine_cos,c0_cos,destroyed_cos,squares,t0,game_window,grid_dim) :
    """
    When the player dig one '0 square', dig all the other '0 squares' that touch each other

    Args:
        x (int)
        y (int)
        grid_limit (int): max value that the lists can use to manipulate the squares int the grid_dim (grid_dim-1)
        mine_cos (list): coordinates of the squares that countains a mine
        c0_cos (list): coordinates of the '0 squares'
        destroyed_cos (list): coordinates of the destroyed squares
        squares (list): 'objects' squares
        t0 (int): time value when the game started
        game_window (tk)
        grid_dim (int): dimension of the grid
    """
    squares[x][y].destroy()  
    destroyed_cos.append([x,y])
    adjacents = [[x-1,y-1],[x-1,y],[x-1,y+1],[x,y-1],[x,y+1],[x+1,y-1],[x+1,y],[x+1,y+1]]  
    for square in adjacents : 
        if square in destroyed_cos or square[0] < 0 or square[0] > grid_limit or square[1] < 0 or square[1] > grid_limit : 
            pass
        else :
            if square in c0_cos : 
                dig0(square[0],square[1],grid_limit,mine_cos,c0_cos,destroyed_cos,squares,t0,game_window,grid_dim)  
            else :
                squares[square[0]][square[1]].destroy() 
                destroyed_cos.append([square[0],square[1]])
                if len(destroyed_cos) == (grid_dim*grid_dim) - len(mine_cos) :  
                    gameover(True,t0,squares,grid_dim,game_window)

def dig(event,x,y,grid_limit,mine_cos,c0_cos,destroyed_cos,squares,t0,game_window,grid_dim) :
    """
    Destroy a blank square, revealing the number (or mine) under it. 

    Args:
        x (int)
        y (int)
        grid_limit (int): max value that the lists can use to manipulate the squares int the grid_dim (grid_dim-1)
        mine_cos (list): coordinates of the squares that countains a mine
        c0_cos (list): coordinates of the '0 squares'
        destroyed_cos (list): coordinates of the destroyed squares
        squares (list): 'objects' squares
        t0 (int): time value when the game started
        game_window (tk)
        grid_dim (int): dimension of the grid
    """
    if [x,y] in mine_cos : 
        squares[x][y].destroy()
        gameover(False,t0,squares,grid_dim,game_window)
    if [x,y] in c0_cos : 
        dig0(x,y,grid_limit,mine_cos,c0_cos,destroyed_cos,squares,t0,game_window,grid_dim)
    else :
        squares[x][y].destroy() 
        destroyed_cos.append([x,y])
        if len(destroyed_cos) == (grid_dim*grid_dim) - len(mine_cos) : 
            gameover(True,t0,squares,grid_dim,game_window)

def unflag(fl) : 
    fl.destroy()
    
def flag(event,x,y,game_window) : 
    fl = Label(game_window,image=cflag)
    fl.bind("<Button-2>",lambda event : unflag(fl))
    fl.bind("<Button-3>",lambda event : unflag(fl))
    fl.grid(row=y,column=x)

def play(grid_dim,mine_number,grid_limit,x,y,game_window) :
    """
    Generate the 'playground'.
    The 'playground' consist of two grids overlapping : the first is the mines and numbers, the second, on top *
    of the first consist of the squares that the player will dig (or not).

    Args:
        grid_dim (int): dimension of the grid
        mine_number (int)
        grid_limit (int): max value that the lists can use to manipulate the squares int the grid_dim (grid_dim-1)
        x and y (int): the coordinates of the first square dug
        game_window (tk) 
    """
    #Contain the images, index matching theirs values
    square_number = [c0,c1,c2,c3,c4,c5,c6,c7,c8]
    #Lists containing the coordinates of the differents types of squares  
    mine_cos = [] 
    c0_cos = [] 
    destroyed_cos = [] 
    #Contain the 'objects' squares 
    squares = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    
    #The first square dug need to be a 0 square, so it and its adjacents squares needs to be ignored by the mine loop
    do_not_touch = [[x,y],[x-1,y-1],[x-1,y],[x-1,y+1],[x,y-1],[x,y+1],[x+1,y-1],[x+1,y],[x+1,y+1]]
    
    #x and y after here are not tied anymore to the first square dug 
    for i in range(mine_number) : 
        x = randint(0,grid_limit)
        y = randint(0,grid_limit)
        while [x,y] in mine_cos or [x,y] in do_not_touch : 
            x = randint(0,grid_limit)
            y = randint(0,grid_limit)
        mine_cos.append([x,y])
        Label(game_window,image=mine).grid(row=y,column=x)
    
    for x in range(grid_dim) :
        for y in range(grid_dim) :
            cos = [x,y]
            if cos in mine_cos :
                pass
            else :
                n = 0
                adjacents = [[x-1,y-1],[x-1,y],[x-1,y+1],[x,y-1],[x,y+1],[x+1,y-1],[x+1,y],[x+1,y+1]] 
                for square in adjacents :
                    if square in mine_cos :  
                        n = n + 1
                if n == 0 : 
                    Label(game_window,image=c0).grid(row=y,column=x)
                    c0_cos.append([x,y])
                else : 
                    Label(game_window,image=square_number[n]).grid(row=y,column=x)
                          
    for x in range(grid_dim):
        for y in range(grid_dim) :
            square = Label(game_window,image=blank) 
            square.bind("<Button-1>",lambda event ,x=x, y=y : dig(event,x,y,grid_limit,mine_cos,c0_cos,destroyed_cos,squares,t0,game_window,grid_dim)) 
            square.bind("<Button-2>",lambda event ,x=x, y=y : flag(event,x,y,game_window)) 
            square.bind("<Button-3>",lambda event ,x=x, y=y : flag(event,x,y,game_window))
            (squares[x]).append(square)  
            square.grid(row=y,column=x)
    
    #The game can now begin ! We start the timer, and formally dig the first square dug 
    t0 = time()
    dig(None,do_not_touch[0][0],do_not_touch[0][1],grid_limit,mine_cos,c0_cos,destroyed_cos,squares,t0,game_window,grid_dim)  
            
def main(grid_dim,mine_number,grid_limit) :
    """
    Generate a first 'false' grid. This to gather the first square on which the player will click, in order
    for it to be automatically a '0 square'. Ensure the game is playable. 

    Args:
        grid_dim (int): dimension of the grid
        mine_number (int)
        grid_limit (int): max value that the lists can use to manipulate the squares int the grid_dim (grid_dim-1)
    """
    titlescreen.withdraw()
    game_window = Toplevel()
    game_window.title("Minesweeper grid x" + str(grid_dim))
    game_window.resizable(False,False)
    game_window.iconbitmap("assets/mine.ico")
    #Contain the 'objects' squares 
    squares = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] 
    for x in range(grid_dim):
        for y in range(grid_dim) :
            case = Label(game_window,image=blank) 
            case.bind("<Button-1>",lambda event ,x=x, y=y : play(grid_dim,mine_number,grid_limit,x,y,game_window)) 
            case.bind("<Button-2>",lambda event ,x=x, y=y : flag(event,x,y,game_window)) 
            case.bind("<Button-3>",lambda event ,x=x, y=y : flag(event,x,y,game_window))
            (squares[x]).append(case)  
            case.grid(row=y,column=x)
    
    
Label(titlescreen,text="Minesweeper",font=("Impact",30),foreground="black").pack(pady=30)     
Button(titlescreen, text = "Easy", height=1, width=6, command =lambda: main(10,10,9)).pack(pady=5)
Button(titlescreen, text = "Normal", height=1, width=6, command =lambda: main(16,40,15)).pack(pady=5)
Button(titlescreen, text = "Hard", height=1, width=6, command =lambda: main(24,99,23)).pack(pady=5)

titlescreen.mainloop()