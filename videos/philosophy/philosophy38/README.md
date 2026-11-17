# Philosophy, Built — Part 38: Justice

Part 38 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)), in Act VII, *Value*:
what a society owes its members. Rawls's first sentence (1971) and Sen's flute (2009); three toy societies scored by
total, least income and Gini. Thrasymachus and the ring of Gyges; Plato's city and soul and Popper's charge (1945);
Aristotle's proportional and corrective justice. The social contract: Hobbes (Part 34's game), Locke (1689) and the
proviso, Rousseau (1762), Hume against tacit consent (1748). Rawls's original position, primary goods, the two
principles and lexical priority; **the difference principle drawn** on an incentive frontier ((8, 6) over (5, 5) and
(12.5, 3.75)); the three conditions for maximin (§26); Rawls's five regimes (2001). Harsanyi against Rawls (1953,
1975) and the separateness of persons; **two hundred societies chosen behind the veil** (the average picks one,
maximin another, CRRA expected utility with η from 0.5 to 5 a third, η ≥ 8 the maximin society); Sen (2009) and
Cohen (2008). Nozick's entitlement theory (1974); **Wilt Chamberlain as a toy economy** (a Gini of 0.01 from free
exchange) and a **Price List** for the argument; the proviso, rectification and Cohen on self-ownership (1995);
left-libertarianism from Paine (1797) and George (1879) to Steiner, Otsuka and Van Parijs (1995). Dworkin's equality of
resources (1981), brute and option luck; **Dworkin's auction built** as a competitive equilibrium from equal incomes
(Varian 1974; prices 1.11, 0.89, 1; envy-free in Foley's sense, 1967); Anderson (1999); Sen's capabilities (1979) and
Nussbaum (2000); Frankfurt (1987), levelling down, Roemer (1998), Casal (2007). Sen's liberal paradox (1970): Lady
Chatterley's Lover as a cycle, and **every assignment of two rights searched** (six, each forced into a cycle) —
**the Wall's thirty-eighth brick**; Gibbard (1974), game forms (Gärdenfors 1981; Sugden 1985; Gaertner, Pattanaik and
Suzumura 1992), and contracting over rights (Harel and Nitzan 1987). Liberty: Berlin (1958), MacCallum (1967), Cohen's
ticket, Pettit's non-domination (1997) and Skinner, Constant (1819), Mill (1859), Hart and Feinberg, nudges (2008),
and Pattanaik and Xu's theorem on measuring freedom (1990) with Sen's reply. Fair division, built: **cut and choose**,
**Selfridge–Conway for three** (every bundle valued by every person; no envy), Steinhaus (1948), Dubins–Spanier (1961),
Brams–Taylor (1995), Aziz–Mackenzie (2016); **envy-free rent division** maximizing the least surplus (Gal, Mash,
Procaccia and Zick 2016; rents 1330, 935, 735); EF1 and maximum Nash welfare; Budish's course allocation (2011); and
**deferred acceptance for school choice** (Gale and Shapley 1962), with all 24 matchings enumerated (3 stable, the
student-proposing one best for every student). Community and role: Sandel (1982), MacIntyre (1981), Taylor, Political
Liberalism (1993), Walzer (1983), Okin (1989), Pateman (1988), Mills (1997), Young (1990), Xunzi on ritual, Mencius,
Chan (2014), Bai (2019) and Bell (2015). Justice beyond borders: Beitz (1979), Pogge (2002), Rawls (1999), Nagel
(2005), Blake (2001), Cohen and Sabel (2006), Carens (1987), Wellman (2008), just savings, Shue (1993), Gardiner
(2011), and justice for machines: Gabriel (2020) and Weidinger et al. (2023).

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/justice.py` (with
`prop` for the Price List), tested in `tests/philosophy/test_justice.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy38.compute       # every computed item (seconds; .cache/philosophy38)
python tools/build.py philosophy38 -q l                # 480p preview
python tools/build.py philosophy38                     # 1080p30 -> renders/philosophy38.mp4
python tools/qa_scene.py philosophy38 Division         # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Rawls (1971); Sen's flute (2009); four answers; the plan. | three societies: totals, minima, Ginis |
| 1 | `Plato` | Thrasymachus; Gyges; the city and the soul; Popper (1945); Aristotle. | — |
| 2 | `Contract` | Hobbes; Locke (1689); Rousseau (1762); Hume (1748). | — |
| 3 | `Rawls` | the original position; two principles; maximin's conditions; five regimes (2001). | the difference principle on a frontier |
| 4 | `Veil` | Harsanyi (1953, 1975); risk attitude; strains of commitment; Sen (2009); Cohen (2008). | 200 societies under average, maximin and CRRA |
| 5 | `Nozick` | Nozick (1974); Cohen (1995); Murphy and Nagel (2002); Paine; George; Steiner; Otsuka; Van Parijs. | Wilt Chamberlain; **the Price List** |
| 6 | `Luck` | Dworkin (1981); Cohen; Arneson; Anderson (1999); Sen (1979); Nussbaum; Frankfurt; Roemer; Casal. | CEEI, envy checked |
| 7 | `Sen` | Sen (1970); Gibbard (1974); Nozick; Gärdenfors; Sugden; Harel and Nitzan; **the Wall's thirty-eighth brick**. | all six assignments of rights searched |
| 8 | `Liberty` | Berlin (1958); MacCallum (1967); Cohen; Pettit (1997); Skinner; Constant; Mill; Pattanaik and Xu (1990); Carter; Kramer. | — |
| 9 | `Division` | Steinhaus; Dubins–Spanier; Brams–Taylor; Aziz–Mackenzie; Procaccia; Lipton et al.; Caragiannis et al.; Budish; Gale–Shapley; Roth. | cut and choose; Selfridge–Conway; rent; deferred acceptance |
| 10 | `Community` | Sandel (1982); MacIntyre; Taylor; Rawls (1993); Walzer (1983); Okin; Pateman; Mills; Young; Xunzi; Mencius; Chan; Bai; Bell. | — |
| 11 | `Global` | Beitz; Pogge; Milanović; Rawls (1999); Nagel; Blake; Cohen and Sabel; Carens; Wellman; Shue; Gardiner; Gabriel; Weidinger et al. | — |
| 12 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Notes

