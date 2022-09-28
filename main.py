from flask import Flask, render_template, request, send_file

from Edit import ImageEdit, VideoEdit
from models import FilePath, db, app


images = ["jpg", "jpeg", "png"]
videos = ["mp4", "aac", "wma"]


@app.route("/", methods=["GET", "POST"])
def file_upload():
    if request.method=="POST":
        if request.form.get("number"):
            num = request.form.get("number")
        else: 
            num=1
        f = request.files.get("file")
        f.save(f"media/{f.filename}")
        extension = f.filename.split(".")[-1:][0]
        print(extension)
        print(f.filename)
        if extension in images:
            f = ImageEdit(f"media/{f.filename}", int(num))
            f.random_files()
        elif extension in videos:
            f = VideoEdit(f"media/{f.filename}")
            f.resize()
        else:
            return "<h2>Enter Valid File</h2>"
        filepath = FilePath(file_name=f.file_name, file_type=extension, file_path=f.path)
        db.session.add(filepath)
        db.session.commit()
        return send_file(f"{f.path}.zip", as_attachment=True)
    # return render_template("multilogin/index.html")
    return render_template("file.html")

 
if __name__ == "__main__":

    db.create_all()
    app.run(debug=True)
    

