import tkinter as tk

# window = tk.Tk()
# window.title("My first GUI program")
# window.minsize(width=500, height=300)
# window.config(padx=20, pady=20)

 
# my_label = tk.Label(text="I am a Label", font=("Arial", 24, "bold"))
# my_label.grid(column=0, row=0)

# my_label.config(text="New Text", font=("Arial", 12, "normal"))

# def button_clicked():
#     print("I got clicked")
#     input_text = input.get()
#     print(input_text)
#     my_label.config(text=input_text)

# my_button = tk.Button(text="Click Me", command=button_clicked)
# my_button.grid(column=1, row=1)
# my_button.config(padx=20, pady=20)

# new_button = tk.Button(text="New Button")
# new_button.grid(column=2, row=0)

# input = tk.Entry(width=10)
# input.grid(column=3, row=2)


# window.mainloop()

window = tk.Tk()
window.title("Mile to Km Converter")
window.minsize(width=300, height=200)
window.config(padx=20, pady=20)

def convert():
    miles = float(miles_input.get())
    km = miles * 1.60934
    result_label.config(text=f"{km:.2f} Km")

miles_input = tk.Entry(width=10)
miles_input.grid(column=1, row=0)
miles_label = tk.Label(text="Miles")
miles_label.grid(column=2, row=0)

convert_button = tk.Button(text="Convert", command=convert)
convert_button.grid(column=1, row=1)

result_label = tk.Label(text="0 Km")
result_label.grid(column=1, row=2)

window.mainloop()
