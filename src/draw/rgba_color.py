from dataclasses import dataclass
from typing import Iterable

@dataclass(slots=True)
class RgbaColor(object):
  red: float
  green: float
  blue: float
  alpha: float

  @property
  def r(self) -> float:
    return self.red

  @property
  def g(self) -> float:
    return self.green

  @property
  def b(self) -> float:
    return self.blue

  @property
  def a(self) -> float:
    return self.alpha

  @property
  def rgb(self) -> tuple[float, float, float]:
    return self.red, self.green, self.blue

  @property
  def rgba(self) -> tuple[float, float, float, float]:
    return self.red, self.green, self.blue, self.alpha

  @classmethod
  def from_rgb(cls, r: float, g: float, b: float) -> 'RgbaColor':
    return cls(r, g, b, 1)

  @classmethod
  def interpolate(cls, from_: 'RgbaColor', to_: 'RgbaColor', t: float) -> 'RgbaColor':
    return cls(
      *(
        from_value + (to_value - from_value) * t
        for from_value, to_value in zip(from_, to_)
      )
    )

  @classmethod
  def interpolate_many(cls, colors: list['RgbaColor'], t: float) -> 'RgbaColor':
    if t <= 0:
      return colors[0]
    elif t >= 1:
      return colors[-1]

    segment = (len(colors) - 1) * t
    index = int(segment)
    fraction = segment - index

    first = colors[index]
    second = colors[index + 1]

    r = float(first.r + (second.r - first.r) * fraction)
    g = float(first.g + (second.g - first.g) * fraction)
    b = float(first.b + (second.b - first.b) * fraction)
    a = float(first.a + (second.a - first.a) * fraction)

    return cls(r, g, b, a)

  def __iter__(self) -> Iterable[float]:
    yield self.red
    yield self.green
    yield self.blue
    yield self.alpha
