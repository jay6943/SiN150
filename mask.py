import cfg
import dxf
import dev
import key
import tip
import dly
import pbs
import voa
import tap
import sem
import y1x2
import y2x2


def amzi(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  _, y = tip.refer(x, y + cfg.ch * 2)
  _, y = dly.dlmzi(x, y + cfg.ch)
  _, y = tip.chips(x, y + cfg.ch, dxf.arange(0.34, 0.54, 0.02))
  _, y = voa.chip(x, y + cfg.ch * 4, 4000, cfg.lchip)
  dev.split('metal', 0, -1)


def delay(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  _, y = tap.chips(x, y + cfg.ch, dxf.arange(3.0, 4.4, 0.1))
  _, y = tip.refer(x, y)
  _, y = dly.dline(x, y + cfg.ch)
  sem.chips(x, y - cfg.ch * 4)


def marks(xpos, ypos):
  x, y = key.frame(xpos, ypos, 2)
  dev.marks('metal', x, y)


def pbs_1x2_2x2(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  _, y = pbs.polarizer(x, y + 2 * cfg.ch, -1)
  _, y = tip.refer(x, y)
  _, y = pbs.chips(x, y, dxf.arange(3.6, 5.2, 0.1))
  _, y = tip.refer(x, y + cfg.ch)
  _, y = y1x2.chips(x, y, dxf.arange(33, 41, 1))
  _, y = tip.refer(x, y - cfg.ch * 0.5)
  _, y = y2x2.chips(x, y, dxf.arange(103, 111, 1))
  _, y = tip.refer(x, y)
  _, y = pbs.polarizer(x, y + cfg.ch, 1)


def chips(region):
  if 0 in region: key.cross(0, 0)
  if 1 in region: amzi(-1, 1)
  if 2 in region: delay(1, 1)
  if 3 in region: marks(-1, -1)
  if 4 in region: pbs_1x2_2x2(1, -1)


if __name__ == '__main__':
  cfg.draft = 'mask'
  filename = f'SiN150_V{cfg.ver}_{cfg.draft}'
  chips([0, 1, 2, 3, 4])
  # dev.savedxf(filename)
  dev.saveas(filename)
  dev.dlayers(filename, 'rect', 'edge')
  dev.dlayers(filename, 'hole', 'bars')
  if cfg.draft in ['draft']: dev.gdstext(filename)
