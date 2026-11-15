# Music, Built: Part 55, Rooms and Space

Part 55 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act X, *The Studio and the Stage*. In 1895 Harvard opened a lecture
room in which nobody could understand a word. A young physicist, Wallace Sabine, spent his nights there with a stopwatch,
an organ pipe and the seat cushions of a nearby theatre, found the law of reverberation, and used it to design Boston's
Symphony Hall. Sixty years later a hall designed with far more science had to be gutted. This part explains both, then
turns from the room to the listener: how two ears hear direction, and how stereo, Ambisonics, binaural rendering and object
audio build space back. The tools are Monochord's (`explainer/music/monochord/space.py`); every room, wall and head is
simulated. Several sounds are rendered for headphones.

* **A room nobody could understand.** An ear question (a voice in a lecture room as built and after its cure: which was
  as built? the first, 5.6 s against 1.1 s); Sabine's nights, the cushions and Symphony Hall; Philharmonic Hall (1962);
  the plan.
* **1. Sabine's law.** A sound that dies away; the law derived from a diffuse field (T60 = 0.161 V/A); Sabine's cushions,
  simulated and heard (5.6, 3.1 and 1.1 s); Eyring's correction; absorption by frequency; how long a room should ring.
* **2. Modes.** A room is a pipe in three directions; the modes of a 5 by 4 by 2.7 m room (18 below 120 Hz); counting
  them against Weyl's formula (20.2); the Schroeder frequency (305 Hz in the room, 20 Hz in a hall); a bass line in a
  corner and in the middle, heard; taming the modes.
