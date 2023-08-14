# import necessary modules
import pandas as pd
import pygame
import time
import cv2
import csv
import random
import multiprocessing
import numpy as np
import gensim.downloader as api
import ssl
import threading
from gensim import models
from gensim.models import KeyedVectors
from ffpyplayer.player import MediaPlayer


if __name__ == '__main__':
    multiprocessing.freeze_support()

FPS = 60

# initialize Pygame
pygame.init()

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (235, 65, 65)
GREEN = (4, 99, 7)
#BLUE = (47, 98, 220)
BLUE = (72, 117, 242)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
BEIGE = (245, 245, 220)

# define screen size
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 921
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
# create the Pygame display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

# hide mouse cursor
pygame.mouse.set_visible(False)

# load my cursor
cursor = pygame.image.load("cursor1.png")

# load sounds
click_sound = pygame.mixer.Sound("click1.mp3")
click_sound.set_volume(0.1)

# define font
tinyfont = pygame.font.Font("ARMY RUST.ttf", 20)
smallfont = pygame.font.Font("ARMY RUST.ttf", 30)
medfont = pygame.font.Font("ARMY RUST.ttf", 50)
largefont = pygame.font.Font("ARMY RUST.ttf", 80)
hugefont = pygame.font.Font("ARMY RUST.ttf", 450)
bigfont = pygame.font.Font("ARMY RUST.ttf", 250)
medlargefont = pygame.font.Font("ARMY RUST.ttf", 200)

# time
FPS = 40 #frames per second
clock = pygame.time.Clock()

# define the duration of the fade-in effect in milliseconds
FADE_DURATION = 2000

ssl._create_default_https_context = ssl._create_unverified_context
model = None
# model = api.load('glove-wiki-gigaword-300')

# Open the CSV file and read its contents
with open('Words_List.csv', 'r') as f:
    reader = csv.reader(f)
    csv_text = list(reader)

# Extract the column of words as a list
word_list = [row[0].lower() for row in csv_text]

# Randomly choose 25 unique words from the word list
word_test = random.sample(word_list, 25)

# load images
background_image = pygame.image.load("main_light_2.png")
bg_game = pygame.image.load("bg_game.png")
title = pygame.image.load("title.png").convert_alpha()
spymaster = pygame.image.load("spymaster_n.png").convert_alpha()
player = pygame.image.load("playerff.png").convert_alpha()
# operative = pygame.image.load("player_2.png").convert_alpha()
htp = pygame.image.load("how to play 2.png").convert_alpha()
how_to_play_touch = pygame.image.load("htp touch1.png").convert_alpha()
return_button = pygame.image.load("return.png").convert_alpha()
return_button_touch = pygame.image.load("return touch.png").convert_alpha()
red_card = pygame.image.load("red_card.png").convert_alpha()
grey_card = pygame.image.load("grey_card.png").convert_alpha()
clues_touch = pygame.image.load("clues.png").convert_alpha()
clues = pygame.image.load("clues_touched.png").convert_alpha()
quit = pygame.image.load("exit.png").convert_alpha()
quit_touch = pygame.image.load("exit_touch.png").convert_alpha()
mute = pygame.image.load("mute.png").convert_alpha()
play_sound = pygame.image.load("play_sound.png").convert_alpha()
reset = pygame.image.load("reset.png").convert_alpha()
reset_touch = pygame.image.load("reset_touch.png").convert_alpha()

spymaster_x, spymaster_y = 910 / 1892 * SCREEN_WIDTH, 330 / 1161 * SCREEN_HEIGHT
spymaster_width, spymaster_height = 310 / 1892 * SCREEN_WIDTH, 700 / 1161 * SCREEN_HEIGHT

player_x, player_y = 1348 / 1892 * SCREEN_WIDTH, 375 / 1161 * SCREEN_HEIGHT
player_width, player_height = 277 / 1892 * SCREEN_WIDTH, 655 / 1161 * SCREEN_HEIGHT

how_to_play_x, how_to_play_y = 20, 20
how_to_play_width, how_to_play_height = 322, 58

quit_x, quit_y = SCREEN_WIDTH - 370, SCREEN_HEIGHT - 100
quit_width, quit_height = 1000, 1000

return_x, return_y = SCREEN_WIDTH - 1470, SCREEN_HEIGHT - 100
return_width, return_height = 730, 320

