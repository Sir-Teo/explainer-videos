"""The Museum: real historical data, transcribed with its source, for *Statistics, Built*.

Every table here is a historical record (published before 1931) or a small published table of facts, kept as plain
Python data with its provenance, so a scene can cite it on screen.  See videos/stats/SYLLABUS.md, section 4.

Sources and notes:

* **Arbuthnot (1710)** -- annual London christenings by sex, 1629-1710, from the Bills of Mortality: J. Arbuthnot,
  "An argument for Divine Providence, taken from the constant regularity observ'd in the births of both sexes",
  *Philosophical Transactions* 27 (1710), 186-190.  Burials and plague deaths for the same years from C. Creighton,
  *A History of Epidemics in Britain* (1891; 2nd ed. 1965), as compiled by R. B. Campbell (2001) and distributed in
  the R package HistData (M. Friendly).  The 1704 christenings duplicate 1674's (a copying error noted by Zabell 1976).
  Christenings are baptisms, not births.
* **Graunt (1662)** -- the life table of *Natural and Political Observations Made upon the Bills of Mortality*,
  ch. 11: of 100 conceived, the number alive at 6, 16, 26, ... 86.
* **Quetelet (1846)** -- chest circumferences (inches) of Scottish militiamen, first printed in the *Edinburgh Medical
  and Surgical Journal* (1817); Quetelet's *Lettres* (1846) reported 5,738 men.  This is the table as corrected
  against the 1817 original by S. M. Stigler, *The History of Statistics* (1986), p. 208 (HistData ``ChestStigler``).
* **Anscombe (1973)** -- "Graphs in statistical analysis", *The American Statistician* 27, 17-21.
* **Nightingale (1858)** -- monthly deaths of the British army in the East, April 1854 to March 1856, by cause
  (zymotic disease, wounds, other), and the army's size; *Notes on Matters Affecting the Health ... of the British
  Army* (1858), via Pearson & Short (2007) and HistData.
* **Playfair (1821)** -- the price of a quarter of wheat (shillings) and a good mechanic's weekly wages, 1565-1821,
  from *A Letter on our Agricultural Distresses* (1821), digitized by Friendly via HistData.
* **Minard (1869)** -- survivors of Napoleon's army along the 1812 Russian campaign (longitude, latitude, survivors,
  direction A = advance / R = retreat, group), from L. Wilkinson's *The Grammar of Graphics*, via HistData.
"""

from __future__ import annotations

# --- Arbuthnot (1710): London christenings, burials and plague deaths, one entry per year from 1629 ---
ARB_YEAR0 = 1629
ARB_MALES = [5218, 4858, 4422, 4994, 5158, 5035, 5106, 4917, 4703, 5359, 5366, 5518, 5470, 5460, 4793, 4107, 4047, 3768, 3796,
    3363, 3079, 2890, 3231, 3220, 3196, 3441, 3655, 3668, 3396, 3157, 3209, 3724, 4748, 5216, 5411, 6041, 5114, 4678,
    5616, 6073, 6506, 6278, 6449, 6443, 6073, 6113, 6058, 6552, 6423, 6568, 6247, 6548, 6822, 6909, 7577, 7575, 7484,
    7575, 7737, 7487, 7604, 7909, 7662, 7602, 7676, 6985, 7263, 7632, 8062, 8426, 7911, 7578, 8102, 8031, 7765, 6113,
    8366, 7952, 8379, 8239, 7840, 7640]
ARB_FEMALES = [4683, 4457, 4102, 4590, 4839, 4820, 4928, 4605, 4457, 4952, 4784, 5332, 5200, 4910, 4617, 3997, 3919, 3395, 3536,
    3181, 2746, 2722, 2840, 2908, 2959, 3179, 3349, 3382, 3289, 3013, 2781, 3247, 4107, 4803, 4881, 5681, 4858, 4319,
    5322, 5560, 5829, 5719, 6061, 6120, 5822, 5738, 5717, 5847, 6203, 6033, 6041, 6299, 6533, 6744, 7158, 7127, 7246,
    7119, 7214, 7101, 7167, 7302, 7392, 7316, 7483, 6647, 6713, 7229, 7767, 7626, 7452, 7061, 7514, 7656, 7683, 5738,
    7779, 7417, 7687, 7623, 7380, 7288]
