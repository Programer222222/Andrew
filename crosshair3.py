import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw
import random
import pyperclip
import json

# Function to update the crosshair label and image
def update_crosshair(player_name):
    if player_name in crosshair_codes:
        crosshair_code = crosshair_codes[player_name]
        crosshair_label.config(text=f"Player: {player_name}\nCrosshair: {crosshair_code}", fg="white")
        draw_crosshair(crosshair_canvas, crosshair_code)
    else:
        crosshair_label.config(text="Crosshair code not found for this player", fg="red")
        crosshair_canvas.delete("all")  # Clear the canvas if no code is found

# Function to draw the crosshair on the canvas
def draw_crosshair(canvas, code, color=None):
    canvas.delete("all")  # Clear previous drawings

    # Parse parameters from the code
    parameters = code.split(';')
    config = {}
    try:
        config = {parameters[i]: parameters[i + 1] for i in range(0, len(parameters), 2)}
    except IndexError:
        print("Error parsing crosshair code: code length is not even")

    # Default settings
    color_dict = {"1": "black", "2": "white", "3": "green", "4": "yellow", "5": "blue", "6": "cyan", "7": "red", "8": "pink"}
    color = color if color else color_dict.get(config.get('c', '1'), "black")
    thickness = int(config.get('0l', 4))
    outline = config.get('0o', '0') == '1'
    outline_thickness = int(config.get('0a', 1))
    dot = config.get('1b', '0') == '1'
    dot_size = int(config.get('0a', 1))

    # Draw crosshair lines
    center_x, center_y = 100, 100

    if '0l' in config and int(config['0l']) > 0:
        if outline:
            canvas.create_line(center_x, center_y - 50, center_x, center_y + 50, fill="black", width=thickness + outline_thickness)
            canvas.create_line(center_x - 50, center_y, center_x + 50, center_y, fill="black", width=thickness + outline_thickness)
        canvas.create_line(center_x, center_y - 50, center_x, center_y + 50, fill=color, width=thickness)
        canvas.create_line(center_x - 50, center_y, center_x + 50, center_y, fill=color, width=thickness)

    if dot:
        if outline:
            canvas.create_oval(center_x - dot_size - outline_thickness, center_y - dot_size - outline_thickness, center_x + dot_size + outline_thickness, center_y + dot_size + outline_thickness, fill="black")
        canvas.create_oval(center_x - dot_size, center_y - dot_size, center_x + dot_size, center_y + dot_size, fill=color)

# Function to generate a truly random crosshair code
def generate_random_code():
    P = random.choice(['1', '2', '3', '4', '5', '6', '7', '8'])
    s = random.choice(['0', '1'])
    c = random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8'])
    h = random.choice(['0', '1'])
    m = random.choice(['0', '1'])
    l = str(random.randint(1, 10))
    o = random.choice(['0', '1'])
    a = str(random.randint(1, 5))
    f = random.choice(['0', '1'])
    b = random.choice(['0', '1'])
    random_code = f"0;s;{s};P;{P};c;{c};h;{h};m;{m};0l;{l};0o;{o};0a;{a};0f;{f};1b;{b};S;c;{c};o;1"
    return random_code

def generate_random_crosshair():
    random_code = generate_random_code()
    crosshair_label.config(text=f"Random Crosshair\nCrosshair: {random_code}", fg="white")
    draw_crosshair(crosshair_canvas, random_code)  # Call draw_crosshair to display the image
    save_crosshair_image(random_code)  # Save crosshair as image

# Function to copy crosshair code to clipboard
def copy_to_clipboard():
    crosshair_text = crosshair_label.cget("text")
    if crosshair_text:
        crosshair_parts = crosshair_text.split("\n")
        if len(crosshair_parts) > 1:
            crosshair_code = crosshair_parts[-1].split(": ")[1]
            pyperclip.copy(crosshair_code)
            print("Crosshair code copied to clipboard.")
        else:
            print("No crosshair code found to copy.")
    else:
        print("No crosshair information available.")

# Function to choose background image from file explorer
def choose_background_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        background_image = Image.open(file_path)
        background_image = background_image.resize((root.winfo_width(), root.winfo_height()))
        background_image = ImageTk.PhotoImage(background_image)
        background_label.configure(image=background_image)
        background_label.image = background_image

