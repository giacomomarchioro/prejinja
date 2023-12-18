from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
supported_languages = ["en", "nl", "it"]

@app.route('/')
def localeRedirect():
   lang = request.accept_languages.best_match(supported_languages)
   return redirect(url_for('indexPage', lang=lang))

@app.route('/<lang>/test')
def indexPage(lang):
   # app variable
   return render_template(f"{lang}-index.html")

@app.route('/<lang>/teststatictemplate')
def testStaticTemplate(lang):
   return send_from_directory('templates',f"{lang}-index.html")

if __name__  == '__main__':
	app.run(debug=True)