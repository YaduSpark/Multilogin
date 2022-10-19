from flask import render_template, request, send_from_directory, session

import json
import os
from rq import Queue
from rq.job import Job
from worker import conn
from dotenv import load_dotenv

from Edit import ImageEdit, VideoEdit, FileZip
from models import FilePath, db, app


load_dotenv()
media_path = os.environ["MEDIA_PATH"]

q = Queue(connection=conn, default_timeout=1800)

images = ["jpg", "jpeg", "png"]
videos = ["mp4", "aac", "wma"]

media_path = os.environ["MEDIA_PATH"]
    

def process_media(filename,number):
    extension = filename.split(".")[-1:][0]
    if extension in images:
        edit_file = ImageEdit(f"{media_path}/{filename}")
    elif extension in videos:
        edit_file = VideoEdit(f"{media_path}/{filename}")
    for _ in range(number):
        job = q.enqueue(edit_file.get_random, result_ttl=5000)
    job_id = job.get_id()
    data = json.dumps({'filename': filename, 'number': number, 'path': f'{edit_file.path}', 'edit_name': f'{edit_file.file_name}', 'extension': edit_file.extension})
    return data, job_id

def zip_media(data):
    zip_file = FileZip(data['path'], data['edit_name'], data['extension'])
    zip_file.file_zip()
    # Database
    try:
        filepath = FilePath(original_file_name=data['filename'], file_type=data['extension'], copies_made=data['number'], edited_file_path=data['path'])
        db.session.add(filepath)
        db.session.commit()
        print("Successfully added to DB")
    except:
        print("Error while adding to DB")
    finally:
        file_name = f"media/{data['edit_name']}.zip"
        return file_name


@app.route("/", methods=["GET", "POST"])
def file_upload():
    if request.method=="POST":
        if request.form.get("number"):
            number = int(request.form.get("number"))
        else:
            number=1 
        upload_file = request.files.get("file")
        filename = upload_file.filename
        extension = filename.split(".")[-1:][0]
        if extension in images + videos:
            upload_file.save(f"{media_path}/{filename}")
            data, job_id = process_media(filename,number)
            session['data'] = data
            print(job_id)
            return job_id
        else:
            return render_template("multilogin/index.html")
    return render_template("multilogin/index.html")


@app.route("/task/<job_id>", methods=["GET"]) # to be replaced it /task/<job-id>
def task_status(job_id):

    job = Job.fetch(job_id, connection=conn)
    if not job.is_finished:
        return "202", 202
    if job.is_finished:
        data = session.get('data')
        data = json.loads(data)
        print(data)
        file_path = data["path"]
        print(file_path)
        if os.path.isdir(f"{file_path}"):
            file_url = zip_media(data)
        return file_url, 200

@app.route("/media/<path:filename>")
def file_download(filename):
    return send_from_directory(directory=media_path, path=filename)

if __name__ == "__main__":

    db.create_all()
    app.run(debug=True)

