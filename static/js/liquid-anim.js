//essential variables
var canvases = document.getElementsByClassName("liquid-canvas"),
    aniId;

//parameters
var particles = [],  //particle array
    level =[],
    fill = false,
    color = "skyblue",
    c;
    amplitude = 15,  // 揺れの振幅
    frequency = 0.02;  // 揺れの周波数

//Particle object constructor
function particle(x, y, d){
    this.x = x;
    this.y = y;
    this.d = d;
    this.respawn = function(w, h){
        this.x = Math.random()*(w * 0.8) + (0.1 * w);
        this.y = Math.random()*30 + h-(h-100)*level/100-50 + 50;
        this.d = Math.random()*5 + 5;
    };
}

//function to start or restart the animation
function init(){
  c = 0;
  particles = [];
  levels = []; // reset levels array
  for(let canvas of canvases) {
    levels.push(parseInt(canvas.dataset.progress)); // 進捗状況に応じてレベルを設定
    canvas.width = canvas.parentElement.offsetWidth;
    canvas.height = canvas.parentElement.offsetHeight;
      let ctx = canvas.getContext("2d");
      for(var i=0; i < 40; i++) {
          var obj = new particle(0,0,0);
          obj.respawn(canvas.width, canvas.height);
          particles.push(obj);
      }

      aniId = window.requestAnimationFrame(() => draw(ctx, canvas.width, canvas.height, levels[Array.from(canvases).indexOf(canvas)]));
  }
}

//function that draws into the canvas in a loop
function draw(ctx, w, h, level) {  // level parameter added to draw function
  ctx.clearRect(0, 0, w, h);

  // draw the liquid only when level is greater than 0
  if (level > 0) {
    ctx.fillStyle = color;
    ctx.strokeStyle = color;

    // draw the liquid
    if (level === 100) {
      ctx.fillRect(0, 0, w, h);
    } else {
      ctx.beginPath();
      ctx.moveTo(w, h - (h - 100) * level / 100 - 50);
      ctx.lineTo(w, h);
      ctx.lineTo(0, h);
      ctx.lineTo(0, h - (h - 100) * level / 100 - 50);
      var temp = amplitude * Math.sin(c * frequency);
      ctx.bezierCurveTo((w / 3), h - (h - 100) * level / 100 - 50 - temp,
        (2 * w / 3), h - (h - 100) * level / 100 - 50 + temp,
        w, h - (h - 100) * level / 100 - 50);
      ctx.fill();
    }
  }
    /* draw the bubbles
    for (var i = 0; i < 40; i++) {
      ctx.beginPath();
      ctx.arc(particles[i].x, particles[i].y, particles[i].d, 0, 2 * Math.PI);
      if (fill)
        ctx.fill();
      else
        ctx.stroke();
    }*/
  update(w, h);
  aniId = window.requestAnimationFrame(() => draw(ctx, w, h, level));  // level parameter added to the call
}

  

//function that updates variables
function update(w, h) {
    c++;
    if (100 * Math.PI <= c)
      c = 0;
    for (var i = 0; i < 40; i++) {
      particles[i].x = particles[i].x + Math.random() * 0.5 - 0.25;  // 速度をゆっくりにするために変更
      particles[i].y = particles[i].y - 0.5;  // 速度をゆっくりにするために変更
      particles[i].d = particles[i].d - 0.02;  // 速度をゆっくりにするために変更
      if (particles[i].d <= 0)
        particles[i].respawn(w, h);
    }
  }

//update canvas size when resizing the window
window.addEventListener('resize', function() {
  //stop the animation before restarting it
  window.cancelAnimationFrame(aniId);
  init();  // レベルの更新のためにinit関数を再呼び出し
});

//start animation
init();
