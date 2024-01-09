from flask import Flask, render_template, request, redirect, url_for,abort

app = Flask(__name__)
supported_languages = ["en", "es", "it"]

@app.route('/')
def localeRedirect():
   lang = request.accept_languages.best_match(supported_languages)
   return redirect(url_for('indexPage', lang=lang))

# single endpoint
@app.route('/<lang>/test')
def indexPage(lang):
   if lang not in supported_languages:abort(404)
   # use {{ url_for('indexPage', lang=[= _LANG =] }} in the source template
   return render_template(f"{lang}-index.html")

# multiple endpoints can be used for translating also the URLs
@app.route('/<lang>/secondpage')
def secondPageFunctionName(lang):
    if lang not in supported_languages:abort(404)
    return render_template(f"{lang}-secondpage.html")

if __name__  == '__main__':
	app.run(debug=True)