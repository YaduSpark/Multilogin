from flask import Flask, render_template, request

from Edit import ImageEdit
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("hello.html")

@app.route("/<name>")
def hello(name):
    return f"<h2>Hello {(name)}</h2>"

@app.route("/image", methods=["GET", "POST"])
def file():
    if request.method=="POST":
        num = request.form["number"]
        f = request.files["file"]
        f.save(f"media/{f.filename}")
        f = ImageEdit(f"media/{f.filename}", int(num))
        f.random_files()
        return render_template("edit.html")
    return render_template("file.html")