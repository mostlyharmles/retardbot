#converts webp to png
import os
from PIL import Image

def convert_webp_to_png(source_folder, destination_folder):
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Loop through all files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith(".webp"):
            webp_path = os.path.join(source_folder, filename)
            png_path = os.path.join(destination_folder, filename.replace(".webp", ".png"))

            # Open the webp image and convert it to PNG
            with Image.open(webp_path) as img:
                img.save(png_path, "PNG")

            print(f"Converted {webp_path} to {png_path}")

# Specify the source and destination folders
source_folder = "cards/"
destination_folder = "cards/png/"

# Call the function to convert the files
convert_webp_to_png(source_folder, destination_folder)