title_x, title_y = (SCREEN_WIDTH - 1200) / 2, 80
title_width, title_height = 686, 80

clues_x, clues_y = 100, SCREEN_HEIGHT / 2 - 200
clues_width, clues_height = 150, 200

Clues_rect = pygame.Rect(clues_x, clues_y, clues_width, clues_height)

clues_touch_x, clues_touch_y = 100, SCREEN_HEIGHT / 2 - 200
clues_touch_width, clues_touch_height = 150, 200

mute_x, mute_y = SCREEN_WIDTH - 200, SCREEN_HEIGHT - 900
mute_width, mute_height = 1000, 1000
mute_rect = mute.get_rect(topleft=(mute_x, mute_y))

reset_x, reset_y = SCREEN_WIDTH - 270, 80
reset_rect = reset.get_rect(topleft=(reset_x, reset_y))
reset_touch_rect = reset_touch.get_rect(topleft=(reset_x, reset_y))

cell_width, cell_height = 180, 100

# get the position of each cell and save it in a list
cell_pos = []
for i in range(5):
    for j in range(5):
        cell_pos.append((SCREEN_WIDTH / 5 + cell_width * i, SCREEN_HEIGHT / 4 + cell_height * j))

# get the center of each cell and save it in a list
cell_center = [(x + cell_width / 2, y + cell_height / 2) for x, y in cell_pos]

# create a copy of the cell_pos list and shuffle it
cell_pos_copy = cell_pos.copy()
random.shuffle(cell_pos_copy)

# get the center of each cell and save it in a list again
cell_center_shuffle = [(x + cell_width / 2, y + cell_height / 2) for x, y in cell_pos_copy]

# create a list of colors for each cell
cell_colors = [RED] * 9 + [BLUE] * 8 + [WHITE] * 7 + [GRAY] * 1

# initialize variables for user input, number of similar items, and input image
input = ''
num_similar = ''
input_image = pygame.image.load("input_name.png")  

# define rectangles for positioning input elements on the screen
input_rect = input_image.get_rect(topleft=(100, SCREEN_HEIGHT / 2 - 200))  
num_rect = input_image.get_rect(topleft=(100, SCREEN_HEIGHT / 2 - 60))     
go_rect = input_image.get_rect(topleft=(100, SCREEN_HEIGHT / 2 + 80))   

# define colors for active and passive states of input elements
color_active = pygame.Color('lightskyblue3')   # color when the element is active (selected)
color_passive = pygame.Color('gray15')          # color when the element is not active

# initialize the initial color as passive
color = color_passive

# initialize flags to track the active state of input elements
active = False   # tracks if input field is active
active2 = False  # tracks if number input field is active

# define a dictionary to map font sizes to font objects
font_sizes = {
    "small": smallfont,
    "medium": medfont,
    "large": largefont,
    "tiny": tinyfont,
    "huge": hugefont,
    "big": bigfont,
    "medlarge": medlargefont
}

# function to display text on the screen
def text_object(text, color, size):
    selected_font = font_sizes.get(size, medfont)  # Default to medfont if size is not found
    text_surface = selected_font.render(text, True, color)
    return text_surface, text_surface.get_rect()

# function to display text on the screen
def message_to_screen(msg, color, y_display=0, size="small"):
    textSerf, textRec = text_object(msg, color, size)
    textRec.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_display)
    screen.blit(textSerf, textRec)

# function to display text on the screen
def text_to_screen(msg, color, x, y, size="small"):
    textSerf, textRec = text_object(msg, color, size)
    textRec.center = (x, y)
    screen.blit(textSerf, textRec)

# function to display role names on the screen
def role_to_screen(msg, color, size="small", role="spymaster"):
    textSerf, textRec = text_object(msg, color, size)
    if role == "spymaster":
        textRec.center = (spymaster_x + spymaster_width / 2, spymaster_y - 60)
    if role == "player":
        textRec.center = (player_x + player_width / 2, player_y - 60)
    screen.blit(textSerf, textRec)

# function to create interactive buttons
def role_button(image, x, y, width, height, action=None):
    button_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    button_surface.blit(image, (0, 0))
    button_rect = pygame.Rect(x, y, width, height)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if button_rect.collidepoint(mouse):
        screen.blit(button_surface, (0, 0))
        if click[0] == 1 and action != None:
            click_sound.play()
            action()

