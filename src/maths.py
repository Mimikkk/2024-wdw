from dataclasses import dataclass

@dataclass(slots=True)
class Vec3(object):
  x: float
  y: float
  z: float

  def __iter__(self):
    yield self.x
    yield self.y
    yield self.z

class Vec2Math:
  @staticmethod
  def cross(first: 'Vec2', second: 'Vec2') -> float:
    return first.x * second.y - first.y * second.x

  @staticmethod
  def dot(first: 'Vec2', second: 'Vec2') -> float:
    return first.x * second.x + first.y * second.y

  @staticmethod
  def sub(first: 'Vec2', second: 'Vec2') -> 'Vec2':
    return Vec2(first.x - second.x, first.y - second.y)

  @staticmethod
  def add(first: 'Vec2', second: 'Vec2') -> 'Vec2':
    return Vec2(first.x + second.x, first.y + second.y)


@dataclass(slots=True)
class Vec2(object):
  x: float
  y: float

  def __iter__(self):
    yield self.x
    yield self.y

@dataclass(slots=True)
class Triangle(object):
  a: Vec2
  b: Vec2
  c: Vec2

  def __iter__(self):
    yield self.a
    yield self.b
    yield self.c

def clamp(x: float, min_: float, max_: float) -> float:
  return max(min(x, max_), min_)

def clamp_01(x: float) -> float:
  return clamp(x, 0, 1)
