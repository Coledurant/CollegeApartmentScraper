import os
import pandas as pd
from functools import reduce

from definitions import *

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

def add_excel_sheet(excel_path, sheet_name, writer):

    '''
    Will read the excel file and create a new sheet inside of the main excel
    file with the title of 'College Name (state abbreviation)'

    Parameters:
        excel_path (os.path): The path to the excel file to read
        sheet_name (str): A string for what the sheet in the main excel file
                            will be named
        writer (ExcelWriter): The ExcelWriter object to be used
    Returns:
        ---
    '''

    frame = pd.read_excel(excel_path, index_col = 1)

    frame.to_excel(writer, sheet_name)





if __name__ == '__main__':

    print('\nWriting all files in the /Excel directory to their own sheet in apartment_information.xlsx...\n')

    walk_dict = get_directory_structure(EXCEL_DIR).get('Excels')

    writer=pd.ExcelWriter("apartment_information.xlsx")


    try:

        for state_abbreviation, dict_college_excel_files in walk_dict.items():

            state_excel_path = os.path.join(EXCEL_DIR, state_abbreviation)

            # Dict of excel file name : None because there will only be excel files here,
            # and no folders
            for excel_name,_ in dict_college_excel_files.items():

                excel_path = os.path.join(state_excel_path, excel_name)

                sheet_name = excel_name.replace('.xlsx', '') + ' ({0})'.format(state_abbreviation)

                add_excel_sheet(excel_path = excel_path, sheet_name = sheet_name, writer = writer)

        os.chdir(EXCEL_DIR)

        writer.save()

        os.chdir(ROOT_DIR)

    except AttributeError as e:

        LOGGER.error(e)
        LOGGER.debug('Make sure there is an /Excels folder and that it is populated')
