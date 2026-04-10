import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):

    try: 
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        if (not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs):
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"

        if (not os.path.isfile(target_file)):
            return f"Error: \"{file_path}\" does not exist or is not a regular file"
        
        if (not target_file.endswith(".py")):
            return f"Error: \"{file_path}\" is not a Python file"
        
        commands = ["python", target_file]
        if args:
            commands.extend(args)

        completed_process = subprocess.run(commands, capture_output=True, text=True, timeout=30)

        if (completed_process.returncode != 0):
            return f"Process exited with code {completed_process.returncode}"
        
        if (not completed_process.stdout and not completed_process.stderr):
            return "No output produced"
        
        return f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"

    
    except Exception as err:
        return f"Error: {err}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file accessible within the project scope",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the file that contains the function to be run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Array of strings containing optional arguments (Default is set to None)",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="String for optional argument"
                )
            )
        },
        required = ["file_path"]
    ),
)