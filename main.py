# IPA MEMORY Game created by Sotirios Gkosdis and Alexander Weyhe

import pygame, random
import sys
from images import *

pygame.init()

# Set up the game window
width, height = 1000, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("IPA Memory Game")

# different colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# different font types
font = pygame.font.SysFont("Times New Roman", 35)
font2 = pygame.font.SysFont("Times New Roman", 45)
font3 = pygame.font.SysFont("Times New Roman", 15)

# counter for the tries and pairs.
all_pairs = 0
all_tries = 0

# A list that holds the cards the user has selected.
selected_cards = []

# Truth values for game modes.
easy_mode = False
hard_mode = False
goat_mode = False

# Truth values for showing the start screen and creating the game board.
show_start_screen = True
new_board = True


# A Class to create the individual cards.
# As arguments, it takes an image, the position on the screen, and a matching parameter (the two/three cards that should
# match get the same matching argument, e.g.: image1 -> matching=1 and image2 -> matching=1).
class Card:
    def __init__(self, image, position, matching):
        self.image = image
        self.position = position
        self.rect = self.image.get_rect(topleft=position)
        self.is_face_up = False
        self.matching = matching

    # This function is used to update the position of each card (This applies to the cards we use in easy and hard mode). 
    # When we initiate each card object they all get the same position on the screen. We only have 12 positions on the screen, 
    # but there are 44 images. Therefore, there would be overlapping positions. After selecting randomly 
    # 6 card pairs or four card triples (so 12 individual cards), we update the position of each card that will be used for 
    # this round of memory. Each round we have different cards in different positions.
    def update_position(self, new_position):
        self.position = new_position
        self.rect = self.image.get_rect(topleft=new_position)


# Here, we have a list of tuples each consisting of the positions for the cards on the screen. We use these positions for
# the modes easy and hard.
card_positions = [
    (50, 50), (300, 50), (550, 50), (800, 50),
    (50, 300), (300, 300), (550, 300), (800, 300),
    (50, 550), (300, 550), (550, 550), (800, 550)
]

# This list consists of tuples that hold the positions for the cards on the screen. These positions are used for the
# goat mode.
card_positions_goat = [
            (5, 120), (95, 120), (185, 120), (275, 120), (365, 120), (455, 120), (545, 120), (635, 120), (725, 120),(815, 120), (905, 120),
            (5, 260), (95, 260), (185, 260), (275, 260), (365, 260), (455, 260), (545, 260), (635, 260), (725, 260), (815, 260), (905, 260),
            (5, 400), (95, 400), (185, 400), (275, 400), (365, 400), (455, 400), (545, 400), (635, 400), (725, 400), (815, 400), (905, 400),
            (5, 540), (95, 540), (185, 540), (275, 540), (365, 540), (455, 540), (545, 540), (635, 540), (725, 540), (815, 540), (905, 540)
]

# These lists create a class object for each card that we use in the game.
# This lists consists of tuples that hold two card class objects that should match. We use this list for the easy mode.
cards_easy = [(Card(image1_normal, card_positions[0], 1), Card(image2_normal, card_positions[0], 1)),
              (Card(image3_normal, card_positions[0], 2), Card(image4_normal, card_positions[0], 2)),
              (Card(image5_normal, card_positions[0], 3), Card(image6_normal, card_positions[0], 3)),
              (Card(image7_normal, card_positions[0], 4), Card(image8_normal, card_positions[0], 4)),
              (Card(image9_normal, card_positions[0], 5), Card(image10_normal, card_positions[0], 5)),
              (Card(image11_normal, card_positions[0], 6), Card(image12_normal, card_positions[0], 6)),
              (Card(image13_normal, card_positions[0], 7), Card(image14_normal, card_positions[0], 7)),
              (Card(image15_normal, card_positions[0], 8), Card(image16_normal, card_positions[0], 8)),
              (Card(image17_normal, card_positions[0], 9), Card(image18_normal, card_positions[0], 9)),
              (Card(image19_normal, card_positions[0], 10), Card(image20_normal, card_positions[0], 10)),
              (Card(image21_normal, card_positions[0], 11), Card(image22_normal, card_positions[0], 11)),
              (Card(image23_normal, card_positions[0], 12), Card(image24_normal, card_positions[0], 12)),
              (Card(image25_normal, card_positions[0], 13), Card(image26_normal, card_positions[0], 13)),
              (Card(image27_normal, card_positions[0], 14), Card(image28_normal, card_positions[0], 14)),
              (Card(image29_normal, card_positions[0], 15), Card(image30_normal, card_positions[0], 15)),
              (Card(image31_normal, card_positions[0], 16), Card(image32_normal, card_positions[0], 16)),
              (Card(image33_normal, card_positions[0], 17), Card(image34_normal, card_positions[0], 17)),
              (Card(image35_normal, card_positions[0], 18), Card(image36_normal, card_positions[0], 18)),
              (Card(image37_normal, card_positions[0], 19), Card(image38_normal, card_positions[0], 19)),
              (Card(image39_normal, card_positions[0], 20), Card(image40_normal, card_positions[0], 20)),
              (Card(image41_normal, card_positions[0], 21), Card(image42_normal, card_positions[0], 21)),
              (Card(image43_normal, card_positions[0], 22), Card(image44_normal, card_positions[0], 22))
              ]

