import pygame, sys
import random
from pygame import *

gridwidth=10
gridheight=11
scale=30
fps=5

#Colors------
white=(255,255,255)
black=(0,0,0)
gray=(127,127,127)
lightblue=(143,214,255)

#Directions-------
Up="up"
Dn="down"
Lt="left"
Rt="right"

def main():
   pygame.init()
   global displaySurf, simpleFont, fpsClock
   fpsClock = pygame.time.Clock()
   displaySurf = pygame.display.set_mode((scale*gridwidth,scale*gridheight+4*scale))
   pygame.display.set_caption("GridFill")

   simpleFont = pygame.font.Font('freesansbold.ttf', 18)

   #The following is the boolean matrix used to turn on/off squares in the matrix.
   #Note the matrix shape is the "transpose" of the shape of the grid. This allows
   # for intuitive adjustment of matrix entries in typical list notation.
   gridMatrix = [[0 for i in range(gridheight)] for j in range(gridwidth)]
   
   st = startingSquare()
   drawSquare(st[0],st[1])
   gridMatrix[st[0]][st[1]] = 1

   st2 = startingSquare()
   drawSquare(st2[0],st2[1])
   gridMatrix[st2[0]][st2[1]] = 1

   movement = None
   finish = ""
   

   while True:
      checkQuit()

      drawEmptyGrid()

      for event in pygame.event.get():
         if event.type == KEYUP:
            if event.key == K_LEFT:
               movement = Lt
            elif event.key == K_RIGHT:
               movement = Rt
            elif event.key == K_DOWN:
               movement = Dn
            elif event.key == K_UP:
               movement = Up
            if event.key == K_SPACE:
               finish = "done"
      
      if finish == "done":
         break
      
      if movement:
         displaySurf.fill(black)
         drawEmptyGrid()
         updateMatrix(gridMatrix,movement)
         redrawSquares(gridMatrix)
      
      pygame.display.update()
      fpsClock.tick(fps)
   while True:
      #End game: Display final score -------------
      finalScore = 0
      for x in gridMatrix:
         for y in x:
            finalScore = finalScore + y
      
      checkQuit()
      pygame.draw.rect(displaySurf, (255,255,255), (scale,(gridheight+1)*scale,(gridwidth-2)*scale,2*scale))
      scoreCard = simpleFont.render("Score: "+str(finalScore), True, black)
      scoreRect = scoreCard.get_rect()
      scoreRect.center = (scale*gridwidth/2, gridheight*scale + 1.5*scale)
      retryButton = simpleFont.render("Retry?", True, black)
      retryRect = retryButton.get_rect()
      retryRect.center = (scale*gridwidth/2, gridheight*scale + 2.5*scale)
      displaySurf.blit(scoreCard,scoreRect)
      displaySurf.blit(retryButton,retryRect)
      for event in pygame.event.get():
         if event.type == MOUSEBUTTONUP:
            if retryRect.collidepoint(event.pos):
               return True
      pygame.display.update()
      fpsClock.tick(fps)

def drawEmptyGrid():
   #Design the empty grid.-----------------------
   for i in range(gridwidth):
      pygame.draw.line(displaySurf, (255,255,255), (scale*i,0), (scale*i,scale*gridheight-1))
   for i in range(gridheight+1):
      pygame.draw.line(displaySurf, (255,255,255), (0,scale*i), (scale*gridwidth-1,scale*i))

def startingSquare():
   #Place the first random square NOT on an edge.-------------
   random.seed()
   startX = random.randint(1,gridwidth-2)
   startY = random.randint(1,gridheight-2)
   start_pt = (startX, startY)
   return start_pt

#QUIT functions --------------------------------
def terminate():
   pygame.quit()
   sys.exit()
def checkQuit():
   for event in pygame.event.get(QUIT):
      terminate()
   for event in pygame.event.get(KEYUP):
      if event.key == K_ESCAPE:
         terminate()
      pygame.event.post(event) #----------------

def drawSquare(gridX,gridY):
   activeSquareRegion = pygame.Rect((scale*gridX+1,scale*gridY+1,scale-2,scale-2))
   activeSquare = pygame.Surface((scale-2,scale-2))
   activeSquare.fill(lightblue)
   displaySurf.blit(activeSquare,activeSquareRegion)

