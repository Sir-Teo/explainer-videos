# Music, Built: Part 59, Live Sound

Part 59 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth part of Act X, *The Studio and the Stage*. In August 1965 fifty-five thousand
people filled a baseball stadium in New York, and the band struggled to be heard over the crowd with the available sound reinforcement. The event exposed limits that later concert systems addressed through developments across many decades. This part works out
why a microphone howls and how to predict the note, why loudspeakers are hung in curved lines, how bass is aimed, why a
festival's back field hears the stage twice, how a system is measured while the band plays, how forty radio microphones
share a stage, why the station announcement is unintelligible, and how loud is too loud. The tools are Monochord's
(`explainer/music/monochord/live.py`, with Part 49's image-source room); every stadium, loudspeaker, crowd and car park
is simulated.

* **Fifty-five thousand people and no sound.** An ear question (the band from the stands over a crowd through a 1965-style
  horn system, 6 dB under the crowd, and a modern one, 8 dB over: which was 1965? the first); Shea Stadium; what came
  after; the plan.
* **1. Why a microphone howls.** The loop; when a loop runs away (candidate instability requires G H = 1: zero imaginary part and positive real part, with open-loop stability assumptions); the loop's response in a simulated 20 × 14 × 8 m hall (the gain before feedback −17.5 dB, the howl
  at 358 Hz; the magnitude alone says −18.4 dB); an ear question (a clap at 6, 0.5 and 2 dB below the edge: which was
  closest? the second); over the edge (the howl builds at 358 Hz, as predicted).
* **2. Ringing out, and monitors.** Six narrow notches at the frequencies that would howl (+3.1 dB); heard; the cheaper
  decibels (distance, nulls, fewer open microphones); potential and needed acoustic gain (24.5 against 26.0 dB); monitors
  and in-ears.
* **3. Point and line sources.** Spheres and cylinders; level against distance (6 dB per doubling from a point, 2.7 near
  a 24-box line at 1 kHz); the transition distance (26, 103 and 411 m at 250 Hz, 1 kHz and 4 kHz for an 8.4 m line); a
  line, or a row of points.
* **4. Arrays and curvature.** Three fields of an arena at 1 kHz (a point, a straight line, a J); the J (splays from 0.3° to
  4.2°); three seats heard (10, 40 and 80 m: 6.4 and 7.3 dB down); steering.
* **5. Subwoofer arrays.** Bass goes everywhere; a cardioid pair (0.9 m, 2.6 ms, inverted: it cancels behind at every
  frequency); heard from behind the stage; end-fire, arc delays and flown subwoofers.
* **6. Delay towers, air and weather.** A delay tower (90 and 30 m: 184.7 ms); an ear question (which was aligned? the
  first); weather (3 ms of drift over 10 °C; refraction; wind); what the air takes (ISO 9613-1: 0.5, 3, 11 and 36 dB over
  100 m at 1, 4, 8 and 16 kHz); heard.
* **7. Measuring a system.** Dual-channel measurement; measured with the Tune (transfer function, coherence, the delay found
  to the sample, 37.8 ms); what can go wrong; tuning a system.
* **8. Wireless and networks.** Intermodulation; a frequency plan (24 evenly spaced carriers, every one hit by a third-order
  product, against Monochord's planner's 20 clean carriers around three TV channels); in-ear monitors; networks and clocks.
* **9. Speech in big rooms.** The speech transmission index; STI over reverberation and noise (0.74 dry and clean, 0.23 at
  6 s); an ear question (one announcement in a studio, a hall and a station: STI 0.64, 0.37 and 0.15); what helps.
* **10. Hearing health.** What loud sound does; the equal-energy rule; one night's doses (2016 % at the barrier, 504 %
  mid-arena, 16 % with earplugs, 794 % for the engineer, 50 % for a drummer in in-ears); rules and remedies.
* **11. Frontier: immersive stages and quiet neighbours.** Immersive live sound; quiet neighbours (sound zones, active
  control); ★ research problem: what settings hold a festival's off-site limit with 95 % confidence over the weather, and
  what do they cost the audience?
* **Variation 59, recap and problems.** The Tune by our session at the mixing desk, the back row (7 dB down) and the car
  park (29 dB down, and mostly bass); the ledger; what we found; five problems; where it comes back; in practice;
  references; Part 60.

## What is computed, and what is heard

`python -m videos.music.music59.compute` (a few minutes; the closed loops and the array fields take the longest) fills
`.cache/music59/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook` | the band over a crowd through two systems | the levels set (tests) |
| `feedback` | Nyquist's gain before feedback, the howl note, ringing out, PAG/NAG, the loop run in time | a pure delay's edge (+6 dB at gain ½); the howl found in the closed loop (tests) |
| `arrays` | fields of a point, a straight and a curved line; levels with distance | 6.02 dB per doubling from a point (tests) |
| `subs` | a cardioid pair, in front and behind | exact cancellation; \|sin(2πfd/c)\| in front (tests) |
| `delay`, `air` | delay-tower times by temperature; ISO 9613-1 absorption | the standard's tabulated values (tests) |
| `measure` | a transfer function, coherence and delay measured with music | the true response and delay (tests) |
| `wireless` | third-order products; an even grid; a greedy plan | no product within 100 kHz of any carrier (tests) |
| `sti`, `dose` | the STI over reverberation and noise; doses | ordering; 85 dBA for 8 h = 100 % (tests) |
| `tune59` | Variation 59 | the levels ordered (tests) |

