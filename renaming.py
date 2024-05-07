import os


def rename_files(input_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            # Extract the number from the input filename
            n = int(filename.split("_")[-1].split(".")[0])

            # Construct the new filename for the output
            new_filename = f"letter_cleaned_{n}.txt"

            # Read the content of the input file
            with open(os.path.join(input_dir, filename), 'r') as file:
                content = file.read()

            # Write the content to the output file with the new name
            with open(os.path.join(output_dir, new_filename), 'w') as file:
                file.write(content)

if __name__ == "__main__":
    # Example usage:
    input_directory = r"C:\Eigene Dateien\Uni\Master\AAA"
    output_directory = "letters/cleaned"
    rename_files(input_directory, output_directory)