def collisionCheck(activeRow, direction):
   ''' This function returns a two row matrix to be added to the gridMatrix
   AFTER moving the remaining rows/columns in their current direction.'''
   zeroslen = len(activeRow)
   zeros = [[0 for i in range(zeroslen)],[0 for i in range(zeroslen)]]
   temp = [0 for i in range(zeroslen)]
   if activeRow.count(1) == 0:
      return zeros
   else:
      if direction == Dn or direction == Up:
         if activeRow[0] == 1:
            zeros[1][0] = 1
            temp[1] = (temp[1]+1)%2
         if activeRow[gridwidth-1] == 1:
            zeros[1][gridwidth-1] = 1
            temp[gridwidth-2] = (temp[gridwidth-2]+1)%2
         for i in range(1,gridwidth-1):
            if activeRow[i] == 1:
               temp[i-1],temp[i+1] = (temp[i-1]+1)%2, (temp[i+1]+1)%2
         for j in range(zeroslen):
            zeros[0][j] = temp[j]# - activeRow[j]
      if direction == Rt or direction == Lt:
         if activeRow[0] == 1:
            zeros[1][0] = 1
            temp[1] = (temp[1]+1)%2
         if activeRow[gridheight-1] == 1:
            zeros[1][gridheight-1] = 1
            temp[gridheight-2] = (temp[gridheight-2]+1)%2
         for i in range(1,gridheight-1):
            if activeRow[i] == 1:
               temp[i-1],temp[i+1] = (temp[i-1]+1)%2, (temp[i+1]+1)%2
         for j in range(zeroslen):
            zeros[0][j] = temp[j]# - activeRow[j]
      return zeros
         

def updateMatrix(grdmatrix, direction):
   splitResults = [0 for i in range(max(gridwidth,gridheight))]
   if direction == Dn:
      #First, check for edge/corner collisions.
      BotRow = [row[gridheight-1] for row in grdmatrix]
      splitResults = collisionCheck(BotRow, Dn)
      #Then, check for overlap (???).
      
      #Finally, move active squares
      for x in range(gridwidth):
         for y in range(gridheight-1,0,-1):
            grdmatrix[x][y] = (grdmatrix[x][y] + grdmatrix[x][y-1])%2
            grdmatrix[x][y-1] = 0
      for x in range(gridwidth):
         grdmatrix[x][gridheight-1] = (grdmatrix[x][gridheight-1] + splitResults[0][x])%2
         grdmatrix[x][gridheight-2] = (grdmatrix[x][gridheight-2] + splitResults[1][x])%2
   elif direction == Up:
      #First.
      TopRow = [row[0] for row in grdmatrix]
      splitResults = collisionCheck(TopRow, Up)
      #Then.

      #Finally.
      for x in range(gridwidth):
         for y in range(gridheight-1):
            grdmatrix[x][y] = (grdmatrix[x][y] + grdmatrix[x][y+1])%2
            grdmatrix[x][y+1] = 0
      for x in range(gridwidth):
         grdmatrix[x][0] = (grdmatrix[x][0] + splitResults[0][x])%2
         grdmatrix[x][1] = (grdmatrix[x][1] + splitResults[1][x])%2
   elif direction == Rt:
      #First.
      RightCol = grdmatrix[gridwidth-1]
      splitResults = collisionCheck(RightCol, Rt)
      #Then.

      #Finally.
      for y in range(gridheight):
         for x in range(gridwidth-1,0,-1):
            grdmatrix[x][y] = (grdmatrix[x][y] + grdmatrix[x-1][y])%2
            grdmatrix[x-1][y] = 0
      for y in range(gridheight):
         grdmatrix[gridwidth-1][y] = (grdmatrix[gridwidth-1][y] + splitResults[0][y])%2
         grdmatrix[gridwidth-2][y] = (grdmatrix[gridwidth-2][y] + splitResults[1][y])%2
   elif direction == Lt:
      #First.
      LeftCol = grdmatrix[0]
      splitResults = collisionCheck(LeftCol, Lt)
      #Then.

      #Finally.
      for y in range(gridheight):
         for x in range(gridwidth-1):
            grdmatrix[x][y] = (grdmatrix[x][y] + grdmatrix[x+1][y])%2
            grdmatrix[x+1][y] = 0
      for y in range(gridheight):
         grdmatrix[0][y] = (grdmatrix[0][y] + splitResults[0][y])%2
         grdmatrix[1][y] = (grdmatrix[1][y] + splitResults[1][y])%2

def redrawSquares(grdmatrix):
   for x in range(gridwidth):
      for y in range(gridheight):
         if grdmatrix[x][y]==1:
            drawSquare(x,y)
while True:
   if __name__ == '__main__':
      main()
