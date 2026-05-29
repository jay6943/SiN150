import sys
import cfg
import ref
import dxf
import dev
import dci
import tip
import pad
import y2x2


class delayline:
  def __init__(self, x, dx, dy, dr, rmax):
    self.xp = x
    self.dx = dx
    self.dy = dy
    self.dr = dr
    self.rmax = rmax
    self.radius = cfg.radius
    self.length = 0

  def inner(self, x, y):
    cfg.radius -= self.dr * 2
    df = dev.euler(cfg.wg, cfg.radius, 90)
    x1, y1 = dev.bends(x, y, 90, 0, 1, 1)
    x2, y2 = dev.tline(x1, y1, self.dy + self.dr * 3)
    x3, y3 = dev.bends(x2, y2, 90, 90, 1, 1)
    x4, y4 = dev.sline(x3, y3, -self.dx)
    x5, y5 = dev.bends(x4, y4, 90, 180, 1, 1)
    x6, y6 = dev.tline(x5, y5, 0 - self.dy - self.dr)
    x7, y7 = dev.bends(x6, y6, 90, 270, 1, 1)
    x8, y8 = dev.sline(x7, y7, self.dx)
    self.length += 2 * (self.dx + self.dy + 2 * self.dr + 2 * df.l)
    return x8, y8

  def center(self, x, y):
    cfg.radius -= self.dr * 2
    print('Center radius =', cfg.radius, 'um')
    df = dev.euler(cfg.wg, cfg.radius, 90)
    dl = self.dx * 0.5 - df.dx
    if dl < 10:
      print(f'Error!, Ceneter line < {dl:.3f} um')
      sys.exit()
    else: print(f'Center line = {dl:.3f} um')
    x1, y1 = dev.bends(x, y, 90, 0, 1, 1)
    x2, y2 = dev.tline(x1, y1, self.dy + self.dr * 3)
    x3, y3 = dev.bends(x2, y2, 90, 90, 1, 1)
    x4, y4 = dev.sline(x3, y3, -dl)
    x5, y5 = dev.bends(x4, y4, 90, 0, -1, -1)
    x6, y6 = dev.tline(x5, y5, 0 - self.dy - self.dr * 2)
    x7, y7 = dev.bends(x6, y6, 90, 90, 1, -1)
    x8, y8 = dev.sline(x7, y7, -dl)
    self.length += 2 * (self.dy + 2 * df.l - dl) + 5 * self.dr
    return x8, y8

  def outer(self, x, y):
    cfg.radius += self.dr * 2
    df = dev.euler(cfg.wg, cfg.radius, 90)
    x1, y1 = dev.bends(x, y, 90, 0, -1, 1)
    x2, y2 = dev.tline(x1, y1, self.dy + self.dr)
    x3, y3 = dev.bends(x2, y2, 90, 90, -1, 1)
    x4, y4 = dev.sline(x3, y3, self.dx)
    x5, y5 = dev.bends(x4, y4, 90, 0, 1, -1)
    x6, y6 = dev.tline(x5, y5, 0 - self.dy - self.dr * 3)
    x7, y7 = dev.bends(x6, y6, 90, 90, 1, -1)
    x8, y8 = dev.sline(x7, y7, 0 - self.dx)
    self.length += 2 * (self.dx + self.dy + 2 * self.dr + 2 * df.l)
    return x8, y8

  def outest(self, x, y):
    cfg.radius += self.dr * 2
    df = dev.euler(cfg.wg, cfg.radius, 90)
    x1, y1 = dev.bends(x, y, 90, 0, -1, 1)
    x2, y2 = dev.tline(x1, y1, self.dy + self.dr)
    x3, y3 = dev.bends(x2, y2, 90, 90, -1, 1)
    x4, y4 = dev.sline(x3, y3, self.dx)
    x5, y5 = dev.bends(x4, y4, 90, 0, 1, -1)
    self.length += self.dx + self.dy + self.dr + 3 * df.l
    return x5, y5

  def outport(self, x, y, dy):
    cfg.radius = 500
    df = dev.euler(cfg.wg, cfg.radius, 90)
    x1, y1 = dev.tline(x, y, dy - y + df.dy)
    x2, y2 = dev.bends(x1, y1, 90, 270, 1, 1)
    self.length += dy - y + df.dy + df.l
    return x2, y2

  def device(self, x, y):
    num = int((self.rmax - cfg.radius - 200) * 0.5 / self.dr) + 1
    print('Rounds =', num)
    cfg.radius = self.rmax
    x1, y1 = x, y
    for _ in range(num): x1, y1 = self.inner(x1, y1)
    x2, y2 = self.center(x1, y1)
    cfg.radius -= self.dr
    for _ in range(num): x2, y2 = self.outer(x2, y2)
    x3, y3 = self.outest(x2, y2)
    x4, y4 = self.outport(x3, y3, y)
    cfg.radius = self.radius
    return x4, y4


def dline(x, y, xp, dx, dy, dr, rmax):
  sf = delayline(xp, dx, dy, dr, rmax)
  x1, _ = sf.device(x + sf.xp, y)
  length = sf.length + sf.xp + x + cfg.size - x1

  cm = length * 1e-4
  ns = length * 1.601 / 3 * 1e-5
  title = f'{ns:.1f} nsec'
  tip.texts(x + sf.xp, y, x, title)
  tip.texts(x1, y, x + cfg.size, title)
  print('Delay length, time =', f'{cm:.3f} cm, {ns:.3f} nsec')
  
  return x, y + cfg.sch * 10


def dlmzi(x, y, xp, dx, dy, dr, rmax):
  y += cfg.sch * 4
  sf = delayline(xp, dx, dy, dr, rmax)
  x2, _ = sf.device(x + sf.xp, y)

  angle = 15
  df = dev.euler(cfg.wg, cfg.radius, angle)
  cf = dev.circular(cfg.wg, 5, 90)
  x3, _, y32 = y2x2.device(x2, y - cfg.s2x2)
  x6, y3 = dci.device(x + sf.xp - 500, y, angle)
  dxf.bends('core', cf, x3, y32, 270, 1, -1)
  idev = len(ref.points)
  x4, y4 = dev.sbend(x2, y3, angle, cfg.sch - cfg.s2x2 * 2)
  x5, _ = dxf.move(idev, x2, y3, x4, y4, x2 - x4, 0, 0)
  x7, _ = dev.sline(x6, y3, x5 - x6 + x2 - x4)
  x8 = x6 + (x7 - x6 - cfg.lpad) * 0.5
  # pad.bends(x8, y3, -1)
  pad.electrode('metal', x8, y3, cfg.lpad, 6, -1)
  pad.electrode('edge', x8, y3, cfg.lpad, cfg.eg, -1)

  tip.texts(x + sf.xp, y, x, '2 nsec')
  tip.texts(x3, y, x + cfg.size, '2 nsec')

  length = sf.length - (df.l * 4 + x3 - x2) + x4 - x3
  print(f'Line {length / 10000:.3f} ({3 * 2 * 10 / 1.601:.3f}) cm')

  return x, y + cfg.sch * 10


def chips(x, y):
  tip.chip(x, y, cfg.size)
  # x1, _ = dline(x, y + cfg.sch, 5600, 1415, 100, 100, 3000)
  x1, _ = dlmzi(x, y + cfg.sch, 5600, 1415, 100, 100, 3000)
  return x, y


if __name__ == '__main__':
  filename = 'dly'
  chips(0, cfg.sch * 2)
  # dev.savedxf(filename)
  dev.filled(0, 0, 1)
  dev.saveas(filename)
  dev.dlayers(filename, 'rect', 'edge')
