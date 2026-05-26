import cfg
import dev
import key
import pbs
import tip
import fgc
import ohm
import wgs
import dly
import y4x4
import rx


def icr(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 0)
  rx.chips(x, y + cfg.size * 0.5)


def pbses(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 0)
  _, y = tip.chip(x, y + cfg.sch * 3, cfg.size)
  _, y = pbs.chips(x, y)
  _, y = tip.chip(x, y, cfg.size)
  _, y = pbs.chips(x, y)
  _, y = tip.chip(x, y, cfg.size)


def hybrids(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 0)
  _, y = tip.chips(x, y + cfg.sch)
  _, y = y4x4.chips(x, y)


def waveguides(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 0)
  _, y = tip.chip(x, y + cfg.sch * 2, cfg.size)
  _, y = wgs.chips(x, y + cfg.sch)
  _, y = tip.chip(x, y + cfg.sch * 4, cfg.size)
  _, y = ohm.chips(x, y + cfg.sch)
  _, y = tip.chip(x, y + cfg.sch, cfg.size)
  _, y = dly.dline(x, y + cfg.sch * 2)


def gratings(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 0)
  fgc.chips(x, y + cfg.sch * 2)


def filled(xpos, ypos):
  key.frame(xpos, ypos, 2)
  dev.split('metal', 1, -1)


def marks(xpos, ypos):
  x, y = key.frame(xpos, ypos, 2)
  dev.marks('metal', x, y, cfg.size, cfg.size)
  title = f'SiN Silicon Photonics'
  dev.texts(x + cfg.size * 0.5, y + 20, title, 0.5, 'cb')
  dev.texts(x + cfg.size * 0.5, y + cfg.size - 20, title, 0.5, 'ct')


def chips(region):
  if 0 in region: key.cross(0, 0)
  # if 1 in region: icr(-1, 1)
  # if 2 in region: pbses(1, 1)
  # if 3 in region: hybrids(-1, -1)
  # if 4 in region: filled(1, -1)
  if 1 in region: waveguides(-1, 1)
  if 4 in region: marks(1, -1)


if __name__ == '__main__':
  cfg.draft = 'draft'
  filename = f'SiN_V{cfg.ver}_{cfg.draft}'
  chips([0, 1, 2, 3, 4])
  # dev.savedxf(filename)
  dev.saveas(filename)
  dev.dlayers(filename, 'rect', 'edge')
  dev.dlayers(filename, 'hole', 'bars')
  if cfg.draft in ['draft']: dev.gdstext(filename)
