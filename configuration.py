import tkinter as tk
from PIL import Image, ImageTk
import json
import os
import time

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
background_image = background_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
background_image = ImageTk.PhotoImage(background_image)
boundary_image = Image.open("images\\boundary.png")
boundary_image = boundary_image.resize((int(screen_height*1.77), screen_height), Image.Resampling.LANCZOS)
boundary_image = ImageTk.PhotoImage(boundary_image)

# Create a canvas for the background image
canvas = tk.Canvas(root, width=1920, height=1080, highlightthickness=0)
canvas.pack()

# Set the background image on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

settings_dict = {}

def clear_canvas():
    canvas.delete('current')
    for entry_widget in canvas.place_slaves():
        entry_widget.destroy()

def apply_settings():
    new_settings = {}
    for setting in settings_dict:
        if type(settings_dict[setting]) != list:
            new_settings[setting] = settings_dict[setting].get()
            for property in settings:
                if setting == property[property_name] and property[data_type] == 'Integer':
                    if new_settings[setting] == None or new_settings[setting] == '':
                        new_settings[setting] = property[default]
                    try:
                        new_settings[setting] = int(new_settings[setting])
                    except Exception:
                        new_settings[setting] = property[default]
        else:
            new_settings[setting] = [settings_dict[setting][0].get(), settings_dict[setting][1].get()]
            for property in settings:
                if setting == property[property_name]:
                    if new_settings[setting][0] == None or new_settings[setting][0] == '' or new_settings[setting][1] == None or new_settings[setting][1] == '':
                        new_settings[setting][0] = property[default][0]
                        new_settings[setting][1] = property[default][1]
                    try:
                        new_settings[setting][0] = int(settings_dict[setting][0])
                        new_settings[setting][1] = int(settings_dict[setting][1])
                    except Exception:
                        new_settings[setting][0] = property[default][0]
                        new_settings[setting][1] = property[default][1]

def generate_settings():
    global settings_dict
    canvas.create_text(40 + screen_height//16, screen_height//18, anchor=tk.W, text='CONFIGURATION', font=('Dubai', screen_height//14, 'bold'), fill='white', tags='current')
    pad_min = screen_height//100
    pad_max = pad_min*4
    x,y = 40,screen_height//8
    font_size = screen_height//50
    entry_width = screen_width//10       
    for setting in settings:
        if y+font_size*3+pad_min*3+5 > screen_height:
            x = x + screen_width//3
            y = screen_height//8
        canvas.create_text(x-20, y, text= setting[name].title()+":", font=('Dubai', font_size, 'bold'), fill='Black', anchor=tk.W, tags='current')
        y = y+font_size + pad_min
        canvas.create_text(x, y, text= setting[description], font=('Dubai', font_size - 5), fill='Grey20', anchor=tk.W, tags='current')
        y = y+font_size + pad_min + 5
        canvas.create_text(x, y, text= f'Default value: {setting[default]} ; ({setting[data_type].upper()})', font=('Dubai', font_size - 5, 'bold'), fill='Grey20', anchor=tk.W, tags='current')
        y = y+font_size + pad_min
        if setting[number_of_entries] == 1:
            entry = tk.Entry(canvas, font= ('Dubai', font_size - 5, 'bold'), justify='right')
            entry.place(x=x, y=y, width=entry_width, height=font_size+pad_min, anchor=tk.W)
            settings_dict[setting[property_name]] = entry
            canvas.create_text(x + entry_width + 5, y, text= setting[units], font=('Dubai', font_size - 5, 'bold'), fill='Grey20', anchor=tk.W, tags='current')
            y = y+font_size + pad_max
        elif setting[number_of_entries] == 2:
            canvas.create_text(x, y, text= 'X:', font=('Dubai', font_size - 5, 'bold'), fill='Black', anchor=tk.W, tags='current')
            entry0 = tk.Entry(canvas, font= ('Dubai', font_size - 5, 'bold'), justify='right')
            entry0.place(x=x + font_size, y=y, width=entry_width//2, height=font_size+10, anchor=tk.W)
            canvas.create_text(x + font_size + entry_width//2 + 5, y, text= setting[units], font=('Dubai', font_size - 5, 'bold'), fill='Grey20', anchor=tk.W, tags='current')
            x_new = x + font_size + entry_width//2 + 40
            canvas.create_text(x_new, y, text= 'Y:', font=('Dubai', font_size - 5, 'bold'), fill='Black', anchor=tk.W, tags='current')
            entry1 = tk.Entry(canvas, font= ('Dubai', font_size - 5, 'bold'), justify='right')
            entry1.place(x=x_new + font_size, y=y, width=entry_width//2, height=font_size+10, anchor=tk.W)
            settings_dict[setting[property_name]] = [entry0, entry1]
            canvas.create_text(x_new + font_size + entry_width//2 + 5, y, text= setting[units], font=('Dubai', font_size - 5, 'bold'), fill='Grey20', anchor=tk.W, tags='current')
            y = y+font_size + pad_max
    canvas.create_image(x + screen_width//4, 0, anchor=tk.NW, image=boundary_image, tags='current')

# Switch button
switch_button_img = Image.open("images\\switch.png")
switch_button_img = switch_button_img.resize((screen_height//16, screen_height//16), Image.Resampling.LANCZOS)
switch_button_img = ImageTk.PhotoImage(switch_button_img)
switch_button = tk.Button(root, image=switch_button_img, bg="#f0f0f0", bd=0, command=clear_canvas)
switch_button.image = switch_button_img
switch_button.place(x=20, y=screen_height//19, anchor=tk.W)


generate_settings()

root.mainloop()