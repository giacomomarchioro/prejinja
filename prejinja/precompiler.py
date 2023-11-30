from jinja2 import FileSystemLoader
import jinja2
from pathlib import Path
import json
from .flagsAndLanguages import languagesFlags,languagesNames

def precompile(srcDirs,
                distDirs,
                translations,
                mainLanguage,
                loreIpsum,
                fileFormats,
                lipsum,
                block_start_string,
                block_end_string,
                variable_start_string,
                variable_end_string):

    def circularLoreIpsum():
        while True:
            for letter in loreIpsum:
                yield letter

    def getDummyText(numberOfLetters,variableName):
        splitted = variableName.split("_")
        end = splitted[-1]
        if end[-1] == "c" and end[:-1].isdigit():
            splitted = splitted[1:-1]
        else:
            splitted = splitted[1:]
        text = " ".join(splitted)
        text += " "
        if isinstance(numberOfLetters,int):
            numberOfLetters -= len(text)
            loreIpsumTxt = circularLoreIpsum()
            text +=  "".join([next(loreIpsumTxt) for i in range(int(numberOfLetters))])
        return text

    # https://stackoverflow.com/a/76312593/2132157
    class NameTrackingEnvironment(jinja2.Environment):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.templatesUsed = []

        def get_template(self, name, parent=None, globals=None):
            self.templatesUsed.append(name)
            return super().get_template(name, parent, globals)

    # we convert to list
    fileFormats = fileFormats.split()
    translations = translations.split()
    translations.append(mainLanguage)
    # get all the HTML templates in the srcTemplateDir
    srcFiles = []
    for d in srcDirs:
        srcFiles += [path for i in fileFormats for path in Path(d).rglob("*."+i)]

    foldersMap = dict(zip(srcDirs, distDirs))

    with open('translations.po.json') as f:
        data = json.load(f)

    if lipsum:
        translations.append("xx")
    # for each template generate a new template for each language with the
    # translation from the translations file
    for template in srcFiles:
        for lang in translations:
            # we have to define a new environment for every language so we can
            # store the linked templates.
            environment = NameTrackingEnvironment(
                loader=FileSystemLoader(""),
                trim_blocks=True,
                block_start_string=block_start_string,
                block_end_string=block_end_string,
                variable_start_string=variable_start_string,
                variable_end_string=variable_end_string,
                undefined=jinja2.StrictUndefined
            )
            jinja2Template = environment.get_template(str(template))
            parts = list(template.parts[1:-1])
            parts.insert(0, foldersMap[template.parts[0]])
            parts.append("-".join((lang,template.parts[-1])))
            newPath = Path(*parts)
            newPath.parent.mkdir(parents=True, exist_ok=True)
            templateVars = data[str(template)]
            # we get the text for the language
            if lang == "xx":
                txt = {i:getDummyText(templateVars[i]['character_number'],i) for i in templateVars}
            else:
                txt = {i: templateVars[i]['texts'][lang]['text'] for i in templateVars}
            # the variables will always have a LANG constant with the current language
            txt["_LANG"] = lang
            otherLanguages = translations[:]
            otherLanguages.remove(lang)
            txt["_OTHERLANGUAGES"] = otherLanguages
            txt["_LANGUAGESNAMES"] = languagesNames
            txt["_LANGUAGESFLAGS"] = languagesFlags
            try:
                content = jinja2Template.render(**txt)
            # in the case the template is using other templates
            except jinja2.UndefinedError as e:
                for templateUsed in environment.templatesUsed:
                    #TODO: check if better to add ./ in get variable
                    if templateUsed.startswith("./"):
                        templateUsed = templateUsed[2:]
                        print(templateUsed)
                        externalTemplateVars = data[str(templateUsed)]
                        for i in externalTemplateVars:
                            if i in  txt:
                                raise ValueError(f"Variable {i} of {templateUsed} already defined in {template}")
                            if lang == "xx":
                                txt[i] = getDummyText(externalTemplateVars[i]['character_number'],i)
                                print("LORE")
                            else:
                                txt[i] = externalTemplateVars[i]['texts'][lang]['text']

                content = jinja2Template.render(**txt)
            with open(newPath, "w") as f:
                f.write(content)

#TODO: test if the output template are modified before overwriting