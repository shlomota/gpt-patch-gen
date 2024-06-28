import os
import subprocess
from src.patch_generator import generate_patch
from src.file_preprocessor import add_line_numbers, remove_line_numbers
from colorama import init, Fore, Style

demo_repo_path = '/Users/shlomota/PycharmProjects/demo-repo'


def colorize_patch(patch):
    colored_patch = []
    for line in patch.splitlines():
        if line.startswith('+'):
            colored_patch.append(Fore.GREEN + line + Style.RESET_ALL)
        elif line.startswith('-'):
            colored_patch.append(Fore.RED + line + Style.RESET_ALL)
        else:
            colored_patch.append(line)
    return "\n".join(colored_patch)

def clean_patch_content(patch_content):
    # Remove "diff" prefix if it appears
    if patch_content.startswith("diff"):
        patch_content = "\n".join(patch_content.split("\n")[1:])

    def adjust_indentation(line):
        # Check if the line starts with multiple +++ or ---
        if line.startswith('+++') or line.startswith('---') or line.startswith("@@"):
            return line

        # Count the leading + or - as part of the indentation
        if line.startswith('+') or line.startswith('-'):
            leading_chars = len(line) - len(line[1:].lstrip())
        else:
            leading_chars = len(line) - len(line.lstrip())

        # Add a space if the number of leading characters is even
        if leading_chars % 2 == 0:
            if line.startswith('+') or line.startswith('-'):
                return line[0] + ' ' + line[1:]
            return ' ' + line
        return line

    # Fix indentation issues based on specified requirements
    lines = patch_content.splitlines()
    cleaned_lines = [adjust_indentation(line) for line in lines if not line[1:].strip() in ["+"]]

    # Ensure a blank line at the end of the patch content
    cleaned_patch_content = "\n".join(cleaned_lines)
    if not cleaned_patch_content.endswith("\n"):
        cleaned_patch_content += "\n"

    return cleaned_patch_content

def apply_patch(patch_content, patch_file_path):
    # Clean the patch content
    cleaned_patch_content = clean_patch_content(patch_content)
    
    with open(patch_file_path, 'w') as patch_file:
        patch_file.write(cleaned_patch_content + "\n")
    
    print(f"Patch saved to {patch_file_path}")

    confirmation = input("Do you want to apply this patch? (yes/no): ").strip().lower()
    if confirmation in ['yes', 'y']:
        original_dir = os.getcwd()
        os.chdir(demo_repo_path)  # Change to the target repo directory
        result = subprocess.run(['git', 'apply', patch_file_path], capture_output=True, text=True)
        os.chdir(original_dir)  # Change back to the original directory
        if result.returncode == 0:
            print("Patch applied successfully.")
        else:
            print(f"Failed to apply patch. Error: {result.stderr}")
    else:
        print("Patch application aborted.")

def main():
    init(autoreset=True)  # Initialize colorama
    patch_files_path = os.path.join(demo_repo_path, 'patch_files')
    file_name = 'example.py'
    file_path = os.path.join(demo_repo_path, file_name)
    change_description = 'Update the function foo to handle edge cases.'

    # Ensure patch_files directory exists
    os.makedirs(patch_files_path, exist_ok=True)

    # Read file content
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Add line numbers (for internal use only)
    numbered_content = add_line_numbers(file_content)

    # Generate patch (without line numbers in the actual diff)
    print(f"Generating patch for file '{file_name}' with description: '{change_description}'")
    patch = generate_patch(file_name, numbered_content, change_description)
    print("Patch generated:\n")
    print(colorize_patch(patch))

    # Find the next available patch file number
    existing_patches = [int(f.split('.')[0]) for f in os.listdir(patch_files_path) if f.endswith('.diff')]
    next_patch_number = max(existing_patches, default=0) + 1
    patch_file_name = f"{next_patch_number:04d}.diff"
    patch_file_path = os.path.join(patch_files_path, patch_file_name)

    # Save and apply the patch
    print(f"\nSaving patch to {patch_file_path} and applying it...")
    apply_patch(patch, patch_file_path)

if __name__ == "__main__":
    main()

