import os
import argparse
from patch_generator import generate_patch
from file_preprocessor import add_line_numbers, remove_line_numbers
from utils import colorize_patch, apply_patch
from colorama import init


def ensure_openai_key():
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        openai_key = input("Enter your OpenAI API key: ").strip()
        os.environ["OPENAI_API_KEY"] = openai_key

        save_persistent = input(
            "Do you want to save the OpenAI API key in your ~/.bashrc for persistence? (yes/no): ").strip().lower()
        if save_persistent in ["yes", "y"]:
            bashrc_path = os.path.expanduser("~/.bashrc")
            with open(bashrc_path, "a") as bashrc_file:
                bashrc_file.write(f"\n# OpenAI API key\nexport OPENAI_API_KEY={openai_key}\n")
            print("OpenAI API key saved in ~/.bashrc. Please run 'source ~/.bashrc' to apply the changes.")
    else:
        print("Using OpenAI API key from environment variables.")


def extract_patch_number(patch_file_name):
    try:
        return int(patch_file_name.split('_')[0])
    except ValueError:
        return -1


def main():
    init(autoreset=True)  # Initialize colorama

    # Ensure OpenAI key is available
    ensure_openai_key()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate and apply patches to a target Git repository.")
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(),
                        help="Target repository directory (default: current directory)")
    args = parser.parse_args()

    target_repo_path = args.directory

    # Get user input for prompt and file names
    change_description = input("Enter the change description: ")
    file_names = [file_name.strip() for file_name in
                  input("Enter a comma-separated list of local files to send as context: ").split(',')]

    # Ensure patch_files directory exists
    patch_files_path = os.path.join(target_repo_path, 'patch_files')
    os.makedirs(patch_files_path, exist_ok=True)

    # Read file contents
    file_contents = {}
    for file_name in file_names:
        file_path = os.path.join(target_repo_path, file_name)
        with open(file_path, 'r') as file:
            file_contents[file_name] = add_line_numbers(file.read())

    # Combine file contents for context
    combined_context = "\n".join([f"File name: {name}\n{content}" for name, content in file_contents.items()])

    # Generate patches using the combined context
    patches = generate_patch(file_names, combined_context, change_description)

    # Find the next available patch file number
    existing_patches = [extract_patch_number(f) for f in os.listdir(patch_files_path) if f.endswith('.diff')]
    next_patch_number = max(existing_patches, default=0) + 1

    # Save and apply each patch
    for file_name, patch in patches.items():
        if patch.lower() == 'no changes needed':
            print(f"No changes needed for {file_name}")
            continue
        print(f"Patch generated for {file_name}:\n")
        print(colorize_patch(patch))
        patch_file_name = f"{next_patch_number:04d}_{file_name.replace('/', '_')}.diff"
        patch_file_path = os.path.join(patch_files_path, patch_file_name)
        print(f"\nSaving patch to {patch_file_path} and applying it...")

        while True:
            confirmation = input("Do you want to apply this patch? (yes/skip/quit): ").strip().lower()
            if confirmation in ['yes', 'y']:
                success = apply_patch(patch, patch_file_path, target_repo_path)
                if not success:
                    input("After making the manual changes, press Enter to proceed to the next patch...")
                next_patch_number += 1
                break
            elif confirmation in ['skip', 's']:
                print("Skipping this patch.")
                next_patch_number += 1
                break
            elif confirmation in ['quit', 'q']:
                print("Quitting the process.")
                return
            else:
                print("Invalid option. Please enter 'yes', 'skip', or 'quit'.")


if __name__ == "__main__":
    main()
