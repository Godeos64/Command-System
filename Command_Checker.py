import os
import importlib

# config
command_directory = "Commands"

# This will store { "prefix": module_object }
# e.g., { "search": <module Search> }
loaded_commands = {}

def load_commands():
    """Loads all commands from the directory into memory."""
    # Failsafe: Create directory if missing
    if not os.path.exists(command_directory):
        print("Commands directory not found. Creating...")
        os.mkdir(command_directory)

    # Clear existing commands (for reloading)
    loaded_commands.clear()

    for filename in os.listdir(command_directory):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3] # Remove .py
            
            # Construct path: e.g., "Commands.Search"
            module_path = f"{command_directory}.{module_name}"
            
            try:
                # Dynamically import the module
                module = importlib.import_module(module_path)
                
                # Check if it has a PREFIX and add to our dictionary
                if hasattr(module, "PREFIX"):
                    prefix = module.PREFIX
                    loaded_commands[prefix] = module
                    print(f"Loaded command: {prefix}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

def execute_command(parsed_request):
    """Finds the correct command based on prefix and runs it."""
    if not parsed_request:
        return None

    prefix = parsed_request[0].lower()
    args = parsed_request[1:]

    # Check if we have a module loaded for this prefix
    if prefix in loaded_commands:
        module = loaded_commands[prefix]
        
        # Standardize: All command files must have an 'execute' function
        if hasattr(module, "execute"):
            print(f"Executing command: {prefix}")
            return module.execute(args)
        else:
            print(f"Error: Module for '{prefix}' does not have an 'execute' function.")
    
    return None