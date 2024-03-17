from typing import Iterable
from matplotlib.colors import LinearSegmentedColormap

from src.draw.rgba_color import RgbaColor

class Normalizer(object):
  def __init__(self, values: Iterable[float]):
    values = iter(values)
    first = next(values)
    min_ = first
    max_ = first

    for value in values:
      if value < min_:
        min_ = value
      if value > max_:
        max_ = value

    if min_ == max_:
      min_ = 0
      max_ = 1

    self.min = min_
    self.max = max_

  def normalize(self, value: float) -> float:
    if self.max - self.min == 0: return 1
    return (value - self.min) / (self.max - self.min)

  def denormalize(self, value: float) -> float:
    return value * (self.max - self.min) + self.min

  def __call__(self, value: float) -> float:
    return self.normalize(value)


class ColorMap(object):
  def __init__(self, colors: Iterable[RgbaColor], normalizer: Normalizer):
    self.colors = tuple(colors)
    self.normalizer = normalizer
    self.map = LinearSegmentedColormap.from_list(
      'color-scheme',
      [color.rgba for color in self.colors]
    )

  def __call__(self, value: float) -> RgbaColor:
    return RgbaColor(*self.map(self.normalizer(value)))
