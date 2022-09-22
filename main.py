from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("hello.html")

@app.route("/<name>")
def hello(name):
    return f"<h2>Hello {(name)}</h2>"

@app.route("/file", methods=["GET", "POST"])
def file():
    if request.method=="POST":
        f = request.files["file"]
        f.save(f"media/{f.filename}")
        return "<h2>File Upload Successfull</h2>"
    return render_template("file.html")