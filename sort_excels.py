import os
import pprint
import pandas as pd

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




#and so on to read different excel

writer=pd.ExcelWriter()




def add_excel(excel_path, sheet_name):

    '''
    Will read the excel file and create a new sheet inside of the main excel
    file with the title of 'College Name (state abbreviation)'

    Parameters:
        excel_path (os.path): The path to the excel file to read
    Returns:
        ---
    '''

    frame = pd.read_excel(excel_path)

    frame.to_excel(writer, sheet_name)


writer.save("apartment_information.xlsx")
