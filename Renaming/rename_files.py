import os
import sys
import re

LOG_FILE = "rename_log.txt"

def log_rename(original_path, new_path):
    """Log the rename operation to a file."""
    with open(LOG_FILE, "a") as log:
        log.write(f"{original_path} -> {new_path}\n")

# Rename logic
# Most files end with a possible $ followed by a number, which may include commas and periods. It may then be followed by a space and a number in a set of parentheses.
# Ex. &1,023.76 (1) or 234

def format_file_name(file_name):
    # Regular expression to match the title, number, optional lot identifier, and parentheses
    pattern = r"^(.*?)(-?\$?\d[\d,\.]*)(?:\s*(L\d+))?(?:\s*\((\d+)\))?(?=\.\w+$|$)"
    match = re.search(pattern, file_name)

    if match:
        # Extract the title, number, lot identifier, and parentheses
        title = match.group(1).strip()
        number = match.group(2).strip()
        lot_identifier = match.group(3)
        parentheses = match.group(4)

        # Remove apostrophes from the title
        title = title.replace("'", "")

        # Capitalize the title as a proper noun while preserving original capitalization
        connecting_words = {"of", "and", "the", "in", "on", "at", "by", "for", "with", "a", "an"}
        title_words = title.split()
        formatted_title = " ".join(
            word if i != 0 and word.lower() in connecting_words else word[0].upper() + word[1:]
            for i, word in enumerate(title_words)
        )

        # Format the number only if it doesn't already start with a dollar sign
        if not number.startswith("$"):
            if number.startswith("-"):
                number = float(number.replace(",", ""))
                formatted_number = f"-${-number:,.2f}"  # Ensure no space between -$ and the number
            else:
                number = float(number.replace(",", ""))
                formatted_number = f"${number:,.2f}"
        else:
            # Keep the number as-is if it already starts with a dollar sign
            formatted_number = number

        # Reconstruct the string
        formatted_name = formatted_title
        if formatted_number:
            formatted_name += f" {formatted_number}"
        if lot_identifier:
            formatted_name += f" {lot_identifier}"
        if parentheses:
            formatted_name += f" ({parentheses})"

        # Add the file extension back
        file_extension = re.search(r"\.\w+$", file_name).group(0)
        return formatted_name + file_extension
    else:
        # Return the original name if no match
        return file_name

# Preview rename function
def preview_rename(folder_path):
    try:
        # Check if the folder exists
        if not os.path.isdir(folder_path):
            print(f"Error: The folder '{folder_path}' does not exist.")
            return

        # Iterate through all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Skip directories
            if os.path.isdir(file_path):
                preview_rename(file_path)
                continue

            # Placeholder for renaming logic
            new_name = format_file_name(filename)
            new_path = os.path.join(folder_path, new_name)

            # Preview the rename operation
            if new_name != filename:
                # Print the preview of the rename
                if os.path.exists(new_path):
                    print(f"[Preview] Would overwrite: {filename} -> {new_name}")
                else:
                    # Print the preview of the rename
                    if filename != new_name:
                        # Print the preview of the rename
                        print(f"[Preview] Would rename: {filename} -> {new_name}")
            # print(f"[Preview] Would rename: {filename} -> {new_name}")

    except Exception as e:
        print(f"An error occurred: {e}")


