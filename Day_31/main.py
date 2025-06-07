import tkinter as tk
import random
import pandas as pd
import os

file_path = os.path.dirname(os.path.abspath(__file__))
current_card = {}
to_learn = {}

try:
    # Attempt to read the CSV file to load words to learn
    data = pd.read_csv(os.path.join(file_path, "data", "words_to_learn.csv"))
except FileNotFoundError:
    # If the file does not exist, read the original words file
    data = pd.read_csv(os.path.join(file_path, "data", "french_words.csv"))
    to_learn = data.to_dict(orient="records")
else:
    # If the file exists, load the words to learn
    to_learn = data.to_dict(orient="records")



BACKGROUND_COLOR = "#B1DDC6"

#----------------------------------- Functions -----------------------------------#
def next_card():
    """Show a random word from the list."""
    global current_card, flip_timer
    if 'flip_timer' in globals() and flip_timer is not None:
        window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_text, text=current_card["French"], fill="black")
    canvas.itemconfig(card_front, image=card_front_img)
    flip_timer = window.after(3000, flip_card)

def flip_card():
    """Flip the card to show the English translation."""
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=current_card["English"], fill="white")
    canvas.itemconfig(card_front, image=card_back_img)

def is_known():
    """Remove the current card from the list of words to learn."""
    to_learn.remove(current_card)
    # Save the updated list to a CSV file
    data = pd.DataFrame(to_learn)
    data.to_csv(os.path.join(file_path, "data", "words_to_learn.csv"), index=False)
    next_card()

#----------------------------------- UI Setup -----------------------------------#
window = tk.Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
# Load the image
image_path = os.path.join(file_path, "images", "card_front.png")
card_front_img = tk.PhotoImage(file=image_path)
# Create the front card image
card_front = canvas.create_image(400, 263, image=card_front_img)
# Load the back image
image_path = os.path.join(file_path, "images", "card_back.png")
card_back_img = tk.PhotoImage(file=image_path)
# Create the back card image
card_back = canvas.create_image(400, 263, image=card_back_img)
# Create the text on the card
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"), fill="black")
card_text = canvas.create_text(400, 263, text="Word", font=("Ariel", 40, "italic"), fill="black")
# Create the wrong button
wrong_image_path = os.path.join(file_path, "images", "wrong.png")
wrong_img = tk.PhotoImage(file=wrong_image_path)
wrong_button = tk.Button(image=wrong_img, highlightthickness=0, command=lambda: next_card())
wrong_button.grid(row=1, column=0)
# Create the right button
right_image_path = os.path.join(file_path, "images", "right.png")
right_img = tk.PhotoImage(file=right_image_path)
right_button = tk.Button(image=right_img, highlightthickness=0, command=lambda: is_known())
right_button.grid(row=1, column=1)

# Start the application with the first card
flip_timer = None
next_card()
window.mainloop()

