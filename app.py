import tkinter as tk
from tkinter import filedialog, Label
from PIL import Image, ImageTk
import io
from google.cloud import vision
from decouple import config

# Load the service account file path from the environment file
service_account_file = config('VISION_SERVICE_ACCOUNT_FILE')

# Initialize Google Cloud Vision client
vision_client = vision.ImageAnnotatorClient.from_service_account_file(service_account_file)

def upload_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        
        panel.config(image=img)
        panel.image = img
        
        # Analyze the image using Google Cloud Vision API
        description = analyze_image(file_path)
        description_label.config(text=description)

def analyze_image(file_path):
    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations

    descriptions = [label.description for label in labels]
    return ' , '.join(descriptions)

# Create the Tkinter window
root = tk.Tk()
root.title("Image Upload and Analysis App")
root.geometry("600x600")

# Create a button to upload files
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=20)

# Label to display the uploaded image
panel = Label(root)
panel.pack(pady=20)

# Label to display the description
description_label = Label(root, text="", wraplength=500)
description_label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