# Function to change crosshair color
def change_crosshair_color():
    global crosshair_color
    color_code = colorchooser.askcolor(title="Choose Crosshair Color")[1]
    if color_code:
        crosshair_color = color_code
        apply_color_change()

# Function to apply the color change to the current crosshair
def apply_color_change():
    crosshair_text = crosshair_label.cget("text")
    if crosshair_text:
        crosshair_parts = crosshair_text.split("\n")
        if len(crosshair_parts) > 1:
            crosshair_code = crosshair_parts[-1].split(": ")[1]
            draw_crosshair(crosshair_canvas, crosshair_code, crosshair_color)

# Function to draw a triangle crosshair
def draw_triangle_crosshair():
    crosshair_canvas.delete("all")
    center_x, center_y = 100, 100
    size = 40
    color = crosshair_color
    crosshair_canvas.create_polygon(center_x, center_y - size, center_x - size, center_y + size, center_x + size, center_y + size, fill=color, outline="black")

# Function to draw a circle crosshair
def draw_circle_crosshair():
    crosshair_canvas.delete("all")
    center_x, center_y = 100, 100
    radius = 40
    color = crosshair_color
    crosshair_canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill=color, outline="black")

# Function to draw a dot crosshair
def draw_dot_crosshair():
    crosshair_canvas.delete("all")
    center_x, center_y = 100, 100
    dot_size = 20
    color = crosshair_color
    crosshair_canvas.create_oval(center_x - dot_size, center_y - dot_size, center_x + dot_size, center_y + dot_size, fill=color, outline="black")

# Function to import crosshair data from a JSON file
def import_crosshair_data():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, 'r') as file:
            data = json.load(file)
        crosshair_codes.update(data)
        player_menu['menu'].delete(0, 'end')
        for player in crosshair_codes.keys():
            player_menu['menu'].add_command(label=player, command=tk._setit(player_var, player))

# Function to save crosshair as an image
def save_crosshair_image(code):
    img = Image.new("RGB", (200, 200), color=(240, 240, 245))
    draw = ImageDraw.Draw(img)
    
    # Parse parameters from the code
    parameters = code.split(';')
    config = {}
    try:
        config = {parameters[i]: parameters[i + 1] for i in range(0, len(parameters), 2)}
    except IndexError:
        print("Error parsing crosshair code: code length is not even")

    # Default settings
    color_dict = {"1": "black", "2": "white", "3": "green", "4": "yellow", "5": "blue", "6": "cyan", "7": "red", "8": "pink"}
    color = color_dict.get(config.get('c', '1'), "black")
    thickness = int(config.get('0l', 4))
    outline = config.get('0o', '0') == '1'
    outline_thickness = int(config.get('0a', 1))
    dot = config.get('1b', '0') == '1'
    dot_size = int(config.get('0a', 1))

    # Draw crosshair lines
    center_x, center_y = 100, 100

    if '0l' in config and int(config['0l']) > 0:
        if outline:
            draw.line([(center_x, center_y - 50), (center_x, center_y + 50)], fill="black", width=thickness + outline_thickness)
            draw.line([(center_x - 50, center_y), (center_x + 50, center_y)], fill="black", width=thickness + outline_thickness)
        draw.line([(center_x, center_y - 50), (center_x, center_y + 50)], fill=color, width=thickness)
        draw.line([(center_x - 50, center_y), (center_x + 50, center_y)], fill=color, width=thickness)

    if dot:
        if outline:
            draw.ellipse([(center_x - dot_size - outline_thickness, center_y - dot_size - outline_thickness), (center_x + dot_size + outline_thickness, center_y + dot_size + outline_thickness)], fill="black")
        draw.ellipse([(center_x - dot_size, center_y - dot_size), (center_x + dot_size, center_y + dot_size)], fill=color)
    
    img.save("random_crosshair.png")

