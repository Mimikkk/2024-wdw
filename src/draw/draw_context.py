from dataclasses import dataclass, field

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.figure import Figure
from matplotlib.pyplot import figure

from src.draw import ColorMap
from src.draw.rgba_color import RgbaColor
from src.maths import Vec2, Triangle

@dataclass
class DrawContext(object):
  figure: Figure = field(default_factory=lambda: figure(figsize=(8, 8)))

  @property
  def context(self) -> Axes:
    return self.figure.gca()

  def triangle(self, triangle: Triangle, color: RgbaColor) -> 'DrawContext':
    self.context.plot(
      (triangle.a.x, triangle.b.x, triangle.c.x, triangle.a.x),
      (triangle.a.y, triangle.b.y, triangle.c.y, triangle.a.y),
      '-',
      color=color.rgba,
      antialiased=True,
      linewidth=3
    )
    return self

  def vec2(self, vec: Vec2, color: RgbaColor) -> 'DrawContext':
    self.context.plot(vec.x, vec.y, 'o', color=color.rgba, antialiased=True)
    return self

  def vecs2(self, vecs: list[Vec2], values: list[float], color_map: ColorMap) -> 'DrawContext':
    plt.scatter(
      [vec.x for vec in vecs],
      [vec.y for vec in vecs],
      c=values,
      antialiased=True,
      cmap=color_map.map
    )

    return self

  def title(self, title: str) -> 'DrawContext':
    self.context.set_title(title)
    return self

  def text(self, at: Vec2, text: str, **kwargs) -> 'DrawContext':
    self.context.text(at.x, at.y, text, antialiased=True, fontweight='bold', fontsize=24, **kwargs)
    return self

  def colorbar(self, map: ColorMap) -> 'DrawContext':
    bar = self.figure.colorbar(
      ScalarMappable(cmap=map.map),
      ticks=[],
      ax=self.context,
    )

    color_count = len(map.colors)
    ticks = [
      i / (color_count - 1) for i in range(color_count)
    ]

    labels = [f'{map.normalizer.denormalize(value):.2f}' for value in ticks]
    bar.set_ticks(ticks, labels=labels)

    return self

  def show(self) -> None:
    plt.show(block=True)
