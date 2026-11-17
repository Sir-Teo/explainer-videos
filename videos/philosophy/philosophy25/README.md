# Philosophy, Built — Part 25: Space and Time

Part 25 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): the philosophy of space and
time, with every geometry and spacetime built. Newton's absolute space and his bucket, its paraboloid computed (a
15 cm bucket at about one turn a second climbs some 4 cm), and Mach's reply. The Leibniz–Clarke correspondence: the
static and kinematic shifts, checked on a universe of six moving bodies (every inter-body distance unchanged by a
shift, a rotation, a boost and a rotation in time, though only the last would curve the water). Kant's incongruent
counterparts: orientation as signed area, two hundred rigid motions that never change its sign, and a frame carried
round a Möbius strip that comes back reversed. Non-Euclidean geometry built in the Poincaré disk: geodesics, many
parallels, hyperbolic triangles whose angle sums fall from 177° to 23.5° while their areas (the defect) approach π;
Gauss's survey triangle and its 15 arcseconds of spherical excess. Poincaré's disk world, whose shrinking rulers
measure a hyperbolic plane, and conventionalism (Poincaré, Reichenbach, Einstein, Putnam). Spacetime structures from
Aristotle to Leibniz, and Earman's symmetry principles: Galilean spacetime has just enough. Special relativity:
the Minkowski diagram with tilting slices of simultaneity, Einstein's lightning strikes in four frames, the invariant
interval. Reichenbach's ε and Malament's theorem. McTaggart's A- and B-series and his regress; presentism, the growing
block, the moving spotlight and eternalism; the Rietdijk–Putnam argument with its boost computed, and the
presentist's replies. General relativity and the hole argument (Einstein 1913; Earman and Norton 1987), the hole
diffeomorphism animated, as a **Price List** and **the Wall's twenty-fifth brick**. Barbour and Bertotti's best
matching, built with the Kabsch algorithm. Gödel's rotating universe, Lewis's grandfather paradox, and Deutsch's
closed timelike curves, whose fixed points are computed for the grandfather and knowledge paradoxes. And, labelled
as speculative, spacetime from entanglement (Maldacena; Ryu and Takayanagi; Van Raamsdonk; ER = EPR), and causal sets
(Bombelli, Lee, Meyer and Sorkin): four hundred events sprinkled into flat spacetime, the coordinates forgotten, and
the dimension (2, 3, 4) recovered from the causal order alone by the Myrheim–Meyer estimator.