# This list consists of tuples that hold three card class objects that should match. We use these positions for the hard
# mode.
cards_hard = [(Card(image45, card_positions[0], 1), Card(image2_normal, card_positions[0], 1),
               Card(image4_normal, card_positions[0], 1)),
              (Card(image46, card_positions[0], 2), Card(image6_normal, card_positions[0], 2),
               Card(image8_normal, card_positions[0], 2)),
              (Card(image47, card_positions[0], 3), Card(image10_normal, card_positions[0], 3),
               Card(image12_normal, card_positions[0], 3)),
              (Card(image48, card_positions[0], 4), Card(image14_normal, card_positions[0], 4),
               Card(image16_normal, card_positions[0], 4)),
              (Card(image49, card_positions[0], 5), Card(image18_normal, card_positions[0], 5),
               Card(image20_normal, card_positions[0], 5)),
              (Card(image50, card_positions[0], 6), Card(image22_normal, card_positions[0], 6),
               Card(image24_normal, card_positions[0], 6)),
              (Card(image51, card_positions[0], 7), Card(image26_normal, card_positions[0], 7),
               Card(image28_normal, card_positions[0], 7)),
              (Card(image52, card_positions[0], 7), Card(image30_normal, card_positions[0], 7),
               Card(image32_normal, card_positions[0], 7)),
              (Card(image53, card_positions[0], 8), Card(image34_normal, card_positions[0], 8),
               Card(image36_normal, card_positions[0], 8)),
              (Card(image54, card_positions[0], 9), Card(image38_normal, card_positions[0], 9),
               Card(image40_normal, card_positions[0], 9)),
              (Card(image55, card_positions[0], 10), Card(image42_normal, card_positions[0], 10),
               Card(image44_normal, card_positions[0], 10))
              ]


