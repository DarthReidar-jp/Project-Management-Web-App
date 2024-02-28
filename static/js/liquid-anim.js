// essential variables
var canvases = document.getElementsByClassName("liquid-canvas");

// parameters
var level = [],
  amplitude = 15,  // amplitude of the swing
  frequency = [0.02, 0.021, 0.022];  // different frequency for each wave

// function to start or restart the animation
function init() {
  levels = [];  // reset levels array
  for (let canvas of canvases) {
    // add phaseShifts property to state object
    canvas.state = {
      c: 0,
      color: canvas.dataset.color,
      amplitude: amplitude,  // amplitude of the swing (fixed)
      frequency: frequency,  // frequency of the swing (modified)
      phaseShifts: [],  // array to hold random phase shifts for this canvas
    };

    // add three random phase shifts for each canvas
    for (let i = 0; i < 3; i++) {
      canvas.state.phaseShifts.push(Math.random() * 2 * Math.PI);
    }

    levels.push(parseInt(canvas.dataset.progress));  // set levels based on progress
    canvas.width = canvas.parentElement.offsetWidth;
    canvas.height = canvas.parentElement.offsetHeight;
    let ctx = canvas.getContext("2d");
    window.requestAnimationFrame(() => draw(ctx, canvas.width, canvas.height, levels[Array.from(canvases).indexOf(canvas)], canvas.state));  // added canvas.state here
  }
}

// function that draws into the canvas in a loop
function draw(ctx, w, h, level, state) {  // added level parameter to draw function
  ctx.clearRect(0, 0, w, h);

  // draw the liquid only when level is greater than 0
  if (level > 0) {
    ctx.fillStyle = state.color;
    ctx.strokeStyle = state.color;

    // draw the liquid
    if (level === 100) {
      ctx.fillRect(0, 0, w, h);
    } else {
      ctx.beginPath();
      ctx.moveTo(w, h - (h - 100) * level / 100 - 50);
      ctx.lineTo(w, h);
      ctx.lineTo(0, h);
      ctx.lineTo(0, h - (h - 100) * level / 100 - 50);
      

      // modify bezierCurveTo method to sum three sine waves with phase shifts and different frequency
      var temp = 0;
      for (let i = 0; i < 3; i++) {
        temp += state.amplitude * Math.sin(state.c * state.frequency[i] + state.phaseShifts[i]);
      }

      ctx.bezierCurveTo((w / 3), h - (h - 100) * level / 100 - 50 - temp,
        (2 * w / 3), h - (h - 100) * level / 100 - 50 + temp,
        w, h - (h - 100) * level / 100 - 50);
      ctx.fill();
    }
  }

  update(state);
  window.requestAnimationFrame(() => draw(ctx, w, h, level, state));  // added state here
}

// function that updates variables
function update(state) {
  state.c++;
}

// update canvas size when resizing the window
window.addEventListener('resize', function () {
  for (let canvas of canvases) {
    window.cancelAnimationFrame(canvas.aniId);
  }
  init();  // re-call init function to update levels
});

// start animation
init();
