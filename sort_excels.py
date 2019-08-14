import os
import pprint

def get_directory_structure(rootdir = os.getcwd()):
    """
    Creates a nested dictionary that represents the folder structure of rootdir.
    Defaults to walking the directory that it is called in

    Parameters:
        rootdir (os.Path): The path at which the function should start mapping.
                            Defaults to os.getcwd()
    Returns:
        dir (dict): A nested dict of all found directories
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir

walk_dict = get_directory_structure(os.path.join(os.getcwd(), 'Excels'))

pp = pprint.PrettyPrinter(indent=4)

pp.pprint(walk_dict)



# walk_dict should be a dict of state, list of college excel files

print('\n\n\n\n')

for state, list_college_excel_files in walk_dict.items():

    print(state)