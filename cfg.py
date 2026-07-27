import os

ver = '1.1'
path = f'../../mask/SiN150-{ver}'
if not os.path.isdir(path): os.mkdir(path)
draft = 'draft'

wg = 2.0
eg = 40.0
ch = 127.0
radius = 500.0
angle = 6.0

w1x2 = 8.4
l1x2 = 37.0
s1x2 = 2.2
w2x2 = 12.6
l2x2 = 107.0
s2x2 = 2.3
lpbs = 395.0
spbs = 4.4
ltpr = 5.0
wtpr = 3.0
ltip = 700.0
lext = 500.0
wtip = 0.44
lpad = 400.0
wpad = 10.0
stap = 3.6

duty = 0.5
period = 1.0

size = 10000.0
wkey = 400.0
wbar = 250.0
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
