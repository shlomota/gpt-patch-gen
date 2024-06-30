import os
import subprocess
from colorama import init, Fore, Style


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


def apply_patch(patch_content, patch_file_path, target_repo_path):
    # Clean the patch content
    cleaned_patch_content = clean_patch_content(patch_content)

    with open(patch_file_path, 'w') as patch_file:
        patch_file.write(cleaned_patch_content + "\n")

    print(f"Patch saved to {patch_file_path}")

    confirmation = input("Do you want to apply this patch? (yes/no/skip): ").strip().lower()
    if confirmation in ['skip', 's']:
        print("Patch application skipped.")
        return False

    if confirmation in ['yes', 'y']:
        original_dir = os.getcwd()
        os.chdir(target_repo_path)  # Change to the target repo directory
        result = subprocess.run(['git', 'apply', patch_file_path], capture_output=True, text=True)
        os.chdir(original_dir)  # Change back to the original directory
        if result.returncode == 0:
            print("Patch applied successfully.")
        else:
            print(f"Failed to apply patch. Error: {result.stderr}")
            # Print the colorized patch for the user to easily copy-paste
            print("Failed patch:\n")
            print(colorize_patch('\n'.join([line[1:] for line in patch_content.splitlines()])))
            return False
    else:
        print("Patch application aborted.")
        return False
    return True

def ensure_openai_key():
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        openai_key = input("Enter your OpenAI API key: ").strip()
        os.environ["OPENAI_API_KEY"] = openai_key

        save_persistent = input("Do you want to save the OpenAI API key in your ~/.bashrc for persistence? (yes/no): ").strip().lower()
        if save_persistent in ["yes", "y"]:
            bashrc_path = os.path.expanduser("~/.bashrc")
            with open(bashrc_path, "a") as bashrc_file:
                bashrc_file.write(f"\n# OpenAI API key\nexport OPENAI_API_KEY={openai_key}\n")
            print("OpenAI API key saved in ~/.bashrc. Please run 'source ~/.bashrc' to apply the changes.")
    else:
        print("Using OpenAI API key from environment variables.")