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

const gridWidth = 30;
const gridHeight = 20;

const width = $(canvasId).parent().width();
const height = gridHeight * width / gridWidth;

$(canvasId)[0].width = width;
$(canvasId)[0].height = height;

const app = new window.PIXI.Application(
    {
        width,
        height,
        background: 0x000000,
        // resizeTo: $(canvasId)[0],
        view: $(canvasId)[0],
        // forceCanvas: false,
        // autoResize: true,
        // resolution: 1,
});

// const {width, height} = app.renderer;
// console.log(app.renderer.width);
// console.log(app.renderer.height);

// app.renderer.resize(width, height);
// app.renderer.view.width = width;
// app.renderer.view.height = gridHeight * width / gridWidth;

// Grid
const gridGraphics = new window.PIXI.Graphics();

const cellSize = width / gridWidth;
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

// The player class

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
        this.blurFilter.blur = cellSize / 2;
        this.graphicsBack.filters = [this.blurFilter];
    }

    update(coeff) {
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

        const nbPoints = Math.floor(coeff * (this.positions.length - 1));

        const coeffDraw = (coeff - nbPoints/(this.positions.length - 1.0))/(1.0 / (this.positions.length - 1.0));

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
                coeffDraw,
            ) * cellSize + Player.width - 1;

            posY = interpolate(
                this.positions[nbPoints]['y'],
                this.positions[nbPoints + 1]['y'],
                coeffDraw,
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

    show() {
        app.stage.addChild(this.graphicsBack);
        app.stage.addChild(this.graphicsFront);
    }

    hide() {
        app.stage.removeChild(this.graphicsBack);
        app.stage.removeChild(this.graphicsFront);
    }

    setPositions(positions) {
        this.positions = positions;
    }

    static width = cellSize / 2;
}

const player1 = new Player(
    colorPlayer1,
    [],
    0,
);

const player2 = new Player(
    colorPlayer2,
    [],
    1,
);

const framePerSecond = 30;
const millisecondPerFrame = Math.floor(1000 / framePerSecond);

let startMachTime = null;
let intervalId = null;
let durationMatch = null;
let matchStarted = false;
let machEnded = false;
let pause = false;
let coeffSaved = 0;

const buttonPlayId = '#button-play';
const buttonMatchPlayClass = 'button-match-play';
const buttonMatchPauseClass = 'button-match-pause';
const buttonMatchReplayClass = 'button-match-replay';

const removeClassesButtonPlay = function() {
    if ($(buttonPlayId).hasClass(buttonMatchPlayClass)) {
        $(buttonPlayId).removeClass(buttonMatchPlayClass);
    }
    if ($(buttonPlayId).hasClass(buttonMatchPauseClass)) {
        $(buttonPlayId).removeClass(buttonMatchPauseClass);
    }
    if ($(buttonPlayId).hasClass(buttonMatchReplayClass)) {
        $(buttonPlayId).removeClass(buttonMatchReplayClass);
    }
};

const setPlayerTime = function(coeff) {
    player1.update(coeff);
    player2.update(coeff);
};

const getCurrentCoeff = function() {
    const currentTime = new Date().getTime();
    return Math.min(Math.max((currentTime - startMachTime) / durationMatch, 0), 1);
};

const updateMatch = function() {
    if (isDragging || pause) {
        return;
    }
    const coeff = getCurrentCoeff();
    setProgress(coeff);
    setPlayerTime(coeff);
    if (coeff >= 1) {
        machEnded = true;
        removeClassesButtonPlay();
        if (!$(buttonPlayId).hasClass(buttonMatchReplayClass)) {
            $(buttonPlayId).addClass(buttonMatchReplayClass);
        }
    } else {
        machEnded = false;
    }
};

const setTimeMatch = function(coeff) {
    const currentTime = new Date().getTime();
    const t = Math.min(Math.max(coeff, 0), 1) * durationMatch;
    startMachTime = currentTime - t;
    setPlayerTime(coeff);
};

const triggerMatch = function(positions1, positions2) {
    player1.setPositions(positions1);
    player2.setPositions(positions2);
    player1.show();
    player2.show();

    setContainerSize();

    durationMatch = Math.min(positions1.length, positions2.length) * 1000;

    startMachTime = new Date().getTime();

    if (intervalId !== null) {
        clearInterval(intervalId);
    }
    intervalId = setInterval(updateMatch, millisecondPerFrame);

    $('#button-beginning').prop('disabled', false);
    $('#button-prev').prop('disabled', false);
    $(buttonPlayId).prop('disabled', false);
    $('#button-next').prop('disabled', false);
    $('#button-end').prop('disabled', false);

    removeClassesButtonPlay();
    if (!$(buttonPlayId).hasClass(buttonMatchPauseClass)) {
        $(buttonPlayId).addClass(buttonMatchPauseClass);
    }

    matchStarted = true;
    machEnded = false;
    pause = false;
    coeffSaved = 0;
};

