var Wave = function(context, analyser) {
    this.speedState= 2;
    this.speedBase = new Firebase("https://blazing-fire-4446.firebaseio.com/cur_speed/bpm");
    this.speedBase.on("value", this.onSpeed.bind(this))
    this.audioCtx = context;
    this.analyser = analyser;
    this.analyser.fftSize=256;
    this.bufferLength = this.analyser.frequencyBinCount;
    this.dataArray = new Uint8Array(this.bufferLength);
    this.canvas = document.querySelector('#wave');
    this.canvas2 = document.querySelector('#wave2');
    this.canvasCtx = this.canvas.getContext("2d");
    this.canvasCtx2 = this.canvas2.getContext("2d");
    this.drawVisual;
    this.visualize();
}

Wave.prototype.onSpeed = function(snapshot) { 
    console.log(snapshot.val());
    if (snapshot.val() > 145) {
        this.speedState = 2;
    }
    else if(snapshot.val() < 135) {
        this.speedState = 0;
    }
    else {
        this.speedState = 1;
    } 
}

Wave.prototype.clearCanvas = function() {
    this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.canvasCtx2.clearRect(0, 0, this.canvas.width, this.canvas.height);
    
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
    this.analyser.getByteFrequencyData(this.dataArray);

    this.canvasCtx.fillStyle = 'rgb(255, 255, 255)';
    this.canvasCtx2.fillStyle= 'rgb(255, 255, 255)';
    this.canvasCtx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    this.canvasCtx2.fillRect(0, 0, this.canvas2.width, this.canvas2.height);

    var barWidth = (this.canvas.width / this.bufferLength) * 2.5;
    var barHeight;
    var x = 0;

    for(var i = 0; i < this.bufferLength; i++) {
        barHeight = this.dataArray[i];

        if (this.speedState == 1){
            this.canvasCtx.fillStyle = 'rgb(' + (barHeight+100) + ',50,50)';
        }
        if (this.speedState == 2){
            this.canvasCtx.fillStyle = 'rgb(50,' + (barHeight+100) + ',50)';
        }
        if (this.speedState == 0){
            this.canvasCtx.fillStyle = 'rgb(50,50,' + (barHeight+100) + ')';
        }
 
        this.canvasCtx.fillRect(x, this.canvas.height-barHeight/4, 
                                barWidth, barHeight/4);

        this.canvasCtx2.fillStyle = 'rgb('+ '0,0,0' + ')'; 
        this.canvasCtx2.fillRect(x, 0, barWidth, barHeight/4);

        x += barWidth + 1;
    }
}

