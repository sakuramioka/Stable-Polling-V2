import tkinter as tk
from PIL import Image, ImageTk
import mysql.connector
import json
import os

# Read from config
data = open('config.json','r+')
configuration_file = json.load(data)
settings = configuration_file['settings']
themes = configuration_file['themes']

# Choose a theme
selected_theme = 'Light' 

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
background_image = Image.open(themes[selected_theme]['background_image'])
background_image = background_image.resize((1920, 1080), Image.Resampling.LANCZOS)
background_image = ImageTk.PhotoImage(background_image)

# Create a canvas for the background image
canvas = tk.Canvas(root, width=1920, height=1080, highlightthickness=0)
canvas.pack()

# Set the background image on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Format displaying images
garbage = []
def format_images(start, stop, post, y):
    global garbage
    list_width = (settings['image_width'] + settings['min_spacing'])*((stop - start)-1)
    x = (screen_width - list_width)//2
    for index in range(start, stop):
        if os.path.isfile(election_dictionary[post][index][4]):
            image = Image.open(election_dictionary[post][index][4])   
        else:
            image = Image.open("images\\placeholder.png")
        image = image.resize((settings['image_width'], settings['image_height']), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(image)
        garbage.append(image)
        canvas.create_image(x, y, image=image, anchor = tk.CENTER)
        canvas.create_text(x, (y + settings['image_height']//2+ 20), text=election_dictionary[post][index][1].upper(), font=(settings['font'], settings['name_size_px'], 'bold'), fill=themes[selected_theme]['text_color_1'], anchor=tk.CENTER, justify='center', tags='existing')
        canvas.create_text(x, (y + settings['image_height']//2+ 40), text=f"{election_dictionary[post][index][2]}-{election_dictionary[post][index][3]}", font=(settings['font'], settings['class_size_px'], 'bold'), fill=themes[selected_theme]['text_color_2'], anchor=tk.CENTER, justify='center', tags='existing')
        vote_button_image = Image.open(themes[selected_theme]['vote_button'])
        vote_button_image = vote_button_image.resize((100, 35), Image.Resampling.LANCZOS)
        vote_button_image = ImageTk.PhotoImage(vote_button_image)
        vote_button = tk.Button(canvas, image=vote_button_image,bg="#f0f0f0", bd=2, highlightthickness= 0, command=lambda post=post, candidate_id=election_dictionary[post][index][0],: vote(post, candidate_id))
        garbage.append(vote_button)
        vote_button.image = vote_button_image
        vote_button.place(x=x, y=y + settings['image_height']//2+ 80, anchor='center')
        
        x = (x + settings['image_width'] + settings['min_spacing'])

# Display candidate images
def generate_list(post):
    global garbage
    for element in garbage:
        try:
            element.destroy()
        except Exception:
            pass
    garbage.clear()
    canvas.delete('existing')
    number_of_candidates = len(election_dictionary[post])
    if number_of_candidates <= settings['per_row']:
        canvas.create_text(screen_width//2, screen_height//2 - settings['image_height'], text=post, font=(settings['font'], settings['header_size_px']), fill=themes[selected_theme]['text_color_1'], anchor=tk.CENTER, justify='center', tags='existing')
        canvas.create_text(screen_width//2, (screen_height//2 - settings['image_height']) + settings['header_size_px']+15, text=f"{all_posts.index(post)+1}/{len(all_posts)}", font=(settings['font'], settings['header_size_px']-10, 'bold'), fill=themes[selected_theme]['text_color_2'], anchor=tk.CENTER, justify='center', tags='existing')
        format_images(0, number_of_candidates, post, screen_height//2)
    else:
        canvas.create_text(screen_width//2, screen_height//2 - settings['image_height']//2 - 150, text=post, font=(settings['font'], settings['header_size_px']), fill=themes[selected_theme]['text_color_1'], anchor=tk.CENTER, justify='center', tags='existing')
        canvas.create_text(screen_width//2, screen_height//2 - settings['image_height']//2 - 120, text=f"{all_posts.index(post)+1}/{len(all_posts)}", font=(settings['font'], settings['header_size_px']-10, 'bold'), fill=themes[selected_theme]['text_color_2'], anchor=tk.CENTER, justify='center', tags='existing')
        format_images(0, settings['per_row'], post, screen_height//2 - 100)
        format_images(settings['per_row'], number_of_candidates, post, screen_height//2 + settings['row_spacing_px'])

def vote(post, candidate_id):
    cursor = db.cursor()
    cursor.execute(f"UPDATE {post} SET votes = votes + 1 WHERE id = {candidate_id}")
    db.commit()
    candidate_name = election_dictionary[post][candidate_id-1][1]
    post_index = all_posts.index(post)
    # Display pop-up ↓
    top = tk.Toplevel(root)
    top.geometry(f"{settings['voted_popup_size'][0]}x{settings['voted_popup_size'][1]}")
    top.title("Vote has been casted!")
    top.geometry(f"{settings['voted_popup_size'][0]}x{settings['voted_popup_size'][1]}+{screen_width//2 - settings['voted_popup_size'][0]//2}+{screen_height//2 - settings['voted_popup_size'][1]//2}")
    top.configure(background= themes[selected_theme]['background_color'])
    if post_index+1 < len(all_posts):
        tk.Message(top, text=f"You have voted for {candidate_name}!", padx=10, pady=100, justify="center" ,font=(settings['font'], settings['header_size_px'] ,"bold"), bg = themes[selected_theme]['background_color'], fg= themes[selected_theme]['text_color_2']).pack()
        top.after(settings['display_time']*1000, top.destroy)
        root.after(settings['display_time']*1000, lambda: generate_list(all_posts[post_index+1]))     
    else:
        tk.Message(top, text=f"You have voted for {candidate_name}!\n\nThank you for voting!", padx=10, pady=100, justify="center" ,font=(settings['font'], settings['header_size_px'] ,"bold"), bg = themes[selected_theme]['background_color'], fg= themes[selected_theme]['text_color_2']).pack()
        top.after((settings['display_time']+2)*1000, top.destroy)
        root.after((settings['display_time']+2)*1000, lambda: generate_list(all_posts[0]))


generate_list(all_posts[0])

root.mainloop()