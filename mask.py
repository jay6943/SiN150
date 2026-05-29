import cfg
import dev
import key
import tip
import dly
import voa
import pbs
import dci


def delay_large(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 1)
  _, y = voa.chip(x, y + cfg.sch * 6, 4000, cfg.size)
  _, y = tip.chip(x, y + cfg.sch * 6, cfg.size)
  _, y = dly.dline(x, y + cfg.sch, 5600, 1415, 100, 100, 3000)


def delay_small(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 1)
  _, y = voa.chip(x, y + cfg.sch * 6, 4000, cfg.size)
  _, y = tip.chip(x, y + cfg.sch * 6, cfg.size)
  _, y = dly.dline(x, y + cfg.sch, 6000, 3170, 100, 50, 1800)


def polarization(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 1)
  _, y = voa.chip(x, y + cfg.sch * 6, 4000, cfg.size)
  _, y = tip.chips(x, y + cfg.sch * 6)
  _, y = pbs.chips(x, y)


def directional(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 1)
  _, y = voa.chip(x, y + cfg.sch * 6, 4000, cfg.size)
  _, y = tip.chips(x, y + cfg.sch * 6)
  _, y = pbs.chips(x, y)


def metal(xpos, ypos):
  key.frame(xpos, ypos, 2)
  dev.split('metal', 1, -1)


def mark(xpos, ypos):
  x, y = key.frame(xpos, ypos, 2)
  dev.marks('metal', x, y, cfg.size, cfg.size)
  title = f'SiN Silicon Photonics'
  dev.texts(x + cfg.size * 0.5, y + 20, title, 0.5, 'cb')
  dev.texts(x + cfg.size * 0.5, y + cfg.size - 20, title, 0.5, 'ct')


def chips(region):
  if 0 in region: key.cross(0, 0)
  # if 1 in region: delay_large(-1, 1)
  # if 2 in region: delay_small(1, 1)
  # if 3 in region: polarization(-1, -1)
  if 3 in region: directional(-1, -1)
  # if 4 in region: metal(1, -1)
  if 4 in region: mark(1, -1)


if __name__ == '__main__':
  cfg.draft = 'draft'
  filename = f'SiN150_V{cfg.ver}_{cfg.draft}'
  chips([0, 1, 2, 3, 4])
  # dev.savedxf(filename)
  dev.saveas(filename)
  dev.dlayers(filename, 'rect', 'edge')
  dev.dlayers(filename, 'hole', 'bars')
  if cfg.draft in ['draft']: dev.gdstext(filename)
