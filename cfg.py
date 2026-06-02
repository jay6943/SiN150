import os

ver = '1.0'
path = f'../../mask/SiN150-{ver}'
if not os.path.isdir(path): os.mkdir(path)
draft = 'draft'

dw = 0.1
wg = 2.0 + dw
eg = 40.0
ch = 127.0
sch = 100.0
radius = 500.0
angle = 6.0

w1x2 = 9.2 + dw
l1x2 = 18.3
s1x2 = 2.3
w2x2 = 12.6 + dw
l2x2 = 107.0
s2x2 = 2.3
lpbs = 56.0
wpbs = 1.85 + dw
ltpr = 5.0
wtpr = 3.0 + dw
ltip = 700.0
lext = 500.0
wtip = 0.3
lpad = 400.0
wpad = 10.0
ldci = 22.3
sdci = 4.0

duty = 0.5
period = 1.2

size = 10000
wkey = 400
wbar = 250
tkey = wkey + wbar
lkey = size + wkey
lbar = size + wkey + wbar
skey = size + wkey + wbar * 2
area = [[0, 0], [-1, 0], [0, 0], [-1, -1], [0, -1]]

labels = {
  'core': 1,
  'edge': 2,
  'keys': 3,
  'bars': 4,
  'cross': 5,
  'metal': 6,
  'hole': 7,
  'rect': 8,
  'text': 9
}
