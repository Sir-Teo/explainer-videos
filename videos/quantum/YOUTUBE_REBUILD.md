# October 10, 2026 YouTube rebuild

Published: [Quantum Mechanics, Visualized: The Wavefunction, the Schrödinger Equation, and Why [x, p] = iħ](https://youtu.be/aaPbLBw0ZYc), grouped in the channel's **Mathematics & Physics** playlist. Public playback was verified at 1080p with English captions; YouTube's copyright checks found no issues.

All 18 chapters were rendered from source at 1920×1080, 30 fps, H.264 CRF 18. The build uses the original PCM narration, lossless ALAC intermediates, and a final 48 kHz stereo AAC soundtrack with a 384 kb/s encoding target. The finished master measures -16.01 LUFS integrated and -1.40 dBTP. Its duration is 1:03:48.702, with 1148 English caption cues and 18 chapters.

The numerical fixtures were recomputed and their mathematical assertions passed before rendering. The complete master passed decoding, audio synchronization, caption timing, and chapter checks. Source-render contact sheets and native frames were visually reviewed before upload.

Source revision: `0be2d034db841d9fe23adb4acd2d69fcf6da2ba3`.

Base source build: [GitHub Actions run 38052032314](https://github.com/Sir-Teo/explainer-videos/actions/runs/38052032314). Final master validation: [GitHub Actions run 38052032314](https://github.com/Sir-Teo/explainer-videos/actions/runs/38052032314).

```sh
python -m videos.quantum.compute
python tools/build.py quantum --crf 18 -j 2
python tools/youtube_qa.py quantum
```

## YouTube chapter timestamps

```text
0:00 One electron at a time
2:34 Part 1: Arrows that add
6:14 A complex number at every point
10:27 Part 2: Building the Schrödinger equation
15:39 Wave packets: why a free particle spreads
18:44 A particle in a box: where quantization comes from
22:24 Quantum carpets: the wave that reassembles itself
24:58 Tunneling through a wall
28:40 Part 3: Wavefunctions are vectors
32:35 Observables, eigenvalues and the Born rule
35:48 Momentum, Fourier, and [x, p] = iħ
38:46 The uncertainty principle, derived
42:35 Part 4: The harmonic oscillator, by ladder operators
46:16 Coherent states, phase space and the classical limit
49:19 The hydrogen atom
54:04 Part 5: Spin, the simplest quantum system
57:56 Entanglement and Bell's theorem
1:02:19 Recap
```