# function to create a button
def create_button(image1, image2, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        screen.blit(image1, (x, y))
        if click[0] == 1 and action != None:
            click_sound.play()
            action()
    else:
        screen.blit(image2, (x, y))

def reset_button(image1, image2, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        screen.blit(image1, (x, y))
        if click[0] == 1 and action != None:
            click_sound.play()
            action()
    else:
        screen.blit(image2, (x+30, y+30))


# function to create a button
def button(image1, image2, x, y, width, height):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        screen.blit(image1, (x, y))
        if click[0] == 1:
            click_sound.play()
    else:
        screen.blit(image2, (x, y))

stage = 2

# function to create sound button
def sound_button(image1, image2, x, y, button_rect):
    global stage
    if stage == 2:
        screen.blit(image1, (x, y))
    if stage == 1:
        screen.blit(image2, (x, y))
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(pos):
                if stage == 1:
                    # play music
                    pygame.mixer.music.play(-1)
                    stage = 2
                elif stage == 2:
                    # stop playing music
                    pygame.mixer.music.stop()
                    stage = 1

# define the function for the fade-in effect
def fade_in():
    # create a surface to use for the fade-in effect
    fade_surface = pygame.Surface(SCREEN_SIZE)
    fade_surface.fill(BLACK)
    fade_surface.set_alpha(255)
    screen.blit(fade_surface, (0, 0))
    pygame.display.flip()

    # loop over the duration of the fade-in effect, gradually increasing the alpha value
    for alpha in range(0, 256):
        fade_surface.set_alpha(255 - alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(FADE_DURATION / 256))

    # fill the screen with white to ensure it's completely opaque
    screen.fill(WHITE)
    pygame.display.flip()

# define a function to load a model and put it into a queue
def load_model(queue):
    global model
    # load the model
    model = api.load('glove-wiki-gigaword-300')
    # put the model in the queue
    queue.put(model)

# define the function to run the model loading and video playing in parallel
def run_parallel():
    global model
    # create a queue for communication
    queue = multiprocessing.Queue()

    # start the process for loading the model
    model_process = multiprocessing.Process(target=load_model, args=(queue,))
    model_process.start()

    # play the video while waiting for the model to load
    play_video()
    
    # wait for the model to finish loading and get the result from the queue
    model = queue.get()
    model_process.join()
    print(model)

    # load the background music file
    pygame.mixer.music.load("BG.mp3")
    # set music volume to 0.2
    pygame.mixer.music.set_volume(0.2)

    # start playing the music, with loop set to -1 to play it continuously
    pygame.mixer.music.play(-1)

    # start the game intro with the loaded model
    game_intro()

def play_video():
    file = "Opening.mp4"
    video = cv2.VideoCapture(file)
    player = MediaPlayer(file)
    
    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(30)  # Adjust the frame rate as needed
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        ret, frame = video.read()
        audio_frame, val = player.get_frame()
        
        if not ret:
            print("End of video")
            break
        
        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame
        
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        video_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")
        
        screen.blit(video_surf, (0, 0))
        pygame.display.flip()
        
        if cv2.waitKey(1) == ord("q"):
            break
    
    video.release()
    cv2.destroyAllWindows()

# function to draw a 5*5 grid at the center of the screen
def draw_grid():
    for i in range(5):
        for j in range(5):
            pygame.draw.rect(screen,
                             BLACK,
                             (SCREEN_WIDTH / 5 + cell_width * i, SCREEN_HEIGHT / 4 + cell_height * j, cell_width,
                              cell_height),
                             5)


# funtion to display words on the game board
def word_to_board(msg, color, size="small"):
    for i in range(25):
        textSerf, textRec = text_object(msg[i], color, size)
        textRec.center = cell_center_shuffle[i]
        screen.blit(textSerf, textRec)


# funtion to fill colors to the cells
def fill_color():
    # fill the first 9 cells with red color
    for i in range(9):
        pygame.draw.rect(screen,
                         RED,
                         (cell_pos_copy[i][0], cell_pos_copy[i][1], cell_width - 5, cell_height - 5))
    # fill the next 8 cells with blue color
    for i in range(9, 17):
        pygame.draw.rect(screen,
                         BLUE,
                         (cell_pos_copy[i][0], cell_pos_copy[i][1], cell_width - 5, cell_height - 5))
    # fill the next 7 cells with white color
    for i in range(17, 24):
        pygame.draw.rect(screen,
                         WHITE,
                         (cell_pos_copy[i][0], cell_pos_copy[i][1], cell_width - 5, cell_height - 5))
    # fill the last cell with grey color
    for i in range(24, 25):
        pygame.draw.rect(screen,
                         GRAY,
                         (cell_pos_copy[i][0], cell_pos_copy[i][1], cell_width - 5, cell_height - 5))


# function to get word, color and position of each cell
def get_word_color_pos(game_board_words, cell_colors, cell_pos_copy):
    for i in range(len(game_board_words)):
        tile = {'word': game_board_words[i], 'position': cell_pos_copy[i], 'color': cell_colors[i]}
        word_color_pos.append(tile)
    return word_color_pos


# function to search a word in the word list

red_list = []
blue_list = []
white_list = []
yellow_list = []
grey_list = []
results = []
word_color_pos = []
get_word_color_pos(word_test, cell_colors, cell_pos_copy)
clue_wpc = word_color_pos.copy()


# print(word_color_pos)
def search_word(word_list, guess_word):
    for word in guess_word:
        for item in word_list:
            if item['word'] == word:
                color = item['color']
                if color == GRAY:
                    if item in grey_list:
                        break
                    else:
                        grey_list.append(item)
                elif color == BLUE:
                    pass
                    blue_list.append(item)
                elif color == RED:
                    if item in red_list:
                        break
                    else:
                        red_list.append(item)
                elif color == WHITE:
                    pass
                    white_list.append(item)
        else:
            print("continue")
            pass
    # return results


# funtion to display words on the game board again
def word_guess_correct(msg, color, cellCenter, size="small"):
    textSerf, textRec = text_object(msg, color, size)
    textRec.center = cellCenter
    screen.blit(textSerf, textRec)


# function to guess words
def get_word_similarity(model, input_word, game_board_words, num_similar_words=5):
    # Check if input word is in the model's vocabulary
    if input_word not in model.key_to_index:
        # convert the word to uppercase
        input_word = input_word.capitalize()
    # Get the word vectors for the input word and game board words
    input_vector = model.get_vector(input_word)
    # Check if game board words are in the model's vocabulary
    for i, word in enumerate(game_board_words):
        if word not in model.key_to_index:
            # convert the word to uppercase
            game_board_words[i] = word.capitalize()
    game_board_vectors = np.array([model.get_vector(word) for word in game_board_words])

    # Calculate cosine similarities between input vector and game board vectors
    similarities = {}
    for i, word in enumerate(game_board_words):
        similarity = np.dot(input_vector, game_board_vectors[i]) / (
                    np.linalg.norm(input_vector) * np.linalg.norm(game_board_vectors[i]))
        similarities[word] = similarity

    # Sort similarities in descending order and return
    sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:int(num_similar_words)]

    return sorted_similarities


# function to get red word
def get_red_word(word_position_color):
    red_words = [w for w in word_position_color if w['color'] == RED]
    print(red_words)
    if not red_words:
        return None
    word = random.choice(red_words)['word']
    for w in word_position_color:
        if w['word'] == word:
            word_position_color.remove(w)
            break
    return word


# function to generate clues for word1
def generate_clues_word(word):
    clue_list = []

    print('q' + str(model))
    # check if word is in the model's vocabulary
    if word not in model.key_to_index:
        # convert the word to capitalize
        word = word.capitalize()
    similar_words = model.most_similar(word, topn=10)
    clues = []
    for sim_word in similar_words:
        clues.append(sim_word[0])
        if len(clues) == 4:
            break
    if clues:
        clue_list.append({word: clues})
    # clue_list = [w for w in clue_list if w in english_words]

    return clue_list


# function to get the first word in the clue list
def get_first_word(clue_list):
    first_word = list(clue_list[0].values())[0][3]
    return first_word


# function to get input for input_word and num_similar_words
def get_input_spy():
    input_word = input("Enter a word: ")
    num_similar_words = int(input("Enter the number of similar words to display: "))
    return input_word, num_similar_words


def get_input_player():
    input_word = input("Enter a word: ")
    return input_word


def get_clicked_word(mouse_pos, word_position_color):
    for word_dict in word_position_color:
        word_pos = word_dict['position']
        if (word_pos[0] <= mouse_pos[0] <= word_pos[0] + cell_width and
                word_pos[1] <= mouse_pos[1] <= word_pos[1] + cell_height):
            return word_dict['word'], word_dict['position']

def game_intro():
    global model
    print(model)

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        screen.blit(background_image, (0, 0))
        role_to_screen("Spymaster", BLACK, "medium", "spymaster")
        role_to_screen("Player", BLACK, "medium", "player")
        mouse_x, mouse_y = pygame.mouse.get_pos()
        role_button(player, player_x, player_y, player_width, player_height, player_mode)
        role_button(spymaster, spymaster_x, spymaster_y, spymaster_width, spymaster_height, spymaster_mode)
        create_button(how_to_play_touch, htp, how_to_play_x, how_to_play_y, how_to_play_width, how_to_play_height,
                      how_to_play)
        create_button(quit_touch, quit, quit_x, quit_y, quit_width, quit_height, quit_game)
        screen.blit(title, [title_x, title_y])
        sound_button(mute, play_sound, mute_x, mute_y, mute_rect)
        screen.blit(cursor, (mouse_x - 142, mouse_y - 142))

        pygame.display.update()
        clock.tick()


# quit the game
def quit_game():
    pygame.quit()
    exit()


def how_to_play():
    htp = True

    while htp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(background_image, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        create_button(return_button_touch, return_button, return_x, return_y, return_width, return_height, game_intro)
        message_to_screen("Codenames is a game of guessing which code names (words) ", BLACK, -400, "small")
        message_to_screen("in a set are related to a hint-word given by another player (the spymaster). "
                          , BLACK, -330, "small")
        message_to_screen(
            "The other players (the field operatives) try to guess their team's words while avoiding the words of the other team.",
            BLACK, -260, "small")
        screen.blit(cursor, (mouse_x - 142, mouse_y - 142))

        pygame.display.update()
        clock.tick(60)

# function to reset spymaster mode
def reset_spymaster():
    red_list = []
    blue_list = []
    white_list = []
    yellow_list = []
    grey_list = []
    results = []


def spymaster_mode():
    global model
    #red_list = []
    blue_list = []
    white_list = []
    yellow_list = []
    #grey_list = []
    results = []
    spy = True
    active = False
    active2 = False
    input_word = ""
    num_similar_words = 0
    input = ""
    num_similar = ""
    input_warning = False  # add flag to control message display
    result = False  # add flag to control message display
    incorrect = False  # add flag to control message display

    while spy:
        screen.fill(WHITE)
        screen.blit(bg_game, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # get input word and number of similar words
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                if input_rect.collidepoint(event.pos):
                    input = ""
                    active = True
                else:
                    active = False

                if num_rect.collidepoint(event.pos):
                    num_similar = ""
                    active2 = True
                else:
                    active2 = False

            if event.type == pygame.KEYDOWN:
                incorrect = False  # add flag to control message display
                click_sound.play()
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        input = input[:-1]
                    else:
                        input += event.unicode
                if active2:
                    if event.key == pygame.K_BACKSPACE:
                        num_similar = num_similar[:-1]
                    else:
                        num_similar += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if go_rect.collidepoint(event.pos):
                    if input == "" or num_similar == "":
                        input_warning = True  # set flag to display message
                    # check if input word is in the model's vocabulary
                    elif input not in model.key_to_index:
                        incorrect = True  # set flag to display message

                    else:
                        input_warning = False  # set flag to display message
                        result = True  # set flag to display message
                        incorrect = False  # set flag to display message
                        input_word = input
                        num_similar_words = num_similar

                        top_similar_words = get_word_similarity(model, input_word, word_test, num_similar_words)
                        top = " ".join([f"{t[0]} ({t[1]:.2f})" for t in top_similar_words])
                        guesses = [t[0] for t in top_similar_words]

        if active:
            color = color_active
        else:
            color = color_passive
        screen.blit(input_image, input_rect)  # blit the image onto the screen at the position of the input_rect
        text_to_screen("Deploy Your Guess", BLACK, input_rect.x + 75, input_rect.y - 25, "small")

        if active2:
            color = color_active
        else:
            color = color_passive
        screen.blit(input_image, num_rect)
        text_to_screen("Words In Play", BLACK, input_rect.x + 75, num_rect.y - 25, "small")

        screen.blit(input_image, go_rect)
        text_to_screen("Execute!", BLACK, input_rect.x + 75, go_rect.y + 40, "small")
        text_surface1 = smallfont.render(input, True, BLACK)
        text_surface2 = smallfont.render(num_similar, True, BLACK)
        screen.blit(text_surface1, (input_rect.x + 5, input_rect.y + 5))
        screen.blit(text_surface2, (num_rect.x + 5, num_rect.y + 5))

        draw_grid()
        fill_color()

        word_to_board(word_test, BLACK, "small")
        mouse_x, mouse_y = pygame.mouse.get_pos()
        create_button(return_button_touch, return_button, return_x, return_y, return_width, return_height, game_intro)
        message_to_screen("Spymaster mode", BLACK, -400, "large")
        reset_button(reset_touch, reset, reset_x, reset_y, reset_rect.width, reset_rect.height, reset_spymaster)


        if incorrect:
            text_to_screen("Please enter a word correctly",
                           BLACK,
                           175,
                           SCREEN_HEIGHT / 2 + 180,
                           "tiny")
        if input_warning:
            text_to_screen("Please enter a word and",
                           BLACK,
                           175,
                           SCREEN_HEIGHT / 2 + 180,
                           "tiny")
            text_to_screen("number of similar words",
                           BLACK,
                           175,
                           SCREEN_HEIGHT / 2 + 210,
                           "tiny")
        if result:
            search_word(word_color_pos, guesses)
            message_to_screen(top, BLACK, +330, "small")
        for item in grey_list:
            screen.blit(grey_card, (item['position'][0], item['position'][1]))
            cellCenter = (item['position'][0] + cell_width / 2, item['position'][1] + cell_height / 2)
            word_guess_correct(item['word'], BLACK, cellCenter, size="small")

        for item in red_list:
            screen.blit(red_card, (item['position'][0], item['position'][1]))
            cellCenter = (item['position'][0] + cell_width / 2, item['position'][1] + cell_height / 2)
            word_guess_correct(item['word'], BLACK, cellCenter, size="small")
        print(red_list)
        print(len(red_list))
        if len(red_list) == 9:
            message_to_screen("MISSION COMPLETE!", GREEN, 0, "medlarge")
        if len(grey_list) == 1:
            message_to_screen("MISSION FAILED!", BLACK, 0, "big")

        screen.blit(cursor, (mouse_x - 142, mouse_y - 142))
        pygame.display.update()
        clock.tick(30)


def player_mode():
    clue_wpc = word_color_pos.copy()
    global model
    #    active = False
    operative = True
    input_warning = False
    clue_list = []
    clue = []
    #    input = ""
    correct_words = []
    team_score = 0

    while operative:
        screen.fill(WHITE)
        screen.blit(bg_game, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # get input word and number of similar words
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                mouse_pos = pygame.mouse.get_pos()
                if Clues_rect.collidepoint(event.pos):
                    red_word = get_red_word(clue_wpc)
                    print(red_word)
                    clue_list = generate_clues_word(red_word)
                    clue = get_first_word(clue_list)
                    input_warning = True

                clicked_word_data = get_clicked_word(mouse_pos, word_color_pos)
                if clicked_word_data is not None:
                    word, clicked_word_pos = clicked_word_data
                    # iterate through clue_list to see if the answer is correct
                    for dict in clue_list:
                        for key in dict:
                            if word == key:
                                # add a point to the team
                                team_score += 1
                                # Add correct word to correct_words list
                                correct_words.append({'word': word, 'position': clicked_word_pos})
                            # elif word != key:


        if active:
            color = color_active
        else:
            color = color_passive

        draw_grid()
        word_to_board(word_test, BLACK, "small")
        # screen.blit(background_image, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button(clues_touch, clues, clues_x, clues_y, clues_width, clues_height)
        create_button(return_button_touch, return_button, return_x, return_y, return_width, return_height, game_intro)
        message_to_screen("operative mode", BLACK, -400, "large")

        if input_warning:
            text_to_screen(clue,
                           BLACK,
                           175,
                           SCREEN_HEIGHT / 2 + 100,
                           "medium")

        for item in correct_words:
            screen.blit(red_card, item['position'])
            cellCenter = (item['position'][0] + cell_width / 2, item['position'][1] + cell_height / 2)
            word_guess_correct(item['word'], BLACK, cellCenter, size="small")

        if team_score == 9:
            message_to_screen("MISSION COMPLETE!", GREEN, 0, "medlarge")

        screen.blit(cursor, (mouse_x - 142, mouse_y - 142))
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    model = run_parallel()

