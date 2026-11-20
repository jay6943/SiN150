import cfg
import dev
import tip


def delay(x, y, dx, dy, num):
  radius = cfg.radius
  r1 = dev.euler(cfg.wg, radius, 90)
  r2 = dev.euler(cfg.wg, radius + cfg.dr, 90)
  r3 = dev.euler(cfg.wg, radius + cfg.dr * 0.5, 90)
  d2 = r1.dx - r2.dx + cfg.dr
  d3 = r1.dx - r3.dx + cfg.dr * 0.5
  x1 = x + r2.dx + (num + 0.5) * cfg.dr + 500
  x2 = x1 + dx - d2 * (num - 1)
  
  for i in range(num):
    ch = radius + (i + 1) * cfg.dr + dy
    y1 = y + radius + num * cfg.dr + dy
    for j, cur in enumerate(['in', 'out']):
      dl = [0, cfg.dr * 0.5][j]
      dt = [0, d3][j]
      y2 = y1 - ch - dl
      y3 = y1 + ch + dl
      y4 = y2 + cfg.dr
      x3 = x1 - i * d2 - dt
      x4 = x2 + i * d2 + dt
      cfg.radius = radius + (i + 1) * cfg.dr + dl
      if (i < num - 1) or ('i' in cur):
        x5, y5 = dev.bends(x4, y2, 90, 0, 1, 1)
      x5, y6 = dev.bends(x4, y3, 90, 0, 1, -1)
      x6, y7 = dev.bends(x3, y3, 90, 0, -1, -1)
      x6, y8 = dev.bends(x3, y4, 90, 0, -1, 1)

      if (i < num - 1) or ('i' in cur):
        dev.tline(x5, y5, y6 - y5)
      dev.tline(x6, y8, y7 - y8)
      dev.sline(x3, y3, x4 - x3)
      dev.sline(x3, y4, x4 - x3 - d2)

      if 'i' in cur: x11, y11 = x4, y2
      if 'o' in cur: x12, y12 = x5, y6

  # 중심부 오른쪽 내각 곡선 도파로
  cfg.radius = radius
  ch = radius + dy
  x41, y41, y42 = x2 - d2, y1 - ch, y1 + ch
  x43, y43 = dev.bends(x41, y41, 90, 0, 1, 1)
  x44, y44 = dev.bends(x41, y42, 90, 0, 1, -1)
  dev.tline(x43, y43, y44 - y43)
  
  # 중심 곡선 도파로
  dl = cfg.dr * 0.5
  x51 = x1 + dx * 0.5 - x41 + x43
  x52 = x1 + dx * 0.5 + x41 - x43
  y51 = y41 + dl
  x53, y53 = dev.bends(x51, y42, 90, 0, -1, -1)
  x54, y54 = dev.bends(x52, y51, 90, 0, 1, 1)
  dev.sline(x41, y42, x51 - x41)
  dev.tline(x53, y53, y54 - y53)

  # 중심부 왼쪽 및 오른쪽 외각 곡선 도파로
  cfg.radius = radius + dl
  ch = radius + dy + dl
  x61, x62 = x1 + dt, x2 - dt
  y61, y62, y63 = y1 + ch, y1 - ch + dl * 2, y1 - ch
  x65, y65 = dev.bends(x61, y61, 90, 0, -1, -1)
  x66, y66 = dev.bends(x61, y62, 90, 0, -1, 1)
  x67, y67 = dev.bends(x62, y63, 90, 0, 1, 1)
  x68, y68 = dev.bends(x62, y61, 90, 0, 1, -1)
  dev.sline(x52, y51, x61 - x52)
  dev.tline(x66, y66, y65 - y66)
  dev.sline(x61, y61, x62 - x61)
  dev.tline(x67, y67, y68 - y67)

  cfg.radius = radius

  return [x11, x12], [y11, y12]


def device(x, y):
  xp, yp = delay(x, y, 6900, 200, 6)
  df = dev.euler(cfg.wg, cfg.radius, 90)
  x1, y1 = xp[1] + df.dx, y
  x2, y2 = dev.bends(x1, y1, 90, 0, -1, 1)
  dev.tline(x2, y2, yp[1] - y2)

  tip.sline(xp[0], y, x, 'Delay')
  tip.sline(x1, y, x + cfg.lchip, 'Delay')
  
  return x, y


if __name__ == '__main__':
  device(0, 0)
  dev.saveas(f'delay_{cfg.draft}')