# This function was created with help from ChatGPT. It draws text on a rectangle or ellipse.
def draw_text( text, figure, color, font):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (figure.x + figure.width // 2, figure.y + figure.height // 2)
    screen.blit(text_surface, text_rect)


# This function was created with help from ChatGPT. It draws multiple lines of text on a rectangle or ellipse.
def draw_multiline_text_in_rect(lines, figure):
    y_offset = figure.top
    for line in lines:
        text_surface = font3.render(line, True, BLACK)
        text_rect = text_surface.get_rect(topleft=(figure.left, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += text_rect.height


# This function was created with help from ChatGPT. It draws a frame around a rectangle.
def draw_frame_rect(figure_x, figure_y, figure_width, figure_height):
    return pygame.draw.rect(screen, BLACK, (figure_x - 3, figure_y - 3,
                                            figure_width + 2 * 3, figure_height + 2 * 3), 3)


# This function was created with help from ChatGPT. It draws a frame around an ellipse.
def draw_frame_ellipse(ellipse_center_x, ellipse_center_y, ellipse_width, ellipse_height):
    return pygame.draw.ellipse(screen, BLACK, (ellipse_center_x - ellipse_width / 2 - 3,
                                        ellipse_center_y - ellipse_height / 2 - 3,
                                        ellipse_width + 2 * 3,
                                        ellipse_height + 2 * 3), 3)


# This function is used to show the final screen of the game.
def show_final_screen():
    # the variables end_game and replay_game hold the button for ending or replaying the game respectively.
    # We use global so we can detect the collidepoint with the mouse inside our game while loop.
    global end_game, replay_game

    # This draws the screen.
    screen.fill(pygame.Color("lightblue"))
    screen.blit(font2.render("Congratulations!", True, WHITE), (300, 100))
    screen.blit(font2.render(f"Tries: {all_tries}.", True, WHITE), (300, 200))

    # This creates the buttons and adds the text as well as the frame.
    end_game = pygame.draw.ellipse(screen, WHITE, (200, 400, 150, 90))
    draw_text("QUIT", end_game, BLACK, font)
    draw_frame_ellipse(end_game.centerx, end_game.centery, end_game.width, end_game.height)

    replay_game = pygame.draw.ellipse(screen, WHITE, (600, 400, 150, 90))
    draw_text("REPLAY", replay_game, BLACK, font)
    draw_frame_ellipse(replay_game.centerx, replay_game.centery, replay_game.width, replay_game.height)


# This funtion resets the game.
def reset_game():
    # We reset all the variables to the default values so the while loop can start at the very beginning of the game and
    # the user can restart any game mode they want. Also, the variables for creating and randomizing the game board are
    # reset. The global statements make sure that we change the variables that are outside of the scope of this
    # function.
    global new_board, all_tries, show_start_screen, hard_mode, easy_mode, goat_mode, all_pairs
    global counter_for_all_cards, counter_for_all_card_positions, counter_for_hard_cards, counter_for_hard_card_positions
    show_start_screen = True
    new_board = True
    hard_mode = False
    easy_mode = False
    goat_mode = False
    all_tries = 0
    all_pairs = 0
    counter_for_all_cards = 0
    counter_for_all_card_positions = 0
    counter_for_hard_cards = 0
    counter_for_hard_card_positions = 0


# Here we start the while loop.
while True:

    # At the very beginning we want to show the start screen. Here, the variable show_start_screen is set to True.
    if show_start_screen:

        # First we set up the screen color and add a welcome message to the user.
        screen.fill(pygame.Color("lightblue"))
        screen.blit(font2.render("IPA MEMORY GAME", True, WHITE), (250, 100))
        screen.blit(font2.render("by", True, WHITE), (450, 150))
        screen.blit(font2.render("Sotirios Gkosdis & Alexander Weyhe", True, WHITE), (150, 200))

        # Here, we create the buttons for the different game modes (easy, hard, and goat).
        easy_button = pygame.draw.ellipse(screen, WHITE, (400, 300, 150, 90))
        draw_text("EASY", easy_button, BLACK, font)
        draw_frame_ellipse(easy_button.centerx, easy_button.centery, easy_button.width, easy_button.height)

        hard_button = pygame.draw.ellipse(screen, WHITE, (400, 450, 150, 90))
        draw_text("HARD", hard_button, BLACK, font)
        draw_frame_ellipse(hard_button.centerx, hard_button.centery, hard_button.width, hard_button.height)

        goat_button = pygame.draw.ellipse(screen, WHITE, (400, 600, 150, 90))
        draw_text("G.O.A.T.", goat_button, BLACK, font)
        draw_frame_ellipse(goat_button.centerx, goat_button.centery, goat_button.width, goat_button.height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # We create a variable that holds the positions of the mouse.
        mouse_pos = pygame.mouse.get_pos()

        # If the position of the mouse collides with the position of one of the game modes, a rectangle with the
        # description of the game mode appears for as long as the mouse is on the respective mode button.
        # If the user clicks on one of the game mode buttons, we set the show_start_screen variable to False and the
        # variable for the selected game mode to True. This way we don't show the start screen again and change to the
        # screen with the game.
        if easy_button.collidepoint(mouse_pos):
            easy_description = pygame.draw.rect(screen, WHITE, (650, 300, 155, 200))
            draw_multiline_text_in_rect(["EASY MODE:", "", "MATCH THE VOWEL", "SYMBOL WITH THE", "RIGHT DESCRIPTION", "", "GOOD LUCK!"],
                                        easy_description)
            draw_frame_rect(easy_description.x, easy_description.y, easy_description.width, easy_description.height)

            if event.type == pygame.MOUSEBUTTONUP:
                show_start_screen = False
                easy_mode = True

        elif hard_button.collidepoint(mouse_pos):
            hard_description = pygame.draw.rect(screen, WHITE, (650, 450, 155, 200))
            draw_multiline_text_in_rect(
                ["HARD MODE:", "", "TWO SYMBOLS", "BELONG TO ONE", "DESCRIPTION", "(4x TRIPLE PAIRS)", "", "THE PARAMETER", "ROUNDING IS NOT", "INCLUDED!", "", "GOOD LUCK!"], hard_description)
            draw_frame_rect(hard_description.x, hard_description.y, hard_description.width, hard_description.height)

            if event.type == pygame.MOUSEBUTTONUP:
                show_start_screen = False
                hard_mode = True

        elif goat_button.collidepoint(mouse_pos):
            goat_description = pygame.draw.rect(screen, WHITE, (650, 450, 155, 200))
            draw_multiline_text_in_rect(
                ["GOAT MODE:", "", "ALL 22 VOWELS", "ARE INCLUDED!", "","MATCH THEIR", "DESCRIPTION", "", "GOOD LUCK!"],
                goat_description)
            draw_frame_rect(goat_description.x, goat_description.y, goat_description.width, goat_description.height)

            if event.type == pygame.MOUSEBUTTONUP:
                show_start_screen = False
                goat_mode = True

        pygame.display.flip()

    # Creating the board. After we leave the if-statement for the start screen we want to create a random board.
    elif new_board:

        # We shuffle the list of card positions everytime we create a new board.
        random.shuffle(card_positions)
        random.shuffle(card_positions_goat)

        # The list with the card class objects for the goat mode is inside the game loop because we want to make sure
        # that we can create a new random board when the user wants to replay the game. Since for the goat mode we use
        # all 44 cards, we can use always the same list and just have randomize the list that holds the positions for
        # the cards.
        cards_goat = [Card(image1_goat, card_positions_goat[0], 1), Card(image2_goat, card_positions_goat[1], 1),
                      Card(image3_goat, card_positions_goat[2], 2), Card(image4_goat, card_positions_goat[3], 2),
                      Card(image5_goat, card_positions_goat[4], 3), Card(image6_goat, card_positions_goat[5], 3),
                      Card(image7_goat, card_positions_goat[6], 4), Card(image8_goat, card_positions_goat[7], 4),
                      Card(image9_goat, card_positions_goat[8], 5), Card(image10_goat, card_positions_goat[9], 5),
                      Card(image11_goat, card_positions_goat[10], 6), Card(image12_goat, card_positions_goat[11], 6),
                      Card(image13_goat, card_positions_goat[12], 7), Card(image14_goat, card_positions_goat[13], 7),
                      Card(image15_goat, card_positions_goat[14], 8), Card(image16_goat, card_positions_goat[15], 8),
                      Card(image17_goat, card_positions_goat[16], 9), Card(image18_goat, card_positions_goat[17], 9),
                      Card(image19_goat, card_positions_goat[18], 10), Card(image20_goat, card_positions_goat[19], 10),
                      Card(image21_goat, card_positions_goat[20], 11), Card(image22_goat, card_positions_goat[21], 11),
                      Card(image23_goat, card_positions_goat[22], 12), Card(image24_goat, card_positions_goat[23], 12),
                      Card(image25_goat, card_positions_goat[24], 13), Card(image26_goat, card_positions_goat[25], 13),
                      Card(image27_goat, card_positions_goat[26], 14), Card(image28_goat, card_positions_goat[27], 14),
                      Card(image29_goat, card_positions_goat[28], 15), Card(image30_goat, card_positions_goat[29], 15),
                      Card(image31_goat, card_positions_goat[30], 16), Card(image32_goat, card_positions_goat[31], 16),
                      Card(image33_goat, card_positions_goat[32], 17), Card(image34_goat, card_positions_goat[33], 17),
                      Card(image35_goat, card_positions_goat[34], 18), Card(image36_goat, card_positions_goat[35], 18),
                      Card(image37_goat, card_positions_goat[36], 19), Card(image38_goat, card_positions_goat[37], 19),
                      Card(image39_goat, card_positions_goat[38], 20), Card(image40_goat, card_positions_goat[39], 20),
                      Card(image41_goat, card_positions_goat[40], 21), Card(image42_goat, card_positions_goat[41], 21),
                      Card(image43_goat, card_positions_goat[42], 22), Card(image44_goat, card_positions_goat[43], 22)
                      ]

        # For the easy and hard mode we need a different approach.
        # We shuffle the list of class objects for the cards everytime we create a new board.
        # The idea behind the following code is that we want to randomly select 6 card pairs (12 individual cards).
        # Since we loop through the list of cards, we will always select the first six tuples (consisting of two cards).
        # To make sure we have new cards for every new round, we shuffle the list and always get new tuples in the first
        # six positions in the list.
        random.shuffle(cards_easy)
        random.shuffle(cards_hard)

        # This list consists of the 12 cards that will be used for the current round of the game.
        cards_easy_mode = []
        cards_hard_mode = []

        # Here, we want to select twelve cards. Our list of all_cards consists of tuples that again consist of two cards
        # that should match. We will randomly select 6 tuples. For each iteration in the cards lists, we also iterate
        # over each tuple and append the individual class objects to our cards list.
        # Now our cards list holds 12 cards, and we have ensured that we have randomly selected 6 pairs that will match.
        counter_for_all_cards = 0

        for i in cards_easy:
            if counter_for_all_cards < 6:
                for j in i:
                    cards_easy_mode.append(j)
            counter_for_all_cards += 1

        # Now we use our class function update_position() on the twelve cards we selected and assign a unique position
        # on the screen to each card. We do this by looping through the cards list and call update_position() function.
        # We assign each card a postion from the list of positions. Since we have shuffled this list before, we always
        # get new positions.
        counter_for_all_card_positions = 0

        for j in cards_easy_mode:
            j.update_position(card_positions[counter_for_all_card_positions])
            counter_for_all_card_positions += 1

        # Here, we do the same thing for the hard mode.
        counter_for_hard_cards = 0
        for x in cards_hard:
            if counter_for_hard_cards < 4:
                for w in x:
                    cards_hard_mode.append(w)
            counter_for_hard_cards += 1

        counter_for_hard_card_positions = 0

        for c in cards_hard_mode:
            c.update_position(card_positions[counter_for_hard_card_positions])
            counter_for_hard_card_positions += 1

        # We set the new_board variable to False, so we don't create a new game board.
        new_board = False

    # Here begins the game loop. After both the variables to show the start screen and to create a new board are set to
    # False, we enter the game loop for the mode the user has selected.
    else:

        # EASY MODE
        if easy_mode:
            # event part
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # The idea for uncovering the cards is for all game modes the same.
                # All cards at the beginning have the is_face_up to False. If the user clicks on one of the covers,
                # the is_face_up variable is set to True and the picture for the card is uncovered.
                if event.type == pygame.MOUSEBUTTONDOWN:

                   # Check if a card is clicked on and flip it around.
                    mouse_pos = pygame.mouse.get_pos()

                    # If the user clicks on one of the cards and the card is not face up, we uncover the card.
                    for card in cards_easy_mode:
                        if card.rect.collidepoint(mouse_pos) and not card.is_face_up:
                            card.is_face_up = True

                            # Also, we add this card to the list that holds the selected cards.
                            selected_cards.append(card)

                            # If the list that holds the selected cards holds two cards, we want to check whether they
                            # match.
                            if len(selected_cards) == 2:

                                # Showing the second selected card.
                                screen.blit(selected_cards[1].image, selected_cards[1].rect)
                                pygame.display.flip()

                                # Adding one count to all tries.
                                all_tries += 1

                                # If the two selected cards have the same number for their matching argument, they match.
                                if selected_cards[0].matching == selected_cards[1].matching:

                                    # We add one to the counter that holds the number of matches.
                                    all_pairs += 1

                                    # Here we add a bit of delay and show a random picture for a match.
                                    pygame.time.delay(200)
                                    screen.blit(animation[random.randint(0, 1)], (250, 200))
                                    pygame.display.flip()
                                    pygame.time.delay(1000)

                                # If the cards don't match, we cover both of them up again by setting their is_face_up
                                # values to False again.
                                else:
                                    pygame.time.delay(1200)

                                    for c in selected_cards:
                                        c.is_face_up = False

                                # We delete the selected cards from our list that holds the selected cards.
                                selected_cards.clear()

                    # If the back button is pressed, we go back to the start screen.
                    if back_button.collidepoint(mouse_pos):
                        show_start_screen = True
                        easy_mode = False
                        new_board = True

            # Drawing the screen
            screen.fill(pygame.Color("lightblue"))

            # Creating the go back button.
            back_button = pygame.draw.ellipse(screen, WHITE, (5, 5, 80, 40))
            draw_text("BACK", back_button, BLACK, font3)

            # If the is_face_up value of the card is True, we show its picture. Otherwise, we show the cover image.
            for card in cards_easy_mode:
                if card.is_face_up:
                    screen.blit(card.image, card.rect)
                else:
                    screen.blit(cover_image, card.rect)

            # We are ending the game when we have six pairs.
            if all_pairs == 6:

                # We call the function to show the final screen.
                show_final_screen()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    # Here, we want to detect when the user presses on the quit or replay button.
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        mouse_pos = pygame.mouse.get_pos()

                        if end_game.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()

                        elif replay_game.collidepoint(mouse_pos):
                            reset_game()

                            # We set the is_face_up variable for all cards to False so they won't be shown when
                            # the user restarts the game.
                            for card in cards_easy_mode:
                                card.is_face_up = False

                            pygame.time.delay(1000)
                            pygame.display.update()

            pygame.display.flip()

        # HARD MODE
        # Here, we have only added comments for the parts that are different from the easy mode. The rest follows the
        # same logic.
        elif hard_mode:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_pos = pygame.mouse.get_pos()

                    for card in cards_hard_mode:
                        if card.rect.collidepoint(mouse_pos) and not card.is_face_up:
                            card.is_face_up = True
                            selected_cards.append(card)

                            # Since in this game mode we want to match three cards with each other, we check if the
                            # length of the list with selected cards is 3.
                            if len(selected_cards) == 3:
                                # showing the second and third selected card
                                screen.blit(selected_cards[1].image, selected_cards[1].rect)
                                screen.blit(selected_cards[2].image, selected_cards[2].rect)
                                pygame.display.flip()

                                all_tries += 1

                                if selected_cards[0].matching == selected_cards[1].matching == \
                                        selected_cards[2].matching:

                                    all_pairs += 1

                                    pygame.time.delay(200)
                                    screen.blit(animation[random.randint(0, 1)], (250, 200))
                                    pygame.display.flip()
                                    pygame.time.delay(1000)

                                else:
                                    pygame.time.delay(600)

                                    for c in selected_cards:
                                        c.is_face_up = False

                                selected_cards.clear()

                    if back_button.collidepoint(mouse_pos):
                        show_start_screen = True
                        hard_mode = False
                        new_board = True

            screen.fill(pygame.Color("lightblue"))

            back_button = pygame.draw.ellipse(screen, WHITE, (5, 5, 80, 40))
            draw_text("BACK", back_button, BLACK, font3)

            for card in cards_hard_mode:
                if card.is_face_up:
                    screen.blit(card.image, card.rect)
                else:
                    screen.blit(cover_image, card.rect)

            # Since there are twelve cards and we match three cards with each other, we are ending the game when there
            # are four pairs.
            if all_pairs == 4:

                show_final_screen()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        mouse_pos = pygame.mouse.get_pos()

                        if end_game.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()

                        elif replay_game.collidepoint(mouse_pos):
                            reset_game()

                            for card in cards_hard_mode:
                                card.is_face_up = False

                            pygame.time.delay(1000)
                            pygame.display.update()

            pygame.display.flip()

        # GOAT MODE
        # Here, we have only added comments for the parts that are different from the easy mode. The rest follows the
        # same logic.
        elif goat_mode:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_pos = pygame.mouse.get_pos()

                    for card in cards_goat:
                        if card.rect.collidepoint(mouse_pos) and not card.is_face_up:
                            card.is_face_up = True
                            selected_cards.append(card)

                            if len(selected_cards) == 2:

                                screen.blit(selected_cards[1].image, selected_cards[1].rect)
                                pygame.display.flip()


                                all_tries += 1

                                if selected_cards[0].matching == selected_cards[1].matching:
                                    all_pairs += 1

                                    pygame.time.delay(200)
                                    screen.blit(animation[random.randint(0, 1)], (250, 200))
                                    pygame.display.flip()
                                    pygame.time.delay(1000)

                                else:
                                    pygame.time.delay(1200)

                                    for c in selected_cards:
                                        c.is_face_up = False

                                selected_cards.clear()

                    if back_button.collidepoint(mouse_pos):
                        show_start_screen = True
                        goat_mode = False
                        new_board = True

            screen.fill(pygame.Color("lightblue"))

            back_button = pygame.draw.ellipse(screen, WHITE, (5, 5, 80, 40))
            draw_text("BACK", back_button, BLACK, font3)

            for card in cards_goat:
                if card.is_face_up:
                    screen.blit(card.image, card.rect)
                else:
                    screen.blit(cover_image2, card.rect)

            # Since in this game mode we show all 44 cards, we are ending the game when we have 22 pairs.
            if all_pairs == 22:

                show_final_screen()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        mouse_pos = pygame.mouse.get_pos()

                        if end_game.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()

                        elif replay_game.collidepoint(mouse_pos):
                            reset_game()

                            for card in cards_goat:
                                card.is_face_up = False

                            pygame.time.delay(1000)
                            pygame.display.update()

            pygame.display.flip()
