import tkinter as tk
from PIL import Image, ImageTk
import mysql.connector
import json
import os

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

# Display candidate images
images = []
def generate_list(post):
    global images
    image_width = 200
    image_height = 200
    list_of_candidates = election_dictionary[post]
    number_of_candidates = len(election_dictionary[post])
    min_spacing = 100
    list_width = (image_width + min_spacing)*(number_of_candidates-1)
    x = screen_width//2 - list_width//2
    y = screen_height//2
    print(list_width)
    print(screen_width)
    print(min_spacing)
    print(x, y)
    for candidate in list_of_candidates:
        if os.path.isfile(candidate[4]):
            image = Image.open(candidate[4])   
        else:
            image = Image.open("images\\placeholder.png")
        image = image.resize((image_width, image_height), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(image)
        images.append(image)
        canvas.create_image(x, y, image=image, anchor = tk.CENTER)
        x = x + image_width + min_spacing

generate_list('Example_post_1')

root.mainloop()
