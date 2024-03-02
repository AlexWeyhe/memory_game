import pygame, random
import sys
from images import *


pygame.init()

# Set up the game window
width, height = 1000, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("IPA Memory Game")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# font
font = pygame.font.SysFont("Times New Roman", 35)
font2 = pygame.font.SysFont("Times New Roman", 45)


# Create a Card class
class Card:
    def __init__(self, image, position, matching):
        self.image = image
        self.position = position
        self.rect = self.image.get_rect(topleft=position)
        self.is_face_up = False
        self.matching = matching

    def update_position(self, new_position):
        self.position = new_position


selected_cards = []

# loading start screen
button_size = pygame.Rect(410, 500, 120, 90)
button_text = "PLAY"
show_start_screen = True

# randomizing the board
new_board = True

# ending the game
# counter for all pairs
all_pairs = 0
# counter for how many tries
all_tries = 0
# final screen
final_rect = pygame.Rect(300, 100, 400, 450)
# end_button
end_button = pygame.Rect(200, 400, 150, 90)
# replay button
replay_button = pygame.Rect(600, 400, 150, 90)


# This function was created with ChatGPT
def draw_text(text, figure, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (figure.x + figure.width // 2, figure.y + figure.height // 2)
    screen.blit(text_surface, text_rect)


def reset_game():
    global new_board
    new_board = True


while True:

    # showing start screen
    if show_start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    show_start_screen = False

        screen.fill(pygame.Color("lightblue"))
        screen.blit(font2.render("IPA MEMORY GAME", True, WHITE), (250, 100))
        screen.blit(font2.render("by", True, WHITE), (450, 150))
        screen.blit(font2.render("Sotirios & Alex", True, WHITE), (325, 200))

        start_button = pygame.draw.ellipse(screen, WHITE, button_size)
        draw_text(button_text, start_button, BLACK)

        pygame.display.flip()

    # randomize the board
    elif new_board:
        # Card positions
        card_positions = [
            (50, 50), (300, 50), (550, 50), (800, 50),
            (50, 300), (300, 300), (550, 300), (800, 300),
            (50, 550), (300, 550), (550, 550), (800, 550)
        ]

        #random.shuffle(card_positions)

        cards = [Card(image1, card_positions[0], 1), Card(image2, card_positions[1], 1),
                 Card(image3, card_positions[2], 2), Card(image4, card_positions[3], 2),
                 Card(image5, card_positions[4], 3), Card(image6, card_positions[5], 3),
                 Card(image7, card_positions[6], 4), Card(image8, card_positions[7], 4),
                 Card(image6, card_positions[8], 5), Card(image6, card_positions[9], 5),
                 Card(image6, card_positions[10], 6), Card(image6, card_positions[11], 6)]
        new_board = False

    # here begins the game loop
    else:
        # event part
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a card is clicked and flip it
                mouse_pos = pygame.mouse.get_pos()
                for card in cards:
                    if card.rect.collidepoint(mouse_pos) and not card.is_face_up:
                        card.is_face_up = True
                        selected_cards.append(card)

                        if len(selected_cards) == 2:
                            # showing the second selected card
                            screen.blit(selected_cards[1].image, selected_cards[1].rect)
                            pygame.display.flip()

                            # adding one count to all tries
                            all_tries += 1

                            if selected_cards[0].matching == selected_cards[1].matching:
                                all_pairs += 1

                                pygame.time.delay(200)
                                screen.blit(animation[random.randint(0, 1)], (250, 200))
                                pygame.display.flip()
                                pygame.time.delay(1000)

                            else:
                                #pygame.time.delay(200)
                                #screen.blit(image_lose1, (250, 200))
                                #pygame.display.flip()
                                pygame.time.delay(1000)

                                for c in selected_cards:
                                    c.is_face_up = False

                            selected_cards.clear()

        # Drawing the screen
        screen.fill(pygame.Color("lightblue"))
        for card in cards:
            if card.is_face_up:
                screen.blit(card.image, card.rect)
            else:
                screen.blit(cover_image, card.rect)

        # ending the game
        if all_pairs == 6:
            screen.fill(pygame.Color("lightblue"))
            screen.blit(font2.render("Congratulations!", True, WHITE), (300, 100))
            screen.blit(font2.render(f"Tries: {all_tries}.", True, WHITE), (300, 200))
            end_game = pygame.draw.ellipse(screen, BLACK, end_button)
            draw_text("QUIT", end_button, WHITE)
            replay_game = pygame.draw.ellipse(screen, BLACK, replay_button)
            draw_text("REPLAY", replay_button, WHITE)

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
                        new_board = True
                        all_pairs = 0
                        all_tries = 0
                        for card in cards:
                            card.is_face_up = False
                        pygame.time.delay(1000)

        pygame.display.flip()
