
export class Vector {
	x = 0;
	y = 0;
	z = 0;

	constructor();
	constructor(x: number, y: number, z: number);
	constructor(x?: number, y?: number, z?: number) {
		this.x = x ?? 0;
		this.y = y ?? 0;
		this.z = z ?? 0;
	}

	add({ x, y, z }: Vector) {
		this.x += x;
		this.y += y;
		this.z += z;
	}

	multiply(scalar: number) {
		this.x *= scalar;
		this.y *= scalar;
		this.z *= scalar;
	}

	divide(scalar: number) {
		this.x /= scalar;
		this.y /= scalar;
		this.z /= scalar;
	}
}
