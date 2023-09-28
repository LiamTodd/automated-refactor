from _ast import AST, Call, alias
import ast
import os
from io import StringIO
from typing import Any
import pyflakes.api as flakes
from pyflakes.reporter import Reporter
from io import StringIO
from contextlib import redirect_stderr


def rename_variables_in_files(directory, old_variable_name, new_variable_name):
    modified_files = []

    # A dictionary to track renamed variables and their new names
    renamed_variables = {old_variable_name: new_variable_name}

    original_content = {}

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

                # Create a visitor to traverse the AST and rename variables
                class RenameVariables(ast.NodeTransformer):
                    def visit_Assign(self, node):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == old_variable_name:
                                target.id = new_variable_name
                        return node

                    def visit_FunctionDef(self, node):
                        # Exclude function names from renaming
                        if node.name != old_variable_name:
                            self.generic_visit(node)
                        return node

                    def visit_ClassDef(self, node):
                        # Exclude class names from renaming
                        if node.name != old_variable_name:
                            self.generic_visit(node)
                        return node

                    def visit_Name(self, node):
                        if node.id == old_variable_name:
                            col_offset = node.col_offset
                            line_number = node.lineno
                            index = sum(len(line)+1 for i, line in enumerate(
                                content.splitlines()) if i < line_number - 1) + col_offset

                            if len(content) > index+len(node.id):
                                if content[index+len(node.id)] != "(":
                                    # do not rename function calls
                                    node.id = new_variable_name
                            else:
                                node.id = new_variable_name
                        return node

                transformer = RenameVariables()
                new_tree = transformer.visit(tree)

                # Generate the modified code from the AST
                modified_code = ast.unparse(new_tree)

                # Write the modified content back to the file
                with open(file_path, "w") as f:
                    f.write(modified_code)

                # Now, let's handle renaming variable-related imports
                content = modified_code
                modified_content = content.replace(
                    f"import {old_variable_name}", f"import {new_variable_name}")
                modified_content = modified_content.replace(
                    f"from {old_variable_name}", f"from {new_variable_name}")

                # If variable-related imports were modified, write the updated content back to the file
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
    old_name = "new_hello"
    new_name = "new_var"

    modified_files = rename_variables_in_files(
        directory_to_refactor, old_name, new_name)

    # if modified_files:
    #     print("Modified files:")
    #     for file_path in modified_files:
    #         print(file_path)
    # else:
    #     print("No files were modified.")
