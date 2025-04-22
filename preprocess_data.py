import os
import json
from pdf2image import convert_from_path
from google.cloud import vision
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Make sure the environment variable is set
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


# Initialize Google Cloud Vision client
client = vision.ImageAnnotatorClient()

def pdf_to_png(pdf_path):
    # Convert the PDF to a list of images (one per page)
    images = convert_from_path(pdf_path)
    
    # Save each image as a PNG file
    png_paths = []
    for i, image in enumerate(images):
        png_path = generate_image_path(pdf_path, f"{re.sub('.pdf', '', os.path.basename(pdf_path))}_page_{i + 1}.png")
        # Ensure the folders exist
        os.makedirs(os.path.dirname(png_path), exist_ok=True)
        image.save(png_path, 'PNG')
        png_paths.append(png_path)
    
    return png_paths

def extract_text_from_image(image_path):
    # Open the image file
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Create the image object directly using vision.Image
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    # Extract the text and bounding boxes
    ocr_data = []
    if response.text_annotations:
        for annotation in response.text_annotations:
            ocr_data.append({
                'text': annotation.description,
                'bounding_box': [(vertex.x, vertex.y) for vertex in annotation.bounding_poly.vertices]
            })
    
    return ocr_data

def process_receipt(pdf_path):
    # Extract the payee and amount from the PDF filename
    filename = os.path.basename(pdf_path)
    payee_match = re.search(r'(.+?)\s+-?\$\d+\.?\d*(?:\s+\(\d+\))?', filename)
    if payee_match:
        payee = re.sub(r'\$', '', payee_match.group(1))
    else:
        print(f"Payee not found in filename: {filename}")
        payee = None

    amount_match = re.search(r'(-?\$\d+\.?\d*)', filename)
    if amount_match:
        amount = re.sub(r'\$', '', amount_match.group(1))
    else:
        print(f"Amount not found in filename: {filename}")
        amount = None
    if payee is None or len(payee) < 1 or amount is None or len(amount) < 1:
        payee = None
        amount = None
    
    # Generate the JSON filename
    json_name = re.sub(r'\.pdf$', '_ocr_data.json', os.path.basename(pdf_path))
    json_output_path = generate_results_path(pdf_path, json_name)

    # Check if the JSON file already exists
    if os.path.exists(json_output_path):
        return json_output_path

    # Step 1: Convert the PDF to PNG(s)
    png_paths = pdf_to_png(pdf_path)
    
    # Step 2: Extract text and bounding box information from the PNG
    ocr_results = []
    for png_path in png_paths:
        ocr_data = extract_text_from_image(png_path)
        ocr_results.append({
            'payee': payee,
            'amount': amount,
            'image_path': png_path,
            'ocr_data': ocr_data
        })
    
    # Step 3: Save the OCR results to a JSON file

    # Ensure the folders exist
    os.makedirs(os.path.dirname(json_output_path), exist_ok=True)

    # Save the OCR results to a JSON file
    with open(json_output_path, 'w') as json_file:
        json.dump(ocr_results, json_file, indent=4)

    return json_output_path

def generate_image_path(pdf_path, new_filename):
    """
    Generate the path for the new image dynamically based on the original PDF path.
    
    Args:
        pdf_path (str): The path to the original PDF file.
        new_filename (str): The new filename for the image (after applying transformations).
    
    Returns:
        str: The dynamically generated path for the new image.
    """
    # Replace 'PDF Receipts' with 'Image Receipts' in the path
    image_path = re.sub(r'PDF Receipts', 'Image Receipts', pdf_path)

    # Extract the directory path (up to the year/month folder)
    image_dir = os.path.dirname(image_path)

    # Combine the new directory with the new filename
    new_image_path = os.path.join(image_dir, new_filename)

    return new_image_path

def generate_results_path(pdf_path, new_filename):
    """
    Generate the path for the new results dynamically based on the original PDF path.
    
    Args:
        pdf_path (str): The path to the original PDF file.
        new_filename (str): The new filename for the results (after applying transformations).
    
    Returns:
        str: The dynamically generated path for the new results.
    """
    # Replace 'PDF Receipts' with 'OCR Outputs' in the path
    results_path = re.sub(r'PDF Receipts', 'OCR Outputs', pdf_path)

    # Extract the directory path (up to the year/month folder)
    results_dir = os.path.dirname(results_path)

    # Combine the new directory with the new filename
    new_results_path = os.path.join(results_dir, new_filename)

    return new_results_path

def preprocess_all(folder_path):
    """
    Process all receipts in the specified folder and its subfolders.
    
    Args:
        folder_path (str): The path to the folder containing PDF files.
    
    Returns:
        list: A list of paths to the generated JSON files.
    """
    json_files = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(root, filename)
                json_file = process_receipt(pdf_path)
                json_files.append(json_file)
    return json_files

# main function
if __name__ == "__main__":
    preprocess_all('/Users/matthewpeterson/Dropbox/Matthew/Clean Receipts/PDF Receipts/2022')
    # Example usage
    # pdf_path = '/Users/matthewpeterson/Dropbox/Matthew/Clean Receipts/PDF Receipts/2022/01_22/Bank of Cleveland $526.00.pdf'
    # process_receipt(pdf_path)