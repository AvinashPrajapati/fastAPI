import configparser


def config(filename="database.ini", section="postgresql"):

    config = configparser.ConfigParser()
    x = config.read(filename)
    db = {}
    if config.has_section(section):
        params = config.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db
