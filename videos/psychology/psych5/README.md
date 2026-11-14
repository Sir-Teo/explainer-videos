# Psychology, Built: Part 5, The Neuron

In the 1780s Luigi Galvani made a dead frog's leg kick by touching its nerve and muscle with two metals, and
concluded that animals carry electricity. In 1850 Helmholtz timed the signal in a frog's nerve at 25 to 43 metres a
second, far too slow for a current in a wire. A century later Alan Hodgkin and Andrew Huxley measured the currents
through the membrane of a squid's giant nerve fibre, fitted them with four equations, and solved the equations by
hand. A nerve signal came out, with a threshold, a fixed size, a dead time, and a speed of 18.8 metres a second
against the 21.2 measured in that axon. Nothing in the equations had been fitted to a nerve signal.

This part opens Act II, in which the series builds the machine. It asks what the mind's smallest moving part is
and what it computes. The route: the neuron doctrine; why a difference of concentration across a membrane is a
battery (Nernst, Goldman); the membrane as a leaky capacitor; the voltage clamp and what it showed; the four
equations; the action potential computed, with each of its properties traced to a gate; propagation on a cable
and the speed recovered; the reduction to two variables and the phase plane; integrate-and-fire and its closed
form; the rate code and the noise in it; and what one cell can compute, with and without dendrites. It is the
series' template for a model: measure the parts, write equations, compute, and compare with something that was
not put in.

## Where the numbers come from

| What | Source |
|---|---|
| The model's conductances, batteries and rate functions; the computed speed 18.8 m/s at 18.5 °C against 21.2 m/s measured; the first intracellular record (rest about −45 mV, peak about +40 mV) | Hodgkin and Huxley (1939, 1952); registered in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md), with what was read and what was not |
| The membrane's conductance rises during the signal and its capacitance does not; the giant axon | Cole and Curtis (1939); J. Z. Young (1936) |
| A single sensory fibre: impulses of one size, more frequent with more stretch | Adrian and Zotterman (1926), from secondary accounts; no rates are quoted |
| Golgi's net against Cajal's cells; the shared prize of 1906 | The Nobel Foundation's account |
| Graded calcium spikes in the dendrites of human cortical neurons | Gidon et al. (2020), from the authors' pages and press accounts |
| The speed of the signal in a frog's nerve, 25 to 43 m/s | Helmholtz (1850), as in Part 1 |
| Every curve, voltage, conductance, rate and speed "computed by Psyche" | `explainer.psychology.psyche.neuron`, from the published equations |
| Ion concentrations of the squid axon (K 20/400, Na 440/50, Cl 560/52 mM) | the figures usually quoted in textbooks; see Open checks |

The numbers that depend on choices made for the film. The spike in the film is the model membrane at 6.3 °C, the
temperature the rate functions are given for, stimulated with a 0.5 ms pulse of twice the threshold; at the squid's
own temperature everything is about three times faster. The cable is the 1952 axon (radius 238 μm, axoplasm
35.4 Ω cm, 18.5 °C). The integrate-and-fire neuron has a time constant of 10 ms, a threshold 15 mV above rest and a
dead time of 2 ms, chosen as round numbers. The stretch-receptor curve in chapter 10 and the two response curves
in chapter 14 are drawn to show a shape and are labelled as such; they are not data. The three trains of the
on-you exercise are one draw from a model cell at 35, 12 and 70 signals a second, and the count shown beside each
is that draw's own.

## Built in this part

* `explainer/psychology/psyche/neuron.py`, Psyche's first piece of tissue: Nernst and Goldman voltages, the
  charging curve, the Hodgkin-Huxley membrane (`HH`: `simulate`, `clamp`, `pulse`, `threshold`, `refractory`,
  `firing_rate`), propagation on a cable (`propagate`, `length_constant`), FitzHugh-Nagumo (`FHN`: nullclines,
  the rest state and its stability), leaky integrate-and-fire (`LIF`: the closed-form `rate`, `simulate`,
  `coincidence`), Poisson spike trains and the Fano factor, and a point neuron against a neuron with thresholding
  branches (`separable` decides exactly, by linear programming, whether any point neuron can match a table).
  Tested in `tests/psychology/test_neuron.py` against closed forms and the 1952 speed.
