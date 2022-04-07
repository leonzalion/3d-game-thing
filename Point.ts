import type { Vector } from './Vector.js';

export class Point {
	static getMidpoint(p: Point, q: Point) {
		return new Point((p.x + q.x) / 2, (p.y + q.y) / 2, (p.z + q.z) / 2);
	}

	x = 0;
	y = 0;
	z = 0;

	constructor(x?: number, y?: number, z?: number) {
		this.x = x ?? 0;
		this.y = y ?? 0;
		this.z = z ?? 0;
	}

	equals(p: Point) {
		return this.x === p.x && this.y === p.y && this.z === p.z;
	}

	add(vector: Vector) {
		const p = new Point(this.x, this.y, this.z);
		p.x += vector.x;
		p.y += vector.y;
		p.z += vector.z;
		return p;
	}

	subtract(vector: Vector) {
		const p = new Point(this.x, this.y, this.z);
		p.x -= vector.x;
		p.y -= vector.y;
		p.z -= vector.z;
		return p;
	}
}
