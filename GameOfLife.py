from graphics import *
import numpy as np
import time

__width__ = 64
__height__ = 32
__scaler__ = 20
button_width = 40
button_height = 5
cells = np.zeros(__width__ * __height__).reshape(__height__, __width__)
PLAY_GAME = False
LIVE_CELL = 1
DEAD_CELL = 0

def startGame():
    start_btn = win.buttons[0]
    start_btn.state = 'disabled'
    start_btn.draw(win, start_btn.x, start_btn.y)
    
    pause_btn = win.buttons[1]
    pause_btn.state = 'active'
    pause_btn.draw(win, pause_btn.x, pause_btn.y)
    
    clearGrid()
    drawCells()
    time.sleep(0.5)
    
    global PLAY_GAME
    PLAY_GAME = True
    
    while PLAY_GAME:
        global cells
        cells_copy = cells.copy()
    
        for i in range(1, cells.shape[0] - 1):
            for j in range(1, cells.shape[1] - 1):
                neighbors = 0
                
                if cells[i][j - 1] == LIVE_CELL:
                    neighbors+=1
                if cells[i][j + 1] == LIVE_CELL:
                    neighbors+=1
                if cells[i - 1][j] == LIVE_CELL:
                    neighbors+=1
                if cells[i + 1][j] == LIVE_CELL:
                    neighbors+=1
                if cells[i - 1][j - 1] == LIVE_CELL:
                    neighbors+=1
                if cells[i + 1][j - 1] == LIVE_CELL:
                    neighbors+=1
                if cells[i - 1][j + 1] == LIVE_CELL:
                    neighbors+=1
                if cells[i + 1][j + 1] == LIVE_CELL:
                    neighbors+=1
                    
                if (neighbors == 2 or neighbors == 3) and cells[i][j] == LIVE_CELL:
                    pass
                elif cells[i][j] == DEAD_CELL and neighbors == 3:
                    cells_copy[i][j] = LIVE_CELL
                else:
                    cells_copy[i][j] = DEAD_CELL
                
        cells = cells_copy
        clearGrid()
        drawCells()
        time.sleep(0.2)
        
def pauseGame():
    start_btn = win.buttons[0]
    start_btn.state = 'active'
    start_btn.draw(win, start_btn.x, start_btn.y)
    
    pause_btn = win.buttons[1]
    pause_btn.state = 'disabled'
    pause_btn.draw(win, pause_btn.x, pause_btn.y)
    
    global PLAY_GAME
    PLAY_GAME = False

def handleMouseClick(pt):
    if (pt.y <= __height__*__scaler__):
        rect = Rectangle(Point(int(pt.x/__scaler__)*__scaler__, int(pt.y/__scaler__)*__scaler__), Point(int(pt.x/__scaler__)*__scaler__ + __scaler__, int(pt.y/__scaler__)*__scaler__ + __scaler__))
    
        foundRect = None
        stringId = str(rect.__repr__)
        start = __width__ - 1 + __height__ - 1
        for i in range(start, len(win.items)):
            if (stringId == str(win.items[i].__repr__)):
                foundRect = win.items[i]
                break           
        if (win._mouseCallback == 1): # Left Mouse Button Clicked
            if foundRect:
                pass
            else:
                rect.setFill('yellow')
                rect.draw(win)
                cells[int(pt.y/__scaler__)][int(pt.x/__scaler__)] = 1
        elif (win._mouseCallback == 3): # Right Mouse Button Clicked            
            if foundRect:
                foundRect.canvas = win
                foundRect.undraw()
                cells[int(pt.y/__scaler__)][int(pt.x/__scaler__)] = 0

def drawGrid():
    # draw small grid-lines
    for i in range(1, __width__):        
        line = Line(Point(__scaler__*i, 0), Point(__scaler__*i, __height__*__scaler__))
        if i == 1 or i == __width__ - 1:
            line.setOutline('red')
        else:
            line.setOutline('gray')
        line.draw(win)
        
    for i in range(1, __height__):       
        line = Line(Point(0, __scaler__*i), Point(__width__*__scaler__, __scaler__*i ))
        if i == 1 or i == __height__ - 1:
            line.setOutline('red')
        else:
            line.setOutline('gray')
        line.draw(win)
        
def drawCells():
     for i in range(cells.shape[0]):
            for j in range(cells.shape[1]):
                if cells[i][j] == LIVE_CELL:
                    rect = Rectangle(Point(j * __scaler__, i * __scaler__), Point((j + 1) * __scaler__, (i + 1) * __scaler__))
                    rect.setFill('yellow')
                    rect.draw(win)    

def drawButtons():
    btn = Button("Start Game", button_width, button_height, '10', startGame)
    btn.draw(win, 0, __height__*__scaler__)
    
    btn = Button("Pause Game", button_width, button_height, '10', pauseGame, state = 'disabled')
    btn.draw(win, 300, __height__*__scaler__)

def clearGrid():
    win.clear()
    drawGrid()
    
##################

win = GraphWin('Game Of Life', __width__*__scaler__, __height__*__scaler__ + 100)
drawGrid()
drawButtons()

while not PLAY_GAME:
    pt = win.getMouse()
    handleMouseClick(pt)
    