Monochord's tools are held in `tests/music/test_live.py`; this part's claims and clips in `tests/music/test_music59.py`.

**Sounds.** Part 8's voice and Part 56's session, through simulated halls, loops, arrays, air and walls.

**What the models are, and are not.** *The hall* is Part 49's image-source room (shoebox, one absorption coefficient),
with loudspeaker and microphone taken as omnidirectional; a real system's gain before feedback also depends on their
patterns. *The arrays* are rows of omnidirectional point sources in a free field (no floor reflection), averaged over a
third of an octave; real boxes are directional and the waveguides of real line arrays couple them more tightly. *The air*
is ISO 9613-1's formula for pure-tone absorption. *The wireless planner* checks only third-order products, without
receiver selectivity, transmitter power or fifth-order products. *The STI* uses Houtgast and Steeneken's formula for an
exponential decay and steady noise, the same in every octave, without the masking and threshold corrections of
IEC 60268-16. *The doses* follow NIOSH's recommendation (85 dBA, a 3 dB exchange rate); laws differ by country and
these numbers are not health advice.

## Build

```bash
python -m videos.music.music59.compute                          # numbers and sounds (a few minutes)
EXPLAINER_TTS=silent python tools/build.py music59 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music59 --sync                         # the sound gates
python tools/dead_air.py renders/music59_480p.mp4 --sound music59  # no empty screen; no sound over a still one
python tools/lecture_length.py music59                          # 30 to 60 minutes, listening included
python tools/build.py music59                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 59                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A tower stands 40 m from you; the stage is 120 m away. At 20 °C, what delay should the tower have? And at
   5 °C?

   *Solution.* c = 331.3 + 0.606 T: 343.4 m/s at 20 °C, 334.3 at 5 °C. The path difference is 80 m: 233.0 ms + 10 ms =
   243 ms at 20 °C; 239.3 ms + 10 = 249 ms at 5 °C. A tower aligned in the warm afternoon is 6 ms early on a cold night.

2. **Prove.** Show that a cardioid pair, the rear box d behind the front, delayed by d/c and inverted, cancels exactly
   behind at every frequency, and find where it is strongest in front.

   *Solution.* Behind, the front box's sound reaches the rear box's position d/c after leaving, exactly when the rear box,
   delayed by d/c, emits its inverted copy; from there on the two travel together and sum to zero, for every frequency.
   In front, the rear box's sound travels d further and is delayed by d/c, so it arrives 2d/c late and inverted: the sum is
   1 − e^(−iω2d/c), of magnitude 2|sin(ωd/c)|, largest where ωd/c = π/2, that is where d is a quarter wavelength
   (f = c/4d: 95 Hz for d = 0.9 m), and falling towards the deepest bass.

3. **Ear.** The lab plays a clap into a loop at two margins below the edge; which was nearer the edge?

   *Solution.* The lab prints the order. Listen for a tone that rings on after the clap: half a decibel from the edge it
   lasts for a second or more, at the frequency the lab's plot marks; six decibels down it stops with the room.

4. **Build.** Extend the frequency planner to fifth-order products, and count how many carriers still fit.

   *Where to look.* Add 3f₁ − 2f₂, 2f₁ + f₂ − 2f₃ and the like to `imd3` (as `imd5`), weight them less (they are about 20 dB
   weaker), keep the 100 kHz guard for third order and a smaller one for fifth, and compare the count with the third-order plan.

5. ★ **What settings hold a festival's off-site limit with 95 % confidence over the weather, and at what cost to the
   audience?**

   *Where the frontier is.* Model arrays, subwoofers, the field and houses a kilometre away with a propagation model that
   includes wind and temperature profiles (parabolic-equation or ray methods); draw profiles from a year of measurements;
   optimize delays and filters for a chance constraint at the houses and an evenness objective in the field.

## Sources

* B. McCarthy, *Sound Systems: Design and Optimization* (3rd ed., 2016); D. Davis, E. Patronis and P. Brown, *Sound System
  Engineering* (4th ed., 2013); G. Ballou (ed.), *Handbook for Sound Engineers* (5th ed., 2015).
* H. Nyquist, "Regeneration theory", *Bell System Technical Journal* (1932); C. P. Boner and C. R. Boner, "Minimizing
  feedback in sound systems and room-ring modes with passive networks", *JASA* (1965).
* M. Urban, C. Heil and P. Bauman, "Wavefront sculpture technology", *JAES* (2003); D. G. Meyer, "Digital control of
  loudspeaker array directivity", *JAES* (1984).
* ISO 9613-1, *Acoustics: attenuation of sound during propagation outdoors, part 1: calculation of the absorption of sound
  by the atmosphere* (1993).
* T. Houtgast and H. J. M. Steeneken, "The modulation transfer function in room acoustics as a predictor of speech
  intelligibility", *Acustica* (1973), and later papers; IEC 60268-16 (5th ed., 2020).
* NIOSH, *Criteria for a recommended standard: occupational noise exposure* (1998); Directive 2003/10/EC; WHO, *Global
  standard for safe listening venues and events* (2022); S. G. Kujawa and M. C. Liberman, "Adding insult to injury:
  cochlear nerve degeneration after 'temporary' noise-induced hearing loss", *J. Neuroscience* (2009).
* AES67-2013, *High-performance streaming audio-over-IP interoperability*; IEEE 1588 (Precision Time Protocol).

Feedback stability uses interpolated zero-imaginary, positive-real crossings within a finite frequency band. The simplified STI and occupational dose illustrations are not compliance measurements or guarantees of safe exposure.