# Dictionary mapping player names to their crosshair codes
crosshair_codes = {
    "TenZ": "0;s;1;P;c;5;h;0;m;1;0l;4;0o;2;0a;1;0f;0;1b;0;S;c;5;o;1",
    "N4RRATE": "0;P;o;1;0t;1;0l;3;0o;1;0a;1;0f;0;1b;0",
    "Wardell": "0;s;1;P;c;7;h;0;f;0;m;1;0t;1;0l;2;0o;1;0a;1;0f;0;1t;3;1l;3;1o;0;1a;1;1m;0;1f;0",
    "Scream": "0;s;1;P;c;1;h;0;f;0;m;1;0t;2;0l;2;0o;1;0a;1;0f;0;1t;3;1l;1;1o;0;1a;1;1m;0;1f;0",
    "Doma": "0;s;1;P;c;3;h;0;f;0;m;1;0t;1;0l;2;0o;3;0a;1;0m;1;0f;0;1t;3;1l;3;1o;0;1a;1;1m;0;1f;0",
    "Yay": "0;s;1;P;c;6;h;0;f;0;m;1;0t;1;0l;2;0o;1;0a;1;0f;0;1t;3;1l;1;1o;0;1a;1;1m;0;1f;0",
    "Asuna": "0;s;1;P;c;7;h;0;f;0;m;1;0t;1;0l;3;0o;1;0a;1;0f;0;1t;2;1l;1;1o;0;1a;1;1m;0;1f;0",
    "ShahZaM": "0;s;1;P;c;8;h;0;f;0;m;1;0t;2;0l;2;0o;1;0a;1;0f;0;1t;2;1l;2;1o;1;1a;1;1m;0;1f;0",
    "Mixwell": "0;s;1;P;c;4;h;0;f;0;m;1;0t;2;0l;3;0o;1;0a;1;0f;0;1t;2;1l;3;1o;1;1a;1;1m;0;1f;0",
    "Subroza": "0;s;1;P;c;2;h;0;f;0;m;1;0t;2;0l;4;0o;1;0a;1;0f;0;1t;2;1l;4;1o;1;1a;1;1m;0;1f;0",
}

crosshair_color = "black"

# Creating the main window with a light blue background color
root = tk.Tk()
root.title("Valorant Crosshair Customizer")
root.configure(bg="#d0e3f0")  # Light blue background

# Background image label
background_label = tk.Label(root)
background_label.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

# Crosshair label with white text on a dark blue background
crosshair_label = tk.Label(root, text="", font=("Arial", 14), bg="#243a5e", fg="white")
crosshair_label.pack()

# Crosshair canvas
crosshair_canvas = tk.Canvas(root, width=200, height=200, bg="#f0f0f5")
crosshair_canvas.pack()

# Dropdown menu with a light blue background
player_var = tk.StringVar(root)
player_var.set("Select Player")
player_menu = tk.OptionMenu(root, player_var, *crosshair_codes.keys())
player_menu.configure(bg="#d0e3f0")  # Light blue background
player_menu.pack()

# Button to update the crosshair
update_button = tk.Button(root, text="Update Crosshair", command=lambda: update_crosshair(player_var.get()), bg="#007acc", fg="white")
update_button.pack()

# Button to generate a random crosshair
random_button = tk.Button(root, text="Generate Random Crosshair", command=generate_random_crosshair, bg="#007acc", fg="white")
random_button.pack()

# Button to copy crosshair code to clipboard
copy_button = tk.Button(root, text="Copy Crosshair Code", command=copy_to_clipboard, bg="#007acc", fg="white")
copy_button.pack()

# Button to choose background image
bg_button = tk.Button(root, text="Choose Background Image", command=choose_background_image, bg="#007acc", fg="white")
bg_button.pack()

# Button to change crosshair color
color_button = tk.Button(root, text="Change Crosshair Color", command=change_crosshair_color, bg="#007acc", fg="white")
color_button.pack()

# Button to draw triangle crosshair
triangle_button = tk.Button(root, text="Draw Triangle Crosshair", command=draw_triangle_crosshair, bg="#007acc", fg="white")
triangle_button.pack()

# Button to draw circle crosshair
circle_button = tk.Button(root, text="Draw Circle Crosshair", command=draw_circle_crosshair, bg="#007acc", fg="white")
circle_button.pack()

# Button to draw dot crosshair
dot_button = tk.Button(root, text="Draw Dot Crosshair", command=draw_dot_crosshair, bg="#007acc", fg="white")
dot_button.pack()

# Button to import crosshair data
import_button = tk.Button(root, text="Import Crosshair Data", command=import_crosshair_data, bg="#007acc", fg="white")
import_button.pack()

# Start the Tkinter event loop
root.mainloop()
