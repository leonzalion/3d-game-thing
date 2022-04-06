from __future__ import annotations

from copy import copy
from dataclasses import dataclass, field

from Point import Point

@dataclass
class Polygon:
    vertices: list = field(default_factory=list)

    def __iadd__(self, other: Vector) -> Polygon:
        for vertex in self.vertices:
            vertex += other
        return self
    def __add__(self, other: Vector) -> Polygon:
        new = copy(self)
        new += other
        return new

    def __isub__(self, other: Vector) -> Polygon:
        for vertex in self.vertices:
            vertex -= other
        return self
    def __sub__(self, other: Vector) -> Polygon:
        new = copy(self)
        new -= other
        return new
