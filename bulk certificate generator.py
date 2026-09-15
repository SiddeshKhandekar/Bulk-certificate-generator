import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# 1. SETTINGS & PATHS (Update these 4 lines)
# ==============================================================================
CSV_FILE = "students.csv"                  # Path to your CSV file
TEMPLATE_FILE = "Copy of CERTIFICATE.jpg"  # Path to your certificate image
OUTPUT_FOLDER = "generated_certificates"   # Folder where PDFs will be saved
FONT_FILE = "C:/Windows/Fonts/arialbd.ttf" # Exact path to your local .ttf font file

# CSV Column Headers
COL_NAME = "Student Name"
COL_COLLEGE = "College Name"

# ==============================================================================
# 2. CERTIFICATE GENERATION
# ==============================================================================
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
df = pd.read_csv(CSV_FILE)

# Read image dimensions once to automatically scale positions and font sizes
with Image.open(TEMPLATE_FILE) as img:
    width, height = img.size

# Automatically size fonts based on the image width (Large for Name, Medium for College)
# ==============================================================================
# TITLE SIZE MECHANISM:
# The title (Student Name) font size is set dynamically to 2.2% of the total template width.
# ==============================================================================
NAME_FONT = ImageFont.truetype(FONT_FILE, size=int(width * 0.022))  #0.033 Default size
COLLEGE_FONT = ImageFont.truetype(FONT_FILE, size=int(width * 0.022))

# Coordinates mapped exactly to the center of the blank lines in your template
# ==============================================================================
# POSITIONAL MECHANISM (TITLE):
# The position uses relative scaling to determine where the title should anchor:
# - X (width * 0.600): The text anchors horizontally at 60.0% of the image's width.
# - Y (height * 0.422): The text anchors vertically at 42.2% of the image's height.
# ==============================================================================
NAME_POS = (int(width * 0.600), int(height * 0.422)) # w:0.600 | h:0.422
COLLEGE_POS = (int(width * 0.545), int(height * 0.475))

print("Starting PDF generation...")

for _, row in df.iterrows():
    student_name = str(row[COL_NAME]).strip()
    college_name = str(row[COL_COLLEGE]).strip()

    # Open a fresh copy of the template for each student
    with Image.open(TEMPLATE_FILE) as img:
        cert = img.convert("RGB")
        draw = ImageDraw.Draw(cert)

        # Draw Student Name (Navy Blue, centered exactly on the top line)
        draw.text(NAME_POS, student_name, fill="#1a243b", font=NAME_FONT, anchor="mm")

        # Draw College Name (Dark Grey, centered exactly on the bottom line)
        draw.text(COLLEGE_POS, college_name, fill="#333333", font=COLLEGE_FONT, anchor="mm")

        # Create a clean filename without symbols that could break file saving
        clean_name = "".join(c for c in f"{student_name}_{college_name}" if c.isalnum() or c in " _-")
        output_path = os.path.join(OUTPUT_FOLDER, f"{clean_name}.pdf")
        
        # Save high-resolution PDF
        cert.save(output_path, "PDF", resolution=300.0)
        print(f" -> Saved: {clean_name}.pdf")

print(f"\nDone! All certificates are saved in: {os.path.abspath(OUTPUT_FOLDER)}")