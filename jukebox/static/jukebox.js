// JavaScript CrossFading - Audio Object
var Audio = function(){
   // use an array as a queue
  
   // initialize AudioContext
   window.AudioContext = window.AudioContext || window.webkitAudioContext;

   // initialize our variables
   this.queue = [];
   this.playing = false;
   this.audioContext = new AudioContext();

}

Audio.prototype.enqueue = function(url) {

    // Load the url into a buffer and shove into our queue
    // (To Be Crossfaded)
    this.load(url);
}

Audio.prototype.play = function() {
    if (this.playing != false) {
        var nextBuffer = this.queue.shift();
        var source = this.audioContext.createBufferSource();
        source.buffer = nextBuffer;
        source.connect(this.audioContext.destination);
        source.start(0);

        if (this.queue.length > 0) {
            this.play();
        }
    }
}

Audio.prototype.load = function(url) {
    var tempBuffer = null;

    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'arraybuffer';
    
    request.onload = function() {
        context.decodeAudioData(request.response, function(buffer) {

            // Enforce a length limit on the queue so it doesn't get huge
            
            if (this.queue.length < 10) {
                // Add the newly-loaded buffer
                this.queue.push(this.load(url));

                // Try to play (all buffers are loaded async)
                this.play();
            }

        }, onError);
    }
    request.send();
}

