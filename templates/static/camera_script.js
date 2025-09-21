var socket = io.connect(
  window.location.protocol + "//" + document.domain + ":" + location.port
);

socket.on("connect", function () {
  console.log("Connected...!", socket.connected);
});

var videoelement = document.getElementById("webcamVideo");
var localStreamConstraints = {
    audio: true,
    video: { width: 1920, height: 1080 },
};

var mediarecorder
var options = { mimeType: "video/webm; codecs=vp9" };
var recordedChunks=[]

if (videoelement) {
    console.log("we have the video")
    navigator.mediaDevices
    .getUserMedia(localStreamConstraints)
    .then(gotStream)
    .catch(function (e) {
        if (confirm("An error with camera occured:(" + e.name + ") Do y ou want to reload?")) {
            location.reload();
        }
    });
}
//if found stream found

function gotStream(stream) {
    console.log("Adding local stream.");
    videoelement.srcObject = stream
    mediarecorder=new MediaRecorder(stream,options)
    mediarecorder.ondataavailable = handleDataAvailable;
}


function capture_frame()
{
    var type = "image/jpeg";
    var data = document.getElementById("canvasOutput").toDataURL(type);
    //data = data.replace('data:' + type + ';base64,', '');
    socket.emit("frame", data);
}


let timerId = setInterval(capture_frame, 35);
