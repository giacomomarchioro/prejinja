# prejinja
A Jinja2 alternative to Babel and a Jinja2 preprocessor.

Prejinja is a Jinja2 preprocessor that extracts static variables to a JSON file that is used for translating the website into different languages.

## Installation

```
pip install git+https://github.com/giacomomarchioro/prejinja
```

## How it works?
Prejinja preprocess special jinja2 templates for each language and allows you to use standard jinja2 to be processes "on the fly".
A working example is shown in the example folder of this repository.
1. `srctempaltes` folder contains the jinja2 source templates. However, all the translatable text is assigned to variables.
2. For each text the user create a variable between `[=` and `=]` tags (e.g. `[= p_website_description_50c =]` ).
3. You can add some logic to be pre-processed using `[.` and  `.]` tags.
4. Standard Jinja2 logic can be added and will not conflict with prejinja, however might be wise to pre-process much of the template.
5. Using `prejinjaget` command the variables will be mapped into a `translations.po.json` file.
6. Once the content has been written and translated in the `translations.po.json`, `prejinjaput` command preprocess the templates and save the results in the `templates` dir. (you can also use `prejinjaput --lipsum` to see a preview with loreipsum text.)

Prejinja will create a file for each language and use a prefix to identify the file (e.g. `en-index.html`, `de-index.html`).
At this point you can return the correct language translation based on the current locale.

## On the templates
There are some built-in variables in the pre-jinja2 context:
`_LANG` : the current language tag of the page e.g. `en`.
`_OTHERLANGUAGES` : a list of other language supported by the website (e.g. `["es","de"]`).
`_LANGUAGESNAMES` : dictionary containing the language name `_LANGUAGESNAMES["en"] = "english"`.
`_LANGUAGESFLAGS` : a dictionary containing the flag emoticon `_LANGUAGESFLAGS["en"] = "🇬🇧"`.

A `source template` might look something like this:

```
[. extends './srctemplates/includes/layout.html' .]
[. block  head .]
[. endblock  head .]
[. block  body .]
<h1> [= h1_Second_Page_8c =] </h1>
<p> [= p_secondpage_description_50c =] </p>
<h1> [= h1_How_it_works_20c =] </h1>
<p> [= p_prejinja_compile_60c =] </p>
<h1> [= h1_a_test_with_format =]</h1>
<p> {{"[= format_test =]"|format(3)}} </p>
[. endblock  body .]
```

## A typical Flask application
A Flask application could look like this:

```python
from flask import Flask, render_template, request, redirect, url_for,abort

app = Flask(__name__)
supported_languages = ["en", "es", "it"]

@app.route('/')
def localeRedirect():
   lang = request.accept_languages.best_match(supported_languages)
   return redirect(url_for('indexPage', lang=lang))

# OPTION 1: single endpoint for multiple languages
@app.route('/<lang>/test')
def indexPage(lang):
   if lang not in supported_languages:abort(404)
   # use {{ url_for('indexPage', lang='[= _LANG =]' }} in the source template
   return render_template(f"{lang}-index.html")

# OPTION 2: multiple endpoints can be used for translating also the URLs
@app.route('/en/apple',endpoint="en_secondPage")
@app.route('/es/manzana',endpoint="es_secondPage")
@app.route('/it/mela',endpoint="it_secondPage")
#@app.route('/xx/lorem',endpoint="xx_secondPage") # LoreIpsum
def secondPage():
    # use {{ url_for('[= _LANG =]_secondPage'}} in the source template
    # OR translate the URLs directly [= URL_mela =] and don't use `url_for`
    lang = request.path.split("/")[1]
    return render_template(f"{lang}-endpointstest.html")

if __name__  == '__main__':
	app.run(debug=True)
```

### Single endpoint
The easiest option is to not translating the URLs (e.g. `en/index` translated to `it/index`) like in OPTION 1 of the example. However, it is a good practice to translate also the URLs to add meaning to the URL itself also when translated.

### Multiple endpoints
If you want also the URLs to be translated (e.g. `en/index` translated to `it/indice`) you have to define multiple endpoints as shown in OPTION 2 of the example (see examples folders for a working example).
The process will be a little more complicated.

Here we provide the components for the two cases:

### Herflang

#### Single endpoint

```html
[. for _otherlang in _OTHERLANGUAGES .]
<link rel="alternate" hreflang="[= _otherlang =]" href="{{ url_for(request.endpoint, lang='[= _otherlang =]', _external=true) }}" />
[. endfor .]
```
#### Multiple endpoints

```html
<html lang="[= _LANG =]" xml:lang="[= _LANG =]" xmlns="http://www.w3.org/1999/xhtml">
[. for _otherlang in _OTHERLANGUAGES .]
<link rel="alternate" hreflang="[= _otherlang =]" href="{{ url_for(request.endpoint.replace('[= _LANG =]','[= _otherlang =]',1))}}" />
[. endfor .]
```

### Language picker

#### Single endpoint
```html
  <div class="dropdown">
    <button class="dropbtn">[= _LANGUAGESFLAGS[_LANG] =]
      <i class="fa fa-caret-down"></i>
    </button>
    <div class="dropdown-content">
      [. for _otherlang in _OTHERLANGUAGES .]
      <a class="dropdown-item" onclick="location.replace(window.location.href.replace('[= _LANG =]', '[= _otherlang =]'))">[= _LANGUAGESFLAGS[_otherlang] =][= _LANGUAGESNAMES[_otherlang] =]</a>
      [. endfor .]
    </div>
  </div>
```

#### Multiple endpoints
```html
  <div class="dropdown">
    <button class="dropbtn">[= _LANGUAGESFLAGS[_LANG] =]
      <i class="fa fa-caret-down"></i>
    </button>
    <div class="dropdown-content">
      [. for _otherlang in _OTHERLANGUAGES .]
      <a class="dropdown-item" href={{ url_for(request.endpoint.replace("[= _LANG =]","[= _otherlang =]",1))}}>[= _LANGUAGESFLAGS[_otherlang] =][= _LANGUAGESNAMES[_otherlang] =]</a>
      [. endfor .]
    </div>
  </div>
```

## Plurals
Plurals are handled by Jinja:

```
{% if number == 1 %}
  [= p_one_user_logged_in_10c =]
{% elif number > 1 %}
  "[= p_n_users_logged_ind_10c =]"|format(number)
{% else %}
  [= p_no_user_logged_in_10c =]
{% endif %}
```

## The benefits
The goal to this package is to separate the layout from the content. In this way it is possible for the WEB developer to create a draft of the layout based on the user needs and leave the copywriter and the translators to work on a separate `.json` file.

## Similar packages
[Flask-Babel](https://python-babel.github.io/flask-babel/#)

