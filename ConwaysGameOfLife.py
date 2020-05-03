import tkinter as tk
from random import randint
import time


CHEIGHT = 1000
CWIDTH = 1000
INCREMENT = 50


class WindowHandler():
	def __init__(self):
		self.canvasHeight = CHEIGHT
		self.canvasWidth = CWIDTH
		self.root = tk.Tk()
		self.canvas = tk.Canvas(
					width=self.canvasWidth,height=self.canvasHeight,
					bg='black')
		self.canvas.pack()

		self.initButtons()

		self.root.bind("<Key>",self.keyPress)
		self.root.bind("<Button-1>",self.mousePress)
		self.root.bind("<B1-Motion>",self.mouseHold)

		self.drawer = CanvasDrawer(self.canvas)
		self.drawGrid()

		self.game = GameLogic(INCREMENT)

		self.turnON = True


		self.drawer.initCells(self.game.cellBoard)

	def mousePress(self,event):
		x2 = self.root.winfo_pointerx() - self.root.winfo_rootx()
		y2 = self.root.winfo_pointery() - self.root.winfo_rooty()
		if y2 > 1000:
			return

		x,y = self.convertMouse(event.x,event.y)
		if self.game.cellBoard[y][x].state == True:
			self.turnON = False
		else:
			self.turnON = True
		self.drawer.changeCellState(x,y,self.game.cellBoard)
		# print(f'event pos: {event.x,event.y}')
		# print(f'relative pos: {x2,y2}')
		# print(f'board pos: {x,y}')

	def mouseHold(self,event):
		x2 = self.root.winfo_pointerx() - self.root.winfo_rootx()
		y2 = self.root.winfo_pointery() - self.root.winfo_rooty()
		if y2 > 1000:
			return
		x,y = self.convertMouse(event.x,event.y)
		if self.turnON == True:
			if self.game.cellBoard[y][x].state == False:
				self.drawer.changeCellState(x,y,self.game.cellBoard)
		else:
			if self.game.cellBoard[y][x].state == True:
				self.drawer.changeCellState(x,y,self.game.cellBoard)


	def initButtons(self):
		self.stepForwardButton = tk.Button(self.root,text="ONE STEP",command=self.moveForwardOneStep,width=15)
		self.stepForwardButton.pack(side='right')

		self.goForwardNSteps = tk.Button(self.root,text="X STEPS",command=self.moveForwardNSteps,width=15)
		self.goForwardNSteps.pack(side='left')

		self.speedLabel = tk.Label(self.root,text="Speed")
		self.speedInput = tk.Entry(self.root)
		self.speedLabel.pack(side='left')
		self.speedInput.pack(side='left')

		self.numStepsLabel = tk.Label(self.root,text='# of steps')
		self.numStepsInput = tk.Entry(self.root)
		self.numStepsLabel.pack(side='left')
		self.numStepsInput.pack(side='left')

		self.resetButton = tk.Button(self.root,text="RESET",command=self.resetStuff)
		self.resetButton.pack()

	def resetStuff(self):
		for y,row in enumerate(self.game.cellBoard):
			for x,cell in enumerate(row):
				if cell.state == True:
					self.drawer.changeCellState(x,y,self.game.cellBoard)
					cell.state = False
		self.root.update()




	def moveForwardNSteps(self):
		try:
			speed = float(self.speedInput.get())
			steps = int(self.numStepsInput.get())
		except:
			speed = .25
			steps = 10

		for x in range(steps):
			print(f'{x+1}/{steps}')
			self.moveForwardOneStep()
			print('test')
			time.sleep(speed)
			self.root.update()



	def convertMouse(self,x,y):
		dX = self.canvasWidth/INCREMENT
		realX = int(x/dX)
		realY = int(y/dX)
		return (realX,realY)

	def keyPress(self,event):
		if event.char == "q":
			self.root.destroy()

	def drawGrid(self):
		self.drawer.drawGrid(self.canvasWidth,INCREMENT)

	def moveForwardOneStep(self):
		cellBoardCopy = []
		for row in self.game.cellBoard:
			tempRow = []
			for cell in row:
				tempRow.append(cell.state)
			cellBoardCopy.append(tempRow)
		for y,row in enumerate(cellBoardCopy):
			for x,cell in enumerate(row):
				if self.judgeCell(x,y):
					if cellBoardCopy[y][x] == True:
						cellBoardCopy[y][x] = False
					else:
						cellBoardCopy[y][x] = True
				else:
					pass
		for y,row in enumerate(cellBoardCopy):
			for x,cell in enumerate(row):
				if self.game.cellBoard[y][x].state != cell:
					self.drawer.changeCellState(x,y,self.game.cellBoard)

	def judgeCell(self,x,y):
		## returns true if should change
		## returns false if not
		cell = self.game.cellBoard[y][x]
		cells = self.game.getNeighbors(x,y)
		counter = self.game.countLive(cells)
		if cell.state == True:
			if self.game.ruleOne(counter):
				return True
			elif self.game.ruleTwo(counter):
				return True
			elif self.game.ruleThree(counter):
				return False
		else:
			if self.game.ruleFour(counter):
				return True
			else:
				return False

	def mainLoop(self):
		while True:
			try:
				self.root.update()
			except:
				print('goodbye')
				break

