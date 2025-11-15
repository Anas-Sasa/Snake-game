"""
main.py

Snake (Snack) game entry point using the turtle graphics library.

This module:
- Configures and displays the game window.
- Shows a start/welcome screen with decorative icons.
- Prompts the player for snake speed and validates input.
- Creates game objects (Food, Snake, Score) and runs the main loop.
- Handles keyboard controls and restart/exit prompts.

Dependencies:
- turtle (Screen)
- food.py (Food)
- snake.py (Snake)
- scoreboard.py (Score)

Usage:
    python main.py
"""


# Standard library imports
# os: used to clear the terminal for a clean console at start
# time: used for simple sleep/delay operations
import os, time

# turtle imports for the game window
from turtle import Screen

# Local game modules
from food import Food        # Food: small collectible pellet that appears randomly
from snake import Snake      # Snake: manages segments, movement, growth, and controls
from scoreboard import Score # Scoreboard: tracks and displays the player's current and last highest score 


def clear_terminal():
    """Clear the terminal screen cross-platform for a clean console view."""
    os.system("clear" if os.name == "posix" else "cls")


def sleep(seconds):
    """Simple wrapper around time.sleep to keep naming consistent in this module."""
    time.sleep(seconds)


# Clear the console at program start
clear_terminal()

# Reusable Food instance used to write temporary messages on screen
WRITE_MESSAGE = Food(color="lavender")

# To check of the user clicks on "X" window to exit
is_on_close = False

# Drawing a welcome message
def show_start_screen(window):
    """
    Draw a welcome message and decorative corner icons, pause, then clear.

    Parameters
    ----------
    window : turtle.Screen
        The main game window to update after drawing the welcome screen.
    """

    # Corner coordinates for decorative icons
    decorative_angels = ((-470, 330), (-470, -330), (430, 330), (430, -330))

    # Use a temporary Food object as a text writer
    t = Food(color="lavender")
    t.goto(x=0, y=330)
    t.write("Welcome to snack game!🐉 🐉", align="center", font=("Arial", 20, "normal"))

    # Change color for corner decorations and write them
    t.color("violet")
    for coord in decorative_angels:
        t.goto(coord)
        t.write("🐉", font=("Arial", 40, "normal"))

    # Ensure display updates and pause so the player can read the message
    window.update()
    sleep(1)
    t.clear()

# Displays the end message 
def show_goodbye_message(window):
    """
    Changes the window color to black and write a goodbye message  
    """
    window.clear()
    window.bgcolor("black")

    WRITE_MESSAGE.write("See you later....👋", align="center", font=("Arial", 20, "italic"))


# Initializing the game
def main():
    """
    Initialize the game window, prompt for valid speed, create objects,
    and run the main game loop until the snake dies.

    Returns Bool of the stop game way of the user
    """

