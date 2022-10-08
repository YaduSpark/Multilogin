// Dropzone.autoDiscover = false;
// $(".dropzone").dropzone({
//    url: "index",
//    success: function (file, response) {
//       if(response != 0){
//          // Download link
//          var anchorEl = document.createElement('a');
//          anchorEl.setAttribute('href',response);
//          anchorEl.setAttribute('target','_blank');
//          anchorEl.innerHTML = "<br>Download";
//          file.previewTemplate.appendChild(anchorEl);
//       }
//    }
// });

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

    this.on("success", function(file, response){
         document.getElementById("wait").style.display="inline"; // Once upload is success, display the Processing message & loader
         const obj = JSON.parse(response);
	 getZip('/process/' + obj.filename + '/' + obj.number);

         async function getZip(taskURL) {
          let myObject = await fetch(taskURL);
          let responseText = await myObject.text();
          var anchorEl = document.getElementById('download_btn');
          anchorEl.setAttribute('href',responseText);
          document.getElementById("wait").style.display="none"; // Hide Processing message & loader
          document.getElementById("download_btn").style.display="inline";
         }
     });
      // document.getElementById("download_btn").addEventListener("click", function(){setTimeout( window.location.reload(), 2000)});
   }    
};
