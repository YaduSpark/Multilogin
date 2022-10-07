from flask import render_template, request, send_from_directory

from Edit import ImageEdit, VideoEdit
from models import FilePath, db, app
import os

images = ["jpg", "jpeg", "png"]
videos = ["mp4", "aac", "wma"]
media_path = os.environ["MEDIA_PATH"]

@app.route("/", methods=["GET", "POST"])
def file_upload():
    if request.method=="POST":
        if request.form.get("number"):
            number = request.form.get("number")
        else: 
            number=1
        upload_file = request.files.get("file")
        extension = upload_file.filename.split(".")[-1:][0]
        if extension in images + videos:
            upload_file.save(f"{media_path}/{upload_file.filename}")
            if extension in images:
                edit_file = ImageEdit(f"{media_path}/{upload_file.filename}", int(number))
            elif extension in videos:
                edit_file = VideoEdit(f"{media_path}/{upload_file.filename}", int(number))
            edit_file.random_files()
            filepath = FilePath(file_name=edit_file.file_name, file_type=extension, file_path=edit_file.path)
            db.session.add(filepath)
            db.session.commit()
            print(f"media/{edit_file.file_name}.zip")
            return f"media/{edit_file.file_name}.zip"
            del edit_file
        else:
            print("hello")
            return render_template("multilogin/index.html")
    return render_template("multilogin/index.html")

@app.route("/media/<path:filename>", methods=["GET"])
def file_download(filename):
    return send_from_directory(directory=media_path, path=filename)

if __name__ == "__main__":

    db.create_all()
    app.run(debug=True)
    

