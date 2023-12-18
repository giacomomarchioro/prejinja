import re
import json
from pathlib import Path

def getText(srcDirs,
            variableRegexPattern,
            mainLanguage,
            translations,
            variableToText,
            fileFormats):
    """Get the variables in the source template.

    Args:
        srcDirs (str): The path of the source templates.
        variableRegexPattern (str): The RegEx pattern for extracting the variables.
        mainLanguage (str): The main language of the document e.g. 'it'.
        translations (str): A list of languages supported e.g. 'es en de'.
        variableToText (str or bool): If True the variables are converted to text.
        fileFormats (str): A string containing the file formats that need to be
          converted.

    Returns:
        True
    """
    variableToText = variableToText == True
    fileFormats = fileFormats.split()
    translations = translations.split()
    srcFiles = []
    for d in srcDirs:
        srcFiles += [path for i in fileFormats for path in Path(d).rglob("*."+i)]

    def get_expectedCharacter(variableName):
        end = variableName.split("_")[-1]
        return int(end[:-1]) if end[-1] == "c" and end[:-1].isdigit() else None

    translationsList = dict()
    for sourceFile in srcFiles:
        sourceFile = str(sourceFile)
        translationsList[sourceFile] = dict()
        with open(sourceFile) as f:
            #TODO: variables with the same name
            print(sourceFile)
            variables = re.findall(variableRegexPattern, f.read())
            print(variables)
            for ind,variable in enumerate(variables):
                varSourceFile = {
                "order": ind,
                "description":"This is a description",
                "character_number":get_expectedCharacter(variable),
                "texts":{}
                }
                text = ""
                if variableToText:
                    end = -1 if get_expectedCharacter(variable) else None
                    text = " ".join(variable.split("_")[1:end])

                varSourceFile['texts'][mainLanguage] = {
                        "type" : "original",
                        "author": "",
                        "comment": "",
                        "text": text
                    }
                for translation in translations:
                    translationTxt =   {
                        "type" : "translation",
                        "translator":"",
                        "comment": "",
                        "text": ""
                    }
                    varSourceFile['texts'][translation] = translationTxt
                translationsList[sourceFile][variable] = varSourceFile

    # we check if we have already a translations file and we update it
    translationsFile = Path('translations.po.json')
    if translationsFile.is_file():
        with open('translations.po.json', 'r') as orig:
            previousTranslations = json.load(orig)
        for page in translationsList:
            # if we already scanned the page we update any new variable
            if page in previousTranslations:
                # we check if we have unused variables
                for previousVariable in previousTranslations[page]:
                    if previousVariable not in translationsList[page]:
                        previousTranslations[page][previousVariable]['unused'] = True
                # we check if we have new variables
                for variable in translationsList[page]:
                    if variable not in previousTranslations[page]:
                        previousTranslations[page][variable] = translationsList[page][variable]
            else:
                previousTranslations[page] = translationsList[page]
        # translationsList will be the updated previousTranslations
        translationsList = previousTranslations

    with open('translations.po.json', 'w') as fp:
        json.dump(translationsList, fp, indent=3)
    return True