from jinja2 import FileSystemLoader
import jinja2
from pathlib import Path
import json
from .flagsAndLanguages import languagesFlags,languagesNames
from .simplemarkdown import simpleMarkdown
import html
import re

def extractLinks(logicRegexPattern,templateName):
    statements = ['extends','import','include','from']
    externalTemplates = []
    def getLinks(logicRegexPattern,templateName):
        with open(templateName,"r") as f:
            logicsBlocks = re.findall(logicRegexPattern, f.read())
            for lb in logicsBlocks:
                lbs = lb.strip().split()
                if lbs[0] in statements:
                    if lbs[1].startswith('['):
                        raise NotImplementedError("Sorry multiple includes are not supported yet!")
                    else:
                        detectedLink = lbs[1].replace("'","").replace('"',"")
                        # This avoid circular imports:
                        if detectedLink not in externalTemplates:
                            getLinks(logicRegexPattern,detectedLink)
                        externalTemplates.append(detectedLink)
    getLinks(logicRegexPattern,templateName)
    return externalTemplates



def preprocess(srcDirs,
                distDirs,
                translations,
                mainLanguage,
                loreIpsum,
                fileFormats,
                lipsum,
                block_start_string,
                block_end_string,
                variable_start_string,
                variable_end_string,
                autoescape,
                markdown,
                sanitize):

    if markdown == "subset":
        if sanitize and not autoescape:
            print("Santizing")
            def md(text):
                sanText = html.escape(text)
                return simpleMarkdown(sanText)
        else:
            md = simpleMarkdown

    elif markdown == "fullmarkdown":
        import markdown
        md = markdown.markdown
    else:
        def md(text):return text

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
    # did not prove effective for multiple imports
    # class NameTrackingEnvironment(jinja2.Environment):
    #     def __init__(self, **kwargs):
    #         super().__init__(**kwargs)
    #         self.templatesUsed = []

    #     def get_template(self, name, parent=None, globals=None):
    #         self.templatesUsed.append(name)
    #         return super().get_template(name, parent, globals)

    # we convert to list
    fileFormats = fileFormats.split()
    translations = translations.split()
    translations.append(mainLanguage)
    # get all the HTML templates in the srcTemplateDir
    srcFiles = []
    for d in srcDirs:
        srcFiles += [path for i in fileFormats for path in Path(d).rglob("*."+i)]

    foldersMap = dict(zip(srcDirs, distDirs))
    # load the translations from the json file.
    with open('translations.po.json') as f:
        data = json.load(f)

    if lipsum:
        translations.append("xx")
    # for each template generate a new template for each language with the
    # translation from the translations file
    for template in srcFiles:
        print("Wokring with %s" %template)
        for lang in translations:
            # we have to define a new environment for every language so we can
            # store the linked templates.
            print(autoescape)
            environment = jinja2.Environment(
                loader=FileSystemLoader(""),
                trim_blocks=True,
                autoescape=autoescape,
                block_start_string=block_start_string,
                block_end_string=block_end_string,
                variable_start_string=variable_start_string,
                variable_end_string=variable_end_string,
                undefined=jinja2.StrictUndefined,
            )
            jinja2Template = environment.get_template(str(template))
            parts = list(template.parts[1:-1])
            parts.insert(0, foldersMap[template.parts[0]])
            parts.append("-".join((lang,template.parts[-1])))
            newPath = Path(*parts)
            newPath.parent.mkdir(parents=True, exist_ok=True)

            try:
                templateVars = data[str(template)]
            except KeyError as e:
                #e.add_note('The template was not found use ')
                s = f'Template {template} not found. Did you use prejinjaget?'
                raise KeyError(s)

            def inUse(templateVars,i,lang):
                """Return true if the variable is in USE and not UNUSED.

                If the user delete some variables from the includes files, these
                are not deleted in the translations. Prejinja check for any
                conflicting variables names so we have to remove the unused
                variables.

                Args:
                    templateVars (list): The variables of the tempalte
                    i (str): The variable name.
                    lang (str): The language.

                Returns:
                    bool: True if the variable is in use.
                """
                return not templateVars[i]['texts'][lang].get('unused')
            # we get the text for the language
            if lang == "xx":
                txt = {i:getDummyText(templateVars[i]['character_number'],i) for i in templateVars}
            else:
                txt = {i: md(templateVars[i]['texts'][lang]['text']) for i in templateVars if inUse(templateVars,i,lang)}
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
                templatesUsed = extractLinks(r"\[.\s(?!_)(.*?)\s.\]",
                                             template)
                for templateUsed in templatesUsed:
                    print("Now adding: %s" %templateUsed)
                    #TODO: check if better to add ./ in get variable
                    # here I check each template if I can find the template.
                    if templateUsed.startswith("./"): # only the other templates
                        templateUsed = templateUsed[2:]
                        print(templateUsed)
                        externalTemplateVars = data[str(templateUsed)]
                        for i in externalTemplateVars:
                            if i in txt and not externalTemplateVars[i].get('unused'):
                                raise ValueError(f"Variable {i} of {templateUsed} already defined in {template}")
                            if lang == "xx":
                                txt[i] = getDummyText(externalTemplateVars[i]['character_number'],i)
                            else:
                                txt[i] = md(externalTemplateVars[i]['texts'][lang]['text'])
                    else:
                        print("Skipped %s" %templateUsed)
                try:
                    content = jinja2Template.render(**txt)
                except jinja2.exceptions.UndefinedError as e:
                    s = f'There was a missing variable. Did you use prejinjaget?'
                    raise KeyError(s)
            with open(newPath, "w") as f:
                f.write(content)

#TODO: test if the output template are modified before overwriting