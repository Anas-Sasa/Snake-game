"""
score.py

Defines a Turtle-based Score display for a simple game.

Classes:
    Score -- Subclasses turtle.Turtle to show and update the current game score,
             display a game-over screen with decorative icons, and clear the score.

Usage:
    from score import Score
    score = Score()
    score.score += 1
    score.score_update()
    score.game_over(screen)
"""

# Import Turtle to draw text on the screen and time to pause briefly on game over
from turtle import Turtle
import time, os 


class Score(Turtle):

    """
    A text-based score display using turtle graphics.

    Attributes
    ----------
    score : int
        Current game score shown on screen.

    Methods
    -------
    score_update()
        Clears previous text and writes the current score centered at the top.
    game_over(window)
        Displays a game-over message, writes decorative symbols, updates the window,
        and pauses briefly.
    hide_score()
        Clears the displayed score text.
    """

    def __init__(self):

        # Initialize the parent Turtle
        super().__init__()

        # Path of last-score file location
        self.score_path = os.path.join(os.getcwd(), "last-score.txt")

         # ensure file exists
        if not os.path.exists(self.score_path):
            with open(self.score_path, "w") as f:
                f.write("0")

        self.penup()
        self.hideturtle()
        self.color("violet")
        self.goto(x= 0, y= 350)

        # Initialize numeric score counter
        self.score = 0
        

    # Save last user score
    def save_score(self):

        """
        Save the last socre of game in a file to display it later as hight reach score
        """

        # Open the current path file 
        with open(f"{self.score_path}", "w+") as file:
            
            file.seek(0)

            # Write score in the current location fiel
            file.write(f"{self.score}")


    # Reading the content in the last score file
    def read_file_score(self):
        """
        Read the content of the last score file and returns int(score) """

        # Open last score file and read the content
        with open(f"{self.score_path}", "r") as file:
            
            # reaturn the cursor at the begin
            file.seek(0)

            # read and reaturn the last score of game
            return int(file.read())


    def score_update(self):
        """
        Refresh the score display.

        Clears any previously written text and writes "Game score: {score} -- Last score: {self.read_file_score()}"
        centered at the turtle's current position using a readable font.
        """
        
        self.clear()

        # Write the updated current score  and last score at the current location
        self.write(f"Current score: {self.score} / Last highest score: {self.read_file_score()}", align= "center", font=("Arial", 20, "normal"))


    # Display the game-over screen
    def game_over(self, window):
        """
        Show the game-over screen.

        Moves the writer to the center, changes background and text color for emphasis,
        writes a message with the last score, displays decorative icons at corners,
        updates the window and pauses for a short time so the player can see the result.

        Parameters
        ----------
        window : turtle.Screen
            The game screen to update background color and refresh.
        """

        # Check if the currently score bigger than the score in the last score file
        if self.score > self.read_file_score():

            # Write this last highest score in the file
            self.save_score()


        self.goto(x= 0, y= 0)

        # Set a dramatic background color for game over
        window.bgcolor("crimson")

        # Change text color to contrast with the new background
        self.color("peach puff")

        # Write the main game-over message including the last score
        self.write(f"Game over!🥲 😔 💔\n\nLast highest score: {self.read_file_score()} ", align= "center", font=("Arial", 20, "italic"))

        # Coordinates for decorative icons near the four corners
        angels = ((-470,330), (-470, -330), (430, 330), (430, -330))

        # Write a decorative symbol at each coordinate
        for i in angels:
            
            self.goto(i)
            self.write("🐉", font=("Arial", 40, "normal"))

        # Ensure the screen shows the changes immediately
        window.update()

        # Pause briefly so the player can see the game-over screen
    

    # Hide the score of screen
    def hide_score(self):
        """
        Clear the score text from the screen.
        """
        self.clear()