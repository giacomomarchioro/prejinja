import argparse
from .getvariablestext import getText
import os
import configparser
from . import defaultConfig


def preJinjaGet():
    description = """
    This is the command line interface of prejinja.

    prejinjaget extract all the variables from the selected files in the folders
    and write a `translations.po.json` file in the same folder.
    A `prejinja.ini`file is also written and can be used to configure the process.

    """
    userConfigParser = configparser.ConfigParser()
    if os.path.isfile("prejinja.ini"):
        userConfigParser.read("prejinja.ini")
    else:
        userConfigParser.read_dict(defaultConfig.dc)
        with open('prejinja.ini', 'w') as configFile:
            userConfigParser.write(configFile)

    parser = argparse.ArgumentParser(description=description)
    srcDirs = [i[0] for i in userConfigParser.items('FoldersMapping')]
    parser.add_argument('--srcdir',
                        required=False,
                        nargs="+",
                        default=srcDirs,
                        help="List of dirs to scan e.g. --scandir srctempalte srcstatic")

    parser.add_argument('--variableregexpattern',
                        required=False,
                        default=userConfigParser['General']['variableregexpattern'],
                        help="RegEx pattern to be used for extracting the variables.")

    parser.add_argument('--mainlanguage',
                        required=False,
                        default=userConfigParser['General']['mainlanguage'],
                        help="The main language used.")

    parser.add_argument('--translations',
                        required=False,
                        default=userConfigParser['General']['translations'],
                        help="The target translations languages.")

    parser.add_argument('--variabletotext',
                    action='store_true',
                    required=False,
                    default=userConfigParser['General']['variabletotext'],
                    help="Writes the variable name in the text.")

    parser.add_argument('--fileformats',
                    required=False,
                    default=userConfigParser['General']['fileformats'],
                    help="File formats that will be analyzed for variables.")

    args = parser.parse_args()
    print(args)
    getText(srcDirs=args.srcdir,
            variableRegexPattern=args.variableregexpattern,
            mainLanguage=args.mainlanguage,
            translations=args.translations,
            variableToText=args.variabletotext,
            fileFormats=args.fileformats)

if __name__ == '__main__':
    preJinjaGet()
