import { Point } from './Point.js';
import { Vector } from './Vector.js';

export class Polygon {
	vertices: Point[];
	constructor(list: Point[]) {
		this.vertices = list;
	}

	add(vector: Vector) {
		for (let i = 0; i < this.vertices.length; i += 1) {
			this.vertices[i].add(vector);
		}
	}

	subtract(vector: Vector) {
		for (let i = 0; i < this.vertices.length; i += 1) {
			this.vertices[i].subtract(vector);
		}
	}
}
