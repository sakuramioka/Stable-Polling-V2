import tkinter as tk
from PIL import Image, ImageTk
import json
import os

settings = [
    ['Image Width', 'image_width', 1, 'Integer', 'Width of the candidate image (in pixels)', 180, 'px'],
    ['Image Height', 'image_height', 1, 'Integer', 'Height of the candidate image (in pixels)', 180, 'px'],
    ['Spacing between images', 'min_spacing', 1, 'Integer', 'Minimum spacing between the candidate image (in pixels)', 130, 'px'],
    ['Name display size', 'name_size_px', 1, 'Integer', "Font size of the candidate's name (in pixels)", 14, 'px'],
    ['Class display size', 'name_size_px', 1, 'Integer', "Font size of the candidate's class and section (in pixels)", 12, 'px'],
    ['Universal font', 'font', 1, 'String', "Name of font that will be used throughout the application", 'Dubai', ''],
    ['Vote button size', 'vote_button_size', 2, 'Integer', "Size of the vote button (x, y) (in pixels)", [135, 40], 'px'],
    ['Header size', 'header_size_px', 1, 'Integer', "Size of the post name display above the images (in pixels)", 22, 'px'],
    ['Row spacing', 'row_spacing_px', 1, 'Integer', "Spacing between row 1 and row 2 (in pixels)", 215, 'px'],
    ['Confirmation display time', 'display_time', 1, 'Integer', "Time to display voting confirmation (in seconds)", 3, 'seconds'],
    ['Confirmation display size', 'voted_popup_size', 2, 'Integer', "Size of voting confirmation pop-up (x, y) (in pixels)", [600, 200], 'px']
]

name, property_name, number_of_entries, data_type, description, default, units = 0, 1, 2, 3, 4, 5, 6

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
    pad_min = screen_height//100
    pad_max = pad_min*4
    x,y = 40,150
    font_size = screen_height//50
    entry_width = screen_width//10       
    for setting in settings:
        canvas.create_text(x-20, y, text= setting[name].upper()+":", font=('Dubai', font_size, 'bold'), fill='Black', anchor=tk.W)
        y = y+font_size + pad_min
        canvas.create_text(x, y, text= setting[description], font=('Dubai', font_size - 5), fill='Grey20', anchor=tk.W)
        y = y+font_size + pad_min + 5
        canvas.create_text(x, y, text= f'Default value: {setting[default]} ; ({setting[data_type].upper()})', font=('Dubai', font_size - 5, 'bold'), fill='Grey20', anchor=tk.W)
        y = y+font_size + pad_min
        if setting[number_of_entries] == 1:
            entry = tk.Entry(canvas, font= ('Dubai', font_size - 5, 'bold'), justify='right')
            entry.place(x=x, y=y, width=entry_width, height=font_size+pad_min, anchor=tk.W)
            canvas.create_text(x + entry_width + 5, y, text= setting[units], font=('Dubai', font_size - 5, 'bold'), fill='Grey20', anchor=tk.W)
            y = y+font_size + pad_max
        elif setting[number_of_entries] == 2:
            canvas.create_text(x, y, text= 'X:', font=('Dubai', font_size - 5, 'bold'), fill='Black', anchor=tk.W)
            entry = tk.Entry(canvas, font= ('Dubai', font_size - 5, 'bold'), justify='right')
            entry.place(x=x + font_size, y=y, width=entry_width//2, height=font_size+10, anchor=tk.W)
            canvas.create_text(x + font_size + entry_width//2 + 5, y, text= setting[units], font=('Dubai', font_size - 5, 'bold'), fill='Grey20', anchor=tk.W)
            x_new = x + font_size + entry_width//2 + 40
            canvas.create_text(x_new, y, text= 'Y:', font=('Dubai', font_size - 5, 'bold'), fill='Black', anchor=tk.W)
            entry = tk.Entry(canvas, font= ('Dubai', font_size - 5, 'bold'), justify='right')
            entry.place(x=x_new + font_size, y=y, width=entry_width//2, height=font_size+10, anchor=tk.W)
            canvas.create_text(x_new + font_size + entry_width//2 + 5, y, text= setting[units], font=('Dubai', font_size - 5, 'bold'), fill='Grey20', anchor=tk.W)
            y = y+font_size + pad_max
        if y+font_size*3+pad_min*3+5 > screen_height:
            x = x + screen_width//3
            y = 150

generate_settings()

root.mainloop()