//essential variables
var canvases = document.getElementsByClassName("liquid-canvas")

//parameters
var level =[],
    color = "skyblue",
    c;
    amplitude = 15,  // 揺れの振幅
    frequency = 0.02;  // 揺れの周波数

//function to start or restart the animation
function init(){
  levels = []; // reset levels array
  for(let canvas of canvases) {
      canvas.state = {
        c: 0,
        amplitude: Math.random() * 30,  // 揺れの振幅（ランダムに設定）
        frequency: 0.01 + Math.random() * 0.04  // 揺れの周波数（ランダムに設定）
      };

    levels.push(parseInt(canvas.dataset.progress)); // 進捗状況に応じてレベルを設定
    canvas.width = canvas.parentElement.offsetWidth;
    canvas.height = canvas.parentElement.offsetHeight;
    let ctx = canvas.getContext("2d");
    window.requestAnimationFrame(() => draw(ctx, canvas.width, canvas.height, levels[Array.from(canvases).indexOf(canvas)]));
  }
}

//function that draws into the canvas in a loop
function draw(ctx, w, h, level, state) {  // level parameter added to draw function
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
      var temp = state.amplitude * Math.sin(state.c * state.frequency);
      ctx.bezierCurveTo((w / 3), h - (h - 100) * level / 100 - 50 - temp,
        (2 * w / 3), h - (h - 100) * level / 100 - 50 + temp,
        w, h - (h - 100) * level / 100 - 50);
      ctx.fill();
    }
  }
  update(state);
  window.requestAnimationFrame(() => draw(ctx, w, h, level));  // level parameter added to the call
}

  

//function that updates variables
function update(w, h) {
    c++;
    if (100 * Math.PI <= c)
      c = 0;
    // Smoothly update the amplitude
    state.amplitude += (Math.random() - 0.5) * 2;
    // Ensure amplitude stays within a reasonable range
    state.amplitude = Math.min(30, Math.max(state.amplitude, 0));
  }

//update canvas size when resizing the window
window.addEventListener('resize', function() {
  for(let canvas of canvases) {
    window.cancelAnimationFrame(canvas.aniId);
  }
  init();  // レベルの更新のためにinit関数を再呼び出し
});

//start animation
init();
