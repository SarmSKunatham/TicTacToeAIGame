#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:16:19 2022

@author: lisa
"""

#import sys 
#sys.path.insert(1,"C:\\Users\julia\Desktop")
#from solvematrix_full import *


import pygame
import pygame.freetype
import tkinter as tk
import numpy as np
# Import tictactoe ai
from tictactoeai import tic_tac_toe_game, legal_moves_generator, move_selector, model
#from tictactoeai import playGame


#%%

# Window
start_window = tk.Tk()
start_window.geometry("1080x720")



#text 1
player_name_text = tk.Label(start_window, text="Enter player name").pack(pady = (350, 0))


# case a remplir pour la latitude
player_name = tk.Entry().pack()



form_choice = tk.Menubutton(start_window, text='Choose form', relief=tk.RAISED)
form_choice.menu = tk.Menu(form_choice, tearoff=0)
form_choice["menu"] = form_choice.menu

circle = tk.IntVar()
cross = tk.IntVar()

form_choice.menu.add_checkbutton(label="Circle", variable=circle, onvalue=1, offvalue=0)
form_choice.menu.add_checkbutton(label="Cross", variable=cross, onvalue=1, offvalue=0)
form_choice.pack()



def form():
    
    
    # Circle is 0, cross is 1
    if circle.get() == 1:        
        result = 0
        

    elif cross.get() == 1:
        result = 1
        
    else:
        raise ValueError
    return result




#start button
play_button = tk.Button(start_window, text="Play",bg='green', command=start_window.destroy).pack(pady=5)


start_window.mainloop()


#%%

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





case = [0 for i in range(9)]
case[0] = (160,160)
case[1] = (360,160)
case[2] = (560,160)

case[3] = (160,360)
case[4] = (360,360)
case[5] = (560,360)

case[6] = (160,560)
case[7] = (360,560)
case[8] = (560,560)


case = np.array(case)




def draw_grid():
    
    
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
    
    pygame.draw.circle(screen,pink,center, 70, 8)
    pygame.display.update()
    
    
def draw_cross(center):
    
    
    length = 60
    pygame.draw.line(screen, pink, (center[0] - length, center[1] - length), (center[0] + length, center[1] + length), 8)
    pygame.draw.line(screen, pink, (center[0] - length, center[1] + length ), (center[0] + length, center[1] - length ), 8)
    pygame.display.update()
  


def analyze():
    
    
    A = np.array([[1, 2, 1],
                  [0, 1, 0],
                  [0, 2, 2]])

    return A




def clear():
    
    screen.fill(white)


def draw_names(choice) :
    
    if choice == 1 :
        font.render_to(screen, (280,10), "Player : Cross", black)
        pygame.display.flip()
        
        font.render_to(screen, (280,30), " Robot : Circle", black)
        pygame.display.flip()

    if choice == 0 :
        font.render_to(screen, (280,10), "Player : Circle", black)
        pygame.display.flip()
        
        font.render_to(screen, (280,30), " Robot : Cross", black)
        pygame.display.flip()




# Game
# Initialize game
game = tic_tac_toe_game()

# toss who play first
game.toss()

print("Starting the game!!!\n")
print(f"Player {game.turn_monitor} play first\n")
print(f"Initialize board: \n {game.board}")

running=True

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
player_moves = {
        1: (0, 0),
        2: (0, 1),
        3: (0, 2),
        4: (1, 0),
        5: (1, 1),
        6: (1, 2),
        7: (2, 0),
        8: (2, 1),
        9: (2, 2)
    }

while running :
    
    #clear()
    draw_grid()
    
    # AI turn
    if game.game_status() == "In Progress" and game.turn_monitor == 0:
        # If its the program's turn, use the Move Selector function to select the next move
        selected_move,new_board_state,score = move_selector(model, game.board, game.turn_monitor)
        
        game_status, board = game.move(game.turn_monitor, selected_move)
        
        #print(selected_move)
        #print(locations[selected_move])
        draw_circle(locations[selected_move])
    
    # Player turn
    elif game.game_status() == "In Progress" and game.turn_monitor == 1:
        try :
            player_move = int(input("Your turn to move: "))
            player_move = player_moves[player_move]

        # Catch error
        except:
            player_move = int(input("Please make an valid move!: "))
            player_move = player_moves[player_move]
        
        game_status, board = game.move(game.turn_monitor, player_move)
        
        #print(player_move)
        #print(locations[player_move])
        draw_cross(locations[player_move])
    
    else:
        players = ["AI", "Player"]
        
        if game.game_status() == "Draw":
            print(f"{game.game_status}")
        else:
            print(f"{players[1 - game.turn_monitor]} has {game.game_status()} ")
        break
        
        
    # playGame()
    
    # choice = form()    
    # draw_names(choice)
    
    # A = np.random.randint(0,3,9).reshape((3,3))
    # A  = A.flatten()
    # for i in range(9):
        # if A[i] == 0 :
            #draw_circle(case[i])
            
        #if A[i] == 1 :
            #draw_cross(case[i])
        
        
        
        
        
        
        
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT :
            
            running = False
        
        if event.type== pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                
                running = False
                
            
    pygame.time.wait(500)       
                
                
                
                
pygame.quit()





#%%



# ouverture de la fenetre
w2= tk.Tk()
w2.geometry("1080x720")


if True  :
        
    titrept1 = tk.Label(w2, height=2, width=35, font=('cambria', 32),
                        text="Player wins :)")
    titrept1.pack()


else :
     titrept1 = tk.Label(w2, height=2, width=35, font=('cambria', 32),
                        text="Robot wins :(")
     titrept1.pack()


w2.mainloop()
