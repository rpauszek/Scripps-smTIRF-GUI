# -*- coding: utf-8 -*-
"""
@author: Raymond F. Pauszek III, Ph.D. (2020)
script >> test results
"""
from pathlib import Path
import smtirf
import matplotlib.pyplot as plt

filename = Path("./testdata/trial_MixedFlap_20181010-08.smtrc").resolve()
print(filename)

e = smtirf.Experiment.load(filename)
print(e)
print(e[1].dwells.get_transitions())

# split histogram
c, h, S, width = smtirf.results.get_split_histogram(e, nBins=300)
for s in S:
    plt.bar(c, s, width=width, alpha=0.5)
plt.step(c, h, where='mid', c='k')
plt.show()

# TDP
x, y, z = smtirf.results.get_tdp(e, bandwidth=0.02)
plt.subplot(1, 1, 1, aspect='equal')
plt.contourf(x, y, z, 150, cmap="cividis")
plt.show()
