import cfg
import ref
import dxf
import dev
import tip
import elr


def device(layer, x, y):
  angle = 5
  lpbs = 395
  spacing = 2.4
  ybend = 25

  df = elr.curve(cfg.wg, cfg.radius, angle, 'mask')

  sign = -1
  dy = sign * ybend
  ds = sign * (spacing + cfg.wg)
  x2, y2 = dxf.sbend(layer, df, x, y + dy + ds * 0.5, -dy)
  x3, y3 = dxf.srect(layer, x2, y2, lpbs, cfg.wg)
  x4, y4 = dxf.sbend(layer, df, x3, y3, dy)
  x5, y5 = dxf.srect(layer, x4, y4, lpbs, cfg.wg)
  x6, y6 = dxf.srect(layer, x4, y4 + ds, lpbs, cfg.wg)
  x7, y7 = dxf.sbend(layer, df, x5, y5, -dy)
  x8, y8 = dxf.sbend(layer, df, x6, y6, dy)
  x9, y91 = dxf.srect(layer, x7, y7, 10, cfg.wg)
  x9, y92 = dxf.srect(layer, x8, y8, 10, cfg.wg)
  dxf.sbend(layer, df, x3, y4 + ds + dy, -dy)

  sign = 1
  dy = sign * ybend
  ds = sign * (spacing + cfg.wg)
  x2, y2 = dxf.sbend(layer, df, x, y + dy + ds * 0.5, -dy)
  x3, y3 = dxf.srect(layer, x2, y2, lpbs, cfg.wg)
  x4, y4 = dxf.sbend(layer, df, x3, y3, dy)
  x5, y5 = dxf.srect(layer, x4, y4, lpbs, cfg.wg)
  x7, y7 = dxf.sbend(layer, df, x5, y5, dy)
  dxf.srect(layer, x7, y7, 10, cfg.wg)

  return x9, y91, y92


def chip(x, y, lchip):
  idev = len(ref.points)
  x1, _, _ = device('core', x, y)
  x5, x6 = dxf.center(idev, x, x1, lchip)

  title = f'PBS-{cfg.lpbs:.0f}'
  tip.texts(x5, y, x, title)
  tip.texts(x6, y + cfg.sch * 0.5, x + lchip, title)
  tip.sline(x6, y - cfg.sch * 0.5, x + lchip)
  print(title)

  return x + lchip, y


if __name__ == '__main__':
  filename = 'pbs'
  # chips(0, 0)
  chip(0, 0, cfg.size)
  dev.savedxf(filename)
  # dev.filled(0, 0, 1)
  # dev.saveas(filename)
