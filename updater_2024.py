# Useful code to share in January 

def update_for_2024(file_path):
    # Check if the file is a Python file
    if not file_path.endswith('.py'):
        print("The file is not a Python (.py) file.")
        return

    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Replace '2023' with '2024'
        updated_content = content.replace('2023', '2024')

        # Create a new file name
        new_file_path = file_path.replace('.py', '_2024.py')

        # Write the updated content to a new file
        with open(new_file_path, 'w') as new_file:
            new_file.write(updated_content)

        print(f"File updated successfully. New file created: {new_file_path}")

    except IOError as e:
        print(f"Error occurred while processing the file: {e}")

# Example usage
file_path = 'example.py'  # Replace with your file path
update_for_2024(file_path)