class CanvasDrawer():
	def __init__(self,canvas):
		self.canvas = canvas

	def drawGrid(self,width,increment):
		### width will be same as height
		self.dX = int(width/increment)
		for x in range(increment):
			x1 = self.dX*x
			y1 = 0
			y2 = width
			self.canvas.create_line(x1,y1,x1,y2,fill='white')
			x1 = 0
			x2 = width
			y1 = self.dX*x
			self.canvas.create_line(x1,y1,x2,y1,fill='white')

	def drawCell(self,cell):
		width = self.dX
		x1 = cell.x*width
		x2 = x1+width
		y1 = cell.y*width
		y2 = y1+width
		cell.drawnImage = self.canvas.create_rectangle(x1,y1,x2,y2,fill='black',outline='white')

	def initCells(self,cellBoard):
		for row in cellBoard:
			for cell in row:
				self.drawCell(cell)

	def changeCellState(self,x,y,cellBoard):
		cell = cellBoard[y][x]
		if cell.state == True:
			self.canvas.itemconfig(cell.drawnImage,fill='black',outline='white')
		else:
			self.canvas.itemconfig(cell.drawnImage,fill='white',outline='black')

		cell.toggleState()

class GameLogic():
	def __init__(self,width):
		self.width = width

		self.board = [[ 0 for x in range(width)] for x in range(width)]
		self.cellBoard = [[ 0 for x in range(width)] for x in range(width)]

		self.insertCells()
		# self.turnOnRandomCells()
		self.convertBoard()

	def printBoard(self):
		for row in self.board:
			print(row)

	def insertCells(self):
		for y,row in enumerate(self.cellBoard):
			for x,cell in enumerate(row):
				self.cellBoard[y][x] = Cell(self,x,y)

	def turnOnRandomCells(self):
		for row in self.cellBoard:
			rand = randint(0,INCREMENT-1)
			row[rand].state = True

	def convertBoard(self):
		for y,row in enumerate(self.cellBoard):
			for x,cell in enumerate(row):
				if cell.state == True:
					self.board[y][x] = 1
				else:
					self.board[y][x] = 0

	def getNeighbors(self,x,y):
		boundary = len(self.cellBoard)-1

		points = []

		topLeft = (x-1,y-1)
		top = (x,y-1)
		topRight = (x+1,y-1)
		right = (x+1,y)
		bottomRight = (x+1,y+1)
		bottom = (x,y+1)
		bottomLeft = (x-1,y+1)
		left = (x-1,y)

		if x == 0 and y == 0:
			points += [right,bottomRight,bottom]
		elif x == 0 and y == boundary:
			points += [top,topRight,right]
		elif x == boundary and y == 0:
			points += [left,bottomLeft,bottom]
		elif x == boundary and y == boundary:
			points += [left,topLeft,top]
		elif x == boundary and y > 0 and y < boundary:
			points += [top,topLeft,left,bottomLeft,bottom]
		elif x == 0 and y > 0 and y < boundary:
			points += [top,topRight,right,bottomRight,bottom]
		elif y == boundary and x > 0 and x < boundary:
			points += [left,topLeft,top,topRight,right]
		elif y == 0 and x > 0 and x < boundary:
			points += [left,bottomLeft,bottom,bottomRight,right]
		else:
			points += [topLeft,top,topRight,right,
					bottomRight,bottom,bottomLeft,left]
		values = []
		for x,y in points:
			values.append(self.cellBoard[y][x])
		return values

	def countLive(self,values):
		counter = 0
		for cell in values:
			if cell.state == True:
				counter += 1
		return counter

	def ruleOne(self,counter):
		## Any live cell with fewer than two live 
		## neighbours dies (referred to as underpopulation or exposure)
		## true = dies
		if counter < 2:
			return True
		else:
			return False

	def ruleTwo(self,counter):
		## Any live cell with more than three live neighbours
		## dies (referred to as overpopulation or overcrowding).
		## true = dies
		if counter > 3:
			return True
		else:
			return False

	def ruleThree(self,counter):
		## Any live cell with two or three live neighbours lives, 
		## unchanged, to the next generation.
		## true = lives
		if counter == 2 or counter == 3:
			return True
		else:
			return False

	def ruleFour(self,counter):
		## Any dead cell with exactly three live neighbours will come to life.
		if counter == 3:
			return True
		else:
			return False


class Cell():
	def __init__(self,game,x,y):
		self.game = game
		self.state = False
		self.x = x
		self.y = y

	def toggleState(self):
		if self.state == True:
			self.state = False
		else:
			self.state = True


window = WindowHandler()
window.mainLoop()