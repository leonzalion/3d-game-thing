/* eslint-disable max-depth */
/* eslint-disable complexity */
import { Vector } from './Vector.js';
import { Polygon } from './Polygon.js';
import { Point } from './Point.js';
import { Matrix } from './Matrix.js';

// Velocity vectors in pixels per second
const X_VEL = new Vector(500, 0, 0);
const Y_VEL = new Vector(0, 500, 0);
const Z_VEL = new Vector(0, 0, 500);

const FPS = 100;

const MOUSE_SENS_X = 1000;
const MOUSE_SENS_Y = 1500;

const polygons = [
	new Polygon([
		new Point(100, 100, 1000),
		new Point(300, 100, 1000),
		new Point(300, 300, 1000),
		new Point(100, 300, 1000),
	]),
];

let angleX = 0;
let angleY = 0;

let windowWidth = window.innerWidth;
let windowHeight = window.innerHeight;

function isInView(p: Point | Polygon): boolean {
	if (p instanceof Point) {
		return (
			p.z >= 0 &&
			Math.abs(p.x) <= windowWidth + 2 * p.z &&
			Math.abs(p.y) <= windowHeight + 2 * p.z
		);
	} else {
		// true if all four of the polygon's points are in view
		return p.vertices.every((vertex) => isInView(vertex));
	}
}

const canvas = document.querySelector<HTMLCanvasElement>('#canvas')!;
(window as any).lockCursor = () => {
	canvas.requestPointerLock();
};

document.addEventListener('pointerlockchange', () => {
	isCursorLocked = document.pointerLockElement === canvas;
	if (isCursorLocked) {
		document.querySelector<HTMLButtonElement>(
			'#pointerLockButton'
		)!.style.display = 'none';
	} else {
		document.querySelector<HTMLButtonElement>(
			'#pointerLockButton'
		)!.style.display = 'block';
	}
});

function updateWindowWidth() {
	windowWidth = window.innerWidth;
	windowHeight = window.innerHeight;
	canvas.width = windowWidth;
	canvas.height = windowHeight;
}

window.addEventListener('resize', updateWindowWidth);
updateWindowWidth();

const context = canvas.getContext('2d')!;
context.lineWidth = 4;

// Draw a blank 1x1 rectangle
context.fillStyle = 'white';
context.fillRect(canvas.width, canvas.height, 1, 1);

// Set up polygons
for (let x = -1000; x < 1000; x += 200) {
	polygons.push(
		new Polygon([
			new Point(x, 1000, -10_000),
			new Point(x + 50, 1000, -10_000),
			new Point(x + 50, 1000, 10_000),
			new Point(x, 1000, 10_000),
		])
	);
}

// Key pressed states
let leftArrowKeyIsPressed = false;
let rightArrowKeyIsPressed = false;
let upArrowKeyIsPressed = false;
let downArrowKeyIsPressed = false;
let shiftIsPressed = false;
let spaceIsPressed = false;
let isMouseDown = false;
let isCursorLocked = false;
let dx = 0;
let dy = 0; // change in mouse position

window.addEventListener('mousedown', () => {
	isMouseDown = true;
});

window.addEventListener('mouseup', () => {
	isMouseDown = false;
});

window.addEventListener('mousemove', (event) => {
	if (!isCursorLocked && !isMouseDown) return;

	dx = event.movementX;
	dy = event.movementY;
});

const leftArrowKeys = new Set(['a', 'ArrowLeft']);
const rightArrowKeys = new Set(['d', 'e', 'ArrowRight']);
const upArrowKeys = new Set(['w', ',', 'ArrowUp']);
const downArrowKeys = new Set(['s', 'o', 'ArrowDown']);

window.addEventListener('keydown', (event) => {
	const { key } = event;
	if (leftArrowKeys.has(key)) leftArrowKeyIsPressed = true;
	else if (rightArrowKeys.has(key)) rightArrowKeyIsPressed = true;
	else if (upArrowKeys.has(key)) upArrowKeyIsPressed = true;
	else if (downArrowKeys.has(key)) downArrowKeyIsPressed = true;
	else if (['shift'].includes(key)) shiftIsPressed = true;
	else if (['space'].includes(key)) spaceIsPressed = true;
});

window.addEventListener('keyup', (event) => {
	const { key } = event;
	if (leftArrowKeys.has(key)) leftArrowKeyIsPressed = false;
	else if (rightArrowKeys.has(key)) rightArrowKeyIsPressed = false;
	else if (upArrowKeys.has(key)) upArrowKeyIsPressed = false;
	else if (downArrowKeys.has(key)) downArrowKeyIsPressed = false;
	else if (['shift'].includes(key)) shiftIsPressed = false;
	else if (['space'].includes(key)) spaceIsPressed = false;
});

