import cfg
import dev
import key
import tip
import dly
import pbs
import voa
import dci


def delay_line(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  _, y = tip.chip(x, y, cfg.size * 2)
  _, y = voa.chip(x, y + cfg.sch * 6, 4000, cfg.size)
  _, y = dly.dlmzi(x, y + cfg.sch * 5)
  _, y = tip.chip(x, y + cfg.sch * 2, cfg.size)
  _, y = pbs.chips(x, y)
  dev.split('metal', 0, -1)


def pbs_dci_tip(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  _, y = tip.chips(x, y + cfg.sch)
  _, y = dci.chips(x, y - cfg.sch)
  _, y = tip.chip(x, y, cfg.size)
  _, y = dly.dline(x, y + cfg.sch)


def marks(xpos, ypos):
  x, y = key.frame(xpos, ypos, 2)
  dev.marks('metal', x, y)


def chips(region):
  if 0 in region: key.cross(0, 0)
  if 1 in region: delay_line(-1, 1)
  if 2 in region: pbs_dci_tip(1, 1)
  if 3 in region: marks(-1, -1)
  if 4 in region: marks(1, -1)


if __name__ == '__main__':
  cfg.draft = 'draft'
  filename = f'SiN150_V{cfg.ver}_{cfg.draft}'
  chips([0, 1, 2])
  # dev.savedxf(filename)
  dev.saveas(filename)
  dev.dlayers(filename, 'rect', 'edge')
  dev.dlayers(filename, 'hole', 'bars')
  if cfg.draft in ['draft']: dev.gdstext(filename)
