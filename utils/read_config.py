import ast
import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


###############################################################################
###############################################################################
###############################################################################


def initialize_config(config_file_path):

    '''
    Used to read a config file and return the ConfigParser variable
    Parameters:
        config_file_path (str): Path to the config file for the ConfigParser
                                object to read
    Returns:
        conf (ConfigParser): ConfigParser object to be used to read the config
                                file at config_file_path
    '''

    conf = configparser.ConfigParser()
    config_file = os.path.join(config_file_path)
    conf.read(config_file)

    return conf


def get_variable(conf, config_variable, variable_type, config_section='all', **kwargs):

    '''
    Finds a config file variable and uses the variable_type to return it as the correct type
    Parameters:
        Required:
            conf (ConfigParser): A ConfigParser variable that will be used to read
                                    the config files. Can be found by passing config
                                    file path into initialize_config() function
            config_variable (str): The variable that should be found from the config file
            variable_type (str): A string representing what the expected return variable type
                                    should be. Supports str, list, dict
        Optional:
            config_section (str): The section under which to search for the config_variable
        kwargs:
            list_seperator (str): Will be used if variable_type is a list to seperate the string
                                    returned by the config parser into a list
    Returns:
        found_config_variable (variable_type): The variable that was found in the config file with
                                                the specified variable_type as its type
    '''

    found_config_variable = conf.get(config_section, config_variable)

    if variable_type == 'str':

        assert isinstance(found_config_variable, str), 'variable is not able a str... please check your variable_type'

    elif variable_type == 'list':

        list_seperator = kwargs.get('list_seperator')

        found_config_variable = found_config_variable.split(list_seperator)

        assert isinstance(found_config_variable, list), 'variable is not able a list... please check your variable_type'

    elif variable_type == 'dict':

        found_config_variable = ast.literal_eval(found_config_variable)

        assert isinstance(found_config_variable, dict), 'variable is not able a dict... please check your variable_type'

    else:
        raise ValueError('variable_type is invalid')

    return found_config_variable