# Declare module-level globals so functions can read/write these variables.

    # WINDOW: the turtle Screen instance used for drawing and event handling.
    global WINDOW

    # game_on: flag that controls the main game loop; True while a round is active.
    global game_on

    game_on = True
    
    # Create and configure the window
    WINDOW = Screen()
    WINDOW.bgcolor("slate blue")
    WINDOW.title("Anas GB!")
    WINDOW.setup(width=1000, height=800)
    WINDOW.tracer(0)  # manual updates for smoother animation

    # Prompt player for a snake speed between 10 and 20 (inclusive)
    speed = WINDOW.textinput("Speed of Snake!", "Enter speed of snake from [10] to [20] <<!!! ")

    # Check if user clicks "Cancle" on the message prompt
    if speed is None:

        show_goodbye_message(window= WINDOW)

        # Sotp game
        return False
    
    else:

        # Validate input: must be a number and in the allowed range
        while not str(speed).isdigit() or int(str(speed)) > 20 or int(str(speed)) < 10:
            
            WRITE_MESSAGE.write("Enter only numbers [ from 10 to 20 ]", align="center", font=("Arial", 15, "italic"))

            WINDOW.update()
            sleep(1.5)
            WRITE_MESSAGE.clear()

            speed = WINDOW.textinput("Speed of Snake!", "Enter speed of snake from [ 10 to 20 ] <<<||")

    # Check if user clicks "Cancle" on the message prompt
            if speed is None:

                show_goodbye_message(window= WINDOW)
                # Stop game
                return False


    # Get the underlying Tkinter Toplevel window object from the turtle Screen.
    # We need this to customize the window manager close button behavior.
    tk_window = WINDOW.getcanvas().winfo_toplevel()

    # Handler for the window manager "close" (X) button.
    def on_close():
        
        # Re-declare globals we will modify inside this function.
        global game_on 
        global is_on_close
        

        # If the game is already stopped (game_on is False), then destroy the Tk window.
        # This performs the actual window tear-down and frees GUI resources.
        if not game_on and is_on_close:
            tk_window.destroy()

        else:
            show_goodbye_message(window= WINDOW)


        # Mark the game as stopped and the program as not running any active round.
        # The rest of the program should observe these flags and stop scheduling callbacks.
        game_on = False
        is_on_close = True
    
    # Register the on_close handler for the window manager close event.
    # After this, clicking the window X will call on_close() instead of auto-destroying.
    tk_window.protocol("WM_DELETE_WINDOW", on_close)


    # Show the start/welcome screen
    show_start_screen(window=WINDOW)

    # Create game objects
    food = Food(color="lime")
    snake = Snake(color="plum", length=6, speed=int(speed))
    score = Score()

    # Place the first food pellet
    food.apear_food()

    # Main game loop
    while game_on:
        # Control game tempo
        sleep(0.05)

        # Update score display
        score.score_update()

        # Move snake and refresh inside move()
        snake.move(window=WINDOW)

        # Check border collision for game over
        if (snake.head.xcor() > 485 or snake.head.xcor() < -485) or (snake.head.ycor() > 385 or snake.head.ycor() < -385):

            game_on = False

            sleep(0.3)

            snake.hide_snake()
            score.hide_score()
            food.hide_food()
            score.game_over(window=WINDOW)

        # Check for eating food: grow snake, reposition food, increment score
        elif snake.head.distance(food) < 15:

            food.apear_food()
            snake.snake_extend()
            score.score += 1

        else:
            # Check for self-collision: head touching any body segment
            for segment in snake.turtles[:-2]:

                if snake.head.distance(segment) < 10:

                    game_on = False

                    sleep(0.3)

                    snake.hide_snake()
                    score.hide_score()
                    food.hide_food()
                    score.game_over(window=WINDOW)
                    break

        # Keyboard event bindings for directional control
        WINDOW.listen()

        WINDOW.onkey(snake.down, "Down")
        WINDOW.onkey(snake.up, "Up")
        WINDOW.onkey(snake.left, "Left")
        WINDOW.onkey(snake.right, "Right")

    # Clear current snake segments before potential restart
    snake.turtles = []

    if is_on_close:

        return False
    else:
        return True

# Start the first game
if main(): # main returns a value of [ is_on_close() ]


    is_new_game = True

    # If running game still running
    # After a round ends, prompt the player to start a new game or exit
    while is_new_game:

        if not is_on_close:
           
            new_game = WINDOW.textinput("New Game! ", "Do you want to play again? Type [ Y ] to start or [ N ] to exit!")

            if str(new_game).lower() == "y":

                WINDOW.clear()

                # Check if the game stil runnig
                main()

            elif str(new_game).lower() == "n" or new_game is None:

                show_goodbye_message(window= WINDOW)

                is_new_game = False

            else:
                # Invalid entry: show message briefly and prompt again
                WINDOW.clear()
                WINDOW.bgcolor("black")

                WRITE_MESSAGE.write(f"Invalid entry: [ {new_game} ]\nEnter [ Y or N ]", align="center", font=("Arial", 15, "italic"))
                WINDOW.update()

                sleep(1.3)
                WRITE_MESSAGE.clear()

        else:
             is_new_game = False

# Keep the window open until closed by the user
WINDOW.exitonclick()

# ____________________________________________________________________________________

# DEBUG NOTES / COMPLAINTS******


# - Issue: Clicking the window X repeatedly kept calling on_close() because the
#   protocol replaced the default close behavior. I had commented out destroy(),
#   so the window stayed alive and the handler kept running.

# - Symptom: If I did call destroy() while the game loop or scheduled callbacks
#   were still active, I got errors like "window has been destroyed" when those
#   callbacks ran afterwards.

# - Root cause: GUI was torn down while other parts of the code still assumed it
#   existed. There were no reliable guards to stop timers/events before destroy.

# - Resolution: Stop the game first (game_on = False, is_running = False), unbind
#   or guard callbacks, show the exit message, and only call tk_window.destroy() 
#   once callbacks are no longer running.

# ---------------------------------------------------------------------------------

# To fix next time! [ Done !! ]

# the destroy of GUI:   [ Done !! ]

# When there is collision border or self --> while prmpt asked for new game, If user click on "X" to stop got destroy error.    [ Done !! ]

# if is there a collision border of self, the game hangon some seconds at game-over screen. If user press on "X" while this hangin-on   [ Done !! ]
# the game stops at the same window without give any hint for user that the game is stoped to make reaction.