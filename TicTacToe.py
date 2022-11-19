# GUI
import pygame
import pygame.freetype
import tkinter as tk
import numpy as np
# Import tictactoe ai
from tictactoeai import tic_tac_toe_game, legal_moves_generator, move_selector, model
# Speech recognition
import speech_recognition as sr
import os

# Setting speech recognition
mic = sr.Microphone(2)
r = sr.Recognizer()


# ==========Functions=================

def form():
    '''
    Value of player set from menu
    Circle = 0, Cross = 1
    '''   

    if circle.get() == 1:        
        result = 0
        
    elif cross.get() == 1:
        result = 1
        
    else:
        raise ValueError
    return result

def draw_grid():

    '''Drawing grid or board of the game'''
    
    black = (0,0,0)

    xstart = 60
    xend = 660
    ystart = 260
    yend = 260
    pygame.draw.line(screen, black, (xend, yend), (xstart, ystart),8)
    
    xstart2 = 60
    xend2 = 660
    ystart2 = 460
    yend2 = 460
    pygame.draw.line(screen, black, (xend2, yend2), (xstart2, ystart2),8)
    
    
    xstart3 = 260
    xend3 = 260
    ystart3 = 60
    yend3 = 660
    pygame.draw.line(screen, black, (xend3, yend3), (xstart3, ystart3),8)
    
    xstart4 = 460
    xend4 = 460
    ystart4 = 60
    yend4 = 660
    pygame.draw.line(screen, black, (xend4, yend4), (xstart4, ystart4),8)
    
    pygame.display.update()

def draw_circle(center):

    '''Drawing circle marker'''

    pink = (255, 153, 204)
    pygame.draw.circle(screen,pink,center, 70, 8)
    pygame.display.update()

def draw_cross(center):
    
    '''Drawing cross marker'''
    
    pink = (255, 153, 204)
    length = 60
    pygame.draw.line(screen, pink, (center[0] - length, center[1] - length), (center[0] + length, center[1] + length), 8)
    pygame.draw.line(screen, pink, (center[0] - length, center[1] + length ), (center[0] + length, center[1] - length ), 8)
    pygame.display.update()

def clear():

    '''Clear all drawing'''
    white = (255, 255, 255)
    screen.fill(white)

def draw_names(turn, player_name) :
    '''Draw name as a title in the game according to each player turn'''
    red = (255, 0, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)

    # AI turn
    if turn == 0:
        screen.fill(white, (0, 0, screen.get_width(), 50))
        font.render_to(screen, (280, 10), "AI TURN : X", red)
        pygame.display.update()
    # Player turn
    else:
        screen.fill(white, (0, 0, screen.get_width(), 50))
        font.render_to(screen, (280, 10), f"{player_name} TURN : O", blue)
        pygame.display.update()



# ==========Functions=================

# Window
start_window = tk.Tk()
start_window.geometry("1080x720")

# Player label
os.system("espeak -p 80 -g 2 'Welcome, What is your name?'")
while True:
    with mic as source:
        audio = r.listen(source)
    try :
        print("What is your name...")
        name = r.recognize_google(audio)
        name = name.lower()
        name = name.split(" ")[-1]
        print(f"name: {name}")
        break
    except:
        os.system("espeak 'Can you say it again'")
        print("Can't recognize your voice")
        continue

username_var = tk.StringVar()
username_var.initialize(name)
player_name_text = tk.Label(start_window, text="Enter player name").pack(pady = (350, 0))
player_name = tk.Entry(start_window, textvariable=username_var)
player_name.pack()

#start button
username = ""
def playButton():
    global username
    username = username_var.get()
    start_window.destroy()
    return username

button = tk.Button(start_window, text="Play",bg='green', command=playButton).pack(pady=7, padx=3)

start_window.mainloop()
pygame.init()

width=720
height=720

white=(255,255,255)
black=(0,0,0)
blue=(0,191,255)
purple = (138, 43, 226)
pink = (255, 153, 204)
size = width,height
background=white

screen=pygame.display.set_mode(size)
screen.fill(background)
center = (width/2 , height/2)
centertext=(width/2 - 45 , height/2 - 150)
font=pygame.freetype.Font('./font/college.ttf', 25)

# ===============Game=================

# Initialize game
game = tic_tac_toe_game()

# toss who play first
game.toss()

os.system("espeak -p 80 -g 2 'Game started'")
print("Starting the game!!!\n")
print(f"Player {game.turn_monitor} play first\n")

running=True

# position on the GUI
locations = {
    (0, 0): (160, 160),
    (0, 1): (360, 160),
    (0, 2): (560, 160),
    (1, 0): (160, 360),
    (1, 1): (360, 360),
    (1, 2): (560, 360),
    (2, 0): (160, 560),
    (2, 1): (360, 560),
    (2, 2): (560, 560)
    }

