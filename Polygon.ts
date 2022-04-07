import { Point } from './Point.js';
import { Vector } from './Vector.js';

export class Polygon {
	vertices: Point[];
	constructor(list: Point[]) {
		this.vertices = list;
	}

	add(vector: Vector) {
		return new Polygon(this.vertices.map((vertex) => vertex.add(vector)));
	}

	subtract(vector: Vector) {
		return new Polygon(this.vertices.map((vertex) => vertex.subtract(vector)));
	}
}
