# October 10, 2026 YouTube rebuild

Published: [General Relativity, Derived: From a Falling Elevator to Einstein's Field Equations](https://youtu.be/HqpjxO4fQmA), grouped in the channel's **Mathematics & Physics** playlist. Public playback was verified at 1080p with English captions; YouTube's copyright checks found no issues.

All 19 chapters were rendered from source at 1920×1080, 30 fps, H.264 CRF 18. The build uses the original PCM narration, lossless ALAC intermediates, and a final 48 kHz stereo AAC soundtrack with a 384 kb/s encoding target. The finished master measures -16.01 LUFS integrated and -1.39 dBTP. Its duration is 1:09:24.001, with 1276 English caption cues and 19 chapters.

The numerical fixtures were recomputed and their mathematical assertions passed before rendering. The complete master passed decoding, audio synchronization, caption timing, and chapter checks. Source-render contact sheets and native frames were visually reviewed before upload.

The equivalence-principle chapter was rendered again after fitting the Pound–Rebka result labels inside the right-hand panel. All other chapters use the completed base source renders. No narration or scientific content was changed by this layout repair.

Source revision: `02ca91aa32b160f7f2ae967d651fce0b27912e8f`.

Base source build: [GitHub Actions run 38052032314](https://github.com/Sir-Teo/explainer-videos/actions/runs/38052032314). Final master validation: [GitHub Actions run 38053349393](https://github.com/Sir-Teo/explainer-videos/actions/runs/38053349393).

```sh
python -m videos.relativity.compute
python tools/build.py relativity --crf 18 -j 2
python tools/youtube_qa.py relativity
```

## YouTube chapter timestamps

```text
0:00 Gravity is not a force
2:07 Newton's gravity, and what's wrong with it
5:47 Part 1: Spacetime and proper time
9:19 The equivalence principle: light falls, clocks slow
13:37 Falling is maximal aging
18:19 Part 2: Curvature, measured from the inside
22:36 Tensors: equations every observer agrees on
26:16 Geodesics and the Christoffel symbols
30:14 The covariant derivative and parallel transport
34:23 The Riemann tensor: curvature is tides
38:45 Part 3: Matter: the stress-energy tensor
41:48 Deriving Einstein's field equations
46:40 What the equation says: a ball of falling particles
49:41 The same equation from an action
52:53 Part 4: The Schwarzschild solution
57:14 Orbits: Mercury's 43 arcseconds
1:01:07 Light: bending, eclipses and black holes
1:04:32 Gravitational waves
1:08:00 Recap
```
