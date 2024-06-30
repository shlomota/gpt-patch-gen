from api_client import call_openai_api


def generate_patch(file_names, combined_context, change_description):
    prompt = (
        f"Generate unified diff patches for the following file contents. "
        f"Ensure to provide sufficient context and do not include line numbers in the content. "
        f"Use similar code patterns to what is provided in the context to generate the patches. "
        f"You may need to add or remove lines, modify existing lines, or fix issues in the code."
        f"Return each patch enclosed in triple backticks, and if no changes are needed for a file, respond with 'No changes needed' within triple backticks:\n\n"
        f"{combined_context}\n\n"
        f"Change description: {change_description}"
    )
    response = call_openai_api(prompt)

    # Extract all patches enclosed in triple backticks
    patches = {}
    blocks = response.split("```")
    for i in range(1, len(blocks), 2):
        patch = blocks[i].strip()
        if patch.lower() == 'no changes needed':
            file_name = file_names[i // 2]
            patches[file_name] = patch
        else:
            # Identify the corresponding file based on the order
            file_name = file_names[(i - 1) // 2]
            patches[file_name] = patch

    return patches