* The Ledger gains one row and the Archive five datasets.
* On the Homunculus map nothing changes yet: a neuron is not a faculty. The first circuits are Part 6.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Voltage-dependent sodium and potassium conductances account for the action potential and its speed | Hodgkin and Huxley 1952 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: the rate code of Adrian and
Zotterman (its row is due with sensory coding, Part 13), the neuron doctrine (a settled piece of anatomy, told as
history), and the graded dendritic spikes of 2020 (one laboratory's report, shown at the frontier). Cole and
Curtis's measurement rests under the row above, and Helmholtz's speed has had its row since Part 1.

## Build it

```bash
python -m videos.psychology.psych5.compute            # every number (about a minute), into .cache/psych5/
python tools/qa_scene.py psych5 Spike                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych5 -q l   # the whole part, silent preview
python tools/build.py psych5                          # 1080p30 with narration
python tools/qa_scene.py psych5 Spike --lang zh       # the Chinese edition of one chapter
python tools/make.py psych5                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 5                    # the lab: a membrane taken from clamp to spike to cable
python tools/check_ledger.py psych5                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                     # Psyche's neuron, the Pool, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | What moves along a nerve? | Galvani and Volta; Helmholtz's speed against a wire's; four equations and a predicted speed; objectives |
| 1 | One net, or many cells | Golgi against Cajal; the neuron doctrine; a neuron drawn, with its direction |
| 2 | Ions and the membrane | Diffusion against voltage; the Nernst potential; two batteries; the Goldman voltage as a dial |
| 3 | The membrane as a circuit | Capacitor, resistor, battery; the charging curve and the time constant; a membrane adds and forgets |
| 4 | The squid and the voltage clamp | The giant axon; the overshoot of 1939; the loop of voltage and channels, and the clamp that breaks it; two conductances with different habits |
| 5 | Four equations | Why a fourth power gives a delay; the gates m, h and n and their speeds; the model whole, fitted only to the clamp |
| 6 | The action potential, computed | One signal with its conductances, step by step; threshold and all-or-none; the refractory period |
| 7 | Down the axon | Passive spread and the length constant; the travelling signal and its computed speed; radius, and myelin |
| 8 | Two variables are enough | FitzHugh-Nagumo; the phase plane, where threshold, size and dead time are geometry; two ways to start firing |
| 9 | Integrate and fire | A leaky capacitor and a rule; the firing rate in closed form; what was kept and what was lost |
| 10 | On you: reading a spike train | Adrian's rate code; three trains to rank; the same stimulus eight times, the Fano factor, and why a brain pools cells |
| 11 | What one neuron can compute | A threshold unit and the table it cannot produce; coincidence detection; a neuron with two thresholding branches |
| 12 | The Ledger | The Hodgkin-Huxley model, in full |
| 13 | In practice: talking to nerves | Cochlear implants, local anaesthetics, deep-brain stimulation, neuromorphic chips; what the model tells an engineer and what it does not |
| 14 | Frontier: how much is one neuron? | Graded dendritic spikes in human cortex; four open questions and a research problem |
| | Recap, problems, and the road ahead | Ten lines; Kant's first objection answered at its strongest; payoffs; problems; references; Part 6 |

## Sources

**Books.** E. R. Kandel, J. D. Koester, S. H. Mack and S. A. Siegelbaum (eds.), *Principles of Neural Science*
(6th ed., 2021), the chapters on the membrane and the action potential. P. Dayan and L. F. Abbott, *Theoretical
Neuroscience* (2001), chapters 5 and 6. E. M. Izhikevich, *Dynamical Systems in Neuroscience* (2007). C. Koch,
*Biophysics of Computation* (1999). S. Finger, *Minds Behind the Brain* (2000).

**Papers.**
- A. L. Hodgkin and A. F. Huxley, "Action potentials recorded from inside a nerve fibre", *Nature* 144 (1939)
  710–712; "A quantitative description of membrane current and its application to conduction and excitation in
  nerve", *Journal of Physiology* 117 (1952) 500–544. A. F. Huxley, "From overshoot to voltage clamp", *Trends in
  Neurosciences* 25 (2002) 553–558.
- K. S. Cole and H. J. Curtis, "Electric impedance of the squid giant axon during activity", *Journal of General
  Physiology* 22 (1939) 649–670.
- E. D. Adrian and Y. Zotterman, "The impulses produced by sensory nerve-endings. Part II. The response of a
  single end-organ", *Journal of Physiology* 61 (1926) 151–171.
- L. Lapicque, "Recherches quantitatives sur l'excitation électrique des nerfs traitée comme une polarisation",
  *Journal de Physiologie et de Pathologie Générale* 9 (1907) 620–635.
- R. FitzHugh, "Impulses and physiological states in theoretical models of nerve membrane", *Biophysical Journal*
  1 (1961) 445–466. J. Nagumo, S. Arimoto and S. Yoshizawa, "An active pulse transmission line simulating nerve
  axon", *Proceedings of the IRE* 50 (1962) 2061–2070.
- A. L. Hodgkin, "The local electric changes associated with repetitive action in a non-medullated axon",
  *Journal of Physiology* 107 (1948) 165–181.
- A. Gidon et al., "Dendritic action potentials and computation in human layer 2/3 cortical neurons", *Science*
  367 (2020) 83–87.

## Problems and solutions

**1.** *Calcium is at 2 mM outside a cell and 0.0001 mM inside, and its ion carries two charges. Find its Nernst
potential at body temperature (RT/F = 26.7 mV). Which way does calcium move when a calcium channel opens at
−65 mV?*

E = (RT/zF) ln(out/in) = (26.7/2) ln(20,000) = 13.35 × 9.90 = +132 mV. At −65 mV the membrane is 197 mV below
calcium's equilibrium, so calcium flows in, hard: both diffusion and the voltage push it the same way. This is
why a brief opening of calcium channels is such an effective signal inside a cell, and why the dendritic spikes of
chapter 14, carried by calcium, are depolarizing. (`neuron.nernst(2, 1e-4, z=2, temp_c=37)`.)

**2.** *A membrane has resistance 10 kΩ cm² and capacitance 1 μF/cm². Find its time constant, and the time a step
of current takes to bring the voltage 95% of the way. Two equal inputs arrive 30 ms apart: how much of the first
is left when the second comes?*

τ = RC = 10⁴ Ω cm² × 10⁻⁶ F/cm² = 10 ms. The voltage covers a fraction 1 − e^(−t/τ) of the distance, which
reaches 0.95 when e^(−t/τ) = 0.05, at t = τ ln 20 = 3.0 τ = 30 ms. After the first input ends, what it left decays
as e^(−t/τ), so 30 ms later 5% of it remains: the two inputs hardly add. Inputs within a few milliseconds of each
other add almost fully. The time constant is the cell's window for summation.

**3.** *A gate starts at n = 0 and relaxes as n(t) = 1 − e^(−t/τ). Show that n starts rising at once, and that n⁴
starts with zero slope. What feature of the potassium record does that reproduce?*

dn/dt = (1/τ) e^(−t/τ), which is 1/τ at t = 0: the steepest part of the curve is its start. d(n⁴)/dt = 4n³ dn/dt,
which is 0 at t = 0 because n = 0 there; for small t, n ≈ t/τ and n⁴ ≈ (t/τ)⁴, flat at first and then rising.
That is the delay before the potassium conductance turns on under the clamp, the S-shaped onset of chapter 4. Any
power above 1 gives a delay; the fourth was what the records needed.

**4.** *At the peak of an action potential dV/dt = 0, with no injected current. Show from the model's first
equation that the peak voltage is an average of the three batteries, weighted by the conductances at that moment.
Why must it lie below E_Na?*

Setting C dV/dt = 0 and I = 0 gives g_Na(V − E_Na) + g_K(V − E_K) + g_L(V − E_L) = 0, where g_Na and g_K stand
for the conductances at that instant. Solving, V = (g_Na E_Na + g_K E_K + g_L E_L)/(g_Na + g_K + g_L). A weighted
average lies strictly inside the range of the things averaged unless all the weight is on one of them, and g_K and
g_L are never zero, so V < E_Na. In the film's spike the conductances at the peak are about 30.5, 2.3 and 0.3
mS/cm², which gives (30.5 × 50 − 2.3 × 77 − 0.3 × 54.4)/33.1 = +40 mV, the computed peak.

**5.** *For the integrate-and-fire neuron derive the time to reach threshold θ from reset under a steady current,
and the firing rate. With τ = 10 ms and a dead time of 2 ms, what is the rate at twice the least current that
fires the cell?*

Measure voltage from rest, with reset at rest. Below threshold V(t) = RI(1 − e^(−t/τ)). Setting V(T) = θ gives
e^(−T/τ) = 1 − θ/RI, so T = τ ln[RI/(RI − θ)], which exists only if RI > θ: the least current is θ/R. The period
is the dead time plus T, so f = 1/(t_ref + T). At RI = 2θ, T = τ ln 2 = 6.93 ms, the period is 8.93 ms and the
rate is 112 signals a second. (`neuron.LIF().rate(3.0)` gives 111.96 with the film's parameters, where the least
current is 1.5 nA.)

**6.** *With `explainer.psychology.psyche.neuron`: find the threshold of `HH()` for pulses of 0.1, 0.5, 2 and
10 ms. Show that for short pulses the charge delivered is what matters, and that long pulses need a least current.
Why does each happen?*

```python
from explainer.psychology.psyche import neuron
hh = neuron.HH()
for ms in (0.1, 0.5, 2, 10):
    th = hh.threshold(ms)                 # uA/cm^2
    print(ms, round(th, 1), round(th * ms, 1))
# 0.1 65.2 6.5      0.5 13.3 6.6      2 3.9 7.7      10 2.2 22.5
```

For pulses much shorter than the membrane's time constant (about 1.5 ms at rest), the threshold falls in
proportion to the duration and the product, the charge, stays near 6.5 nC/cm²: the membrane is a capacitor, and a
short pulse simply deposits charge on it before any can leak away. For long pulses the threshold levels off at
about 2.2 μA/cm², the least current that will ever fire the cell: a steady current weaker than that is balanced by
the leak and by the potassium it recruits before the sodium loop can start. This is the strength-duration curve
that the designer of any stimulator starts from.

**7.** ★ *Find the smallest change to the integrate-and-fire neuron that lets one cell compute "one but not
both", and say what measurement on a real cell would show whether it does.*

Open. Two candidates to start from. A response that is not monotonic in the input, as in the dendritic spikes of
chapter 14: add to the cell a branch whose contribution is largest at its own threshold and smaller above it; one
input then fires the cell and two together do not. Or inhibition recruited by coincidence: a second threshold,
above the first, at which the cell is shut. Each makes a different prediction on a real cell: the first, that the
somatic response to dendritic input of growing strength rises and then falls; the second, that blocking inhibition
restores the response to both inputs. The measurement has to deliver two inputs separately and together to the
same branch, and record at the soma.

## Where it comes back

How neurons talk, and how talking changes them: Part 6. What an electrode or a scanner measures: Part 8.
Detection as the counting of noisy signals: Part 12. Coincidence detectors that locate a sound: Part 15.
Accumulation to a threshold as a model of deciding: Part 25. The unit with its spikes left out, in artificial
networks: Part 60. Psyche's neuron (`psyche/neuron.py`) is the tissue under every later circuit.

## Open checks

Before the narrated master:

* Hodgkin and Huxley (1952) was not read. The computed speed (18.8 m/s at 18.5 °C) was confirmed from a textbook
  figure adapted from the paper; the measured speed (21.2 m/s), the axon's radius (238 μm) and its axoplasm
  resistivity (35.4 Ω cm) are from memory of the paper and should be checked there, with the statement that the
  equations were integrated by hand on a mechanical calculator.
* The rest and peak of the 1939 record (about −45 and +40 mV) are as Huxley recalls them in 2002; check the
  *Nature* letter.
* The squid's ion concentrations are the usual textbook figures; check them against Hodgkin's own tables. The
  film's potassium battery (−72 mV) is the Nernst value for those figures, while the model uses −77 mV.
* Adrian and Zotterman (1926) was not read; the film gives the preparation and the finding, with schematic trains
  and no rates.
* Galvani's experiments, the dispute with Volta, Young's giant axon (1936), the voltage clamp's history (Cole,
  Marmont; Hodgkin, Huxley and Katz), Lapicque (1907), FitzHugh (1961), Nagumo et al. (1962), Hodgkin's classes
  (1948) and the four-part structure of potassium channels are stated from standard accounts.
* Gidon et al. (2020) was not read; the film's curve is a schematic and is labelled so.
* The practice chapter's statements about cochlear implants, lidocaine, deep-brain stimulation and neuromorphic
  chips are general knowledge and carry no figures except "hundreds of thousands" of implant users, which should
  be checked or cut.
* Loewi's dream (the hook for Part 6) is told as he told it; the date and the detail of the unreadable note
  should be checked against his own account before Part 6 is written.
