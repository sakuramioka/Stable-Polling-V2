import tkinter as tk
from PIL import Image, ImageTk
import mysql.connector
import json
import os

settings = {
    'image_width' : 180, # Width of candidate image
    'image_height' : 180, # Height of candidate image
    'min_spacing' : 100, # Distance between two candidate images (in pixels)
    'per_row' : 5 # Number of candidates displayed per row
}

themes = {
    'Light' : {
        'background_image': "images//background_light.jpg",
        'text_color_1': "Black",
        'text_color_2': "Grey20"
    }
}
 

# Read from config
data = open('config.json','r+')
configuration_file = json.load(data)

db = mysql.connector.connect(
    host=configuration_file['host'],
    user=configuration_file['user'],
    password=configuration_file['password'],
    database=configuration_file['database']
)


#Load data to memory
election_dictionary = {}
all_posts = configuration_file['posts']
cursor = db.cursor(buffered=True)
for post_index in range(0, len(all_posts)):
    cursor.execute(f"SELECT id, name, class, section, image_path, votes FROM {all_posts[post_index]}")
    post_candidates = cursor.fetchall()
    election_dictionary[all_posts[post_index]] = post_candidates

# SAMPLE ELECTION DICTIONARY ELEMENT: (id, name, class, section, image_path, votes)

# Create the main window
root = tk.Tk()
root.title("Election Application")
root.attributes('-fullscreen', True)

# Important variables
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

# Load and resize the background image to fit the window
background_image = Image.open("images//background_light.jpg")  # Replace with your image path
background_image = background_image.resize((1920, 1080), Image.Resampling.LANCZOS)
background_image = ImageTk.PhotoImage(background_image)

# Create a canvas for the background image
canvas = tk.Canvas(root, width=1920, height=1080, highlightthickness=0)
canvas.pack()

# Set the background image on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

def format_images(start, stop, post, y):
    list_width = (settings['image_width'] + settings['min_spacing'])*((stop - start)-1)
    x = (screen_width - list_width)//2
    for index in range(start, stop):
        if os.path.isfile(election_dictionary[post][index][4]):
            image = Image.open(election_dictionary[post][index][4])   
        else:
            image = Image.open("images\\placeholder.png")
        image = image.resize((settings['image_width'], settings['image_height']), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(image)
        images.append(image)
        canvas.create_image(x, y, image=image, anchor = tk.CENTER)
        canvas.create_text(x, (y + settings['image_height']//2+ 20), text=election_dictionary[post][index][1].upper(), font=('Dubai', '12', 'bold'), fill='Black', anchor=tk.CENTER)
        canvas.create_text(x, (y + settings['image_height']//2+ 40), text=f"{election_dictionary[post][index][2]}-{election_dictionary[post][index][3]}", font=('Dubai', '12', 'bold'), fill='Black', anchor=tk.CENTER)
        x = (x + settings['image_width'] + settings['min_spacing'])

# Display candidate images
images = []
def generate_list(post):
    global images
    images.clear()
    number_of_candidates = len(election_dictionary[post])
    if number_of_candidates <= settings['per_row']:
        format_images(0, number_of_candidates, post, screen_height//2)
    else:
        format_images(0, settings['per_row']-1, post, screen_height//2 - 100)
        format_images(settings['per_row']-1, number_of_candidates, post, screen_height//2 + 400)


    


generate_list('Example_post_1')

root.mainloop()
