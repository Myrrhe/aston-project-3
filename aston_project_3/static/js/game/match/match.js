class InterpolationFunction {
    static LINEAR = new InterpolationFunction('linear');
    static SQUARE = new InterpolationFunction('square');

    constructor(name) {
        this.name = name;
    }
}

const interpolate = function(a, b, coeff, interpolationFunction = InterpolationFunction.LINEAR) {
    let res = 0;
    coeff = Math.min(1, Math.max(coeff, 0));
    switch (interpolationFunction) {
        case InterpolationFunction.LINEAR:
            res = a * (1 - coeff) + b * coeff;
            break;
        case InterpolationFunction.SQUARE:
            res = a * (1 - coeff * coeff) + b * coeff * coeff;
            break;
        default:
            break;
    }
    return res;
};

const canvasId = '#canvas-match';

const {width, height} = $(canvasId)[0];

const app = new window.PIXI.Application({
    background: 0x000000,
    resizeTo: $(canvasId)[0],
    view: $(canvasId)[0],
});

app.renderer.resize(width, width);

// Grid
const gridGraphics = new window.PIXI.Graphics();

const gridWidth = 30;
const gridHeight = 20;
const cellSize = 10;
const gridColor = 0xffffff;

const colorPlayer1 = 0x00ff88;
const colorPlayer2 = 0xff0088;

for (let i = 0; i < gridWidth; i++) {
    gridGraphics.lineStyle(1, gridColor, 0.5);
    gridGraphics.moveTo(i * cellSize, 0);
    gridGraphics.lineTo(i * cellSize, cellSize * gridHeight);
}

for (let j = 0; j < gridHeight; j++) {
    gridGraphics.lineStyle(1, gridColor, 0.5);
    gridGraphics.moveTo(0, j * cellSize);
    gridGraphics.lineTo(gridWidth * cellSize, j * cellSize);
}

app.stage.addChild(gridGraphics);


class Player {
    constructor(color, positions, index) {
        this.color = color;
        this.positions = positions;
        this.index = index;

        this.graphicsBack = new window.PIXI.Graphics();
        this.graphicsFront = new window.PIXI.Graphics();
        this.graphicsBack.lineStyle({
            width: Player.width,
            color: this.color,
            cap: window.PIXI.LINE_CAP.ROUND,
            join: window.PIXI.LINE_JOIN.ROUND,
        });
        this.graphicsFront.lineStyle({
            width: 5,
            color: this.color,
            cap: window.PIXI.LINE_CAP.ROUND,
            join: window.PIXI.LINE_JOIN.ROUND,
        });

        this.blurFilter = new window.PIXI.BlurFilter();
        this.blurFilter.blur = 5;
        this.graphicsBack.filters = [this.blurFilter];

        const posX1 = this.positions[0]['x'] * cellSize + Player.width - 1;
        const posY1 = this.positions[0]['y'] * cellSize + Player.width;
        const posX2 = posX1 + 1;
        const posY2 = posY1;

        this.graphicsBack.moveTo(
            posX1,
            posY1,
        );
        this.graphicsFront.moveTo(
            posX1,
            posY1,
        );

        this.graphicsBack.lineTo(
            posX2,
            posY2,
        );
        this.graphicsFront.lineTo(
            posX2,
            posY2,
        );

        app.stage.addChild(this.graphicsBack);
        app.stage.addChild(this.graphicsFront);
    }

    update(t) {
        this.graphicsBack.clear();
        this.graphicsFront.clear();

        this.graphicsBack.lineStyle({
            width: Player.width,
            color: this.color,
            cap: window.PIXI.LINE_CAP.ROUND,
            join: window.PIXI.LINE_JOIN.ROUND,
        });
        this.graphicsFront.lineStyle({
            width: Player.width,
            color: this.color,
            cap: window.PIXI.LINE_CAP.ROUND,
            join: window.PIXI.LINE_JOIN.ROUND,
        });

        let posX = this.positions[0]['x'] * cellSize + Player.width - 1;
        let posY = this.positions[0]['y'] * cellSize + Player.width;

        this.graphicsBack.moveTo(
            posX,
            posY,
        );
        this.graphicsFront.moveTo(
            posX,
            posY,
        );

        const nbPoints = Math.min(Math.floor(t / 1000), this.positions.length - 1);

        for (let i = 1; i <= nbPoints; i++) {
            posX = this.positions[i]['x'] * cellSize + Player.width - 1;
            posY = this.positions[i]['y'] * cellSize + Player.width;

            this.graphicsBack.lineTo(
                posX,
                posY,
            );

            this.graphicsFront.lineTo(
                posX,
                posY,
            );
        }

        if (nbPoints < this.positions.length - 1) {
            posX = interpolate(
                this.positions[nbPoints]['x'],
                this.positions[nbPoints + 1]['x'],
                (t - nbPoints * 1000)/1000,
            ) * cellSize + Player.width - 1;

            posY = interpolate(
                this.positions[nbPoints]['y'],
                this.positions[nbPoints + 1]['y'],
                (t - nbPoints * 1000)/1000,
            ) * cellSize + Player.width;

            this.graphicsBack.lineTo(
                posX,
                posY,
            );

            this.graphicsFront.lineTo(
                posX,
                posY,
            );
        }
    }

    static width = 5;
}

const positions1 = [
    {'x': 0, 'y': 0},
    {'x': 1, 'y': 0},
    {'x': 1, 'y': 1},
    {'x': 1, 'y': 2},
    {'x': 2, 'y': 2},
];

const positions2 = [
    {'x': 29, 'y': 19},
    {'x': 28, 'y': 19},
    {'x': 28, 'y': 18},
    {'x': 28, 'y': 17},
    {'x': 27, 'y': 17},
];

const player1 = new Player(
    colorPlayer1,
    positions1,
    0,
);

const player2 = new Player(
    colorPlayer2,
    positions2,
    1,
);

const startMachTime = new Date().getTime();

const updateMatch = function() {
    const currentTime = new Date().getTime();
    const t = currentTime - startMachTime;
    player1.update(t);
    player2.update(t);
};

const framePerSecond = 30;
const millisecondPerFrame = Math.floor(1000 / cellSize);

const intervalId = setInterval(updateMatch, millisecondPerFrame);

setTimeout(function() {
    clearInterval(intervalId);
}, positions1.length * 1000);
