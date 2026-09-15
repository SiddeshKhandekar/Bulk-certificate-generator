import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# 1. SETTINGS & PATHS (Update these 4 lines)
# ==============================================================================
CSV_FILE = "E:\College\Dump\Bulk Certificate Generator\Students.csv"                  # Path to your CSV file
TEMPLATE_FILE = "E:\College\Dump\Bulk Certificate Generator\certificate_template.png"  # Path to your certificate image
OUTPUT_FOLDER = "E:\College\Dump\Bulk Certificate Generator\Generated certificates"   # Folder where PDFs will be saved
FONT_FILE = "E:\College\Dump\Bulk Certificate Generator\TitilliumWeb-SemiBold.ttf" # Exact path to your local .ttf font file

# CSV Column Headers
COL_NAME = "Full Name of Participant"
COL_COLLEGE = "Name of Organization/ Institute"

# ==============================================================================
# 2. CERTIFICATE GENERATION (PRECISION ALIGNMENT & SMART SCALING)
# ==============================================================================
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
df = pd.read_csv(CSV_FILE)

# Read image dimensions to scale positions and font sizes
with Image.open(TEMPLATE_FILE) as img:
    width, height = img.size

# Base Font Sizes (Sized for prominence)
BASE_NAME_SIZE = int(width * 0.035)
BASE_COLLEGE_SIZE = int(width * 0.021)

# PRECISION POSITIONS (Calculated directly from template lines):
# Name: Centered exactly at the midpoint of the top line (57.3% X, 43.4% Y)
NAME_POS = (int(width * 0.573), int(height * 0.408))

# College: Left-aligned starting right after the word "From" (22.5% X, 48.1% Y)
COLLEGE_POS = (int(width * 0.225), int(height * 0.467))

print("Starting PDF generation...")

for _, row in df.iterrows():
    student_name = str(row[COL_NAME]).strip()
    college_name = str(row[COL_COLLEGE]).strip()

    # Smart Scaling: If college name is over 45 characters, scale font down by 15% so it fits!
    name_size = int(BASE_NAME_SIZE * 0.88) if len(student_name) > 30 else BASE_NAME_SIZE
    college_size = int(BASE_COLLEGE_SIZE * 0.85) if len(college_name) > 45 else BASE_COLLEGE_SIZE
    
    font_name = ImageFont.truetype(FONT_FILE, size=name_size)
    font_college = ImageFont.truetype(FONT_FILE, size=college_size)

    with Image.open(TEMPLATE_FILE) as img:
        cert = img.convert("RGB")
        draw = ImageDraw.Draw(cert)

        # Draw Student Name (Centered over the top line)
        draw.text(NAME_POS, student_name, fill="#1a243b", font=font_name, anchor="mm")

        # Draw College Name (Left-aligned starting right after "From")
        draw.text(COLLEGE_POS, college_name, fill="#333333", font=font_college, anchor="lm")

        # Clean filename without breaking characters
        clean_name = "".join(c for c in f"{student_name}_{college_name}" if c.isalnum() or c in " _-")
        output_path = os.path.join(OUTPUT_FOLDER, f"{clean_name}.pdf")
        
        cert.save(output_path, "PDF", resolution=300.0)
        print(f" -> Saved: {clean_name}.pdf")

print(f"\nDone! All certificates are saved in: {os.path.abspath(OUTPUT_FOLDER)}")