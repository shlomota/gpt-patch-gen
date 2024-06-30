import os
import argparse
from src.patch_generator import generate_patch
from src.file_preprocessor import add_line_numbers, remove_line_numbers
from src.utils import colorize_patch, apply_patch
from colorama import init

def main():
    init(autoreset=True)  # Initialize colorama

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate and apply patches to a target Git repository.")
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(), help="Target repository directory (default: current directory)")
    args = parser.parse_args()

    target_repo_path = args.directory

    # Get user input for prompt and file names
    change_description = input("Enter the change description: ")
    file_names = input("Enter a comma-separated list of local files to send as context: ").split(',')

    # Ensure patch_files directory exists
    patch_files_path = os.path.join(target_repo_path, 'patch_files')
    os.makedirs(patch_files_path, exist_ok=True)

    # Read file contents
    file_contents = {}
    for file_name in file_names:
        file_name = file_name.strip()  # Remove leading/trailing whitespace
        file_path = os.path.join(target_repo_path, file_name)
        with open(file_path, 'r') as file:
            file_contents[file_name] = file.read()

    # Generate patch for each file
    patches = {}
    for file_name, file_content in file_contents.items():
        numbered_content = add_line_numbers(file_content)
        print(f"Generating patch for file '{file_name}' with description: '{change_description}'")
        patch = generate_patch(file_name, numbered_content, change_description)
        if patch.lower() == 'no changes needed':
            print(f"No changes needed for {file_name}")
            continue
        print("Patch generated:\n")
        print(colorize_patch(patch))
        patches[file_name] = patch

    # Find the next available patch file number
    existing_patches = [int(f.split('.')[0]) for f in os.listdir(patch_files_path) if f.endswith('.diff')]
    next_patch_number = max(existing_patches, default=0) + 1

    # Save and apply each patch
    for file_name, patch in patches.items():
        patch_file_name = f"{next_patch_number:04d}_{file_name.replace('/', '_')}.diff"
        patch_file_path = os.path.join(patch_files_path, patch_file_name)
        print(f"\nSaving patch to {patch_file_path} and applying it...")
        success = apply_patch(patch, patch_file_path, target_repo_path)
        if not success:
            input("After making the manual changes, press Enter to proceed to the next patch...")
        next_patch_number += 1

if __name__ == "__main__":
    main()
