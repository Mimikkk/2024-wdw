from dataclasses import dataclass

from src.maths import Vec2

@dataclass(slots=True)
class BarycentricCoord(object):
  origin: 'BarycentricSystem'
  u: float
  v: float
  w: float

  @property
  def x(self) -> float: return (
      self.u * self.origin.a.x
      + self.v * self.origin.b.x
      + self.w * self.origin.c.x
  )

  @property
  def y(self) -> float: return (
      self.u * self.origin.a.y
      + self.v * self.origin.b.y
      + self.w * self.origin.c.y
  )

  @property
  def xy(self) -> Vec2:
    return Vec2(self.x, self.y)

  @property
  def uvw(self) -> tuple[float, float, float]:
    return self.u, self.v, self.w
