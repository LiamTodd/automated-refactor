def format_python_file(file_path):
    try:
        # Read the content of the file into a string
        with open(file_path, 'r') as file:
            code = file.read()

        # Format the code using autopep8 (or any other formatter you prefer)
        import autopep8
        formatted_code = autopep8.fix_code(code)

        # Write the formatted code back to the file
        with open(file_path, 'w') as file:
            file.write(formatted_code)

        print(f"Formatted '{file_path}' successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Replace 'your_file.py' with the path to your Python file
    file_to_format = './src/rope.py'

    format_python_file(file_to_format)
