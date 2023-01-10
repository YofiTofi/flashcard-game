from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Ariel", 40, "italic")
BODY_FONT = ("Ariel", 60, "bold")


# ----------------------------------  Word Management ---------------------------------- #


def next_combo():
    global random_combination
    global word
    global title
    if not words_dict:
        card_canvas.delete(title)
        card_canvas.delete(word)
        title = card_canvas.create_text(400, 150, text="End", fill="white", font=TITLE_FONT)
        word = card_canvas.create_text(400, 263, text="No more cards", fill="black", font=BODY_FONT)
        return
    random_combination = random.choice(words_dict)
    french_word = random_combination["French"]
    card_canvas.create_image(400, 263, image=card_front)
    if "title" in globals():
        card_canvas.delete(title)
    title = card_canvas.create_text(400, 150, text="French", fill="black", font=TITLE_FONT)
    if "word" in globals():
        card_canvas.delete(word)
    word = card_canvas.create_text(400, 263, text=french_word, fill="black", font=BODY_FONT)
    window.after(3000, show_english)


def show_english():
    global random_combination
    global title
    global word
    english_word = words_dict[words_dict.index(random_combination)]["English"]
    card_canvas.create_image(400, 263, image=card_back)
    card_canvas.delete(title)
    title = card_canvas.create_text(400, 150, text="English", fill="white", font=TITLE_FONT)
    card_canvas.delete(word)
    word = card_canvas.create_text(400, 263, text=english_word, fill="white", font=BODY_FONT)


def known_word():
    global words_dict
    del words_dict[words_dict.index(random_combination)]
    next_combo()


def unknown_word():
    global unknown_words
    current_combo = {"French": words_dict[words_dict.index(random_combination)]["French"],
                     "English": words_dict[words_dict.index(random_combination)]["English"]
                     }
    unknown_words.append(current_combo)
    del words_dict[words_dict.index(random_combination)]
    next_combo()


# ----------------------------------  GUI Design ---------------------------------- #


window = Tk()
window.title("Flashcard Game")
window.config(pady=50, padx=20, bg=BACKGROUND_COLOR)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_canvas = Canvas(width=800, height=526, highlightthickness=0)
card_canvas.create_image(400, 263, image=card_front)
card_canvas.config(bg=BACKGROUND_COLOR)
card_canvas.grid(row=0, column=0, columnspan=3)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, bg=BACKGROUND_COLOR, borderwidth=0, command=known_word)
right_button.grid(row=1, column=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0, command=unknown_word)
wrong_button.grid(row=1, column=0)


# ----------------------------------  Game Manager ---------------------------------- #

unknown_words = []
try:
    words_frame = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    words_frame = pandas.read_csv("data/french_words.csv")
words_dict = words_frame.to_dict("records")
next_combo()

window.mainloop()

if unknown_words:
    unknown_df = pandas.DataFrame.from_dict(list(unknown_words))
    unknown_df.to_csv("words_to_learn.csv", index=False)
