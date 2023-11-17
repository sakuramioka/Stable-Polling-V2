import tkinter as tk
from PIL import Image, ImageTk
import json
import os

settings = [
    ['Image Width', 'image_width', 1, 'Integer'],
    ['Image Height', 'image_height', 1, 'Integer']
]

name, property_name, number_of_entries, data_type = 0, 1, 2, 3

# Create the main window
root = tk.Tk()
root.title("Configuration Menu")
root.attributes('-fullscreen', True)

# Important variables
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

# Load and resize the background image to fit the window
background_image = Image.open("images\\background_light.jpg")
background_image = background_image.resize((1920, 1080), Image.Resampling.LANCZOS)
background_image = ImageTk.PhotoImage(background_image)

# Create a canvas for the background image
canvas = tk.Canvas(root, width=1920, height=1080, highlightthickness=0)
canvas.pack()

# Set the background image on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

def generate_settings():
    x,y = 20,20
    font_size = 20
    for setting in settings:
        canvas.create_text(x, y, text= setting[name]+":", font=('Dubai', font_size, 'bold'), anchor=tk.W)
        y = y+font_size*2
        print(y)
        if setting[number_of_entries] == 1:
            entry = tk.Entry(canvas, font= ('Dubai', font_size))
            entry.place(x=x, y=y, width=100, height=font_size+10, anchor=tk.W)
            y = y+font_size*4
            print(y)

generate_settings()

root.mainloop()