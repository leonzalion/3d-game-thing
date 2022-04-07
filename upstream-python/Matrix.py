from math import sin, cos
from typing import overload, Union

from Polygon import Polygon
from Point import Point
from Vector import Vector

class Matrix:
    @overload
    @staticmethod
    def rotateX(p: Polygon, angle: float) -> Polygon: ...

    @overload
    @staticmethod
    def rotateX(p: Point, angle: float) -> Point: ...

    @overload
    @staticmethod
    def rotateX(p: Vector, angle: float) -> Vector: ...

    @staticmethod
    def rotateX(p: Union[Polygon, Point, Vector], angle: float) -> Union[Polygon, Point, Vector]:
        if isinstance(p, Polygon):
            return type(p)([Matrix.rotateX(p, angle) for p in p.vertices])
        return type(p)(
            int(p.x),
            int(p.y * cos(angle) - p.z * sin(angle)),
            int(p.y * sin(angle) + p.z * cos(angle)),
        )

    @overload
    @staticmethod
    def rotateY(p: Polygon, angle: float) -> Polygon: ...

    @overload
    @staticmethod
    def rotateY(p: Point, angle: float) -> Point: ...

    @overload
    @staticmethod
    def rotateY(p: Vector, angle: float) -> Vector: ...

    @staticmethod
    def rotateY(p: Union[Polygon, Point, Vector], angle: float) -> Union[Polygon, Point, Vector]:
        if isinstance(p, Polygon):
            return type(p)([Matrix.rotateY(p, angle) for p in p.vertices])
        return type(p)(
            int(p.x * cos(angle) + p.z * sin(angle)),
            int(p.y),
            int(-p.x * sin(angle) + p.z * cos(angle)),
        )
