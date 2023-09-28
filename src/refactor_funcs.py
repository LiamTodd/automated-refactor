import ast
import os
from io import StringIO
import pyflakes.api as flakes
from pyflakes.reporter import Reporter
from io import StringIO
from contextlib import redirect_stderr


def rename_functions_in_files(directory, old_function_name, new_function_name):
    modified_files = []

    # A dictionary to track renamed functions and their new names
    renamed_functions = {old_function_name: new_function_name}

    original_content = {}

    def update_function_calls(node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in renamed_functions:
                node.func.id = renamed_functions[node.func.id]
        for child_node in ast.iter_child_nodes(node):
            update_function_calls(child_node)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                # Read the Python file
                with open(file_path, "r") as f:
                    content = f.read()
                    original_content[file_path] = content

                # Parse the code into an Abstract Syntax Tree (AST)
                tree = ast.parse(content)

                # Create a visitor to traverse the AST and rename functions
                class RenameFunctions(ast.NodeTransformer):
                    def visit_FunctionDef(self, node):
                        if node.name == old_function_name:
                            node.name = new_function_name
                            modified_files.append(file_path)
                        return node

                transformer = RenameFunctions()
                new_tree = transformer.visit(tree)

                # Update function calls in the AST
                update_function_calls(new_tree)

                # Generate the modified code from the AST
                modified_code = ast.unparse(new_tree)

                # Write the modified content back to the file
                with open(file_path, "w") as f:
                    f.write(modified_code)

    # Now, let's handle renaming function-related imports
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                # Read the Python file
                with open(file_path, "r") as f:
                    content = f.read()

                # Replace old import statements with new ones for functions
                modified_content = content.replace(
                    f"import {old_function_name}", f"import {new_function_name}")
                modified_content = modified_content.replace(
                    f"from {old_function_name}", f"from {new_function_name}")

                # If function-related imports were modified, write the updated content back to the file
                if content != modified_content:
                    with open(file_path, "w") as f:
                        f.write(modified_content)
                    modified_files.append(file_path)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                if len(find_undefined_variables(content, file_path)) > 0:
                    with open(file_path, "w") as f:
                        f.write(original_content[file_path])

    return modified_files


class StreamToList():
    def __init__(self):
        self.stream = []

    def write(self, new_item):
        self.stream.append(new_item)


def find_undefined_variables(code_str, file_path):

    warnings = StreamToList()
    errors = StreamToList()

    # Redirect stderr to capture Pyflakes output
    with redirect_stderr(StringIO()):
        reporter = Reporter(warnings, errors)
        flakes.check(codeString=code_str,
                     filename=file_path, reporter=reporter)

    undefined_names = []
    for warning in warnings.stream:
        if "undefined name" in warning:
            name = warning.split("'")[-2]
            undefined_names.append(name)
    return undefined_names


if __name__ == "__main__":
    directory_to_refactor = "./dummy_code"
    old_name = "greetings"
    new_name = "new_hello"

    modified_files = rename_functions_in_files(
        directory_to_refactor, old_name, new_name)

    if modified_files:
        print("Modified files:")
        for file_path in modified_files:
            print(file_path)
    else:
        print("No files were modified.")
