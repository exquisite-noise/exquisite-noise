var promise = navigator.mediaDevices.getUserMedia({audio: true, video: false});

var recordButton = document.getElementById('js-record-button');
var stopButton = document.getElementById('js-stop-button');
var audio = document.querySelector('#js-audio');
var uploadSpan = document.getElementById('js-upload-span');
var audioFile = document.querySelectorAll('[data-django-audio-recorder]')[0];
var submitOverride = document.getElementById('submit-override');
var canvas = document.querySelector('.visualizer');
var mainSection = document.querySelector('.main-controls');
var timerIndicator = document.getElementById('timer-indicator');
var submitTopicButton = document.getElementById('submit-topic-button');
var instructionHeader = document.getElementById('instruction-header');
var formData;
var audioCtx = new (window.AudioContext || webkitAudioContext)();
var canvasCtx = canvas.getContext('2d');

$(submitOverride).hide();
$(recordButton).hide();
$(stopButton).hide();
$(audio).hide();
$(canvas).hide();

promise.then(function(stream) {
  var recorder = new MediaRecorder(stream);
  recorder.chunks = [];

  visualize(stream);

  submitTopicButton.addEventListener('click', function() {
    $(submitTopicButton).hide();
    $(instructionHeader).text('2. Record your audio');
    $(timerIndicator).text('Press record to start your 15 seconds. Re-record it as many times as you like before submitting.');
    $(recordButton).fadeIn();
    $(canvas).fadeIn();
  });

  recordButton.addEventListener('click', function(){
    recordButton.disabled = true;
    stopButton.disabled = false;
    audio.removeAttribute('src');
    // recorder.start();
    $(audio).hide();
    $(canvas).show();
    $(timerIndicator).text('Recording will begin in 3');
    $(timerIndicator).css('color', '#F53240');
    var counter = setInterval(timer, 1000); //1000 will  run it every 1 second
    // window.setTimeout(buttonClick, 5000);
    // document.getElementById("timer-number").innerHTML = count;
    var count = 13;

    function timer(){
      count = count - 1;
      if (count <= 0){

        clearInterval(counter);
        $('#js-stop-button').click();
        document.getElementById("timer-indicator").innerHTML = 'Listen below then re-record or submit.';
        return;
      }
      if (count < 11) {
        if (count === 10) {
          recorder.start();
          $(recordButton).text('Recording...');
        }
        document.getElementById("timer-indicator").innerHTML = '* Recording: ' + count + ' *';
      } else {
        document.getElementById("timer-indicator").innerHTML = 'Recording will begin in ' + (count - 10) + '';
      }
    }
  });

  stopButton.addEventListener("click", function(){
    stopButton.disabled = true;
    recordButton.disabled = false;
    uploadSpan.classList.remove('hidden');
    recorder.stop();
    $(audio).fadeIn();
  });

  recorder.ondataavailable = function(e) {
    this.chunks.push(e.data);
  };

  recorder.onstop = function(event) {
    $(instructionHeader).text('3. Re-record or Submit!');
    $(timerIndicator).text('Use the audio player below to review your clip and submit when you\'re ready.');
    var blob = new Blob(this.chunks, {'type': 'audio/mp3;'});
    this.chunks = [];
    var audioURL = window.URL.createObjectURL(blob);
    audio.src = audioURL;
    console.log(audioURL);
    var formEl = document.getElementById('new-audio-form');
    formData = new FormData(formEl);
    formData.append('audio_file', blob, "story.mp3");
    $(timerIndicator).css('background-color', '');
    $(recordButton).text('Re-Record');
    $(canvas).hide();
    $(submitOverride).fadeIn();

  };

  submitOverride.addEventListener('click', function(event){
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
        window.location = '../link';
      },
      error: function(jqXHR, textStatus, errorThrown){
        uploadSpan.classList.add('hidden');
        recordButton.disabled = false;
        console.error('jqXHR:', jqXHR);
        console.error('textStatus:', textStatus);
        console.error('errorThrown:', errorThrown);
      },
    });
  });
});

promise.catch(function(err) { console.log(err.name); });


function visualize(stream) {
  var source = audioCtx.createMediaStreamSource(stream);

  var analyser = audioCtx.createAnalyser();
  analyser.fftSize = 2048;
  var bufferLength = analyser.frequencyBinCount;
  var dataArray = new Uint8Array(bufferLength);

  source.connect(analyser);
  //analyser.connect(audioCtx.destination);

  draw();

  function draw() {
    const WIDTH = canvas.width;
    const HEIGHT = canvas.height;

    requestAnimationFrame(draw);

    analyser.getByteTimeDomainData(dataArray);

    canvasCtx.fillStyle = 'rgb(200, 200, 200)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

    canvasCtx.beginPath();

    var sliceWidth = WIDTH * 1.0 / bufferLength;
    var x = 0;


    for(var i = 0; i < bufferLength; i++) {

      var v = dataArray[i] / 128.0;
      var y = v * HEIGHT / 2;

      if(i === 0) {
        canvasCtx.moveTo(x, y);
      } else {
        canvasCtx.lineTo(x, y);
      }

      x += sliceWidth;
    }

    canvasCtx.lineTo(canvas.width, canvas.height / 2);
    canvasCtx.stroke();

  }
}

window.onresize = function() {
  canvas.width = mainSection.offsetWidth;
}

window.onresize();
