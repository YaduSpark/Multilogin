from flask import render_template, request, send_file

from Edit import ImageEdit, VideoEdit
from models import FilePath, db, app


images = ["jpg", "jpeg", "png"]
videos = ["mp4", "aac", "wma"]

@app.route("/", methods=["GET", "POST"])
def file_upload():
    if request.method=="POST":
        if request.form.get("number"):
            number = request.form.get("number")
        else: 
            number=1
        upload_file = request.files.get("file")
        extension = upload_file.filename.split(".")[-1:][0]
        print(extension)
        print(upload_file.filename)
        if extension in images + videos:
            upload_file.save(f"media/{upload_file.filename}")
        if extension in images:
            edit_file = ImageEdit(f"media/{upload_file.filename}", int(number))
            edit_file.random_files()
        elif extension in videos:
            edit_file = VideoEdit(f"media/{upload_file.filename}")
            edit_file.resize()
        else:
            print("hello")
            return render_template("multilogin/index.html")
        filepath = FilePath(file_name=edit_file.file_name, file_type=extension, file_path=edit_file.path)
        db.session.add(filepath)
        db.session.commit()
        print(f"{edit_file.path}.zip")
        return send_file(f"{edit_file.path}.zip", as_attachment=True)
    return render_template("multilogin/index.html")


if __name__ == "__main__":

    db.create_all()
    app.run(debug=True)
    

