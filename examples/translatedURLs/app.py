from flask import Flask, render_template, request, redirect, url_for,abort

app = Flask(__name__)
supported_languages = ["en", "es", "it"]

@app.route('/')
def localeRedirect():
   lang = request.accept_languages.best_match(supported_languages)
   return redirect(url_for(f'{lang}_test'))

@app.route('/en/test',endpoint="en_test")
@app.route('/es/test',endpoint="es_test")
@app.route('/it/test',endpoint="it_test")
def indexPage():
   lang = request.path.split("/")[1]
   # use {{ url_for('indexPage', lang=[= _LANG =] }} in the source template
   return render_template(f"{lang}-index.html")

@app.route('/en/secondpage',endpoint="en_secondPage")
@app.route('/es/secundapagina',endpoint="es_secondPage")
@app.route('/it/secondapagina',endpoint="it_secondPage")
def secondPage():
    # use {{ url_for('[= _LANG =]-secondPage'}} in the source template or
    # translate the URLs directly [= URL_mela =]
    # .replace("en","it")
    lang = request.path.split("/")[1]
    return render_template(f"{lang}-endpointstest.html")

if __name__  == '__main__':
	app.run(debug=True)