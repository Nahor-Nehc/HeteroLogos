import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from components.PhonemeDistanceMatrix import PhonemeDistanceMatrix
from components.Phoneme import Phoneme

pdm = PhonemeDistanceMatrix(os.path.join("assets", "arpabet_delta_matrix.csv"))

phonemes = [Phoneme(x) for x in pdm._dict.keys()]
xs = []
for p1 in phonemes:
    for p2 in phonemes:
        xs.append(p1.distance(p2, pdm))

xs = np.array(xs)

print(np.mean(xs), np.std(xs))

plt.hist(xs)
plt.show()

close = [x for x in xs if 0 < x < 70]

# we can see a bimodal distribution
# analysing closer out of the phonemes which are kinda similar
# but not the same phoneme:

mu, sigma = np.mean(close), np.std(close)

plt.hist(close)
xs = np.linspace(0, 70, 1000)
ys_unscaled = norm.pdf(xs, mu, sigma)
ys = ys_unscaled/max(ys_unscaled) * 180
plt.plot(xs, ys, 'r')

plt.show()
# for the close phonemes the mean is 19