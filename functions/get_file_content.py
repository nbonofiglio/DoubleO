import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try: 
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        if (not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs):
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
        
        if (not os.path.isfile(target_file)):
            return f"Error: File not found or is not a regular file: \"{file_path}\""
        
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string
    
    except Exception as err:
        return f"Error: {err}"

"""


Tips
os.path.abspath(): Get an absolute path from a relative path
os.path.join(): Join two paths together safely (handles slashes)
os.path.normpath(): Normalize a path (handles things like ..)
os.path.commonpath(): Get the common sub-path shared by multiple paths
os.path.isfile(): Check if a path points to an existing regular file
open(): Open a file for reading or writing
.read(): Read a text file to a string, optionally specifying a maximum number of characters
Example of reading up to a certain number of characters from a text file:

MAX_CHARS = 10000

with open(file_path, "r") as f:
    file_content_string = f.read(MAX_CHARS)

The with statement automatically closes the file for us when the block finishes.
"""