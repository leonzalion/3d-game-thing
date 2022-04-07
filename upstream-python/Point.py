from __future__ import annotations

from copy import copy
from dataclasses import dataclass

from Vector import Vector

@dataclass
class Point:
    x: int = 0
    y: int = 0
    z: int = 0

    def __post_init__(self) -> None:
        # Ensure components are ints
        self.x = int(self.x)
        self.y = int(self.y)
        self.z = int(self.z)

    def getMidpoint(p: Point, q: Point) -> Point:
        return Point((p.x+q.x)//2, (p.y+q.y)//2, (p.z+q.z)//2)

    def __iadd__(self, other: Vector) -> Point:
        self.x += int(other.x)
        self.y += int(other.y)
        self.z += int(other.z)
        return self
    def __add__(self, other: Vector) -> Point:
        new = copy(self)
        new += other
        return new

    def __isub__(self, other: Vector) -> Point:
        self.x -= int(other.x)
        self.y -= int(other.y)
        self.z -= int(other.z)
        return self
    def __sub__(self, other: Vector) -> Point:
        new = copy(self)
        new -= other
        return new
