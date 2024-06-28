def add_line_numbers(file_content):
    lines = file_content.splitlines()
    numbered_lines = [f"{idx+1:04d}: {line}" for idx, line in enumerate(lines)]
    return "\n".join(numbered_lines)

def remove_line_numbers(file_content):
    lines = file_content.splitlines()
    original_lines = [line.split(": ", 1)[1] if ": " in line else line for line in lines]
    return "\n".join(original_lines)