* **3. Absorption and diffusion.** Three ways to absorb; a flutter echo (every 35 ms) bare and scattered, heard;
  scattering without absorbing; a quadratic-residue diffuser (n² mod 7); why it works, by Gauss's sum; scattering computed
  (diffusion coefficient 0.39 against a flat panel's 0.07 at 1 kHz); diffusers at work.
* **4. Early reflections and hall shapes.** The first 80 milliseconds; what arrives at one seat, and from where; the
  lateral fraction; narrow halls surround you (0.20 at 14 m wide, 0.11 at 40 m); an ear question (two halls ringing for
  the same 1.9 s: which was the narrow one? the first); shoebox, fan, vineyard and surround halls.
* **5. Simulating a room.** The image method; how many reflections (833 images to the eighth order; 169,000 a second
  after one second in a 3,000 m³ hall); the simulator checked (a smooth box rings longer than Sabine and Eyring predict,
  because it is not diffuse; its bass peaks sit within 0.4 Hz of the exact modes); rays; waves; auralization.
* **6. How we hear direction.** The duplex theory; the time difference (Woodworth: up to 656 µs); the level difference
  (Brown and Duda: up to 15 dB at 4 kHz); the cues apart and together, heard; the cone of confusion; an ear question (a
  voice 30° in front and 150° behind a spherical head: which was in front? neither can be told: the renderings are
  identical); breaking the cone.
* **7. Stereo and panning.** Two channels from Ader to the stereo LP; the stereo triangle and the tangent law (a half pan
  sits at 13.4°); pan laws (linear: −3.01 dB in the middle); a pan heard both ways; the sweet spot; microphones for stereo.
* **8. Ambisonics and wave-field synthesis.** After quadraphony; encoding a direction (W, X, Y); decoding to a ring of
  eight; Gerzon's vectors (rE 0.667 basic, 0.707 max-rE); higher orders (spread 45° at first order, 11° at seventh);
  wave-field synthesis.
* **9. Binaural rendering.** Two signals; the filters of a head; a binaural renderer; round the head twice, heard; inside
  the head; head tracking; binaural on loudspeakers.
* **10. Object audio.** Channels, scenes and objects; objects in the cinema and at home; placing an object (VBAP); one mix,
  every playback; space as part of the music.
* **11. Frontier: personal ears and real-time waves.** Personal HRTFs; why waves are expensive (cost as f⁴); real-time
  waves; rooms you can program; ★ research problem: what is the least a renderer must know about a listener's ears?
* **Variation 55, recap and problems.** The Tune with no room, in a small room, a shoebox hall and a cathedral, then
  circling the listener; the ledger (reverberation 0, 0.45, 1.9 and 5.0 s; one circle of the head in 7.6 s); what we
  found; five problems; where it comes back; in practice; references; Part 56.

## What is computed, and what is heard

`python -m videos.music.music55.compute` (about two minutes; the image-source checks take the longest) fills
`.cache/music55/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `cushions` | a lecture room of the Fogg's size with and without cushions | Sabine's law (tests) |
| `modes`, `check` | a room's exact modes; an image-source room's response and decay | Weyl's count; Sabine, Eyring and the modes (tests) |
| `flutter`, `diffuser` | an echo between parallel walls; a residue diffuser's scattering | Gauss's sum; the flat panel (tests) |
| `halls`, `images` | early reflections and lateral fractions; image counts | the closed-form count (tests) |
| `cues`, `cone` | ITD and ILD round a sphere; front against back | Woodworth's formula; identical signals (tests) |
| `pan`, `ambi` | pan laws and the tangent law; Ambisonic decoders | −3.01 dB; Gerzon's 2/3 and cos 45° (tests) |
| `circle` | a shaker circling a spherical head | — |
| `tune55` | Variation 55 | — |

Monochord's tools are held in `tests/music/test_space.py`; this part's claims and clips in `tests/music/test_music55.py`.

**Sounds.** Part 8's voice, Part 38's plucked bass, claps, noise bursts and a shaker, placed in simulated rooms and
rendered round a simulated head.

**What the models are, and are not.** *The rooms* are rectangular, with one absorption for every wall and every
frequency in the image method, and a statistical tail with darker highs for the halls and the cathedral. *The diffuser*
is computed in the Fraunhofer approximation at normal incidence. *The head* is a rigid sphere (Woodworth's delay and Brown
and Duda's one-pole shadow), with no pinnae and no torso, which is why it cannot tell front from back and why many
listeners hear its sounds inside the head. *The loudspeakers* of the panning demonstration are ideal sources at ±30°.

## Build

```bash
python -m videos.music.music55.compute                          # numbers and sounds (about two minutes)
EXPLAINER_TTS=silent python tools/build.py music55 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music55 --sync                         # the sound gates
python tools/dead_air.py renders/music55_480p.mp4 --sound music55  # no empty screen; no sound over a still one
python tools/lecture_length.py music55                          # 30 to 60 minutes, listening included
python tools/build.py music55                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 55                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A room 10 by 8 by 4 m has an average absorption coefficient of 0.2 on every surface. Find T60 by Sabine
   and by Eyring.

   *Solution.* V = 320 m³ and S = 2(80 + 32 + 40) = 304 m². Sabine: A = 0.2 × 304 = 60.8 m², T = 0.161 × 320 / 60.8 =
   0.85 s. Eyring: −S ln(0.8) = 67.8 m², T = 0.161 × 320 / 67.8 = 0.76 s.

2. **Prove.** Prove that |Σ_{n=0}^{N−1} e^{2πi(n² + kn)/N}| = √N for an odd prime N and every k.

   *Solution.* Call the sum G. Then |G|² = Σ_{m,n} e^{2πi(m² − n² + k(m − n))/N}. Put m = n + h: m² − n² + k(m − n) =
   h(2n + h + k), so |G|² = Σ_h e^{2πi h(h + k)/N} Σ_n e^{2πi·2hn/N}. Since N is odd and prime, 2h is a unit mod N for
   h ≠ 0, so the inner sum over n vanishes unless h = 0, where it is N. Hence |G|² = N.

3. **Ear.** The lab plays noise bursts from random directions round a spherical head; name each angle.

   *Solution.* The lab prints them. Left and right are easy and the angle to the side is close; a burst straight ahead
   and one straight behind would be identical, which is why the lab never plays one from behind.

4. **Build.** Add scattering to the image-source room and see its T60 approach Eyring's.

   *Where to look.* Keep the image method for the first two orders, then let each later reflection lose a fraction s of
   its energy into a diffuse tail (a noise tail decaying at the rate set by the average absorption), or randomize the
   image positions by a few centimetres per bounce. As s grows, the long-lived grazing paths lose their advantage and the
   decay moves from the specular box's (longer than Sabine's) towards Eyring's.

