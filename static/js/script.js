Dropzone.options.uploadForm = { // The camelized version of the ID of the form element

  // The configuration we've talked about above
  autoProcessQueue: false,
  uploadMultiple: false,
  maxFilesize: 100,
  acceptedFiles:'.jpg, .jpeg, .png, .mp4',

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
    });

    // this.on("success", function(response){
    //     console.log('GET response:');
    //     var headers = response.data.headers();
    //     var blob = new Blob([response.data],{type:headers['content-type']});
    //     console.log(blob); 
    //     var link = document.createElement('a');
    //     link.href = window.URL.createObjectURL(blob);
    //     link.download = "download.zip";
    //     link.click();
        
    //   });
    
      }
  };