#  https://www.lfd.uci.edu/~gohlke/pythonlibs/#cx_freeze

import cx_Freeze, os, shutil

executables = [cx_Freeze.Executable("game.py")]

cx_Freeze.setup(
    name="ColorLines Python", 
    options={"build_exe":{"packages":["pygame","time","math","sys","random"],
                          "include_files":["Square.png"],
                          "excludes": ["numpy", "test", "email", "pydoc_data"],
                          "optimize": 2}}, 
    executables = executables)


# Removing unused modules
output_folder = os.path.abspath(os.path.dirname(__file__)) + '\\build\\exe.win-amd64-3.7\\'

print (output_folder)
to_remove = ['lib\\pygame\\examples', 'lib\\pygame\\tests', 'lib\\pygame\\docs']
 
 
for path in to_remove:
    print('Removing directory: ' + output_folder + path)
    shutil.rmtree(output_folder + path)
