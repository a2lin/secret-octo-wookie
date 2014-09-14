var Wave = function(context, analyser) {
    this.audioCtx = context;
    this.analyser = analyser;
    this.analyser.fftSize=256;
    this.bufferLength = this.analyser.frequencyBinCount;
    this.dataArray = new Uint8Array(this.bufferLength);
    this.canvas = document.querySelector('#wave');
    this.canvasCtx = this.canvas.getContext("2d");
    this.drawVisual;
    this.visualize();
    this.edges = new Edges();
}

Wave.prototype.clearCanvas = function() {
    this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height);
}

Wave.prototype.visualize = function() {
    this.bufferLength = this.analyser.frequencyBinCount;
    this.dataArray = new Uint8Array(this.bufferLength);
    this.clearCanvas();
    this.drawVis(); 
}

Wave.prototype.drawLineVis = function() {
    this.drawVisual = requestAnimationFrame(this.drawLineVis.bind(this));

    this.analyser.getByteTimeDomainData(this.dataArray);

    this.canvasCtx.fillStyle = 'rgb(255, 255, 255)';
    this.canvasCtx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    this.canvasCtx.lineWidth = 2;
    this.canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

    this.canvasCtx.beginPath();

    var sliceWidth = this.canvas.width * 1.0 / this.bufferLength;
    var x = 0;

    for(var i = 0; i < this.bufferLength; i++) {
 
      var v = this.dataArray[i] / 128.0;
      var y = v * this.canvas.height/2;

      if(i === 0) {
        this.canvasCtx.moveTo(x, y);
      } else {
        this.canvasCtx.lineTo(x, y);
      }

      x += sliceWidth;
    }

    this.canvasCtx.lineTo(this.canvas.width, this.canvas.height/2);
    this.canvasCtx.stroke();
}

Wave.prototype.drawVis = function() {
    this.drawVisual = requestAnimationFrame(this.drawVis.bind(this));
    console.log("hi");
    this.analyser.getByteFrequencyData(this.dataArray);

    this.canvasCtx.fillStyle = 'rgb(255, 255, 255)';
    this.canvasCtx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    var barWidth = (this.canvas.width / this.bufferLength) * 2.5;
    var barHeight;
    var x = 0;

    for(var i = 0; i < this.bufferLength; i++) {
        barHeight = this.dataArray[i];

        this.canvasCtx.fillStyle = 'rgb('+ '0,0,0' + ')'; 
        this.canvasCtx.fillRect(x, this.canvas.height-barHeight/2, barWidth, barHeight/2);

        x += barWidth + 1;
    }     
}