5. ★ **What is the least you need to know about a listener's ears to render space for them as well as their own HRTF
   would?**

   *Where the frontier is.* Take databases of measured HRTFs with head and ear scans; predict each listener's set from a
   photograph, a depth scan or a few chosen test sounds; and test by listening, counting front-back reversals, elevation
   errors and externalization against the listener's own measured set.

## Sources

* H. Kuttruff, *Room Acoustics* (6th ed., 2016); L. Beranek, *Concert Halls and Opera Houses* (2nd ed., 2004);
  J. Blauert, *Spatial Hearing* (rev. ed., 1997); F. Zotter and M. Frank, *Ambisonics* (2019).
* W. C. Sabine, "Reverberation", *The American Architect* (1900), in *Collected Papers on Acoustics* (1922); C. F. Eyring,
  "Reverberation time in 'dead' rooms", *JASA* (1930); M. R. Schroeder, "Die statistischen Parameter der Frequenzkurven von
  grossen Räumen", *Acustica* (1954).
* M. R. Schroeder, "Diffuse sound reflection by maximum-length sequences", *JASA* (1975), and "Binaural dissimilarity and
  optimum ceilings for concert halls: more lateral sound diffusion", *JASA* (1979); T. J. Cox and P. D'Antonio, *Acoustic
  Absorbers and Diffusers* (3rd ed., 2016).
* A. H. Marshall, "A note on the importance of room cross-section in concert halls", *JSV* (1967); M. Barron and
  A. H. Marshall, "Spatial impression due to early lateral reflections in concert halls", *JSV* (1981).
* J. B. Allen and D. A. Berkley, "Image method for efficiently simulating small-room acoustics", *JASA* (1979);
  A. Krokstad, S. Strøm and S. Sørsdal, "Calculating the acoustical room response by the use of a ray tracing technique",
  *JSV* (1968); M. Kleiner, B.-I. Dalenbäck and P. Svensson, "Auralization: an overview", *JAES* (1993).
* Lord Rayleigh, "On our perception of sound direction", *Phil. Mag.* (1907); R. S. Woodworth, *Experimental Psychology*
  (1938); C. P. Brown and R. O. Duda, "A structural model for binaural sound synthesis", *IEEE Trans. Speech Audio Proc.*
  (1998); H. Wallach, "The role of head movements and vestibular and visual cues in sound localization", *J. Exp. Psych.*
  (1940); E. M. Wenzel et al., "Localization using nonindividualized head-related transfer functions", *JASA* (1993).
* A. D. Blumlein, British patent 394,325 (1931); J. C. Bennett, K. Barker and F. O. Edeko, "A new approach to the
  assessment of stereophonic sound system performance", *JAES* (1985); M. A. Gerzon, "Periphony: with-height sound
  reproduction", *JAES* (1973), and "General metatheory of auditory localisation" (AES, 1992); A. J. Berkhout,
  "A holographic approach to acoustic control", *JAES* (1988); V. Pulkki, "Virtual sound source positioning using vector
  base amplitude panning", *JAES* (1997).
* B. S. Atal and M. R. Schroeder, US patent 3,236,949 (1966; filed 1962); W. G. Gardner and K. D. Martin, "HRTF
  measurements of a KEMAR", *JASA* (1995); V. R. Algazi et al., "The CIPIC HRTF database" (2001); N. Raghuvanshi and
  J. Snyder, "Parametric wave field coding for precomputed sound propagation", *ACM Trans. Graph.* (2014).
