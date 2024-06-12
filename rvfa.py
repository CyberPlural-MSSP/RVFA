from flask import Flask, render_template, request

app = Flask(__name__)

DEMOS = {
  'CWE-209': {
    'name': 'Generation of Error Message Containing Sensitive Information',
    'description': 'The product generates an error message that includes sensitive information about its environment, users, or associated data.',
    'template': 'demos/cwe-209.html'
  }
}

@app.route("/")
def index():
  return render_template("index.html", DEMOS = DEMOS)

@app.route("/demo/<name>")
def demo(name: str):
  if not name in DEMOS:
    return app.redirect("/")
  
  return render_template(DEMOS[name]['template'], title=name, name=DEMOS[name]['name'], description=DEMOS[name]['description'])

@app.post("/demo/CWE-209")
def demo_209():
  data = request.json

  print(data)

  if data['username'] != "admin":
    return {'error': 'User not found'}
  else:
    if data['password'] == "admin":
      return {'success': 'Yay! Valid Credentails!!'}
    return {'error': 'Incorrect Password'}