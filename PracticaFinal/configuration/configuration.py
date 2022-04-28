from configparser import ConfigParser
from typing import Any

class ParameterNotFoundError(Exception):
    """ The parameter indicated could not be found at the config.ini file. """

class Configuration:
    """ Controller class for configuration data access."""

    def __init__(self, config_file_path: str) -> None:
        # Saves the config path
        self.CONFIG_PATH = config_file_path
        # Creates the configParser
        self._cp = ConfigParser()
        # Saves the configuration data in the cache
        self._cp.read(config_file_path)

    def set_config_param(self, section: str, param_key: str, param_value: Any) -> None:
        """ Sets the parameter in the section at the configuration file path specified. """
        try:
            try:
                # Sets the new parameter in the existing section
                self._cp[section][param_key] = param_value
            except KeyError:
                # Creates a new section with the new parameter
                self._cp[section] = {param_key: param_value}
            # Saves parameters in configuration file
            with open(self.CONFIG_PATH, 'w') as config_file:
                self._cp.write(config_file)
        except:
            # Something went wrong
            print("[Configuration]:  Something went wrong while saving the configuration!")

    def get_config_param(self, section: str, param: str) -> str:
        """ Gets the parameter in the section at the configuration file path specified. """
        try:
            # Returns the parameter value 
            param_value = self._cp[section].get(param)
            if param_value is not None:
                # Returns the parameter read
                return param_value
            else:
                raise ParameterNotFoundError(section, param)
        except KeyError:
            print(f"[Error] No such section {section}")        
        except ParameterNotFoundError:
            print(f"[Error] Parameter {param} could not be found in Section{section}!")