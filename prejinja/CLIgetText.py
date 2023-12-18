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

    parser = argparse.ArgumentParser(description=description)
    srcDirs = [i[0] for i in userConfigParser.items('FoldersMapping')]
    distDirs = [i[1] for i in userConfigParser.items('FoldersMapping')]

    parser.add_argument('--srcdir',
                        required=False,
                        nargs="+",
                        default=srcDirs,
                        help="List of dirs to scan e.g. --srcdir srctempalte srcstatic")

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

    parser.add_argument('--distdirs',
                    required=False,
                    nargs="+",
                    default=distDirs,
                    help="Corrispettive  list of dirs.")

    pArgs = parser.parse_args()
    translations = pArgs.translations.split()
    if pArgs.mainlanguage in translations:
        translations.remove(pArgs.mainlanguage)
        pArgs.translations = " ".join(translations)

    getText(srcDirs=pArgs.srcdir,
            variableRegexPattern=pArgs.variableregexpattern,
            mainLanguage=pArgs.mainlanguage,
            translations=pArgs.translations,
            variableToText=pArgs.variabletotext,
            fileFormats=pArgs.fileformats)
    if not os.path.isfile("prejinja.ini"):
        with open('prejinja.ini', 'w') as configFile:
            userConfigParser['General']['variableregexpattern'] = pArgs.variableregexpattern
            userConfigParser['General']['mainlanguage'] = pArgs.mainlanguage
            userConfigParser['General']['translations'] = pArgs.translations
            userConfigParser['General']['variabletotext'] = pArgs.variabletotext
            userConfigParser['General']['fileformats'] = pArgs.fileformats
            for srcDir,distDir in zip(srcDirs,distDirs):
                 userConfigParser['FoldersMapping'][srcDir] = distDir
            userConfigParser.write(configFile)

if __name__ == '__main__':
    preJinjaGet()
