from math import sin, cos

import Polygon

class Matrix:
    @staticmethod
    def rotateX(p, angle: float):
        if isinstance(p, Polygon):
            return type(p)([Matrix.rotateX(p, angle) for p in p.vertices])
        return type(p)(
            p.x,
            p.y * cos(angle) - p.z * sin(angle),
            p.y * sin(angle) + p.z * cos(angle),
        )

    @staticmethod
    def rotateY(p, angle: float):
        if isinstance(p, Polygon):
            return type(p)([Matrix.rotateY(p, angle) for p in p.vertices])
        return type(p)(
            p.x * cos(angle) + p.z * sin(angle),
            p.y,
            -p.x * sin(angle) + p.z * cos(angle),
        )
