from dataclasses import dataclass
import sys
from typing import Callable

from src.barycentric.barycentric_system import BarycentricSystem
from src.barycentric.barycentric_coord import BarycentricCoord
from src.draw import DrawContext, RgbaColor
from src.draw.color_map import Normalizer, ColorMap
from argparse import ArgumentParser

def parse_fn(formula: str) -> Callable[[float, float, float], float]:
  def create_fn(formula: str) -> Callable[[float, float, float], float]:
    try:
      return eval(f'lambda u, v, w: {formula}')
    except Exception as error:
      print(f'[Error] Invalid function: "{formula}" returned with "{error}"', file=sys.stderr)
      exit(1)

  fn = create_fn(formula)
  def handle_coord(coord: BarycentricCoord) -> float:
    try:
      return round(fn(coord.u, coord.v, coord.w), 6)
    except ZeroDivisionError as error:
      print(f'[Warn]: "{error}"', file=sys.stderr)
      return 1
    except ValueError as error:
      print(f'[Warn]: "{error}"', file=sys.stderr)
      return None
  return handle_coord

@dataclass
class Arguments(object):
  k: int
  formula: str
  fn: Callable[[float, float, float], float]

  @classmethod
  def parse(cls):
    parser = ArgumentParser()
    parser.add_argument(
      '-k',
      type=int,
      default=100,
      help='Carpet size (default: 100)'
    )
    parser.add_argument(
      '-formula',
      type=str,
      default='u + v',
      help=
      'Function to plot (default: u + v).'
      '\nAvailable variables: u, v, w which are float values between 0 and 1.'
      '\nAvailable package: math'
    )
    arguments = parser.parse_args()
    return cls(arguments.k, arguments.formula, parse_fn(arguments.formula))

def main():
  arguments = Arguments.parse()
  system = BarycentricSystem.classic

  coords = system.random.carpet(arguments.k)

  values = [value for value in map(arguments.fn, coords) if value is not None]
  color_map = ColorMap((
    RgbaColor.from_rgb(0, 0, 1),
    RgbaColor.from_rgb(0, 1, 1),
    RgbaColor.from_rgb(0, 1, 0),
    RgbaColor.from_rgb(1, 1, 0),
    RgbaColor.from_rgb(1, 0, 0),
  ),
    Normalizer(values)
  )

  (DrawContext()
   .triangle(system.origin, RgbaColor.from_rgb(0, 0, 0))
   .vecs2([coord.xy for coord in coords], values, color_map)
   .colorbar(color_map)
   .title(f'Barycentric formula - $f(u, v, w) = {arguments.formula}$')
   .text(system.origin.a, 'U', ha='right', va='center')
   .text(system.origin.b, 'V', ha='left', va='center')
   .text(system.origin.c, 'W', ha='center', va='bottom').show())

if __name__ == '__main__':
  main()
