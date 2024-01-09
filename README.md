# prejinja
A Jinja2 alternative to Babel and a Jinja2 preprocessor.

Prejinja is a Jinja2 preprocessor that extracts static variables to a JSON file that is used for translating the website into different languages.

## Installation

```
pip install git+https://github.com/giacomomarchioro/prejinja
```

## How it works?
A working example is shown in the example folder of this repository.
1. `srctempaltes` folder contains the jinja2 source templates. However, all the translatable text is assigned to variables.
2. For each text the user create a variable between `[=` and `=]` tags (e.g. `[= p_website_description_50c =]` ).
3. Standard Jinja2 logic can be added and will not conflict with prejinja, however might be wise to pre-process much of the template.
4. Using `prejinjaget` command the variables will be mapped into a `translations.po.json` file.
5. Once the content has been written and translated in the `translations.po.json`, `prejinjaput` command preprocess the templates and save the results in the `templates` dir. (you can also use `prejinjaput --lipsum` to see a preview with loreipsum text.)

Prejinja will create a file for each language and use a prefix to identify the file (e.g. `en-index.html`, `de-index.html`).
At this point you can return the correct language translation based on the current locale.

```python
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
supported_languages = ["en", "nl", "it"]

@app.route('/')
def localeRedirect():
   lang = request.accept_languages.best_match(supported_languages)
   return redirect(url_for('indexPage', lang=lang))

@app.route('/<lang>/test')
def indexPage(lang):
   return render_template(f"{lang}-index.html")

@app.route('/<lang>/teststatictemplate')
def testStaticTemplate(lang):
   return send_from_directory('templates',f"{lang}-index.html")

if __name__  == '__main__':
	app.run(debug=True)
```

## The benefits
The goal to this package is to separate the layout from the content. In this way it is possible for the WEB developer to create a draft of the layout based on the user needs and leave the copywriter and the translators to work on a separate `.json` file.

## Similar packages
[Flask-Babel](https://python-babel.github.io/flask-babel/#)

