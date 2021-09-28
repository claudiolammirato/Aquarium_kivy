#!/usr/bin/env python3

import configparser

class Aq_Settings:
    def __init__(self):
        pass

    def read_settings(section, parameter):
        config = configparser.ConfigParser()
        config.read('settings.ini')

        x = config[section][parameter]
        return x

    def write_settings(section, parameter, value):

        config = configparser.ConfigParser()
        config.read('settings.ini')
        try:
            config.add_section(section)
        except:
            pass

        config[section][parameter] = value
        
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)




