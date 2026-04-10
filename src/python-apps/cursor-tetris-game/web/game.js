(() => {
  'use strict';

  // Canvas & board sizing (logical pixels; canvas uses DPR scaling).
  const COLS = 10;
  const ROWS = 20;
  const BLOCK_SIZE = 30; // logical
  const DROP_INTERVAL_MS = 700;

  // Tetromino definitions as 4x4 matrices.
  // 1s mean "occupied"; color is stored separately.
  const TETROMINOES = [
    {
      name: 'I',
      color: '#00E5FF',
      matrix: [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
      ],
    },
    {
      name: 'O',
      color: '#FFD500',
      matrix: [
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
      ],
    },
    {
      name: 'T',
      color: '#B400FF',
      matrix: [
        [0, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
      ],
    },
    {
      name: 'S',
      color: '#00E676',
      matrix: [
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
      ],
    },
    {
      name: 'Z',
      color: '#FF1744',
      matrix: [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
      ],
    },
    {
      name: 'J',
      color: '#3F51B5',
      matrix: [
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
      ],
    },
    {
      name: 'L',
      color: '#FF9100',
      matrix: [
        [0, 0, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
      ],
    },
  ];

  const canvas = document.getElementById('game');
  const scoreEl = document.getElementById('score');
  const overlay = document.getElementById('overlay');
  const overlayText = document.getElementById('overlayText');
  const overlayHint = document.getElementById('overlayHint');
  const ctx = canvas.getContext('2d');

  function setOverlay(visible, text, hint) {
    overlay.classList.toggle('hidden', !visible);
    if (text != null) overlayText.textContent = text;
    if (hint != null) overlayHint.innerHTML = hint;
  }

  function createEmptyBoard() {
    // board[y][x] -> color string or null
    const b = [];
    for (let y = 0; y < ROWS; y++) {
      const row = [];
      for (let x = 0; x < COLS; x++) row.push(null);
      b.push(row);
    }
    return b;
  }

  function cloneMatrix(m) {
    return m.map((row) => row.slice());
  }

  function rotateMatrixCW(m) {
    const N = m.length;
    const res = Array.from({ length: N }, () => Array(N).fill(0));
    for (let y = 0; y < N; y++) {
      for (let x = 0; x < N; x++) {
        res[x][N - 1 - y] = m[y][x];
      }
    }
    return res;
  }

  let board = createEmptyBoard();
  let current = null; // { matrix, x, y, color }
  let paused = false;
  let gameOver = false;
  let score = 0;

  function setScore(next) {
    score = next;
    scoreEl.textContent = String(score);
  }

  const dpr = window.devicePixelRatio || 1;
  const logicalW = COLS * BLOCK_SIZE;
  const logicalH = ROWS * BLOCK_SIZE;
  canvas.style.width = `${logicalW}px`;
  canvas.style.height = `${logicalH}px`;
  canvas.width = Math.floor(logicalW * dpr);
  canvas.height = Math.floor(logicalH * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

  function collides(piece, dx = 0, dy = 0) {
    const m = piece.matrix;
    for (let y = 0; y < 4; y++) {
      for (let x = 0; x < 4; x++) {
        if (!m[y][x]) continue;
        const nx = piece.x + x + dx;
        const ny = piece.y + y + dy;
        // Walls & floor are solid.
        if (nx < 0 || nx >= COLS) return true;
        if (ny >= ROWS) return true;
        // Ceiling is not solid; pieces spawn above the visible area.
        if (ny >= 0 && board[ny][nx]) return true;
      }
    }
    return false;
  }

  function spawnPiece() {
    const tpl = TETROMINOES[Math.floor(Math.random() * TETROMINOES.length)];
    current = {
      matrix: cloneMatrix(tpl.matrix),
      x: Math.floor(COLS / 2) - 2,
      y: -2,
      color: tpl.color,
    };
    if (collides(current, 0, 0)) {
      gameOver = true;
      paused = false;
      setOverlay(true, 'Game Over', 'Press <b>R</b> to restart.');
    }
  }

  function lockPiece() {
    const m = current.matrix;
    for (let y = 0; y < 4; y++) {
      for (let x = 0; x < 4; x++) {
        if (!m[y][x]) continue;
        const nx = current.x + x;
        const ny = current.y + y;
        if (ny < 0) continue; // If it locks above the board, gameOver will already trigger on spawn collision.
        if (ny >= 0 && ny < ROWS && nx >= 0 && nx < COLS) {
          board[ny][nx] = current.color;
        }
      }
    }
  }

  function clearLines() {
    let cleared = 0;
    for (let y = ROWS - 1; y >= 0; y--) {
      if (board[y].every((cell) => cell != null)) {
        board.splice(y, 1);
        const newRow = Array.from({ length: COLS }, () => null);
        board.unshift(newRow);
        cleared++;
        y++; // re-check same y index after shifting
      }
    }
    return cleared;
  }

  function tryMove(dx, dy) {
    if (!collides(current, dx, dy)) {
      current.x += dx;
      current.y += dy;
      return true;
    }
    return false;
  }

  function tryRotate() {
    const rotated = rotateMatrixCW(current.matrix);
    const prev = current.matrix;
    current.matrix = rotated;
    if (collides(current, 0, 0)) {
      current.matrix = prev;
      return false;
    }
    return true;
  }

  function stepDown() {
    if (tryMove(0, 1)) return true;
    // Can't move down => lock.
    lockPiece();
    const cleared = clearLines();
    if (cleared > 0) setScore(score + cleared * 100);
    spawnPiece();
    return false;
  }

  function softDropOnce() {
    if (gameOver || paused) return;
    // One row per key press (browser key repeat can drive continuous soft drop).
    if (tryMove(0, 1)) {
      setScore(score + 1);
    } else {
      lockPiece();
      const cleared = clearLines();
      if (cleared > 0) setScore(score + cleared * 100);
      spawnPiece();
    }
  }

  function hardDrop() {
    if (gameOver || paused) return;
    let moved = 0;
    while (!collides(current, 0, 1)) {
      current.y += 1;
      moved += 1;
    }
    if (moved > 0) setScore(score + moved * 2);
    lockPiece();
    const cleared = clearLines();
    if (cleared > 0) setScore(score + cleared * 100);
    spawnPiece();
  }

  function restart() {
    board = createEmptyBoard();
    current = null;
    paused = false;
    gameOver = false;
    setScore(0);
    setOverlay(false);
    spawnPiece();
  }

  function togglePause() {
    if (gameOver) return;
    paused = !paused;
    if (paused) {
      setOverlay(true, 'Paused', 'Press <b>P</b> to resume.');
    } else {
      setOverlay(false);
    }
  }

  function drawBlock(x, y, color) {
    const px = x * BLOCK_SIZE;
    const py = y * BLOCK_SIZE;
    ctx.fillStyle = color;
    ctx.fillRect(px, py, BLOCK_SIZE, BLOCK_SIZE);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.18)';
    ctx.strokeRect(px + 0.5, py + 0.5, BLOCK_SIZE - 1, BLOCK_SIZE - 1);
  }

  function draw() {
    // Background
    ctx.clearRect(0, 0, logicalW, logicalH);
    ctx.fillStyle = '#0b1020';
    ctx.fillRect(0, 0, logicalW, logicalH);

    // Grid lines
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.06)';
    ctx.lineWidth = 1;
    for (let x = 0; x <= COLS; x++) {
      ctx.beginPath();
      ctx.moveTo(x * BLOCK_SIZE, 0);
      ctx.lineTo(x * BLOCK_SIZE, logicalH);
      ctx.stroke();
    }
    for (let y = 0; y <= ROWS; y++) {
      ctx.beginPath();
      ctx.moveTo(0, y * BLOCK_SIZE);
      ctx.lineTo(logicalW, y * BLOCK_SIZE);
      ctx.stroke();
    }

    // Locked blocks
    for (let y = 0; y < ROWS; y++) {
      for (let x = 0; x < COLS; x++) {
        const color = board[y][x];
        if (color) drawBlock(x, y, color);
      }
    }

    // Active piece
    if (current) {
      const m = current.matrix;
      for (let y = 0; y < 4; y++) {
        for (let x = 0; x < 4; x++) {
          if (!m[y][x]) continue;
          const nx = current.x + x;
          const ny = current.y + y;
          if (ny < 0) continue;
          drawBlock(nx, ny, current.color);
        }
      }
    }
  }

  // Input
  window.addEventListener('keydown', (e) => {
    // Prevent arrow keys from scrolling.
    if (
      e.key === 'ArrowLeft' ||
      e.key === 'ArrowRight' ||
      e.key === 'ArrowDown' ||
      e.key === 'ArrowUp' ||
      e.key === ' '
    ) {
      e.preventDefault();
    }

    if (e.key === 'p' || e.key === 'P') {
      togglePause();
      return;
    }
    if (e.key === 'r' || e.key === 'R') {
      restart();
      return;
    }

    if (gameOver || paused) return;

    if (e.key === 'ArrowLeft') tryMove(-1, 0);
    else if (e.key === 'ArrowRight') tryMove(1, 0);
    else if (e.key === 'ArrowDown') softDropOnce();
    else if (e.key === 'ArrowUp') tryRotate();
    else if (e.key === ' ') hardDrop();
  });

  // Main loop
  let lastTs = 0;
  let dropAccum = 0;

  function loop(ts) {
    if (!lastTs) lastTs = ts;
    const dt = ts - lastTs;
    lastTs = ts;

    if (!paused && !gameOver) {
      dropAccum += dt;
      while (dropAccum >= DROP_INTERVAL_MS) {
        dropAccum -= DROP_INTERVAL_MS;
        stepDown();
        if (gameOver) {
          dropAccum = 0;
          break;
        }
      }
    }

    draw();
    requestAnimationFrame(loop);
  }

  // Start
  setScore(0);
  setOverlay(false);
  spawnPiece();
  requestAnimationFrame(loop);
})();

