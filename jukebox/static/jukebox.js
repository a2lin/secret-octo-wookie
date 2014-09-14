// JavaScript CrossFading - Audio Object
// refer to:
// http://www.html5rocks.com/en/tutorials/webaudio/intro/
var Tracks = function() {
    this.fb_tracks = new Firebase("https://blazing-fire-4446.firebaseio.com/tracks");
    this.queued_nodes = [];

    this.context;
    if (typeof AudioContext !== "undefined") {
       this.context = new AudioContext();
    } else if (typeof webkitAudioContext !== "undefined") {
       this.context = new webkitAudioContext();
    } else {
       throw new Error('AudioContext not supported. :(');
    }

    this.analyser = this.context.createAnalyser();
    this.fb_tracks.on("child_added", this.initQueue.bind(this));
}

Tracks.prototype.initQueue = function(childSnapShot, prevChildName) {
    var url = childSnapShot.child('url').val();
    var offset = childSnapShot.child('offset').val();
    this.queue(url, offset);
}


Tracks.prototype.queue = function(url, time) {
    var request = new XMLHttpRequest();

    request.open('GET', url, true);
    request.responseType = 'arraybuffer';

    // must maintain 'this' context in the function
    request.onload = (function() {
        this.context.decodeAudioData(request.response, (function(buffer) {
            this.schedule_track(buffer, time);
        }).bind(this));
    }).bind(this);

    request.send();
}


Tracks.prototype.schedule_track = function(audio, time) {
    var s_node = this.context.createBufferSource();
    var g_node = this.context.createGain();
    var a_node = this.analyser;
    var d_node = this.context.destination;

    s_node.buffer = audio;
    s_node.connect(g_node);
    g_node.connect(a_node);
    a_node.connect(d_node);

    var node_data = {}
    node_data["audio"] = audio;
    node_data["time"] = time;
    node_data["source_node"] = s_node;
    node_data["gain_node"] = g_node;
    this.queued_nodes.push(node_data);

    this.fade_transition(node_data);

    s_node.start(time - Math.floor(new Date().getTime()/1000));
}

Tracks.prototype.fade_transition = function(node_data) {
    var fade_time = 5; //length of fade in and fade out, in seconds.

    var time = node_data["time"];
    var duration = node_data["audio"].duration;
    var g_node = node_data["gain_node"]

    g_node.gain.linearRampToValueAtTime(0, time);
    g_node.gain.linearRampToValueAtTime(1, time + fade_time);

    g_node.gain.linearRampToValueAtTime(1, time + duration - fade_time);
    g_node.gain.linearRampToValueAtTime(0, time + duration);
}