// PROGRESS BAR

let isDragging = false;
let initialX = null;
let initialY = null;
let containerSize = null;

const progressContainerId = '#progress-container';

const setContainerSize = function() {
    containerSize = $(progressContainerId).width();
};

const setProgress = function(coeff) {
    $('#progress-bar-match')[0].style.width = `${Math.min(Math.max(coeff, 0), 1) * containerSize}px`;
};

const updateProgress = function(coeff) {
    setProgress(coeff);
    setTimeMatch(coeff);
};

const startDrag = function(e) {
    isDragging = true;
    initialX = $(progressContainerId)[0].getBoundingClientRect().left;
    initialY = $(progressContainerId)[0].getBoundingClientRect().top;
    setContainerSize();
    $(progressContainerId)[0].style.cursor = 'grabbing';
    if (matchStarted) {
        const coeff = (e.clientX - initialX) / containerSize;
        updateProgress(coeff);
        if (coeff >= 1) {
            machEnded = true;
            removeClassesButtonPlay();
            if (!$(buttonPlayId).hasClass(buttonMatchReplayClass)) {
                $(buttonPlayId).addClass(buttonMatchReplayClass);
            }
        } else {
            machEnded = false;
            removeClassesButtonPlay();
            if (pause) {
                if (!$(buttonPlayId).hasClass(buttonMatchPlayClass)) {
                    $(buttonPlayId).addClass(buttonMatchPlayClass);
                }
            } else if (!$(buttonPlayId).hasClass(buttonMatchPauseClass)) {
                $(buttonPlayId).addClass(buttonMatchPauseClass);
            } else {
                // Nothing to do
            }
        }
    }
};

const drag = function(e) {
    if (isDragging && matchStarted) {
        const coeff = Math.min(Math.max((e.clientX - initialX) / containerSize, 0), 1);
        updateProgress(coeff);
        if (coeff >= 1) {
            machEnded = true;
            removeClassesButtonPlay();
            if (!$(buttonPlayId).hasClass(buttonMatchReplayClass)) {
                $(buttonPlayId).addClass(buttonMatchReplayClass);
            }
        } else {
            machEnded = false;
            removeClassesButtonPlay();
            if (pause) {
                if (!$(buttonPlayId).hasClass(buttonMatchPlayClass)) {
                    $(buttonPlayId).addClass(buttonMatchPlayClass);
                }
            } else if (!$(buttonPlayId).hasClass(buttonMatchPauseClass)) {
                $(buttonPlayId).addClass(buttonMatchPauseClass);
            } else {
                // Nothing to do
            }
        }
    }
};

const stopDrag = function(e) {
    if (isDragging && matchStarted) {
        coeffSaved = (e.clientX - initialX) / containerSize;
        updateProgress(coeffSaved);
    }
    $(progressContainerId)[0].style.cursor = 'grab';
    isDragging = false;
};

$(document).ready(function() {
    $(progressContainerId)[0].addEventListener('mousedown', startDrag);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', stopDrag);
    $(progressContainerId)[0].style.cursor = 'grab';
    $('#button-beginning').on('click', function() {
        coeffSaved = 0;
        setTimeMatch(coeffSaved);
        setProgress(coeffSaved);
        removeClassesButtonPlay();
        if (pause) {
            if (!$(buttonPlayId).hasClass(buttonMatchPlayClass)) {
                $(buttonPlayId).addClass(buttonMatchPlayClass);
            }
        } else if (!$(buttonPlayId).hasClass(buttonMatchPauseClass)) {
            $(buttonPlayId).addClass(buttonMatchPauseClass);
        } else {
            // Nothing to do
        }
        machEnded = false;
    });
    $(buttonPlayId).on('click', function() {
        if (machEnded) {
            machEnded = false;
            pause = false;
            updateProgress(0);
            removeClassesButtonPlay();
            if (!$(buttonPlayId).hasClass(buttonMatchPauseClass)) {
                $(buttonPlayId).addClass(buttonMatchPauseClass);
            }
        } else {
            pause = !pause;
            removeClassesButtonPlay();
            if (pause) {
                if (!$(buttonPlayId).hasClass(buttonMatchPlayClass)) {
                    $(buttonPlayId).addClass(buttonMatchPlayClass);
                }
                coeffSaved = getCurrentCoeff();
            } else {
                if (!$(buttonPlayId).hasClass(buttonMatchPauseClass)) {
                    $(buttonPlayId).addClass(buttonMatchPauseClass);
                }
                updateProgress(coeffSaved);
            }
        }
    });
    $('#button-end').on('click', function() {
        coeffSaved = 1;
        setTimeMatch(coeffSaved);
        setProgress(coeffSaved);
        removeClassesButtonPlay();
        $(buttonPlayId).addClass(buttonMatchReplayClass);
        machEnded = true;
    });
});
