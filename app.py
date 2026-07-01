from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "¡Hola! Mi proyecto Flask funciona."

@app.route("/login", methods=["GET","POST"])
def login(): 
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)