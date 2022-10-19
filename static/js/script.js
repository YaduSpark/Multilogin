Dropzone.options.uploadForm = { // The camelized version of the ID of the form element

  // The configuration we've talked about above
  autoProcessQueue: false,
  uploadMultiple: false,
  maxFilesize: 100,
  acceptedFiles: '.jpg, .jpeg, .png, .mp4',
  maxFiles: 1,
  timeout: 60000,
  // The setting up of the dropzone
  init: function () {
    var myDropzone = this;

    // First change the button to actually tell Dropzone to process the queue.
    this.element.querySelector("button[type=submit]").addEventListener("click", function (e) {
      // Make sure that the form isn't actually being sent.
      e.preventDefault();
      e.stopPropagation();
      myDropzone.processQueue();
    });

    this.on("sending", function () {
      document.querySelector("button[type=submit]").style.display = "none";
      //document.getElementById("wait").style.display="inline";
      date1 = new Date();
    });

    this.on("success", (file, response) => {
      document.getElementById("wait").style.display = "inline"; // Once upload is success, display the Processing message & loader
      console.log(response)
      const taskURL = "/task/" + response; // should be replaced with /task/taskID once python code is modified.

      async function getTaskStatus() {
        let promise = new Promise(async function (resolve, reject) {
          let response = await fetch(taskURL);
          if (response.status === 200) {
            let responseText = await response.text();
            resolve(responseText);
          } else {
            reject(response);
          }
        });
        return promise;
      }

      function taskStatusLongPoll() {
        getTaskStatus().then((res) => {
          if (res) {
            var anchorEl = document.getElementById('download_btn');
            anchorEl.setAttribute('href', res);
            document.getElementById("wait").style.display = "none"; // Hide Processing message & loader
            document.getElementById("download_btn").style.display = "inline";
            date2 = new Date();
            time_taken(date1, date2);
          }
        }).catch(err => {
          setTimeout(() => {
            console.log(err.status);
            taskStatusLongPoll();
          }, 5000);
        })
      }
      taskStatusLongPoll();
    });
    // document.getElementById("download_btn").addEventListener("click", function(){setTimeout( window.location.reload(), 2000)});
  }
};


function time_taken(date1, date2) {
  var diff = date2.getTime() - date1.getTime();

  var msec = diff;
  var hh = Math.floor(msec / 1000 / 60 / 60);
  msec -= hh * 1000 * 60 * 60;
  var mm = Math.floor(msec / 1000 / 60);
  msec -= mm * 1000 * 60;
  var ss = Math.floor(msec / 1000);
  msec -= ss * 1000;

  console.log(hh + ":" + mm + ":" + ss);
}