def rename_files_in_folder(folder_path):
    try:
        # Check if the folder exists
        if not os.path.isdir(folder_path):
            print(f"Error: The folder '{folder_path}' does not exist.")
            return

        # Iterate through all files in the folder
        for index, filename in enumerate(os.listdir(folder_path)):
            file_path = os.path.join(folder_path, filename)

            # Skip directories
            if os.path.isdir(file_path):
                rename_files_in_folder(file_path)
                continue

            # Placeholder for renaming logic
            new_name = format_file_name(filename)
            new_path = os.path.join(folder_path, new_name)

            # Rename the file
            os.rename(file_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

def transform_filename(filename):
    """Transform the filename according to the renaming rules."""
    new_name = filename

    # Trying to make the function fix all problems at once:

    # Fix Lot identifiers (e.g., Lot 12, Lot12) to be consistent (L12)

    # Add decimals if missing

    # Add dollar sign if missing (with negative signs in front of dollar sign)

    # Capitalize names as needed


    # Replace " $ $" with " $"
    # new_name = re.sub(r'\s*\$\s*\$', r' $', new_name)

    # Move lot identifiers (e.g., L25) before the amount
    # new_name = re.sub(
    #     r'(\$\d[\d,\.]*)\s+(L\d+)\b',
    #     r'\2 \1',
    #     new_name
    # )

    # Remove unnecessary spaces before ".pdf"
    # new_name = re.sub(r'\s+\.pdf$', r'.pdf', new_name)

    # Remove all commas from the string
    # new_name = re.sub(r',', '', new_name)

    # Fix negative numbers
    # new_name = re.sub(r'\$-(\d[\d,\.]*)', r'-$\1', new_name)

    # Fix improperly renamed lot identifiers (e.g., "L $26.00" -> "L26")
    # new_name = re.sub(r'\bL\s*\$(\d+)(?:\.00)?\b', r'L\1', new_name)

    # Capitalize the title
    # new_name = capitalize_title(new_name)

    # Add a space between the title and amount: cleveland plywood-$207.13.pdf
    # new_name = re.sub(r'(\w+)-\$(\d[\d,\.]*)', r'\1 -$\2', new_name)
    
    # Remove patterns like " L11" (L followed by two digits)
    # new_name = re.sub(r' L\d{2}\b', '', new_name)

    # Add .00 to amounts that don't have it
    # new_name = re.sub(
    #     r'(?<!\.\d{2})(\$\d{1,3}(?:,\d{3})*)\b(?!\.\d{2})',  # Match amounts without decimals
    #     r'\1.00',  # Append .00 to the matched amount
    #     new_name
    # )

    # Add a space between name and amount
    # new_name = re.sub(
    #     r'(\w)(\$)',  # Match a word character directly followed by a dollar sign
    #     r'\1 \2',     # Insert a space between the word character and the dollar sign
    #     new_name
    # )

    # Remove the pattern '$- $'
    # new_name = re.sub(r'\$-\s\$', '$', new_name)

    # Replace '.pdf' with '.00.pdf' for names ending with two digits followed by '.pdf', not preceded by '.'
    # new_name = re.sub(r'\$(\d+)(?=(?:\s*\(|\s*\.pdf$))(?!\.\d{2})', r'$\1.00', new_name)

    # Replace Gas N Go with GasNGo
    # new_name = re.sub(r'Gas N Go', 'GasNGo', new_name)

    return new_name

def capitalize_title(title):
    """Capitalize words in the title that aren't connecting words, preserving internal capitalization."""
    connecting_words = {"of", "and", "the", "in", "on", "at", "by", "for", "with", "a", "an"}
    title_words = title.split()
    formatted_title = " ".join(
        word if i != 0 and word.lower() in connecting_words else word[0].upper() + word[1:]
        if word.islower() or word[0].islower() else word
        for i, word in enumerate(title_words)
    )
    return formatted_title

def preview_fix_filenames(directory):
    """Preview the renaming of files without making changes."""
    for root, _, files in os.walk(directory):
        for filename in files:
            original = filename
            new_name = transform_filename(original)

            if new_name != original:
                full_original_path = os.path.join(root, original)
                full_new_path = os.path.join(root, new_name)
                print(f"[Preview] Would rename: {original} -> {new_name}")


def fix_filenames(directory):
    """Perform the renaming of files and log the changes."""
    for root, _, files in os.walk(directory):
        for filename in files:
            original = filename
            new_name = transform_filename(original)

            if new_name != original:
                full_original_path = os.path.join(root, original)
                full_new_path = os.path.join(root, new_name)

                # Perform the rename
                os.rename(full_original_path, full_new_path)

                # Log the rename
                log_rename(full_original_path, full_new_path)
                print(f"Renamed: {full_original_path} -> {full_new_path}")

def write_filenames_to_file(directory, output_file="filenames.txt"):
    """Write all filenames (with paths) to a text file."""
    try:
        # Ensure the output file path is absolute
        output_file = os.path.abspath('Renaming/' + output_file)
        print(f"Writing filenames to: {output_file}")

        with open(output_file, "w") as file:
            for root, _, files in os.walk(directory):
                for filename in files:
                    # Construct the full path relative to the main folder
                    relative_path = os.path.relpath(os.path.join(root, filename), start=directory)
                    file.write(relative_path + "\n")
        print(f"Filenames written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def revert_renames():
    """Revert renames based on the log file."""
    if not os.path.exists(LOG_FILE):
        print(f"No log file found: {LOG_FILE}")
        return

    with open(LOG_FILE, "r") as log:
        lines = log.readlines()

    # Revert renames in reverse order
    for line in reversed(lines):
        original, renamed = line.strip().split(" -> ")
        if os.path.exists(renamed):
            os.rename(renamed, original)
            print(f"Reverted: {renamed} -> {original}")

    # Clear the log file after reverting
    open(LOG_FILE, "w").close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rename_files.py <command> <folder_path>")
        print("Commands:")
        print("  preview <folder_path> - Preview renames")
        print("  fix <folder_path> - Perform renames and log them")
        print("  revert - Revert renames based on the log")
        print("  previewfix" + " <folder_path> - Preview fixes")
        print("  previewrename" + " <folder_path> - Preview renames")
        print("  rename" + " <folder_path> - Rename files")
        print("  list" + " <folder_path> - List filenames")
    else:
        command = sys.argv[1]
        if command == "previewfix" and len(sys.argv) == 3:
            folder_path = sys.argv[2]
            preview_fix_filenames(folder_path)
        elif command == "fix" and len(sys.argv) == 3:
            folder_path = sys.argv[2]
            fix_filenames(folder_path)
        elif command == "revert":
            revert_renames()
        elif command == "previewrename" and len(sys.argv) == 3:
            folder_path = sys.argv[2]
            preview_rename(folder_path)
        elif command == "rename" and len(sys.argv) == 3:
            folder_path = sys.argv[2]
            rename_files_in_folder(folder_path)
        elif command == "list" and len(sys.argv) == 3:
            folder_path = sys.argv[2]
            write_filenames_to_file(folder_path)
        else:
            print("Invalid command or arguments.")
