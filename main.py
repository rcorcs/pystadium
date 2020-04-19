import io
from time import sleep
import threading
import signal
import logging
from PIL import Image
import signal
from starlette.responses import StreamingResponse
from fastapi import BackgroundTasks, FastAPI
from fastapi.staticfiles import StaticFiles

import game

app = FastAPI()

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

app.mount("/client", StaticFiles(directory="public", html=True), name="public")

imgByteArr = None
killed = False

@app.get("/health-check")
def read_root():
    return {"Hello": "World"}

@app.get("/image/{image_name}")
def read_image(image_name: str):
    global imgByteArr
    return StreamingResponse(io.BytesIO(imgByteArr), media_type="image/png")

def on_exit(signum, frame):
    logger.info('Killing remaining threads...')
    logger.info('Bye!')
    killed = True

signal.signal(signal.SIGINT, on_exit)
signal.signal(signal.SIGTERM, on_exit)

# Import the pygame library and initialise the game engine
import pygame
 
pygame.init()
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)

class Paddle(pygame.sprite.Sprite):
    #This class represents a paddle. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the paddle, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
   
def game():
    global imgByteArr
    global killed
    # Open a new window
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong")
     
    paddleA = Paddle(WHITE, 10, 100)
    paddleA.rect.x = 20
    paddleA.rect.y = 200
     
    paddleB = Paddle(WHITE, 10, 100)
    paddleB.rect.x = 670
    paddleB.rect.y = 200
     
    #This will be a list that will contain all the sprites we intend to use in our game.
    all_sprites_list = pygame.sprite.Group()
     
    # Add the paddles to the list of sprites
    all_sprites_list.add(paddleA)
    all_sprites_list.add(paddleB)
     
    # The loop will carry on until the user exit the game (e.g. clicks the close button).
    carryOn = True
     
    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()
     
    # -------- Main Program Loop -----------
    while carryOn and (not killed):
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                  carryOn = False # Flag that we are done so we exit this loop
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x: #Pressing the x Key will quit the game
                         carryOn=False  
     
        # --- Game logic should go here
        all_sprites_list.update()
     
     
        # --- Drawing code should go here
        # First, clear the screen to black. 
        screen.fill(BLACK)
        #Draw the net
        pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
        
        #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(screen) 
     
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        pygame.image.save(screen, "screenshot.jpeg")
        img = Image.open("screenshot.jpeg")
        imgByteIO = io.BytesIO()
        img.save(imgByteIO, format='PNG')
        imgByteArr = imgByteIO.getvalue()

        # --- Limit to 60 frames per second
        clock.tick(60)
     
    #Once we have exited the main program loop we can stop the game engine:
    pygame.quit()


x = threading.Thread(target=game)
x.start()
