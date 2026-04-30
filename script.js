/**
 * Simmi vCard — Matrix Rain
 * Klassischer grüner Matrix-Code-Regen auf schwarzem Hintergrund.
 */

const canvas = document.getElementById('landscape-canvas');
const ctx = canvas.getContext('2d');

let W, H, DPR;
const chars = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ{}[]<>()/\\|!@#$%^&*_+-=~';

const COLUMNS = [];
const FONT_SIZE = 14;
const FALL_SPEED = 0.8;

/* ─── RESIZE ─── */
function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = canvas.width  = Math.floor(window.innerWidth  * DPR);
    H = canvas.height = Math.floor(window.innerHeight * DPR);
    canvas.style.width  = window.innerWidth  + 'px';
    canvas.style.height = window.innerHeight + 'px';
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    initColumns();
}
window.addEventListener('resize', resize);

function initColumns() {
    const cols = Math.ceil(window.innerWidth / FONT_SIZE);
    COLUMNS.length = 0;
    for (let i = 0; i < cols; i++) {
        COLUMNS.push({
            x: i * FONT_SIZE,
            y: Math.random() * -window.innerHeight,
            speed: FALL_SPEED + Math.random() * 1,
            length: 200 + Math.random() * 20,
            chars: [],
            lastUpdate: 0,
        });
    }
}

/* ─── MATRIX RAIN ─── */
function drawMatrix() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, window.innerWidth, window.innerHeight);

    ctx.font = `${FONT_SIZE}px "Courier New", monospace`;

    for (let c = 0; c < COLUMNS.length; c++) {
        const col = COLUMNS[c];
        col.y += col.speed;

        // Reset when off-screen
        if (col.y - col.length * FONT_SIZE > window.innerHeight) {
            col.y = -FONT_SIZE * (Math.random() * 10);
            col.speed = FALL_SPEED + Math.random() * 2;
            col.length = 8 + Math.random() * 20;
        }

        // Generate new characters
        for (let i = 0; i < Math.ceil(col.speed * 1.5); i++) {
            col.chars.unshift(chars[Math.floor(Math.random() * chars.length)]);
        }
        if (col.chars.length > col.length + 5) {
            col.chars.length = col.length + 5;
        }

        // Draw each character in the column
        for (let i = 0; i < col.chars.length && i < col.length + 5; i++) {
            const y = col.y - i * FONT_SIZE;
            if (y < -FONT_SIZE || y > window.innerHeight + FONT_SIZE) continue;

            const alpha = 1 - (i / (col.length + 5)) * 0.85;

            if (i === 0) {
                // Leading character — bright white/green
                ctx.fillStyle = `rgba(200, 255, 220, ${alpha})`;
            } else if (i < 3) {
                ctx.fillStyle = `rgba(100, 255, 100, ${alpha})`;
            } else {
                ctx.fillStyle = `rgba(0, 200, 50, ${alpha * 0.6})`;
            }

            ctx.fillText(col.chars[i], col.x, y);
        }
    }
}

/* ─── MAIN LOOP ─── */
function tick() {
    drawMatrix();
    requestAnimationFrame(tick);
}

/* Init */
resize();
tick();
