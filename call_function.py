from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
)
"""
For each declaration, you'll need to update at minimum the name and description of the function, as well as the key and description of each item in parameters.properties.
If any function arguments are required, it's a good idea to put them in a required list under parameters. For example, the declaration for get_file_content would have required=["file_path"].
If a function accepts more than one argument from the LLM caller, the declaration will have multiple items in parameters.properties. For example, the declaration for write_file should include both file_path and content.
Pay attention to the type of each parameter. Most of them will be types.Type.STRING, but the optional args parameter of run_python_file should be types.Type.ARRAY – which then has items that are types.Type.STRING. Yes, this can get pretty nested!
"""