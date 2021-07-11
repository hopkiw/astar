#!/usr/bin/env python3
"""Module docstring."""

import pyglet
from pyglet import shapes
from pyglet.window import mouse

# A-star
#


class Tile:
  """Class docstring."""

  def __init__(self, idx, x, y, width, height, color, batch, fgbatch):
    """A game tile."""
    self.idx = idx
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.color = color
    self.batch = batch
    self.fgbatch = fgbatch

    self.rectangle = shapes.Rectangle(x, y, width, height, color=color,
                                      batch=batch)
    self.make_labels()

    self.active = False

  def make_labels(self):
    """Given the coordinate of the lower left corner of a tile, return a tuple
    of 3 labels for f, g and h scores.
    """
    self.label_1 = pyglet.text.Label('X', font_name='Times New Roman',
                                     font_size=20, x=self.x+10, y=self.y+70,
                                     batch=self.fgbatch)
    self.label_2 = pyglet.text.Label('X', font_name='Times New Roman',
                                     font_size=20, x=self.x+70, y=self.y+70,
                                     batch=self.fgbatch)
    self.label_3 = pyglet.text.Label(f'{self.idx}', font_name='Times New Roman',
                                     font_size=24, x=self.x+35, y=self.y+25,
                                     batch=self.fgbatch)


class Game:
  """Class docstring."""

  def __init__(self, rows=3, columns=3):
    """A game window for displaying the A* pathing algorithm."""
    self.dragging = False
    self.tiles = []
    self.circles = []

    self.rows = rows
    self.columns = columns

    self.window = pyglet.window.Window(1320, 770)
    self.batch = pyglet.graphics.Batch()
    self.fgbatch = pyglet.graphics.Batch()

    self.make_tiles()
    self.window.push_handlers(on_draw=self.on_draw)
    self.window.push_handlers(on_mouse_press=self.on_mouse_press)
    self.window.push_handlers(on_mouse_drag=self.on_mouse_drag)
    self.window.push_handlers(on_mouse_release=self.on_mouse_release)

  def make_tiles(self):
    """Populate self.tiles."""
    x = 0
    y = 0
    for idx in range(self.rows * self.columns):
      self.tiles.append(Tile(idx, x, y, 100, 100, (255, 255, 255), self.batch,
                             self.fgbatch))
      if (idx+1) % self.columns == 0:
        x = 0
        y = y + 110
      else:
        x = x + 110

  def draw_circle(self, x, y):
    circle = shapes.Circle(x, y, radius=10, color=(50, 225, 30),
                           batch=self.fgbatch)
    self.circles.append(circle)
    pyglet.clock.schedule_once(self.delete_circle, 0.65, circle)

  def delete_circle(self, dt, circle):
    """Delete an on-click circle."""
    circle.delete()
    self.circles.remove(circle)

  def tile(self, x, y):
    row = int(y / 110)
    col = int(x / 110)
    idx = (row*self.columns) + col
    print(f'that\'s tile #{idx}')

    return self.tiles[idx]

  def on_draw(self):
    self.window.clear()
    self.batch.draw()
    self.fgbatch.draw()

  def on_mouse_press(self, x, y, button, modifiers):
    """On mouse press."""
    if button == mouse.LEFT:
      print(f'The left mouse button was pressed at ({x},{y}).')
      self.draw_circle(x, y)

      if x < 110 * self.columns and y < 110 * self.rows:
        tile = self.tile(x, y)
        if tile.rectangle.color == [55, 55, 255]:
          print('make red')
          tile.rectangle.color = (255, 55, 55)
          # labels[idx][0].text = ' '
        else:
          print('make blue')
          tile.rectangle.color = (55, 55, 255)
          # labels[idx][0].text = 'X'
    elif button == mouse.RIGHT:
      for tile in self.tiles:
        tile.rectangle.color = (255, 255, 255)
        # for labelset in self.labels:
        #     for label in labelset:
        #         label.text = ' '

  def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
    print(f'mouse DRAG - {x},{y} -{dx},{dy}')
    self.dragging = True
    tile = self.tile(x, y)
    # if already active
    if not tile.active:
      tile.rectangle.color = (55, 55, 255)
      tile.active = True

  def on_mouse_release(self, x, y, button, modifiers):
    if self.dragging:
      print('clear dragging')
      self.dragging = False
      for tile in self.tiles:
        tile.rectangle.color = (255, 255, 255)


def main():
  g = Game(7, 12)
  pyglet.app.run()


if __name__ == '__main__':
  main()
