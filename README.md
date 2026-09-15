# Bulk Certificate Generator

A Python script designed to automatically generate bulk certificates by overlaying names and organization details from a CSV file directly onto a certificate template image. It correctly scales font sizes and accurately aligns text automatically based on the template's dimensions.

## Requirements
Ensure you have Python installed, then install the required dependencies:
```bash
pip install pandas Pillow
```

## Settings & File Locations
Before running the generator, ensure your files are organized correctly. The script `bulk_certificate_generator.py` looks for these files in the project folder:

* **CSV File (`Students.csv`)**: 
  * The dataset containing the list of participants.
  * Required columns:
    * `Full Name of Participant` (Mapped to the student's name on the top line).
    * `Name of Organization/ Institute` (Mapped to the college/organization on the bottom line).
* **Template File (`certificate_template.png`)**: 
  * The blank certificate image template where text will be drawn. 
* **Output Folder (`Generated certificates/`)**: 
  * The script will automatically create this folder if it does not exist.
  * All generated certificates will be saved here in high-resolution PDF format.
* **Font File (`TitilliumWeb-SemiBold.ttf`)**: 
  * The typography used to render the text on the certificate. Ensure it is a `.ttf` file.

*To change any of these files, modify the `CSV_FILE`, `TEMPLATE_FILE`, `OUTPUT_FOLDER`, and `FONT_FILE` variables at the top of the Python script.*

## Smart Scaling (Font Size Mechanism)
You don't need to manually configure hardcoded font sizes. The generator detects the width of your certificate template and sizes the font accordingly:
* **The base title (Your Name) font size** is calculated as exactly **3.5% (0.035)** of the template's total width.
* **The sub-title (Your College/Host) font size** is calculated as **2.1% (0.021)** of the width.

**Smart Scaling:** If a participant's name is exceptionally long (over 30 characters), the script intelligently reduces the font size by **12%**. If the college name is over 45 characters, it reduces it by **15%** to prevent text from overflowing off the edges.

## Precision Alignment (Positional Mechanism)
The text elements are bound to precise coordinates calculated via percentages of the main template canvas. This means it maintains perfect alignment regardless of if your template is 1080p, 4K, or 8K:

* **Name Title Position**: The text is anchored horizontally at **57.3% (0.573)** of the total image width and vertically at **40.8% (0.408)** of the height. 
* **College Position**: Anchored horizontally at **22.5% (0.225)** and vertically at **48.1% (0.467)**.

When plotting the generated text dynamically looping over your CSV file, the Python Pillow (`ImageDraw`) function utilizes `anchor="mm"`. This acts as an absolute centering mechanism, dropping the exact Middle-Middle coordinate point of the actual text string directly onto those precise percentage coordinates.

## How to Run:
Make sure your CSV and template files are set up, open a terminal in this directory, and type:
```bash
python bulk_certificate_generator.py
```
Check your `Generated certificates/` folder when it finishes!
