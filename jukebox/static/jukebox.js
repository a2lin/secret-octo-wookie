// JavaScript CrossFading - Audio Object
// refer to:
// http://www.html5rocks.com/en/tutorials/webaudio/intro/

var fb_tracks = new Firebase("https://blazing-fire-4446.firebaseio.com/tracks");
var queued_nodes = [];

var context;
if (typeof AudioContext !== "undefined") {
   context = new AudioContext();
} else if (typeof webkitAudioContext !== "undefined") {
   context = new webkitAudioContext();
} else {
   throw new Error('AudioContext not supported. :(');
}

fb_tracks.on("child_added", function(childSnapShot, prevChildName) {
  var url = childSnapShot.child('url').val();
  var offset = childSnapShot.child('offset').val();

  queue(url, offset);
});

function queue(url, time) {
  var request = new XMLHttpRequest();

  request.open('GET', url, true);
  request.responseType = 'arraybuffer';

  request.onload = function() {
    context.decodeAudioData(request.response, function(buffer) {
      schedule_track(buffer, time);
    });
  }

  request.send();
}

function schedule_track(audio, time) {
  var s_node = context.createBufferSource();
  var g_node = context.createGain();
  var d_node = context.destination;

  s_node.buffer = audio;
  s_node.connect(g_node);
  g_node.connect(d_node);

  var node_data = {}
  node_data["audio"] = audio;
  node_data["time"] = time;
  node_data["source_node"] = s_node;
  node_data["gain_node"] = g_node;
  queued_nodes.push(node_data);

  fade_transition(node_data);

  s_node.start(time);
}

function fade_transition(node_data) {
  var fade_time = 5; //length of fade in and fade out, in seconds.

  var time = node_data["time"];
  var duration = node_data["audio"].duration;
  var g_node = node_data["gain_node"]

  g_node.gain.linearRampToValueAtTime(0, time);
  g_node.gain.linearRampToValueAtTime(1, time + fade_time);

  g_node.gain.linearRampToValueAtTime(1, time + duration - fade_time);
  g_node.gain.linearRampToValueAtTime(0, time + duration);
}
