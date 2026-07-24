import cfg
import dxf
import dev
import key
import tip
import dly
import pbs
import voa
import tap
import y1x2
import y2x2


def delay_line(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  _, y = tip.chip(x, y + cfg.ch * 2, cfg.size)
  _, y = dly.dlmzi(x, y + cfg.ch)
  _, y = tip.chips(x, y + cfg.ch, dxf.arange(0.34, 0.54, 0.02))
  _, y = voa.chip(x, y + cfg.ch * 4, 4000, cfg.size)
  dev.split('metal', 0, -1)


def pbs_tap_tip(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  _, y = tap.chips(x, y + cfg.ch, dxf.arange(3.0, 4.4, 0.1))
  _, y = tip.chip(x, y, cfg.size)
  _, y = dly.dline(x, y + cfg.ch)


def marks(xpos, ypos):
  x, y = key.frame(xpos, ypos, 2)
  dev.marks('metal', x, y)


def pbs_1x2_2x2(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  _, y = tip.chip(x, y + cfg.ch * 2, cfg.size)
  _, y = pbs.chips(x, y, dxf.arange(4.0, 5.4, 0.1))
  _, y = tip.chip(x, y + cfg.ch, cfg.size)
  _, y = y1x2.chips(x, y, dxf.arange(33, 41, 1))
  _, y = tip.chip(x, y - cfg.ch * 0.5, cfg.size)
  _, y = y2x2.chips(x, y, dxf.arange(103, 111, 1))


def chips(region):
  if 0 in region: key.cross(0, 0)
  if 1 in region: delay_line(-1, 1)
  if 2 in region: pbs_tap_tip(1, 1)
  if 3 in region: marks(-1, -1)
  if 4 in region: pbs_1x2_2x2(1, -1)


if __name__ == '__main__':
  cfg.draft = 'draft'
  filename = f'SiN150_V{cfg.ver}_{cfg.draft}'
  chips([0, 1, 2, 3, 4])
  # dev.savedxf(filename)
  dev.saveas(filename)
  dev.dlayers(filename, 'rect', 'edge')
  dev.dlayers(filename, 'hole', 'bars')
  if cfg.draft in ['draft']: dev.gdstext(filename)
