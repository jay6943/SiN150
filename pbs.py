import cfg
import ref
import dxf
import dev
import tip
import elr


def device(x, y):
  df = elr.curve(cfg.wg, cfg.radius, 5, cfg.draft)
  ch = 25
  ds = cfg.spbs + cfg.wg - cfg.dw
  dy = ch - ds * 0.5
  x1, y1 = dxf.sbend('core', df, x, y, -dy)
  x2, y2 = dxf.srect('core', x1, y1, cfg.lpbs, cfg.wg)
  x5, y5 = dxf.sbend('core', df, x2, y2, dy)

  x2, y2 = dxf.srect('core', x1, y1 - ds, cfg.lpbs, cfg.wg)
  dxf.bends('core', df, x1, y2, 0, -1, -1)
  x3, y3 = dxf.sbend('core', df, x2, y2, -dy)
  x4, y4 = dxf.srect('core', x3, y3, cfg.lpbs, cfg.wg)
  x6, y6 = dxf.srect('core', x3, y3 - ds, cfg.lpbs, cfg.wg)
  dxf.bends('core', df, x3, y6, 0, -1, -1)
  dxf.bends('core', df, x4, y4, 0, 1, 1)
  df = elr.curve(cfg.wg, cfg.radius, 9, cfg.draft)
  # x7, y7 = dxf.sbend('core', df, x6, y6, -dy * 2)
  x7, y7 = dxf.sbend('core', df, x6, y6, y - y6 - cfg.ch)
  dxf.srect('core', x5, y5, x7 - x5, cfg.wg)
  dxf.crect('edge', x, y + cfg.eg * 0.5, x7, y7 - cfg.eg * 0.5)

  return x7, y5, y7


def chip(x, y, lchip):
  idev = len(ref.points)
  x1, _, _ = device(x, y)
  x5, x6 = dxf.center(idev, x, x1, lchip)

  title = f'PBS-{cfg.spbs:.1f}'
  tip.texts(x5, y, x, title)
  tip.texts(x6, y, x + lchip, title)
  tip.sline(x6, y - cfg.ch, x + lchip)
  print(title)

  return x + lchip, y


def chips(x, y):
  spbs = cfg.spbs
  for cfg.spbs in dxf.arange(2.1, 2.7, 0.1):
    _, y = chip(x, y + cfg.ch * 2, cfg.size)
  cfg.spbs = spbs

  return x + cfg.size, y


if __name__ == '__main__':
  filename = 'pbs'
  chips(0, 0)
  dev.savedxf(filename)
  # dev.filled(0, 0, 1)
  # dev.saveas(filename)
