from dataclasses import dataclass, field
from typing import ClassVar

from src.barycentric.barycentric_coord import BarycentricCoord
from src.maths import Vec2, Triangle

@dataclass(slots=True)
class BarycentricRandom(object):
  system: 'BarycentricSystem'

  def carpet(self, k: int) -> list[BarycentricCoord]:
    coords = []
    for u in range(k + 1):
      for v in range(k + 1 - u):
        w = k - u - v

        coords.append(BarycentricCoord(self.system, u / k, v / k, w / k))
    return coords

@dataclass(slots=True)
class BarycentricSystem(object):
  origin: Triangle
  random: BarycentricRandom = field(init=False)
  classic: ClassVar['BarycentricSystem']

  def __post_init__(self):
    self.random = BarycentricRandom(self)

  @property
  def a(self) -> Vec2: return self.origin.a
  @property
  def b(self) -> Vec2: return self.origin.b
  @property
  def c(self) -> Vec2: return self.origin.c

  def create(self, u: float, v: float, w: float) -> BarycentricCoord:
    if u + v + w != 1: raise ValueError(f"u + v + w must equal 1, got {u:.2f} + {v:.2f} + {w:.2f} = {u + v + w:.2f}")
    return BarycentricCoord(self, u, v, w)
BarycentricSystem.classic = BarycentricSystem(
  Triangle(
    Vec2(0, 0),
    Vec2(1, 0),
    Vec2(1 / 2, 3 ** 0.5 / 2),
  )
)