// Game loop
function render() {
	// Translate each polygon
	for (let [i, polygon] of polygons.entries()) {
		if (leftArrowKeyIsPressed) {
			polygon = polygon.add(Matrix.rotateY(X_VEL.divide(FPS), -angleX));
		}

		if (rightArrowKeyIsPressed) {
			polygon = polygon.subtract(Matrix.rotateY(X_VEL.divide(FPS), -angleX));
		}

		if (upArrowKeyIsPressed) {
			polygon = polygon.subtract(
				Matrix.rotateX(Matrix.rotateY(Z_VEL.divide(FPS), -angleX), angleY)
			);
		}

		if (downArrowKeyIsPressed) {
			polygon = polygon.add(
				Matrix.rotateX(Matrix.rotateY(Z_VEL.divide(FPS), -angleX), angleY)
			);
		}

		if (spaceIsPressed) {
			// Here we add because the positive y-axis is downward
			polygon = polygon.add(Y_VEL.divide(FPS));
		}

		if (shiftIsPressed) {
			// Here we subtract because the positive y-axis is downward
			polygon = polygon.subtract(Y_VEL.divide(FPS));
		}

		polygons[i] = polygon;
	}

	// Set up rotation angles
	angleX += dx / MOUSE_SENS_X;
	angleY += -dy / MOUSE_SENS_Y;

	// Rotate the polygons
	const transformedPolygons: Polygon[] = polygons.map((polygon) => {
		// Here, Matrix.rotateY() rotates about the y-axis.
		// Hence, angleX is passed to rotateY() (up-down view rotation).
		// Similarly, angleY is passed to rotateX() (left-right view rotation)
		polygon = Matrix.rotateY(polygon, angleX);
		polygon = Matrix.rotateX(polygon, angleY);
		return polygon;
	});

	// Clip points to boundary of the viewing frustum
	for (const [i, polygon] of transformedPolygons.entries()) {
		// If one or more of the vertices are out of view,
		// clip the polygon to the viewing frustum
		if (!isInView(polygon)) {
			// All vertices of newPoly will be in the viewing frustum
			const newPoly = new Polygon([]);

			// Number of vertices of the current polygon
			const numVertices = polygon.vertices.length;

			// Loop over the current polgon's vertices
			for (const [j, curPoint] of polygon.vertices.entries()) {
				const nextPoint = polygon.vertices[(j + 1) % numVertices]!;

				if (isInView(curPoint)) {
					newPoly.vertices.push(curPoint);
				}

				// If the points lie across the border of the viewing frustum
				if (isInView(curPoint) !== isInView(nextPoint)) {
					let inView: Point;
					let outOfView: Point;
					if (isInView(curPoint)) {
						[inView, outOfView] = [curPoint, nextPoint];
					} else {
						[inView, outOfView] = [nextPoint, curPoint];
					}

					// Locate the intersection of the line connecting
					// inView and outView with the boundary of the
					// viewing frustum
					for (;;) {
						const midpoint = Point.getMidpoint(inView, outOfView);
						if (midpoint.equals(inView) || midpoint.equals(outOfView)) break;
						else if (isInView(midpoint)) inView = midpoint;
						else outOfView = midpoint;
					}

					const intersectionPoint = inView;

					// Add the intersectionPoint (which is in view) to the new polygon
					newPoly.vertices.push(intersectionPoint);
				}
			}

			// Replace current polygon with clipped polygon
			transformedPolygons[i] = newPoly;
		}
	}

	for (const [_i, polygon] of transformedPolygons.entries()) {
		for (const [_j, _p] of polygon.vertices.entries()) {
			// console.log(`Polygon ${i}, Vertex ${j}: (${p.x},${p.y},${p.z})`);
		}
	}

	// Clear the canvas
	context.clearRect(0, 0, canvas.width, canvas.height);

	// Project the polygons onto the viewing plane
	for (const polygon of transformedPolygons) {
		if (polygon.vertices.length === 0) continue;

		// eslint-disable-next-line @typescript-eslint/no-loop-func
		const xPoints: Point[] = polygon.vertices.map((vertex) => {
			const xPoint = new Point();

			// Scale the point according to how far away from the viewing plane it is (z coordinate)
			xPoint.x = (vertex.x * windowWidth) / (windowWidth + 2 * vertex.z);
			xPoint.y = (vertex.y * windowHeight) / (windowHeight + 2 * vertex.z);

			// Translate from game coordinates to screen coordinates
			xPoint.x += windowWidth / 2;
			xPoint.y += windowHeight / 2;

			return xPoint;
		});

		// Fill in a polygon connecting each of the points
		context.beginPath();
		context.moveTo(xPoints[0]!.x, xPoints[0]!.y);

		for (const vertex of xPoints.slice(1)) {
			context.lineTo(vertex.x, vertex.y);
		}

		context.closePath();
		context.fillStyle = 'black';
		context.fill();
	}

	// Reset rotation variables
	dx = 0;
	dy = 0;

	// Pause for a bit
	requestAnimationFrame(render);
}

render();
