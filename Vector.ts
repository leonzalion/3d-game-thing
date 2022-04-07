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
		const v = new Vector(this.x, this.y, this.z);
		v.x += x;
		v.y += y;
		v.z += z;
		return v;
	}

	multiply(scalar: number) {
		const v = new Vector(this.x, this.y, this.z);
		v.x *= scalar;
		v.y *= scalar;
		v.z *= scalar;
		return v;
	}

	divide(scalar: number) {
		const v = new Vector(this.x, this.y, this.z);
		v.x /= scalar;
		v.y /= scalar;
		v.z /= scalar;
		return v;
	}
}