The worked model results are computed by the Reasoner's new module `explainer/philosophy/reasoner/spacetime.py` (with
`prop` for the Price List), tested in `tests/philosophy/test_spacetime.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy25.compute       # every computed item (seconds; .cache/philosophy25)
python tools/build.py philosophy25 -q l                # 480p preview
python tools/build.py philosophy25                     # 1080p30 -> renders/philosophy25.mp4
python tools/qa_scene.py philosophy25 Hole             # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Augustine; four questions; the plan. | — |
| 1 | `Bucket` | Newton (1687); Mach (1883); Maudlin. | the bucket's paraboloid |
| 2 | `Leibniz` | Leibniz and Clarke (1715–16); Galileo's ship. | shifted universes, every distance checked |
| 3 | `Hands` | Kant (1768, 1783); Möbius; Wu (1957). | signed areas; Möbius transport |
| 4 | `Geometry` | Euclid; Lobachevsky (1829); Bolyai (1832); Gauss; Poincaré; Riemann (1854). | hyperbolic triangles; Gauss's excess |
| 5 | `Convention` | Poincaré (1902); Reichenbach (1928); Einstein; Putnam; Duhem and Quine. | the disk world's measurements |
| 6 | `Structures` | Aristotle; Newton; Galileo; Leibniz; Earman (1989); Maudlin (2012). | — |
| 7 | `Relativity` | Einstein (1905); Minkowski (1908). | simultaneity in four frames; the interval |
| 8 | `Simultaneity` | Reichenbach (1928); Malament (1977); Sarkar and Stachel (1999). | Reichenbach's ε |
| 9 | `McTaggart` | McTaggart (1908); Prior; Russell, Mellor, Smart. | — |
| 10 | `Theories` | Rietdijk (1966); Putnam (1967); Stein (1968). | the Rietdijk–Putnam boost |
| 11 | `Hole` | Einstein (1913, 1915); Earman and Norton (1987); **the Wall's twenty-fifth brick**; the hole as a **Price List**. | the hole diffeomorphism |
| 12 | `Relational` | Barbour and Bertotti (1982); Barbour (1999); Kabsch (1976). | best matching |
| 13 | `TimeTravel` | Gödel (1949); Lewis (1976); Deutsch (1991); Novikov; Hawking (1992). | Deutsch's fixed points |
| 14 | `Emergence` | Maldacena (1997); Ryu and Takayanagi (2006); Van Raamsdonk (2010); Maldacena and Susskind (2013); Hawking, King and McCarthy (1976); Malament (1977); Bombelli, Lee, Meyer and Sorkin (1987); Huggett and Wüthrich. | a causal set's links; the dimension from order |
| 15 | `Outro` | recap; the Reasoner's module; the Wall; problems; payoffs; references. | — |

## Problems and solutions

1. How fast must a 15 cm bucket spin for the water to rise 10 cm at the wall?

   *Solution.* The surface is the paraboloid $h(r) = \omega^2 r^2/2g$, so the rise at the wall, $R = 0.15$ m, is $\omega^2R^2/2g$. Setting it to 0.10 m: $\omega^2 = 2 \times 9.81 \times 0.10 / 0.0225 = 87.2$, $\omega = 9.3$ rad/s, about 1.5 turns a second (89 rpm). As a check, the film's one turn a second ($\omega = 6.28$) gives $6.28^2 \times 0.0225/19.62 = 4.5$ cm.

2. Show that a rotation of the plane keeps the sign of a polygon's signed area.

   *Solution.* The signed area of a polygon with vertices $(x_i, y_i)$ is $A = \tfrac12\sum_i (x_i y_{i+1} - x_{i+1} y_i)$, a sum of two-dimensional cross products of successive vertices. Under a linear map $M$ each cross product is multiplied by $\det M$, so $A$ becomes $(\det M) A$. A rotation has $\det M = \cos^2\theta + \sin^2\theta = 1$, so the sign is kept. A translation adds the same vector to every vertex; the extra terms telescope around the closed polygon and cancel. A reflection has $\det M = -1$ and flips the sign: that is Kant's left and right hand.

3. A hyperbolic triangle has angles $30^\circ$, $45^\circ$, $60^\circ$. What is its area?

   *Solution.* In the hyperbolic plane of curvature $-1$ a triangle's area is its angle defect, $\pi$ minus the angle sum. Here the angles are $\pi/6 + \pi/4 + \pi/3 = 3\pi/4$, so the area is $\pi/4 \approx 0.785$. (With curvature $-K$ the area is $(\pi/4)/K$.)

4. Find the boost that makes the event $(t, x) = (0.3, 0.5)$ simultaneous with the origin.

   *Solution.* In units with $c = 1$, a boost of velocity $v$ gives $t' = \gamma(t - vx)$, $x' = \gamma(x - vt)$. The event is simultaneous with the origin when $t' = 0$, so $v = t/x = 0.6$, and $\gamma = 1/\sqrt{1 - 0.36} = 1.25$. In that frame $x' = 1.25\,(0.5 - 0.18) = 0.4$. Check: the interval is $x^2 - t^2 = 0.25 - 0.09 = 0.16 = 0.4^2$. Such a boost exists because the event is spacelike, $|x| > |t|$; for a timelike event no observer would call it simultaneous with the origin.

5. State the hole argument for Newtonian gravity in Galilean spacetime. Does it go through?

   *Solution.* Set Newtonian gravity in Galilean spacetime: fixed absolute time, Euclidean space on each instant, a fixed flat connection, and a potential $\varphi$ with $\nabla^2\varphi = 4\pi G\rho$. The hole argument needs a transformation that is the identity outside a region and not inside it, and that carries solutions to solutions. Here it would have to preserve the fixed structure, and the symmetries of Galilean spacetime (rotations, translations, boosts) are rigid: one that is the identity on an open region is the identity everywhere. So no hole transformation exists and the argument does not go through. It does go through for the generally covariant Newton–Cartan version, where the connection is itself a dynamical field: then the hole argument is a lesson about any theory with no fixed background, not about relativity alone.

6. Grandfather circuit with a CNOT instead of a NOT: find Deutsch's fixed points.

   *Solution.* Let the ordinary bit be the control and the time-travelling qubit the target of the CNOT. Deutsch's condition is that the state entering the curve, $\rho$, equals what comes out of the interaction, traced over the ordinary bit. If the ordinary bit is 0 the CNOT does nothing, and every state is a fixed point: a knowledge paradox, with Deutsch's maximum-entropy rule picking $I/2$. If it is 1, the CNOT is a NOT on the loop, the grandfather paradox: fixed points are the states with $\rho = X\rho X$, that is $\tfrac12(I + r_x X)$, including $I/2$ and the states $|{+}\rangle$, $|{-}\rangle$, and no classical bit. If it is $|{+}\rangle$, the map averages the two cases and the fixed points are the same as for 1. In every case $I/2$ is consistent, and the classical paradox appears only when the control is definitely 1.

## Sources

Texts: Earman, *World Enough and Space-Time* (1989); Huggett (ed.), *Space from Zeno to Einstein* (1999); Barbour,
*The End of Time* (1999); Dainton, *Time and Space* (2nd ed., 2010); Maudlin, *Philosophy of Physics: Space and Time*
(2012); Arntzenius, *Space, Time, and Stuff* (2012); Norton, "The Hole Argument" (*Stanford Encyclopedia of
Philosophy*).

Papers and primary texts: Newton (1687); Leibniz and Clarke (1715–16); Kant (1768); Lobachevsky (1829); Bolyai
(1832); Riemann (1854); Mach (1883); Poincaré (1902); Einstein (1905, 1915); Minkowski (1908); McTaggart (1908);
Reichenbach (1928); Gödel (1949); Rietdijk (1966); Putnam (1967); Stein (1968); Hawking, King and McCarthy (1976);
Lewis (1976); Malament (1977); Barbour and Bertotti (1982); Bombelli, Lee, Meyer and Sorkin (1987); Earman and Norton
(1987); Meyer (1988); Deutsch (1991); Hawking (1992); Maldacena (1997); Sarkar and Stachel
(1999); Ryu and Takayanagi (2006); Van Raamsdonk (2010); Maldacena and Susskind (2013); Huggett and Wüthrich (2013).
