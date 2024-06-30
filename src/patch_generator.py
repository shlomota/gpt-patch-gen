from api_client import call_openai_api


def generate_patch(file_name, file_content, change_description):
    prompt = (
        f"Generate a unified diff patch for the following file content. "
        f"Ensure to provide sufficient context and do not include line numbers in the content. "
        f"Return only the patch enclosed in triple backticks or respond with 'No changes needed' between the backticks if no changes are necessary:\n\n"
        f"File name: {file_name}\n"
        f"File content:\n{file_content}\n\n"
        f"Change description: {change_description}"
    )
    response = call_openai_api(prompt)

    # Extract the patch enclosed in triple backticks
    start = response.find("```") + 3
    end = response.rfind("```")
    patch = response[start:end].strip()

    return patch
