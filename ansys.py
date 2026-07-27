import cfg
import dxf
import gds
import dev
import elr
import fgc


def bends(path):
  angle = 6
  df = dev.euler(cfg.wg, cfg.radius, angle)
  x1, y1 = dxf.srect('core', 0, 0, 10, cfg.wg)
  x2, y2 = dxf.bends('core', df, x1, y1, 0, 1, 1)
  dxf.tilts('core', x2, y2, 10, cfg.wg, angle)
  gds.savelayer(f'{path}/{cfg.radius:.0f}r_{angle:.0f}deg')


def sbend(path):
  radius = 100
  angle, dy, dl, length = 45, 50, 10, 250
  df = dev.euler(cfg.wg, radius, angle)
  x1, y1 = dxf.srect('core', -dl, 0, dl, cfg.wg)
  x2, y2 = dxf.sbend('core', df, x1, y1, dy)
  dxf.srect('core', x2, y2, length - x2, cfg.wg)
  gds.savelayer(f'{path}/0.15t-{radius:.0f}r_{angle:.0f}a')


def ubend(path):
  length = 20
  df = dev.euler(cfg.wg, cfg.radius, 180)
  x1, y1 = dxf.srect('core', 0, 0, length, cfg.wg)
  x1, y1 = dxf.bends('core', df, x1, y1, 0, 1, 1)
  dxf.srect('core', x1, y1, -length, cfg.wg)
  gds.savelayer(f'{path}/{cfg.radius:.0f}r_180a')


def dc(path):
  df = dev.euler(cfg.wg, cfg.radius, 30)
  dxf.bends('core', df, 0, 0, 0, -1, -1)
  dxf.bends('core', df, 0, 0, 0, 1, -1)
  gds.savelayer(f'{path}/dc{cfg.radius:.0f}r')


def dc_pbs(path):
  cfg.radius = 500
  angle = 1
  lpbs = 395
  spacing = 2.4

  df = elr.curve(cfg.wg, cfg.radius, angle, 'mask')

  sign = -1
  dy = sign * 2
  ds = sign * (spacing + cfg.wg)
  x2, y2 = dxf.sbend('core', df, 10, dy + ds * 0.5, -dy)
  x3, y3 = dxf.srect('core', x2, y2, lpbs, cfg.wg)
  x4, y4 = dxf.sbend('core', df, x3, y3, dy)
  x5, y5 = dxf.srect('core', x4, y4, lpbs, cfg.wg)
  x6, y6 = dxf.srect('core', x4, y4 + ds, lpbs, cfg.wg)
  x7, y7 = dxf.sbend('core', df, x5, y5, -dy)
  x8, y8 = dxf.sbend('core', df, x6, y6, dy)
  dxf.srect('core', x7, y7, 10, cfg.wg)
  dxf.srect('core', x8, y8, 10, cfg.wg)
  dxf.sbend('core', df, x3, y4 + ds + dy, -dy)

  sign = 1
  dy = sign * 2
  ds = sign * (spacing + cfg.wg)
  x1, y1 = dxf.srect('core', 0, dy + ds * 0.5, 10, cfg.wg)
  x2, y2 = dxf.sbend('core', df, x1, y1, -dy)
  x3, y3 = dxf.srect('core', x2, y2, lpbs, cfg.wg)
  x4, y4 = dxf.sbend('core', df, x3, y3, dy)
  x5, y5 = dxf.srect('core', x4, y4, lpbs, cfg.wg)
  x7, y7 = dxf.sbend('core', df, x5, y5, dy)
  dxf.srect('core', x7, y7, 10, cfg.wg)

  gds.savelayer(f'{path}/dc_pbs')


def grating_coupler(path):
  fgc.grating('core', 0, 0, 1, 0)
  dxf.srect('core', -10, 0, 10, cfg.wg)
  gds.savelayer(f'{path}/grating_{cfg.period}_{cfg.duty}')


if __name__ == '__main__':
  cfg.draft = 'mask'
  workspace = '../../ansys'
  sbend(f'{workspace}/euler')
