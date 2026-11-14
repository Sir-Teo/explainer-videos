# Psychology, Built: Part 6, Synapses and Circuits

Part 5 ended with a signal at the end of an axon, and a gap. For half a century physiologists argued over what
crosses it: a current (the "sparks") or a chemical (the "soups"). In 1921 Otto Loewi, in Graz, slowed one frog's
heart by stimulating its vagus nerve, moved the fluid that had bathed it to a second heart with no nerve at all,
and the second heart slowed too. The connection is chemical. A chemical step has quantities in it (how much is
released, how many receptors wait, how fast it is cleared), and a quantity can change. A synapse therefore has a
strength, and a strength that can change can store what happened.

This part asks how neurons talk, and how talking changes them. The route: the chemical synapse step by step, and
the packets Katz found; seven transmitters and the six places where a drug can act; how a membrane adds its
inputs in time, and how a shunt divides; Hebb's rule, why it runs away, and Oja's repair, which finds a principal
component; long-term potentiation, the NMDA receptor as the molecule that computes "both at once", spike timing,
and a sliding threshold; then three small circuits built on one motif, mutual inhibition, which sharpen edges
(Hartline's crab, Mach's bands), hold a choice (winner-take-all), and keep time (Graham Brown's half-centres);
populations of excitatory and inhibitory cells that rest, oscillate or saturate (Wilson and Cowan); and the
neuromodulators as two knobs, gain and learning rate. On the way the viewer looks at the Hermann grid, hears its
textbook explanation, computes it, and then watches it fail on a grid with curved streets.

## Where the numbers come from

| What | Source |
|---|---|
| Two frog hearts and a transferred fluid; *Vagusstoff*; the dream | Loewi (1921) and his own later account; registered in [`SOURCES.md`](../../../explainer/psychology/archive/SOURCES.md), with what was read and what was not |
| Transmitter released in packets of one size at the frog's nerve-muscle junction | del Castillo and Katz (1954), from the PubMed Central record and a 2006 retrospective; no figure is quoted |
| Hebb's postulate, quoted | Hebb (1949), p. 62, as quoted in textbooks |
| Long-lasting potentiation in the rabbit's dentate gyrus | Bliss and Lømo (1973), from later reviews; the plot in chapter 5 is a sketch of the design, not their data |
| The sign of a synaptic change depends on spike order, within about 20 ms | Bi and Poo (1998), from the abstract |
| Mutual inhibition of receptor units in *Limulus*, linear in the neighbour's activity | Hartline and Ratliff (1957), from the abstract |
| Curving the streets of the Hermann grid abolishes its spots | Geier, Bernáth, Hudák and Séra (2008), from the first author's pages and secondary summaries |
| Reactivating cells tagged during fear learning makes mice freeze | Liu, Ramirez et al. (2012), from the abstract; no percentages are quoted |
| 74 registered antidepressant trials: 51% positive as registered, 94% as published | Turner et al. (2008), from the abstract |
| Every curve, voltage, response, period and frequency "computed by Psyche" | `explainer.psychology.psyche.circuits` |

The numbers that depend on choices made for the film. The membrane is a passive patch with a time constant of
10 ms, an excitatory battery at 0 mV and an inhibitory one at −80 mV; one synaptic event is an alpha function of
1 ms, sized so that a single input gives 2.5 mV. The model synapse of chapter 1 has five release sites, each
releasing with probability 0.3, and a packet worth 0.4 mV; its histogram is 2,000 simulated impulses. The inputs
to the Hebbian cell are 4,000 draws from a correlated Gaussian whose first principal component carries 97% of the
variance. The spike-timing curve has the shape and the scale (tens of milliseconds) of Bi and Poo's window with
illustrative constants, and is tagged as Psyche's. The row of 80 units has inhibition of strength 0.25 that falls
by half every two units; the film shows units 8 to 72, leaving off the two ends, where a unit has neighbours on
one side only. The ramp of the Mach-band demonstration is ten units wide. The Hermann grid is five squares of 40
pixels with streets of 10, filtered with a difference of two Gaussians whose centre is a fifth of the street; the
curved grid bends each street by a sine of amplitude 4 pixels. The winner-take-all pair, the half-centre
oscillator (Matsuoka's equations) and the Wilson-Cowan populations use round parameters chosen so that each shows
its behaviour; the periods and frequencies they give (740 ms; 18 a second) are properties of those choices and
not measurements of any animal. The EEG trace in chapter 10 and the beating hearts of the hook are drawings.

## Built in this part

* `explainer/psychology/psyche/circuits.py`, Psyche's second piece of tissue: conductance synapses on a passive
  membrane (`Membrane.response`, `steady_voltage`), learning rules for a linear unit (`hebb` with Hebb's and
  Oja's rules, `bcm`, `stdp`), a row of units with lateral inhibition (`lateral`, `inhibition_kernel`), a
  centre-surround filter and the Hermann grid straight and curved (`dog`, `hermann_grid`, `hermann_response`), a
  winner-take-all pair (`WTA`), a half-centre oscillator (`HalfCentre`) and Wilson and Cowan's two populations
  (`WilsonCowan`). Tested in `tests/psychology/test_circuits.py` against closed forms and fixed points.
* The Ledger gains three rows and the Archive nine datasets.
* On the Homunculus map nothing lights yet: these circuits are parts of faculties, not faculties. The map's first
  rooms are opened by the act on perception.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| A brief burst of strong activity leaves a synapse stronger for a long time (long-term potentiation) | Bliss and Lømo 1973 | replicated |
| Neighbouring receptors in an eye inhibit one another in proportion to their activity (lateral inhibition) | Hartline and Ratliff 1957 | replicated |
| The grey spots of the Hermann grid are produced by centre-surround receptive fields | Baumgartner 1960 | story and record |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Loewi's experiment and Katz's
packets (settled physiology, told as history), Hebb's postulate (a hypothesis; the finding that bears on it is the
first row), the reactivated memory of Liu et al. (one laboratory's report at the frontier; whether strengthened
synapses are the memory is argued in Part 20), and Turner et al.'s comparison of registered and published trials
(entered with the evidence on treatments, Part 42). Bi and Poo's timing window rests under the first row.

## Build it

```bash
python -m videos.psychology.psych6.compute            # every number (a few seconds), into .cache/psych6/
python tools/qa_scene.py psych6 Grid                  # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych6 -q l   # the whole part, silent preview
python tools/build.py psych6                          # 1080p30 with narration
python tools/qa_scene.py psych6 Grid --lang zh        # the Chinese edition of one chapter
python tools/make.py psych6                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 6                    # the lab: a synapse, a learning rule and three circuits
python tools/check_ledger.py psych6                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                     # Psyche's circuits, the Pool, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Two hearts and a dream | The gap; sparks against soups; Loewi's experiment; why a chemical step can be adjusted; objectives |
| 1 | The chemical synapse | Six steps from spike to clearance; packets, failures and strength as n p q; two kinds of receptor and two directions |
| 2 | Transmitters, and where the drugs act | Seven transmitters in two groups; agonist and antagonist; six sites on one diagram |
| 3 | Adding up | One EPSP against the threshold; summation in time; many inputs add to less than the sum; a shunt that divides |
| 4 | Hebb's rule | The postulate and locality; the rule run until it diverges; Oja's rule derived; a cell that finds the first principal component |
| 5 | A synapse that remembers | Long-term potentiation; the NMDA receptor as an AND; spike timing; a sliding threshold and a cell that becomes selective |
| 6 | Lateral inhibition | The horseshoe crab's eye; a row of units shown an edge; Mach's bands on the viewer and in the model |
| 7 | On you: a grid of grey spots | The Hermann grid; the receptive-field account, computed; the curved grid, where the account predicts spots and none are seen |
| 8 | A circuit that decides | Two rivals; winner-take-all; a choice held after the evidence has gone; harder choices take longer |
| 9 | A circuit that keeps time | Graham Brown's cats; mutual inhibition with fatigue; what sets the tempo and what stops the rhythm; one motif, three behaviours |
| 10 | Populations | Berger's rhythm; Wilson and Cowan's two equations; rest, rhythm and saturation as the drive rises |
| 11 | Knobs: the neuromodulators | Broadcast systems; gain; the learning rate and a three-factor rule |
| 12 | The Ledger | Long-term potentiation, lateral inhibition, and the Hermann grid's explanation |
| 13 | In practice: drugs at the synapse | Receptor occupancy and the shift an antagonist makes; four families of drug and their catches; registered against published trials |
| 14 | Frontier: where is a memory? | A memory switched on with light; three open questions and a research problem |
| | Recap, problems, and the road ahead | Ten lines; what today adds to the reply to Kant; payoffs; problems; references; Part 7 |

## Sources

**Books.** E. R. Kandel, J. D. Koester, S. H. Mack and S. A. Siegelbaum (eds.), *Principles of Neural Science*
(6th ed., 2021), the chapters on synaptic transmission and plasticity. P. Dayan and L. F. Abbott, *Theoretical
Neuroscience* (2001), chapters 7 and 8. D. O. Hebb, *The Organization of Behavior* (1949). E. S. Valenstein, *The
War of the Soups and the Sparks* (2005). F. Ratliff, *Mach Bands: Quantitative Studies on Neural Networks in the
Retina* (1965).

**Papers.**
- O. Loewi, "Über humorale Übertragbarkeit der Herznervenwirkung", *Pflügers Archiv* 189 (1921) 239–242.
- P. Fatt and B. Katz, "Spontaneous subthreshold activity at motor nerve endings", *Journal of Physiology* 117
  (1952) 109–128. J. del Castillo and B. Katz, "Quantal components of the end-plate potential", *Journal of
  Physiology* 124 (1954) 560–573.
- E. Oja, "A simplified neuron model as a principal component analyzer", *Journal of Mathematical Biology* 15
  (1982) 267–273. E. L. Bienenstock, L. N. Cooper and P. W. Munro, "Theory for the development of neuron
  selectivity", *Journal of Neuroscience* 2 (1982) 32–48.
- T. V. P. Bliss and T. Lømo, "Long-lasting potentiation of synaptic transmission in the dentate area of the
  anaesthetized rabbit following stimulation of the perforant path", *Journal of Physiology* 232 (1973) 331–356.
- G.-Q. Bi and M.-M. Poo, "Synaptic modifications in cultured hippocampal neurons: dependence on spike timing,
  synaptic strength, and postsynaptic cell type", *Journal of Neuroscience* 18 (1998) 10464–10472.
- H. K. Hartline and F. Ratliff, "Inhibitory interaction of receptor units in the eye of *Limulus*", *Journal of
  General Physiology* 40 (1957) 357–376.
- G. Baumgartner, "Indirekte Größenbestimmung der rezeptiven Felder der Retina beim Menschen mittels der
  Hermannschen Gittertäuschung", *Pflügers Archiv* 272 (1960) 21–22. J. Geier, L. Bernáth, M. Hudák and L. Séra,
  "Straightness as the main factor of the Hermann grid illusion", *Perception* 37 (2008) 651–665.
- T. Graham Brown, "The intrinsic factors in the act of progression in the mammal", *Proceedings of the Royal
  Society B* 84 (1911) 308–319. K. Matsuoka, "Sustained oscillations generated by mutually inhibiting neurons with
  adaptation", *Biological Cybernetics* 52 (1985) 367–376.
- H. R. Wilson and J. D. Cowan, "Excitatory and inhibitory interactions in localized populations of model
  neurons", *Biophysical Journal* 12 (1972) 1–24.
- X. Liu, S. Ramirez et al., "Optogenetic stimulation of a hippocampal engram activates fear memory recall",
  *Nature* 484 (2012) 381–385.
- E. H. Turner et al., "Selective publication of antidepressant trials and its influence on apparent efficacy",
  *New England Journal of Medicine* 358 (2008) 252–260.

## Problems and solutions

**1. Packets.** *A synapse has n = 5 release sites, each releasing with probability p = 0.3, and one packet gives
q = 0.4 mV. Find the mean response, its variance, and the share of impulses that release nothing. If learning
doubled the mean and left the share of failures unchanged, which of n, p, q changed?*

The number of packets is binomial. Mean: n p q = 5 × 0.3 × 0.4 = 0.6 mV. Variance (ignoring the spread of single
packets): n p (1 − p) q² = 5 × 0.3 × 0.7 × 0.16 = 0.168 mV², a standard deviation of 0.41 mV. Failures:
(1 − p)ⁿ = 0.7⁵ = 16.8%. The share of failures depends on n and p only, so if it did not move, q doubled: the
change is on the receiving side (more receptors). Had p doubled to 0.6 the failures would have fallen to 1%; had n
doubled, to 2.8%. This is how recordings of failures are used to ask on which side of a synapse a change was made.

**2. Adding in time.** *Treat an EPSP as a jump of 2.5 mV that decays as e^(−t/τ) with τ = 10 ms. Two arrive a
time Δ apart. Find the peak of the sum, and how close they must be for it to reach 4 mV.*

The sum peaks when the second arrives, at 2.5 (1 + e^(−Δ/τ)) mV. Setting this to 4 gives e^(−Δ/10) = 0.6, so
Δ = 10 ln(1/0.6) = 5.1 ms. For Δ = 3 ms the formula gives 4.35 mV; Psyche's membrane gives 4.56, because its
EPSPs take a millisecond or two to rise and so overlap more. Thirty milliseconds apart the formula gives 2.62 mV
and the membrane 2.63.

**3. A shunt divides.** *For a passive membrane with g_L = 0.1 mS/cm² and E_E − E_L = 65 mV, find the steady
response to g_E = 0.05 with and without a shunt g_I = 0.15 whose battery is at rest. Show that for small g_E the
shunt divides the response by (g_L + g_I)/g_L.*

At a steady state the currents balance: g_L (V − E_L) + g_E (V − E_E) + g_I (V − E_L) = 0, so
V − E_L = g_E (E_E − E_L) / (g_L + g_E + g_I). Without the shunt: 0.05 × 65 / 0.15 = 21.7 mV. With it:
0.05 × 65 / 0.30 = 10.8 mV, half as much. When g_E is small beside the other two conductances it can be dropped
from the denominator, and the response is g_E (E_E − E_L)/(g_L + g_I): the unshunted response divided by
(g_L + g_I)/g_L = 2.5. With g_E = 0 the shunt changes nothing, which is why it cannot be seen by itself.

**4. Hebb and Oja.** *Average Hebb's rule over the inputs to get dw/dt = η C w, and show that w grows fastest
along the first eigenvector. Then show that a fixed point of Oja's rule satisfies C w = (wᵀ C w) w, so that w is an
eigenvector of length 1.*

With y = wᵀx, the average of η x y is η ⟨x xᵀ⟩ w = η C w. Write w in the eigenvectors of C, w = Σ aₖ eₖ. Then
daₖ/dt = η λₖ aₖ and aₖ(t) = aₖ(0) e^(η λₖ t): every component with a positive eigenvalue grows without bound,
and the one with the largest eigenvalue outgrows the rest, so the direction of w tends to e₁ while its length
diverges. For Oja's rule the average of η y (x − y w) is η (C w − (wᵀ C w) w), since ⟨y²⟩ = wᵀ C w. At a fixed
point C w = (wᵀ C w) w, so w is an eigenvector, with eigenvalue λ = wᵀ C w = λ ‖w‖²; hence ‖w‖ = 1. Perturbing a
fixed point eₖ along another eigenvector eⱼ gives a component that changes at the rate η (λⱼ − λₖ), which is
negative for every j only when k is the first: the first principal component is the one stable fixed point.

**5. Where a BCM cell settles.** *A BCM cell sees two patterns equally often and responds y₁ and y₂; its threshold
is θ = ⟨y²⟩. Show that in the selective state (y₂ = 0) the response settles at y₁ = 2. Where does it settle if
pattern 1 is shown only a quarter of the time?*

A synapse active in pattern k changes in proportion to yₖ (yₖ − θ), so at a fixed point each pattern has either
yₖ = 0 or yₖ = θ. In the selective state θ = ½ y₁² + ½ × 0 = y₁, so y₁ = 2 (and θ = 2). Psyche's cell ends at
2.03, with the other pattern at 0.00. If pattern 1 has probability p, θ = p y₁² = y₁ gives y₁ = 1/p: 4 for a
quarter. A cell that settles on a rare pattern responds to it more strongly, since the threshold is an average
over time.

**6. What sets the bands.** *With `explainer.psychology.psyche.circuits`: apply `lateral` to a step of light with
the strength of inhibition at 0.1, 0.25 and 0.4. How does the ratio across the edge change? What does a wider
reach (`space=4`) do to the bands?*

```python
import numpy as np
from explainer.psychology.psyche import circuits as C
step = np.r_[np.full(40, 1.0), np.full(40, 2.0)]
for strength in (0.1, 0.25, 0.4):
    r = C.lateral(step, strength=strength)
    print(strength, r[40:46].max() / r[34:40].min())
```

The plateaus keep the light's ratio of 2 at every strength (0.76 and 1.53; 0.56 and 1.13; 0.45 and 0.90), while
the ratio across the edge grows from 2.6 to 4.3 to 11.7: stronger inhibition lowers the response everywhere and
exaggerates the edge more. With `space=4` the inhibition reaches twice as far, the bright band is about seven
units wide where it was four, and the dark band is driven to zero, where the response is clipped. The width of a
Mach band measures the reach of the inhibition, which is how Ratliff and Hartline used it.

**7. ★ Synapses or cells.** *Design the experiment that would tell "the memory is the pattern of strengthened
synapses" from "the memory is which cells were chosen", and say what each outcome would look like.*

One design: tag the cells active during learning with a light-sensitive channel, as Liu et al. did, and straight
after the learning give a treatment that prevents synapses from being strengthened (blocking the synthesis of new
protein does this). Then test recall twice, once with the natural cue (the box) and once by lighting the tagged
cells. If the memory is the strengthened synapses, both tests fail: the cells are there, and nothing useful is
stored in them. If the memory is in which cells were chosen and how they are wired to the rest of the brain, the
natural cue fails (it reaches the cells through synapses that were never strengthened) and the light succeeds.
Controls: light on cells tagged in another box, and animals given the treatment after the memory has had time to
settle. What the design cannot show is that what the light brings back is the memory as the animal would recall
it; freezing is one behaviour. Experiments of this kind have been reported and their reading is disputed, which
is why this is on the frontier.

## Where it comes back

What damage and a scanner can say about circuits: Parts 7 and 8. Transmitters, hormones and the body's clock:
Part 10. Lateral inhibition in the viewer's own retina, and receptive fields: Part 13. Dopamine as the third
factor of a learning rule: Part 17. A choice held in activity, as working memory: Part 19. Whether long-term
potentiation is how memories are stored: Part 20. The circuit that decides, against people's reaction times:
Part 25. What the four families of drug do for a disorder: Parts 40 to 42. Learning without a local rule: Part 58.
Psyche's circuits (`psyche/circuits.py`) are the motifs every later model is assembled from.

## Open checks

Before the narrated master:

* Loewi (1921) was not read. The design and result are from standard accounts; the dream is his own later telling
  (the night before Easter Sunday, a note he could not read, three o'clock the next night), and the film says so.
  The Nobel Prize of 1936 shared with Dale is from memory.
* Eccles's change of mind is given as 1951, "on his own experiment", from an institutional history and an
  encyclopedia entry; check his own account. That a minority of synapses are electrical is from textbooks.
* del Castillo and Katz (1954) and Fatt and Katz (1952) were not read; the narration's description (spontaneous
  blips of one size; responses in steps when calcium is lowered) follows the retrospective, and "the early
  1950s, in London" should be checked. The cleft of about 20 nm, "thousands of molecules" in a vesicle, and a
  delay of about half a millisecond are textbook figures.
* The lines on the seven transmitters, on curare, naloxone, botulinum toxin, L-DOPA, caffeine, the
  benzodiazepines, the SSRIs, cocaine and the nerve agents are general pharmacology and carry no figures; "more
  than a hundred transmitters" should be checked or cut.
* Hebb's postulate is quoted from memory of the usual textbook quotation; check the wording and the page.
* Bliss and Lømo (1973) was not read. "For hours" is the film's only statement of duration; check it against the
  abstract. "In Oslo" and the order of the two names in the narration follow the history as usually told.
* The NMDA receptor's magnesium block and the insertion of AMPA receptors are stated from textbooks.
* Bi and Poo (1998): "about 20 ms either side" is from the abstract as summarized; the curve is Psyche's.
* Bienenstock, Cooper and Munro (1982) and Oja (1982) are cited from memory; the derivations are in the README.
* Hartline and Ratliff (1957) was read only as an abstract. "About a thousand receptor units", "hundreds of
  millions of years", and the statement that they recorded the overshoot at an edge in the crab's own eye
  (Ratliff and Hartline 1959) are from memory and should be checked or softened.
* That Mach bands are seen at the ends of a ramp and mostly not at a sharp step is from a secondary source
  (Kingdom 2014, on Ratliff 1984); check before the master.
* Baumgartner (1960) was not read; Geier et al. (2008) was not read. Whether a wave of 4 pixels on a 10-pixel
  street abolishes the spots for most viewers of this film should be tried on people before the master; the
  narration says "what you've probably just found".
* Graham Brown (1911), Sherrington's reflex-chain view, and "ignored for half a century" are from standard
  accounts. Matsuoka's condition for oscillation is tested in `test_circuits.py`.
* Berger's recordings (Jena, published 1929; a rhythm near ten a second with the eyes closed) are from memory.
* The statement that a dopamine receptor blocked by antipsychotics also serves movement, that the stimulants act
  on the transporter cocaine blocks, and that the benefit of an SSRI takes weeks, are textbook pharmacology;
  check each against a current text.
* Turner et al. (2008): 74 trials, 12 drugs, 51% and 94% are from the abstract. "Nearly every positive trial had
  been published; most of the others had not, or had been written up as successes" is from memory of the paper
  (37 of 38; 22 unpublished and 11 published as positive, of 36) and should be checked there.
* Liu et al. (2012) was read only as an abstract; the false-memory experiment of 2013 is cited from memory.
* Phineas Gage (the hook for Part 7): September 1848, Vermont, a rod "more than a metre long", conscious
  afterwards. Check against Harlow's reports before Part 7 is written.
