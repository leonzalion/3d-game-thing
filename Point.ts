import { Vector } from './Vector.js';

export class Point {
	x = 0;
	y = 0;
	z = 0;

	constructor(x?: number, y?: number, z?: number) {
		this.x = x ?? 0;
		this.y = y ?? 0;
		this.z = z ?? 0;
	}

	getMidpoint(p: Point, q: Point) {
		return new Point(
			(p.x + q.x) / 2,
			(p.y + q.y) / 2,
			(p.z + q.z) / 2
		);
	}

	equals(p: Point) {
		return this.x === p.x && this.y === p.y && this.z === p.z;
	}

	add(vector: Vector) {
		this.x += vector.x;
		this.y += vector.y;
		this.z += vector.z;
	}

	subtract(vector: Vector) {
		this.x -= vector.x;
		this.y -= vector.y;
		this.z -= vector.z;
	}
}
