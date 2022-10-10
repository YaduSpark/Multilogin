Dropzone.options.uploadForm = { // The camelized version of the ID of the form element

  // The configuration we've talked about above
  autoProcessQueue: false,
  uploadMultiple: false,
  maxFilesize: 100,
  acceptedFiles:'.jpg, .jpeg, .png, .mp4',
  maxFiles: 1,
  timeout: 60000,
  // The setting up of the dropzone
  init: function() {
    var myDropzone = this;

    // First change the button to actually tell Dropzone to process the queue.
    this.element.querySelector("button[type=submit]").addEventListener("click", function(e) {
      // Make sure that the form isn't actually being sent.
      e.preventDefault();
      e.stopPropagation();
      myDropzone.processQueue();
    });

    this.on("sending", function() {
      document.querySelector("button[type=submit]").style.display="none";
      //document.getElementById("wait").style.display="inline";
    });

    this.on("success", function startProcessing(file, response){
      document.getElementById("wait").style.display="inline"; // Once upload is success, display the Processing message & loader
      
      const taskURL = "/task/" + response; // should be replaced with /task/taskID once python code is modified.
      // console.log(taskURL)

      const delay = (ms = 5000) => new Promise(r => setTimeout(r, ms));

      async function getTaskStatus() {
        await delay();
        let response = await fetch(taskURL);
        console.log(response.status)
        if (parseInt(response.status) == 202){
          getTaskStatus()}
        let responseText = await response.text();
        return  responseText;
      }

      async function taskStatusLongPoll() {
        const response = await getTaskStatus();
        // const taskStatus = JSON.parse(response);
        if (response != "Please Wait!!!") { // filestatus 2 stands for complete
          var anchorEl = document.getElementById('download_btn');
          anchorEl.setAttribute('href',response);
          document.getElementById("wait").style.display="none"; // Hide Processing message & loader
          document.getElementById("download_btn").style.display="inline";
        } else {
          setTimeout(() => {
            taskStatusLongPoll();
          }, 5000);
        }
      }

      taskStatusLongPoll();
       
    });
      // document.getElementById("download_btn").addEventListener("click", function(){setTimeout( window.location.reload(), 2000)});
   }    
};
