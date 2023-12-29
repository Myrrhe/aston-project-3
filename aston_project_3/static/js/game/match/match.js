// import * as PIXI from '/static/js/pixijs/pixi.js';

const canvasId = '#canvas-match';

const {width, height} = $(canvasId)[0];
// const height = $(canvasId)[0].height;

const app = new PIXI.Application({
    background: '#000000ff',
    resizeTo: $(canvasId)[0],
    view: $(canvasId)[0],
});

app.renderer.resize(width, width);

// $(canvasId).appendChild(app.view);
// document.body.appendChild(app.view);

// create a new Sprite from an image path
// const bunny = PIXI.Sprite.from('https://pixijs.com/assets/bunny.png');
const bunny = PIXI.Sprite.from('/static/img/png/sprite_001.png');

// center the sprite's anchor point
bunny.anchor.set(0.5);

// move the sprite to the center of the screen
bunny.x = app.screen.width / 2;
bunny.y = app.screen.height / 2;

app.stage.addChild(bunny);

// Listen for animate update
// app.ticker.add(delta => {
//     bunny.rotation += 0.001 * delta;
// });

// Grid
const gridGraphics = new PIXI.Graphics();

const gridSize = 10;
const gridColor = 0xffffff;

for (let i = 0; i <= app.renderer.width; i += gridSize) {
    gridGraphics.lineStyle(1, gridColor, 0.5);
    gridGraphics.moveTo(i, 0);
    gridGraphics.lineTo(i, app.renderer.height);
}

for (let j = 0; j <= app.renderer.height; j += gridSize) {
    gridGraphics.lineStyle(1, gridColor, 0.5);
    gridGraphics.moveTo(0, j);
    gridGraphics.lineTo(app.renderer.width, j);
}

app.stage.addChild(gridGraphics);



// Player 1
const vertices = [
    0, 0,
    128, 0,
    128, 128,
    0, 128,
];

const texture = PIXI.Texture.from('/static/img/png/sprite_001.png');

const simpleMesh = new PIXI.SimpleMesh(texture, vertices);

// simpleMesh.drawMode = PIXI.TRIANGLE_STRIP;

// simpleMesh.geometry.addAttribute('color', [0xffffff, 0xffffff, 0xffffff, 0xffffff], 4);

// const colors = new Float32Array([1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]);
// simpleMesh.geometry.addAttribute('aVertexColor', colors, 4, false, PIXI.TYPES.FLOAT);

// simpleMesh.color.setLight(0.5, 0.5, 0.5);

simpleMesh.position.set(50, 50);

app.stage.addChild(simpleMesh);
