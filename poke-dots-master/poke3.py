# Poke the Dots V3
# This is a graphical game where two dots move around the screen, bouncing
# off the edges. The user tries to prevent the dots from colliding by
# pressing and releasing the mouse button to teleport the dots to a random
# location. The score is the number of seconds from the start of the game.

from uagame import Window
from random import randint
from time import sleep
from pygame import QUIT, MOUSEBUTTONUP, Color
from pygame.time import get_ticks
from pygame.event import get as get_events
from pygame.draw import circle as draw_circle

# User-defined functions


def main():
    window = create_window()
    game = create_game(window)
    play_game(game)
    window.close()


def create_window():
    # Create a Window for the game, open it, and return it.

    window = Window("Poke the Dots", 500, 400)
    window.set_font_name('ariel')
    window.set_font_size(64)
    window.set_font_color('white')
    window.set_bg_color("black")
    return window


def create_game(window):
    # Create a Game object for Poke the Dots.
    # - window is the Window that the game is played in

    game = Game()
    game.window = window
    game.frame_rate = 90  # larger is faster game
    game.close_selected = False
    game.small_dot = create_dot("red", [50, 100], 30, [1, 2])
    game.big_dot = create_dot("blue", [200, 100], 40, [2, 1])
    randomize_dot(game.window, game.small_dot)
    randomize_dot(game.window, game.big_dot)
    game.score = 0
    return game


def create_dot(color, center, radius, velocity):
    # Create a Dot object for Poke the Dots.
    # - color is the str color of the dot
    # - center is a list containing the x and y int coords of the center
    # of the dot
    # - radius is the int pixel radius of the dot
    # - velocity is the list of horizontal int and vertical int speeds of
    # the dot

    dot = Dot()
    dot.color = color
    dot.center = center
    dot.radius = radius
    dot.velocity = velocity
    return dot


def randomize_dot(window, dot):
    # Randomize the x and y int coords of the center of the dot. Ensure that
    # no part of a dot extends beyond the surface boundary.
    # - window is the Window that the game is played in
    # - dot is the Dot to randomize

    size = [window.get_width(), window.get_height()]
    for index in range(2):
        dot.center[index] = randint(dot.radius, size[index] - dot.radius)


def play_game(game):
    # Play the game until the player presses the close icon.
    # - game is the Game to play

    while not game.close_selected:
        # play frame
        handle_events(game)
        draw_game(game)
        update_game(game)


def handle_events(game):
    # Handle the current game events by changing the game state appropriately.
    # - game is the Game whose events will be handled
    event_list = get_events()
    for event in event_list:
        # handle one event
        if event.type == QUIT:
            game.close_selected = True
        elif event.type == MOUSEBUTTONUP:
            randomize_dot(game.window, game.small_dot)
            randomize_dot(game.window, game.big_dot)


def draw_game(game):
    # Draw all game objects.
    # - game is the Game to draw for

    game.window.clear()
    draw_score(game)
    draw_dot(game.window, game.small_dot)
    draw_dot(game.window, game.big_dot)
    game.window.update()


def draw_score(game):
    # Draw scoreboard until the player presses the close icon.
    # - game is the Game to draw for

    score_string = "Score: %d" % game.score
    game.window.draw_string(score_string, 0, 0)


def draw_dot(window, dot):
    # Draw the dot on the window.
    # - window is the Window that the game is played in
    # - dot is the Dot to draw

    surface = window.get_surface()
    color = Color(dot.color)
    draw_circle(surface, color, dot.center, dot.radius)


def update_game(game):
    # Update all game objects with state changes that are not due to
    # user events.
    # - game is the Game to update

    move_dot(game.window, game.small_dot)
    move_dot(game.window, game.big_dot)
    # control frame rate
    sleep(0.01)
    game.score = get_ticks() / 1000 # turn milisecods to seconds


def move_dot(window, dot):
    # Change the location and the velocity of the Dot so it remains on the
    # surface by bouncing from its edges.
    # - window is the Window that the game is played in
    # - dot is the Dot to move

    size = [window.get_width(), window.get_height()]
    for index in range(2):
        # update center at coordinate
        dot.center[index] += dot.velocity[index]
        # dot edge outside window?
        if dot.center[index] + dot.radius >= size[index] or\
           dot.center[index] - dot.radius <= 0:
            # change direction
            dot.velocity[index] = -dot.velocity[index]


class Game:
    # An object in this class represents a complete game.
    # - window
    # - frame_rate
    # - close_selected
    # - small_dot
    # - big_dot
    # - score
    pass


class Dot:
    # An object in this class represents a colored circle that can move.
    # - color
    # - center
    # - radius
    # - velocity
    pass


main()
