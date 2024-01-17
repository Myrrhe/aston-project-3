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
const blockOutputId = '#block-output';

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

// Grid
const gridGraphics = new window.PIXI.Graphics();

const cellSize = width / gridWidth;
const gridColor = 0xffffff;
// ffd2e9
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

        // Initial position
        this.graphicsBack.moveTo(
            posX,
            posY,
        );
        this.graphicsFront.moveTo(
            posX,
            posY,
        );

        const nbPoints = Math.floor(coeff * (this.positions.length - 1));

        const coeffDraw = coeff * (this.positions.length - 1) - nbPoints;

        if (this.positions.length > 1) {
            // We add the points completely passed
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

            // We add one last point half passed
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
        } else {
            this.graphicsBack.lineTo(
                posX - 1,
                posY,
            );
            this.graphicsFront.lineTo(
                posX - 1,
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
let nbIterMatch = null;
let matchStarted = false;
let matchEnded = false;
let pause = false;
let coeffSaved = 0;

const buttonPlayId = '#button-play';
const fightResultId = '#fight-result';
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

const setMatchEnd = function(coeff) {
    removeClassesButtonPlay();
    if (coeff >= 1) {
        matchEnded = true;
        if (!$(buttonPlayId).hasClass(buttonMatchReplayClass)) {
            $(buttonPlayId).addClass(buttonMatchReplayClass);
        }
        if ($(fightResultId).hasClass('d-none')) {
            $(fightResultId).removeClass('d-none');
        }
    } else {
        matchEnded = false;
        setPauseButton();
        if (!$(fightResultId).hasClass('d-none')) {
            $(fightResultId).addClass('d-none');
        }
    }
};

const setPauseButton = function() {
    if (pause) {
        if (!$(buttonPlayId).hasClass(buttonMatchPlayClass)) {
            $(buttonPlayId).addClass(buttonMatchPlayClass);
        }
    } else if (!$(buttonPlayId).hasClass(buttonMatchPauseClass)) {
        $(buttonPlayId).addClass(buttonMatchPauseClass);
    } else {
        // Nothing to do
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
    setMatchEnd(coeff);
};

const setTimeMatch = function(coeff) {
    const currentTime = new Date().getTime();
    const t = Math.min(Math.max(coeff, 0), 1) * durationMatch;
    startMachTime = currentTime - t;
    setPlayerTime(coeff);
};

const setupMatch = function(data) {
    const positions = data['match_movements'].split('|').map(s =>
        s.split(';').map(function(p) {
            const [x, y] = p.split(',');
            return {'x': parseInt(x, 10), 'y': parseInt(y, 10)};
    }));

    const len1 = positions[0].length;
    const len2 = positions[1].length;

    const lenMatch = Math.min(len1, len2);

    if (len1 > len2) {
        positions[0].splice(len2 - len1);
    } else if (len2 > len1) {
        positions[1].splice(len1 - len2);
    } else {
        // The arrays are already the same size
    }

    if (data['match_result'] !== '') {
        if (data['match_result']) {
            $('#fight-result').html(`${data['bot_name']} a gagné !`);
        } else {
            $('#fight-result').html(`${data['bot_name']} a perdu :(`);
        }
    }

    // Logging
    $(blockOutputId).empty();
    if ($(blockOutputId).hasClass('d-none')) {
        $(blockOutputId).removeClass('d-none');
    }

    const firstErrPlayer1 = data['stderr'][0].shift() ?? [];
    const firstErrPlayer2 = data['stderr'][1].shift() ?? [];

    let startWrite = false;

    if (firstErrPlayer1.length > 0 || firstErrPlayer2.length) {
        const blockOneOutput = $('<div></div>');

        const blockRound = $(`<div class='text-color-fore pb-2 fw-bold fs-6'>0/${lenMatch}</div>`);
        blockRound.appendTo(blockOneOutput);

        // 1
        const blocStderr1 = $('<div class=\'pb-1\'></div>');

        const errorTitlePlayer1 = $('<div class=\'text-color-bright fw-bold\'>Sortie d\'erreur :</div>');
        errorTitlePlayer1.appendTo(blocStderr1);

        const blocStderrContent1 = $('<div class=\'text-color-alert\'></div>');
        if (firstErrPlayer1.length > 0) {
            for (const err of firstErrPlayer1) {
                if (err !== null) {
                    const lineError = $(`<div class='output-line'>${err}</div>`);
                    lineError.appendTo(blocStderrContent1);
                }
            }
        }

        blocStderrContent1.appendTo(blocStderr1);
        blocStderr1.appendTo(blockOneOutput);

        // 2
        const blocStderr2 = $('<div class=\'pb-1\'></div>');

        const errorTitlePlayer2 = $('<div class=\'text-color-bright-alt fw-bold\'>Sortie d\'erreur :</div>');
        errorTitlePlayer2.appendTo(blocStderr2);

        const blocStderrContent2 = $('<div class=\'text-color-alert\'></div>');
        if (firstErrPlayer2.length > 0) {
            for (const err of firstErrPlayer2) {
                if (err !== null) {
                    const lineError = $(`<div class='output-line'>${err}</div>`);
                    lineError.appendTo(blocStderrContent2);
                }
            }
        }

        blocStderrContent2.appendTo(blocStderr2);
        blocStderr2.appendTo(blockOneOutput);

        blockOneOutput.appendTo(blockOutputId);

        startWrite = true;
    }

    for (let i = 0; i < lenMatch; i++) {
        const blockOneOutput = $('<div></div>');

        if (startWrite) {
            const separatorLine = $('<hr class=\'hr\' />');
            separatorLine.appendTo(blockOneOutput);
        }

        const blockRound = $(`<div class='text-color-fore pb-2 fw-bold fs-6'>${i + 1}/${lenMatch}</div>`);
        blockRound.appendTo(blockOneOutput);

        // 1
        const blockPlayer1 = $('<div class=\'pb-1\'></div>');
        const blocStderr1 = $('<div class=\'pb-1\'></div>');

        const errorTitlePlayer1 = $('<div class=\'text-color-bright fw-bold\'>Sortie d\'erreur :</div>');
        errorTitlePlayer1.appendTo(blocStderr1);

        const blocStderrContent1 = $('<div class=\'text-color-alert\'></div>');
        if (i < data['stderr'][0].length) {
            for (const err of data['stderr'][0][i]) {
                if (err !== null) {
                    const lineError = $(`<div class='output-line'>${err}</div>`);
                    lineError.appendTo(blocStderrContent1);
                }
            }
        }

        blocStderrContent1.appendTo(blocStderr1);
        blocStderr1.appendTo(blockPlayer1);

        const blocStdout1 = $('<div class=\'pb-1\'></div>');
        const outputTitlePlayer1 = $('<div class=\'text-color-bright fw-bold\'>Sortie standard :</div>');
        outputTitlePlayer1.appendTo(blocStdout1);

        const lineOutputPlayer1 = $(`<div class='text-color-fore output-line'>${data['stdout'][0][i]}</div>`);
        lineOutputPlayer1.appendTo(blocStdout1);

        blocStdout1.appendTo(blockPlayer1);

        blockPlayer1.appendTo(blockOneOutput);

        // 2
        const blockPlayer2 = $('<div class=\'pb-1\'></div>');
        const blocStderr2 = $('<div class=\'pb-1\'></div>');

        const errorTitlePlayer2 = $('<div class=\'text-color-bright-alt fw-bold\'>Sortie d\'erreur :</div>');
        errorTitlePlayer2.appendTo(blocStderr2);

        const blocStderrContent2 = $('<div class=\'text-color-alert\'></div>');
        if (i < data['stderr'][1].length) {
            for (const err of data['stderr'][1][i]) {
                if (err !== null) {
                    const lineError = $(`<div class='output-line'>${err}</div>`);
                    lineError.appendTo(blocStderrContent2);
                }
            }
        }

        blocStderrContent2.appendTo(blocStderr2);
        blocStderr2.appendTo(blockPlayer2);

        const blocStdout2 = $('<div class=\'pb-1\'></div>');
        const outputTitlePlayer2 = $('<div class=\'text-color-bright-alt fw-bold\'>Sortie standard :</div>');
        outputTitlePlayer2.appendTo(blocStdout2);

        const lineOutputPlayer2 = $(`<div class='text-color-fore output-line'>${data['stdout'][1][i]}</div>`);
        lineOutputPlayer2.appendTo(blocStdout2);

        blocStdout2.appendTo(blockPlayer2);

        blockPlayer2.appendTo(blockOneOutput);

        blockOneOutput.appendTo(blockOutputId);

        startWrite = true;
    }
    
    return positions;
}

const triggerMatch = function(positions1, positions2) {
    player1.setPositions(positions1);
    player2.setPositions(positions2);
    player1.show();
    player2.show();

    setContainerSize();

    nbIterMatch = Math.min(positions1.length, positions2.length);

    durationMatch = nbIterMatch * 1000;

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

    setMatchEnd(0);

    matchStarted = true;
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
        setMatchEnd(coeff);
    }
};

const drag = function(e) {
    if (isDragging && matchStarted) {
        const coeff = Math.min(Math.max((e.clientX - initialX) / containerSize, 0), 1);
        updateProgress(coeff);
        setMatchEnd(coeff);
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
        setMatchEnd(0);
    });

    $('#button-prev').on('click', function() {
        if (pause) {
            coeffSaved = Math.max(coeffSaved - 1.0/(nbIterMatch - 1), 0);
        } else {
            coeffSaved = Math.max(getCurrentCoeff() - 1.0/(nbIterMatch - 1), 0);
        }
        pause = true;
        updateProgress(coeffSaved);
        removeClassesButtonPlay();
        setPauseButton();
    });
    $(buttonPlayId).on('click', function() {
        removeClassesButtonPlay();
        if (matchEnded) {
            setMatchEnd(0);
            pause = false;
            updateProgress(0);
        } else {
            pause = !pause;
            if (pause) {
                coeffSaved = getCurrentCoeff();
            } else {
                updateProgress(coeffSaved);
            }
        }
        setPauseButton();
    });
    $('#button-next').on('click', function() {
        if (pause) {
            coeffSaved = Math.min(coeffSaved + 1.0/(nbIterMatch - 1), 1);
        } else {
            coeffSaved = Math.min(getCurrentCoeff() + 1.0/(nbIterMatch - 1), 1);
        }
        pause = true;
        updateProgress(coeffSaved);
        removeClassesButtonPlay();
        setPauseButton();
        setMatchEnd(coeffSaved);
    });
    $('#button-end').on('click', function() {
        coeffSaved = 1;
        setTimeMatch(coeffSaved);
        setProgress(coeffSaved);
        setMatchEnd(1);
    });
});
