# AI, Built — Part 18: Agents and Worlds

Part 18 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). What it
takes to act over many steps in a partly seen world. A hook and four chapters:

* **Many steps in a row.** Thirty steps at 97% each: 0.97³⁰ = 0.40.
* **Acting without seeing everything.** A robot localizing itself in a corridor of 40 cells and 4 doors: its belief,
  predicted and updated by Bayes' rule step by step (a POMDP's belief state; Part 6's forward algorithm); the
  uncertainty falling from 5.3 bits.
* **Long horizons.** pⁿ; the task length finished half the time, ln 2 / (−ln p) ≈ 0.69 / (1 − p); METR's measured
  doubling of AI agents' task length about every seven months.
* **World models.** A small world model trained here on a bouncing ball (an encoder to 8 numbers, learned dynamics, a
  decoder); its imagined future against the real one, the error growing with the horizon; Dreamer and Genie.
* **Acting in the physical world.** Vision-language-action models: RT-2's action tokens, π0's flow-matching action
  expert, action chunks.
* **Recap**, where it comes back, Part 19's teaser, references.

Run from the repo root:

```
python -m videos.ai.ai18.compute
python tools/build.py ai18                # English
python tools/build.py ai18 --lang zh      # Chinese
```

References: Thrun, Burgard & Fox (2005); Sutton & Barto (2018); Kwa et al. (METR, 2025); Ha & Schmidhuber (2018);
Hafner et al., Dreamer (2020–2025); Bruce et al., Genie (2024); Brohan et al., RT-2 (2023); Black et al., π0 (2024).
