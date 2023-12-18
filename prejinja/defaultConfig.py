# Default configuration
dc = {
    "General": {
        "mainLanguage": "en",
        "translations": "es it de",
        "fileFormats": "html htm htmx js svg php",
        "variableToText": True,
        "lipsum": False,
        "srcTemplateDir": "srctemplates",
        "outputTemplateDir": "templates",
        "srcStaticDir": "srcstatic",
        "outputStaticDir": "static",
        "loreIpsum": "Lorem ipsum dolor sit amet, consectetur adipisci elit, sed do eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrum exercitationem ullamco laboriosam, nisi ut aliquid ex ea commodi consequatur. Duis aute irure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "block_start_string": "[.",
        "block_end_string": ".]",
        "variable_start_string": "[=",
        "variable_end_string": "=]",
        "variableRegexPattern": "\[=\s(?!_)(.*?)\s=\]",
        "autoescape": False,
        "markdown": "subset",
        "sanitize": True,
    },
    "FoldersMapping":{
        "srctemplates":"templates",
        "srcstatic":"static"
    }
}
