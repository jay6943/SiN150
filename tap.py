import cfg
import ref
import dxf
import dev
import tip


def device(x, y, angle):
  y -= cfg.stap
  dev.bends(x, y, angle, 0, -1, -1)
  x1, y1 = dev.sbend(x, y, angle, cfg.stap - cfg.ch)
  return x1, y1


def chip(x, y, lchip):
  idev = len(ref.points)
  x1, y1 = device(x, y, 15)
  x2, y2 = dev.sline(x, y, x1 - x)
  x3, x4 = dxf.center(idev, x, x2, lchip)

  title = f'TAP-{cfg.stap:.1f}'
  tip.texts(x3, y, x, title)
  tip.texts(x4, y, x + lchip, title)
  tip.sline(x4, y - cfg.ch, x + lchip)
  print(title)

  return x, y


def chips(x, y, ranges):
  stap = cfg.stap
  for cfg.stap in ranges:
    _, y = chip(x, y + cfg.ch * 2, cfg.size)
  cfg.stap = stap
  return x, y + cfg.ch


if __name__ == '__main__':
  chips(0, 0)
  dev.savedxf('tap')
