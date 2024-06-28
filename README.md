# GPTPatchGen

GPTPatchGen is a tool that generates and applies patch files to update a code repository using OpenAI's API.

## Project Structure
- `demo-repo/`: A submodule containing example files for demonstrating patch application.
  - `another_example.py`
  - `example.py`
  - `orig/`
    - `another_example.py`
    - `example.py`
- `examples/`: Directory containing example scripts.
  - `example_script.py`
- `requirements.txt`: File containing project dependencies.
- `src/`: Directory containing source code for the project.
  - `__pycache__/`: Directory containing cached bytecode files.
    - `api_client.cpython-311.pyc`
    - `file_preprocessor.cpython-311.pyc`
    - `patch_generator.cpython-311.pyc`
  - `api_client.py`
  - `file_preprocessor.py`
  - `patch_generator.py`

## Installation

1. Clone the repository.
2. Install the requirements:

pip install -r requirements.txt

## Usage

Run the example script:

python examples/example_script.py

