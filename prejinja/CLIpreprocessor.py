import argparse
from .preprocessor import preprocess
import os
import configparser
from . import defaultConfig
def preJinjaPut():
    description = """
    This is the command line interface of prejinja.

    prejinjaput creates for each `translation` and for the `mainlanguage` a
    copy of the file translated using the mapping in `translations.po.json`

    """
    userConfigParser = configparser.ConfigParser()
    if os.path.isfile("prejinja.ini"):
        userConfigParser.read("prejinja.ini")
    else:
        userConfigParser.read_dict(defaultConfig.dc)
        with open('prejinja.ini', 'w') as configFile:
            userConfigParser.write(configFile)

    parser = argparse.ArgumentParser(description=description)
    srcDirs, distDirs = zip(*userConfigParser.items('FoldersMapping'))

    parser.add_argument('--srcdirs',
                        required=False,
                        nargs="+",
                        default=srcDirs,
                        help="List of dirs to scan e.g. --scandir srctempalte srcstatic")

    parser.add_argument('--distdirs',
                        required=False,
                        nargs="+",
                        default=distDirs,
                        help="Corrispettive  list of dirs.")

    parser.add_argument('--translations',
                        required=False,
                        default=userConfigParser['General']['translations'],
                        help="The target translations languages.")

    parser.add_argument('--mainlanguage',
                        required=False,
                        default=userConfigParser['General']['mainlanguage'],
                        help="The main language used")

    parser.add_argument('--loreipsum',
                        required=False,
                        default=userConfigParser['General']['loreipsum'],
                        help="The text to be used as loreipsum")

    parser.add_argument('--fileformats',
                    required=False,
                    default=userConfigParser['General']['fileformats'],
                    help="File formats that will be analyzed for variables.")

    parser.add_argument('--lipsum',
                        action='store_true',
                        required=False,
                        default=userConfigParser['General']['lipsum'],
                        help="Output the loreipsum for each variable.")

    parser.add_argument('--block_start_string',
                    required=False,
                    default=userConfigParser['General']['block_start_string'],
                    help="The Jinja2 block start string.")

    parser.add_argument('--block_end_string',
                    required=False,
                    default=userConfigParser['General']['block_end_string'],
                    help="The Jinja2 block end string.")

    parser.add_argument('--variable_start_string',
                    required=False,
                    default=userConfigParser['General']['variable_start_string'],
                    help="The Jinja2 variable start string.")

    parser.add_argument('--variable_end_string',
                    required=False,
                    default=userConfigParser['General']['variable_end_string'],
                    help="The Jinja2 variable end string.")
    
    parser.add_argument('--autoescape',
                    action='store_true',
                    required=False,
                    default=userConfigParser['General']['autoescape'],
                    help="Autoescape al the html tags.")

    parser.add_argument('--markdown',
                    required=False,
                    default=userConfigParser['General']['markdown'],
                    help="Set the markdown.")

    parser.add_argument('--sanitize',
                action='store_true',
                required=False,
                default=userConfigParser['General']['sanitize'],
                help="Sanitize string before markdown.")


    args = parser.parse_args()
    print(args)
    autoescape = args.autoescape == "True"
    sanitize = args.sanitize == "True"
    lipsum = args.lipsum == "True"
    preprocess(srcDirs=args.srcdirs,
                distDirs=args.distdirs,
                translations=args.translations,
                mainLanguage=args.mainlanguage,
                loreIpsum=args.loreipsum,
                fileFormats=args.fileformats,
                lipsum=lipsum,
                block_start_string=args.block_start_string,
                block_end_string=args.block_end_string,
                variable_start_string=args.variable_start_string,
                variable_end_string=args.variable_end_string,
                autoescape= autoescape,
                markdown=args.markdown,
                sanitize=sanitize)

if __name__ == '__main__':
    preJinjaPut()
