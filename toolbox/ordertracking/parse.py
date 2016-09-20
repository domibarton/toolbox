#!/usr/bin/env python
from __future__ import unicode_literals, absolute_import, print_function
from post import TrackAndTrace

TrackAndTrace.get_shipping_status(('RJ843530753CN', 'meh', 'RL246645949CN'))

import sys
sys.exit(0)

with open('/Users/dbarton/Desktop/track.html', 'r') as f:
    h = f.read()

from bs4 import BeautifulSoup

p = BeautifulSoup(h, 'html.parser')

r = p.find_all('span', attrs={'class': 'shipmentNumber'})
r = p.body.find_all('td', attrs={'class': 'fvEvent'})

print(r)