The veil's societies are drawn at random (seed 1971): five equal classes, with richer societies tending to be more
unequal; CRRA utilities are compared through the mean of w^(1−η) so that large η does not tie in floating point. The
CEEI is found by proportional response dynamics (3,000 rounds). Cake valuations are piecewise constant on tenths and
normalized to 1. Rent prices are searched on a $5 grid. The school-choice preferences were picked from random
profiles so that deferred acceptance takes several rounds and there is more than one stable matching.

## Problems and solutions

1. Show that if only one person has rights, over any number of pairs, rights and Pareto never force a cycle.

   *Solution.* Social strict preference is built from two sources: person 1's preferences on her decisive pairs, and unanimous preferences (Pareto). Every Pareto preference is also person 1's preference, since she is one of the unanimous. So every strict social preference agrees with person 1's own ranking, which is transitive, and a cycle $x \succ y \succ z \succ x$ would be a cycle in her ranking. No cycle can be forced, however many pairs she controls. Sen's paradox needs two people with rights, each over a pair, whose preferences the Pareto principle can link into a loop.

2. Compute the Gini coefficient of the incomes (0, 0, 0, 1), and explain why it is not 1.

   *Solution.* Using $G = \sum_i \sum_j |x_i - x_j| / (2n^2\mu)$: the ordered pairs with different incomes contribute $2 \times 3 \times 1 = 6$, and $2n^2\mu = 2 \times 16 \times 0.25 = 8$, so $G = 0.75$ (the Reasoner's formula gives the same). It is not 1 because with $n$ people the most unequal distribution, one person with everything, has $G = (n - 1)/n$: the one rich person is equal to herself. Only as $n \to \infty$ does the maximum approach 1.

3. With societies (1, 9) and (4, 4), for which η does the CRRA chooser prefer the second?

   *Solution.* With utility $u(x) = x^{1 - \eta}/(1 - \eta)$ ($\log x$ at $\eta = 1$) and an equal chance of being either person, the chooser prefers $(4, 4)$ when $u(4) > \tfrac12[u(1) + u(9)]$. At $\eta = 0$ the averages are 4 against 5, and $(1, 9)$ wins. At $\eta = \tfrac12$, $u(x) = 2\sqrt x$: $u(4) = 4$ and $\tfrac12(2 + 6) = 4$, a tie. For $\eta > \tfrac12$ the concavity outweighs the higher mean (at $\eta = 1$: $\log 4 = 1.39$ against $\tfrac12\log 9 = 1.10$). So the chooser prefers the equal society exactly when $\eta > 1/2$.

4. Show that Ana, the first cutter, never envies whoever took the trimmed piece in Selfridge–Conway.

   *Solution.* In Ana's measure her three pieces are worth $\tfrac13$ each, and the trimmed piece is worth less than $\tfrac13$ by the value of its trimming, $t$. Ana always gets an untrimmed piece, worth $\tfrac13$ to her. Whoever took the trimmed piece then gets at most part of the trimmings, worth at most $t$ to Ana. So in Ana's measure that person ends with at most $(\tfrac13 - t) + t = \tfrac13$, no more than Ana's untrimmed piece alone, and Ana also gets a share of the trimmings. She never envies them, whatever happens in the second round.

5. Check that rents (1400, 900, 700) are also envy-free, and find the least surplus.

   *Solution.* Rooms are assigned as in the film (person 1 the first room, and so on), with values person 1: (1500, 1000, 500), person 2: (1300, 1100, 600), person 3: (1200, 900, 900). With rents (1400, 900, 700) the surpluses are $1500 - 1400 = 100$, $1100 - 900 = 200$ and $900 - 700 = 200$. Envy checks: person 1 would get $1000 - 900 = 100$ from room 2 (no better) and $-200$ from room 3; person 2 would get $-100$ from either other room; person 3 would get $-200$ from room 1 and $0$ from room 2. So the rents are envy-free, and the least surplus is 100, against 165 for the Reasoner's maximin prices (1330, 935, 735).

6. State the Wilt Chamberlain argument as an inconsistent set, and say which claim you would deny.

   *Solution.* (1) D1, the equal distribution, is just. (2) Whatever arises from a just distribution by just steps is just. (3) Each fan's paying a quarter to watch Wilt is a just step. (4) D2, in which Wilt is far richer, violates the patterned principle that made D1 just, so it is unjust. The four are inconsistent. Nozick denies (4), and with it every patterned principle. I would deny (2), with Rawls: justice is a property of the basic structure, and individually fair transactions can cumulatively erode the background conditions (fair bargaining, equal political power) that made them fair, so the structure needs ongoing adjustment, such as taxation, rather than a one-off just start.