ARB_BURIALS = [8771, 10554, 8562, 9535, 8393, 10400, 10651, 23359, 11763, 13624, 9862, 12771, 13142, 13273, 13212, 10933, 11479,
    12780, 14059, 9894, 10566, 8754, 10827, 12569, 10087, 13247, 11357, 13921, 12434, 14993, 14756, 12681, 16665, 13664,
    12741, 15453, 97306, 12738, 15842, 17278, 19432, 20198, 15729, 18230, 17504, 21201, 17244, 18732, 19076, 20678,
    21730, 21053, 23951, 20691, 20587, 23202, 23222, 22609, 21460, 22921, 23502, 21461, 22691, 20874, 20959, 24109,
    19047, 18638, 20292, 20183, 20795, 19443, 20471, 19481, 20720, 22684, 22097, 19847, 21600, 21291, 21800, 24620]
ARB_PLAGUE = [0, 1317, 274, 8, 0, 1, 0, 10400, 3082, 363, 314, 1450, 1375, 1274, 996, 1492, 1871, 2365, 3597, 611, 67, 15, 23,
    16, 6, 16, 9, 6, 4, 14, 36, 13, 20, 12, 9, 5, 68596, 1998, 35, 14, 3, 0, 5, 5, 5, 3, 1, 2, 2, 5, 2, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ARB_YEARS = list(range(ARB_YEAR0, ARB_YEAR0 + len(ARB_MALES)))

# --- Graunt (1662): of 100 conceived, alive at each age ---
GRAUNT_AGES = [0, 6, 16, 26, 36, 46, 56, 66, 76, 86]
GRAUNT_ALIVE = [100, 64, 40, 25, 16, 10, 6, 3, 1, 0]

# --- Quetelet / Stigler: chest circumference in inches, and the number of militiamen ---
CHEST_IN = list(range(33, 49))
CHEST_COUNT = [3, 19, 81, 189, 409, 753, 1062, 1082, 935, 646, 313, 168, 50, 18, 3, 1]

# --- Anscombe (1973): four datasets with the same summary statistics ---
ANSCOMBE_X = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
ANSCOMBE = {
    1: (ANSCOMBE_X, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    2: (ANSCOMBE_X, [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    3: (ANSCOMBE_X, [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    4: ([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8], [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
}

# --- Nightingale (1858): the army in the East, monthly from April 1854 ---
NIGHT_MONTH = ['1854-04', '1854-05', '1854-06', '1854-07', '1854-08', '1854-09', '1854-10', '1854-11', '1854-12', '1855-01',
    '1855-02', '1855-03', '1855-04', '1855-05', '1855-06', '1855-07', '1855-08', '1855-09', '1855-10', '1855-11',
    '1855-12', '1856-01', '1856-02', '1856-03']
NIGHT_ARMY = [8571, 23333, 28333, 28722, 30246, 30290, 30643, 29736, 32779, 32393, 30919, 30107, 32252, 35473, 38863, 42647,
    44614, 47751, 46852, 37853, 43217, 44212, 43485, 46140]
NIGHT_DISEASE = [1, 12, 11, 359, 828, 788, 503, 844, 1725, 2761, 2120, 1205, 477, 508, 802, 382, 483, 189, 128, 178, 91, 42, 24, 15]
NIGHT_WOUNDS = [0, 0, 0, 0, 1, 81, 132, 287, 114, 83, 42, 32, 48, 49, 209, 134, 164, 276, 53, 33, 18, 2, 0, 0]
NIGHT_OTHER = [5, 9, 6, 23, 30, 70, 128, 106, 131, 324, 361, 172, 57, 37, 31, 33, 25, 20, 18, 32, 28, 48, 19, 35]

# --- Playfair (1821): wheat price and wages; None where Playfair gives no value ---
PLAYFAIR_YEAR = [1565, 1570, 1575, 1580, 1585, 1590, 1595, 1600, 1605, 1610, 1615, 1620, 1625, 1630, 1635, 1640, 1645, 1650, 1655,
    1660, 1665, 1670, 1675, 1680, 1685, 1690, 1695, 1700, 1705, 1710, 1715, 1720, 1725, 1730, 1735, 1740, 1745, 1750,
    1755, 1760, 1765, 1770, 1775, 1780, 1785, 1790, 1795, 1800, 1805, 1810, 1815, 1820, 1821]
PLAYFAIR_WHEAT = [41.0, 45.0, 42.0, 49.0, 41.5, 47.0, 64.0, 27.0, 33.0, 32.0, 33.0, 35.0, 33.0, 45.0, 33.0, 39.0, 53.0, 42.0, 40.5,
    46.5, 32.0, 37.0, 43.0, 35.0, 27.0, 40.0, 50.0, 30.0, 32.0, 44.0, 33.0, 29.0, 39.0, 26.0, 32.0, 27.0, 27.5, 31.0,
    35.5, 31.0, 43.0, 47.0, 44.0, 46.0, 42.0, 47.5, 76.0, 79.0, 81.0, 99.0, 78.0, 54.0, 54.0]
PLAYFAIR_WAGES = [5.0, 5.05, 5.08, 5.12, 5.15, 5.25, 5.54, 5.61, 5.69, 5.78, 5.94, 6.01, 6.12, 6.22, 6.3, 6.37, 6.45, 6.5, 6.6, 6.75,
    6.8, 6.9, 7.0, 7.3, 7.6, 8.0, 8.5, 9.0, 10.0, 11.0, 11.75, 12.5, 13.0, 13.3, 13.6, 14.0, 14.5, 15.0, 15.7, 16.5,
    17.6, 18.5, 19.5, 21.0, 23.0, 25.5, 27.5, 28.5, 29.5, 30.0, None, None, None]

# --- Minard (1869): (longitude, latitude, survivors, direction, group) ---
MINARD = [(24.0, 54.9, 340000, 'A', 1), (24.5, 55.0, 340000, 'A', 1), (25.5, 54.5, 340000, 'A', 1), (26.0, 54.7, 320000, 'A',
    1), (27.0, 54.8, 300000, 'A', 1), (28.0, 54.9, 280000, 'A', 1), (28.5, 55.0, 240000, 'A', 1), (29.0, 55.1, 210000,
    'A', 1), (30.0, 55.2, 180000, 'A', 1), (30.3, 55.3, 175000, 'A', 1), (32.0, 54.8, 145000, 'A', 1), (33.2, 54.9,
    140000, 'A', 1), (34.4, 55.5, 127100, 'A', 1), (35.5, 55.4, 100000, 'A', 1), (36.0, 55.5, 100000, 'A', 1), (37.6,
    55.8, 100000, 'A', 1), (37.7, 55.7, 100000, 'R', 1), (37.5, 55.7, 98000, 'R', 1), (37.0, 55.0, 97000, 'R', 1),
    (36.8, 55.0, 96000, 'R', 1), (35.4, 55.3, 87000, 'R', 1), (34.3, 55.2, 55000, 'R', 1), (33.3, 54.8, 37000, 'R', 1),
    (32.0, 54.6, 24000, 'R', 1), (30.4, 54.4, 20000, 'R', 1), (29.2, 54.3, 20000, 'R', 1), (28.5, 54.2, 20000, 'R', 1),
    (28.3, 54.3, 20000, 'R', 1), (27.5, 54.5, 20000, 'R', 1), (26.8, 54.3, 12000, 'R', 1), (26.4, 54.4, 14000, 'R', 1),
    (25.0, 54.4, 8000, 'R', 1), (24.4, 54.4, 4000, 'R', 1), (24.2, 54.4, 4000, 'R', 1), (24.1, 54.4, 4000, 'R', 1),
    (24.0, 55.1, 60000, 'A', 2), (24.5, 55.2, 60000, 'A', 2), (25.5, 54.7, 60000, 'A', 2), (26.6, 55.7, 40000, 'A', 2),
    (27.4, 55.6, 33000, 'A', 2), (28.7, 55.5, 33000, 'A', 2), (28.7, 55.5, 33000, 'R', 2), (29.2, 54.2, 30000, 'R', 2),
    (28.5, 54.1, 30000, 'R', 2), (28.3, 54.2, 28000, 'R', 2), (24.0, 55.2, 22000, 'A', 3), (24.5, 55.3, 22000, 'A', 3),
    (24.6, 55.8, 6000, 'A', 3), (24.6, 55.8, 6000, 'R', 3), (24.2, 54.4, 6000, 'R', 3), (24.1, 54.4, 6000, 'R', 3)]
