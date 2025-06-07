from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import os 
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, "data.json")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = [
    "!", "#", "$", "%", "&", "(", ")", "*", "+", "-", ".", "/", ":",
    ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "{", "|", "}", "~"
]

def generate_password():
    password_entry.delete(0, END)  # Clear the entry field before generating a new password
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():

        website = website_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        new_data = {
            website: {
                "email": email,
                "password": password
            }
        }

        if website == "" or email == "" or password == "":
            messagebox.showerror(
                title="Error", message="Please fill in all fields."
            )
        else:
            try:
                with open(data_file_path, "r") as data_file:
                    # Load existing data
                    data = json.load(data_file)
            except FileNotFoundError:
                # If the file does not exist, create a new one
                with open(data_file_path, "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open(data_file_path, "w") as data_file:
                    # Save updated data
                    json.dump(data, data_file, indent=4)
            finally:
                # Clear the input fields after saving
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- SEARCH BUTTON ------------------------------- #
def search_password():
    website = website_entry.get()
    if not website:
        messagebox.showerror(title="Error", message="Please enter a website to search.")
        return

    try:
        with open(data_file_path, "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found.")
        return

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(
            title=website,
            message=f"Email: {email}\nPassword: {password}"
        )
        pyperclip.copy(password)
    else:
        messagebox.showerror(title="Error", message=f"No details for the website '{website}' exists.")
    
# ---------------------------- UI SETUP ------------------------------- #


logo_path = os.path.join(os.path.dirname(__file__), "logo.png")

window = Tk()
window.title("Niki Password Manager")
window.config(padx=50, pady=50, bg="White")
canvas = Canvas(width=200, height=200, bg="White", highlightthickness=0)
logo_img = PhotoImage(file=logo_path)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)


website_label = Label(text="Website:", bg="White")
website_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
website_entry = Entry(width=32, highlightthickness=1, highlightbackground="black")
website_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
website_entry.focus()

email_label = Label(text="Email/Username:", bg="White")
email_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
email_entry = Entry(width=39, highlightthickness=1, highlightbackground="black")
email_entry.insert(0, "niklas.lengert@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

password_label = Label(text="Password:", bg="White")
password_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
password_entry = Entry(width=32, highlightthickness=1, highlightbackground="black")
password_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

generate_button = Button(text="Generate Password", width=14, command=generate_password)
generate_button.config(highlightthickness=1, highlightbackground="black")
generate_button.config(bg="LightGray", fg="Black")
generate_button.grid(row=3, column=2, sticky="ew", padx=5, pady=5)

add_button = Button(text="Add", width=33, command=save_password)
add_button.config(highlightthickness=1, highlightbackground="black")
add_button.config(bg="LightGray", fg="Black")
add_button.grid(row=4, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

search_button = Button(text="Search", width=14, command=search_password)
search_button.config(highlightthickness=1, highlightbackground="black")
search_button.config(bg="LightGray", fg="Black")
search_button.grid(row=1, column=2, sticky="ew", padx=5, pady=5)




window.mainloop()

