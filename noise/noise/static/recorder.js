var promise = navigator.mediaDevices.getUserMedia({audio: true, video: false});

var recordButton = document.getElementById('js-record-button');
var stopButton = document.getElementById('js-stop-button');
var audio = document.getElementById('js-audio');
var uploadSpan = document.getElementById('js-upload-span');
var audioFile = document.querySelectorAll('[data-django-audio-recorder]')[0];

promise.then(function(stream) {
  var recorder = new MediaRecorder(stream);
  recorder.chunks = [];

  recordButton.addEventListener("click", function(){
    recordButton.disabled = true;
    stopButton.disabled = false;
    audio.removeAttribute('src');
    recorder.start();
    var counter = setInterval(timer, 1000); //1000 will  run it every 1 second
    // window.setTimeout(buttonClick, 5000);
    // document.getElementById("timer-number").innerHTML = count;
    var count = 5;
    function timer(){
      count = count - 1;
      if (count <= 0){
        
        clearInterval(counter);
        $('#js-stop-button').click();
        document.getElementById("timer-element").innerHTML = 'Audio clip submitted.';
        return;
      }
      document.getElementById("timer-number").innerHTML = count;
    }
  });

  // function buttonClick () {
    //   $('#js-stop-button').click();
    // }
    
  

  stopButton.addEventListener("click", function(){
    stopButton.disabled = true;
    uploadSpan.classList.remove('hidden');
    recorder.stop();
  });

  recorder.ondataavailable = function(e) {
    this.chunks.push(e.data);
  };

  

  recorder.onstop = function(event) {
    var blob = new Blob(this.chunks, {'type': 'audio/mpeg;'});
    this.chunks = [];
    var formEl = document.getElementById('new-audio-form');
    var formData = new FormData(formEl);
    formData.append('audio_file', blob, "story.mp3");
    $.ajax({
      type: "POST",
      url: audioFile.dataset.url,
      data: formData,
      processData: false,
      contentType: false,
      success: function(data){
        uploadSpan.classList.add('hidden');
        recordButton.disabled = false;
        audioFile.value = data.id;
        audio.src = data.url;
      },
      error: function(jqXHR, textStatus, errorThrown){
        uploadSpan.classList.add('hidden');
        recordButton.disabled = false;
        console.error('jqXHR:', jqXHR);
        console.error('textStatus:', textStatus);
        console.error('errorThrown:', errorThrown);
      },
    });
  };
});

promise.catch(function(err) { console.log(err.name); });
