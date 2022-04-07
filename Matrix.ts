import { Point } from './Point.js';
import { Polygon } from './Polygon.js';
import { Vector } from './Vector.js';

export class Matrix {
	static rotateX(p: Point, angle: number): Point;
	static rotateX(p: Vector, angle: number): Vector;
	static rotateX(p: Polygon, angle: number): Polygon;
	static rotateX(
		p: Point | Vector | Polygon,
		angle: number
	): Point | Vector | Polygon {
		if (p instanceof Polygon) {
			const newVertices = p.vertices.map((vertex) =>
				Matrix.rotateX(vertex, angle)
			);
			return new Polygon(newVertices);
		} else {
			// eslint-disable-next-line prefer-destructuring
			const x = p.x;
			const y = p.y * Math.cos(angle) - p.z * Math.sin(angle);
			const z = p.y * Math.sin(angle) + p.z * Math.cos(angle);

			if (p instanceof Point) {
				return new Point(x, y, z);
			} else if (p instanceof Vector) {
				return new Vector(x, y, z);
			} else {
				throw new TypeError('p is not a Point, Vector, or Polygon');
			}
		}
	}

	static rotateY(p: Point, angle: number): Point;
	static rotateY(p: Vector, angle: number): Vector;
	static rotateY(p: Polygon, angle: number): Polygon;
	static rotateY(
		p: Point | Vector | Polygon,
		angle: number
	): Point | Vector | Polygon {
		if (p instanceof Polygon) {
			const newVertices = p.vertices.map((vertex) =>
				Matrix.rotateY(vertex, angle)
			);
			return new Polygon(newVertices);
		} else {
			const x = p.x * Math.cos(angle) + p.z * Math.sin(angle);
			// eslint-disable-next-line prefer-destructuring
			const y = p.y;
			const z = -p.x * Math.sin(angle) + p.z * Math.cos(angle);

			if (p instanceof Point) {
				return new Point(x, y, z);
			} else if (p instanceof Vector) {
				return new Vector(x, y, z);
			} else {
				throw new TypeError('p is not a Point, Vector, or Polygon');
			}
		}
	}
}