# For misspel case
spellLists = {
    "1": ["1", "11", "one", "wan", "fun"],
    "2": ["2", "22", "two", "too", "foo", "tube"],
    "3": ["3", "33", "three", "free", "tree", "tee", "thee"],
    "4": ["4", "44", "four", "for", "fo", "foe", "far"],
    "5": ["5", "55", "five", "fight", "fire"],
    "6": ["6", "66", "six", "sex", "sig", "sit"],
    "7": ["7", "77", "seven", "swan", "sen"],
    "8": ["8", "88", "eight", "egg", "eache", "a", "ed", "faith", "at", "aunt"],
    "9": ["9", "99", "nine", "nigh", "night"]
}
check = 0
while running :

    #clear()
    draw_grid()
    draw_names(game.turn_monitor, username)
    
    # AI turn
    if game.game_status() == "In Progress" and game.turn_monitor == 0:
        os.system("espeak 'AI turn'")
        # If its the program's turn, use the Move Selector function to select the next move
        selected_move,new_board_state,score = move_selector(model, game.board, game.turn_monitor)
        
        game_status, board = game.move(game.turn_monitor, selected_move)
        ai_mark = {
            (0, 0): 'one',
            (0, 1): 'two',
            (0, 2): 'three',
            (1, 0): 'four',
            (1, 1): 'five',
            (1, 2): 'six',
            (2, 0): 'seven',
            (2, 1): 'eight',
            (2, 2): 'nine'
        }
        draw_circle(locations[selected_move])
        speech = f"AI mark on {ai_mark[selected_move]}"
        position = str(ai_mark[selected_move])
        os.system(f"espeak 'AI mark on {position}'")
    
    # Player turn
    elif game.game_status() == "In Progress" and game.turn_monitor == 1:
        
        if check == 0 or check == 1:
            os.system(f"espeak '{username} turn please give a command'")
        else: 
            os.system(f"espeak '{username} turn.'")
        with mic as source:
            print('Command should be your position that you want to put your mark [1-9].')
            print('Tell your command: ')
            audio = r.listen(source)
        try :
            text = r.recognize_google(audio)
            text = text.lower()
            print(f"Text: {text}")

            # command 1
            if str(text) in spellLists["1"]:
                player_move = (0, 0)
                print(f"=====================================")
                print(f"Your command is marking position : 1")
                print(f"=====================================")
            # command 2
            elif str(text) in spellLists["2"]:
                player_move = (0, 1)
                print(f"=====================================")
                print(f"Your command is marking position : 2")
                print(f"=====================================")
            # command 3
            elif str(text) in spellLists["3"]:
                player_move = (0, 2)
                print(f"=====================================")
                print(f"Your command is marking position : 3")
                print(f"=====================================")
            # command 4
            elif str(text) in spellLists["4"]:
                player_move = (1, 0)
                print(f"=====================================")
                print(f"Your command is marking position : 4")
                print(f"=====================================")
            # command 5
            elif str(text) in spellLists["5"]:
                player_move = (1, 1)
                print(f"=====================================")
                print(f"Your command is marking position : 5")
                print(f"=====================================")
            # command 6
            elif str(text) in spellLists["6"]:
                player_move = (1, 2)
                print(f"=====================================")
                print(f"Your command is marking position : 6")
                print(f"=====================================")
            # command 7
            elif str(text) in spellLists["7"]:
                player_move = (2, 0)
                print(f"=====================================")
                print(f"Your command is marking position : 7")
                print(f"=====================================")
            # command 8
            elif str(text) in spellLists["8"]:
                player_move = (2, 1)
                print(f"=====================================")
                print(f"Your command is marking position : 8")
                print(f"=====================================")
            # command 9
            elif str(text) in spellLists["9"]:
                player_move = (2, 2)
                print(f"=====================================")
                print(f"Your command is marking position : 9")
                print(f"=====================================")
            else:
                print('Please give a right command.')
                continue

            game_status, board = game.move(game.turn_monitor, player_move)
            draw_cross(locations[player_move])
        
        except:
            os.system("espeak 'Sorry could not recognize your voice'")
            print('Sorry could not recogonize your voice.')
            continue   
    
    else:
        players = ["AI", username]
        
        if game.game_status() == "Draw":
            print(f"{game.game_status}")
            os.system("espeak 'Draw'")
        else:
            print(f"{players[1 - game.turn_monitor]} has {game.game_status()} ")
            os.system(f"espeak '{players[1 - game.turn_monitor]} has won'")
        break
    check += 1           
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT :
            
            running = False
        
        if event.type== pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                
                running = False
                
            
    pygame.time.wait(500)                      
pygame.quit()

# Window for the result
w2= tk.Tk()
w2.geometry("1080x720")

players = ["AI", username]

if game.game_status() == "Draw":
    heading = tk.Label(w2, height = 360, width = 35, font=('cambria', 32), text=f"{game.game_status()}")
    heading.pack()
else:
    heading = tk.Label(w2, height = 360, width = 35, font=('cambria', 32), text=f"{players[1 - game.turn_monitor]} has {game.game_status()}")
    heading.pack()

w2.mainloop()
