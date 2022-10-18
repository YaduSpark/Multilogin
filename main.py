import json
from flask import render_template, request, send_from_directory

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
        print(edit_file.image)
    elif extension in videos:
        edit_file = VideoEdit(f"{media_path}/{filename}")
        clip = edit_file.clip 
        print(clip)
    for _ in range(number):
        work = q.enqueue(edit_file.get_random, result_ttl=5000)
        print(work.get_id())
    work_id = work.get_id()
    data = json.dumps({'filename': filename, 'number': number, 'path': f'{edit_file.path}', 'edit_name': f'{edit_file.file_name}', 'extension': edit_file.extension})
    return data, work_id

def zip_media(data):
    data = json.loads(data)
    zip_file = FileZip(data['path'], data['edit_name'], data['extension'])
    zip_file.file_zip()
    # Database
    filepath = FilePath(original_file_name=data['filename'], file_type=data['extension'], copies_made=data['number'], edited_file_path=data['path'])
    db.session.add(filepath)
    db.session.commit()
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
            # details = { "filename" : f"{upload_file.filename}", "number" : number }
            job = q.enqueue_call(func='main.process_media', args=(filename,number,), result_ttl=5000)
            # print('job_id: ', job.get_id())
            job_id = job.get_id()
            return job_id
            # return redirect(url_for('task_status', job_id = job_id))
        else:
            return render_template("multilogin/index.html")
    return render_template("multilogin/index.html")


@app.route("/task/<job_id>", methods=["GET"]) # to be replaced it /task/<job-id>
def task_status(job_id):

    job = Job.fetch(job_id, connection=conn)
    # print(job.result)
    if job.is_finished:
        data, work_id = job.result
        work = Job.fetch(work_id, connection=conn)
        if work.is_finished:
            return zip_media(data), 200
        else:
            return "Please Wait!!!", 202
    else:
        return "Please Wait!!!", 202
    # random_num = 5
    # if random_num < 6:
    #     response = { "filename" : f"media/8acb39dc-b318-4a68-b1c0-9b52d56411ab.zip", "filestatus" : 2 }
    # else:
    #     response = { "filestatus" : 1 }
    # return  json.dumps(response)

@app.route("/media/<path:filename>")
def file_download(filename):
    return send_from_directory(directory=media_path, path=filename)

if __name__ == "__main__":

    db.create_all()
    app.run(debug=True)

