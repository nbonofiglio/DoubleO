import os
from google.genai import types

def write_file(working_directory, file_path, content):

    try: 
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        if (not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs):
            return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"

        if (os.path.isdir(target_file)):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as err:
        return f"Error: {err}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Provides ability to create and write new files, as well as modify existing files, anywhere within the scope of the project",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to file to which is being written, relative to the working directory (default is the working directory itself)",
            ),
             "content": types.Schema(
                type=types.Type.STRING,
                description="String containing text to be written to the desired file",
            ),   
        },
        required = ["file_path", "content"]
    ),
)