from configparser import ConfigParser


def get_config(section, value):
    config = ConfigParser()
    config.read(r'C:\Users\ieshcherba\PycharmProjects\PyTestSwagger\config.ini')
    return config.get(section, value)
