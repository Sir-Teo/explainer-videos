# Music, Built: Part 60, The Business of Music

Part 60 of a sixty-eight-part course in music (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act X, *The Studio and the Stage*. It follows one stream's fraction
of a cent from a phone to a songwriter. On the way the money passes two copyrights, four kinds of licence and half a dozen
intermediaries, each created when a new machine (the player piano, radio, the sampler, the file, the model) broke the old
arrangement. The tools are Monochord's (`explainer/music/monochord/business.py`, with Part 14's melody model). **Every
term, price, population and market here is illustrative and dated (2026, mostly American); none of it is legal or
financial advice.** No third-party recording is played; the songs in the lawsuits are named, not heard.

* **Two melodies, one opening.** An ear question (two melodies with the same eight-note opening: did one copy the other?
  neither; both were drawn independently from Part 14's model, and the 396th draw repeated an opening); chance; the
  business of music; the plan.
* **1. Two copyrights.** One song, two works (the composition and the sound recording, their owners and terms); one
  composition in two recordings, heard; how long and where (the Statute of Anne, Bach v. Longman, 1831, 1897, 1911, 1972,
  the Music Modernization Act); the Tune's own rights; *Happy Birthday*; each machine broke the last arrangement.
* **2. Licences and collecting societies.** Four licences (mechanical, performance, synchronization, master use);
  collecting societies (SACEM's café, ASCAP, Herbert v. Shanley); where a stream's money flows; gaps (US radio, unmatched
  royalties, the MLC's 2021 receipts).
* **3. Where a stream's money goes.** One stream, heard past its 30 seconds; one month's subscription divided (11.99
  dollars: 3.60 to the service, 5.21 to the label, 1.19 credited to the artist, 0.41 to each of three songwriters); one
  million streams at 0.47 cents (4,655 dollars to rights holders: the artist credited 658 on a label deal, 3,016
  self-released; 224 to each songwriter); is that a lot?
* **4. Deals and recoupment.** A record deal; a 100,000-dollar advance and 50,000 of costs at an 18 % royalty (the artist
  recoups after 228 million streams, the label breaks even at 50 million); other deals; how musicians are paid.
* **5. Dividing the pool.** A simulated service (4,020 accounts, 4.2 million streams); the same month divided two ways (user
  by user, the niche artists +108 %, the chart stars −25 %); why fraud pays (a bot farm paying 168 dollars takes 1,303 pro
  rata); reforms (dated).
* **6. Superstars and cumulative advantage.** The economics of superstars (Rosen; Krueger's concert shares); MusicLab
  (Salganik, Dodds and Watts, 2006); the experiment simulated (Gini 0.43 independent, 0.61 social; unpredictability 0.010
  against 0.018; winners ranked 1st to 11th in quality); two worlds' hits, heard; what it means.
* **7. Charts and attention.** How the charts count (1958, SoundScan in 1991, streams in 2012–13, equivalent units in 2014);
  a long and a short introduction, heard (Lamere's skips; Léveillé Gauvin's shrinking intros); the attention economy.
* **8. Live music: the cost disease and tickets.** A string quartet, heard; Baumol's cost disease (×3.3 since 1966 at 2 % a
  year); one night's tickets sold three ways (face value 1.8 million dollars to the artist's side and 0.8 to resellers; one
  clearing price 3.4 million; seat-by-seat dynamic prices 6.4 million); the ticket market (dated).
* **9. How many melodies are there?** Counting melodies (collision probabilities, effective numbers); the curve (52,206
  effective eight-note openings against 20⁸ ≈ 2.6 × 10¹⁰); the birthday problem for melodies (5.2 % for two 60-note songs;
  about 10¹¹ pairs among 100 million songs share an eight-note opening); what makes two melodies the same (the Tune a fourth
  higher against a re-contoured Tune, heard); in court (US, dated).
* **10. Sampling and machines.** An ear question (a sample or a replay? the first was the sample); sampling in court (Grand
  Upright, Bridgeport, VMG Salsoul, Pelham); an ear question (an old folk song or the model's melody? the first was the
  model's, 1.9 bits a note against 2.7); models and rights (dated); voices and styles.
* **11. Frontier: payout reform and training data.** Payout reform; training data (licensing, attribution, memorization,
  detection); ★ research problem: can a model give a court a calibrated probability that a shared phrase arose by chance?
* **Variation 60, recap and problems.** The Tune's family of copyrights: our recording, a quartet's cover, a remix that
  samples it; the statement after a million streams each (4,655 dollars to rights holders; all of it to us, none, half; to
  the melody's unknown composer of 1761, nothing); the ledger; what we found; five problems; where it comes back; in
  practice; references; Part 61.

## What is computed, and what is heard

`python -m videos.music.music60.compute` (under a minute) fills `.cache/music60/`.

| Item | What it computes | Checked against |
|---|---|---|
| `hook`, `melodies`, `similar`, `ai` | melodies from Part 14's model; exact collision probabilities; similarity counts; surprise | the DP against sampled pairs; a uniform model's A⁻ᵏ (tests) |
| `waterfall`, `deals` | a subscription and a million streams divided; recoupment | the shares add up; hand-worked accounts (tests) |
| `pool` | a simulated month divided pro rata and user by user | a two-user case by hand; bots repaid exactly (tests) |
| `market` | Salganik, Dodds and Watts's experiment simulated | Gini of known vectors (tests) |
| `live` | the cost disease; three ways to sell tickets | the revenue ordering (tests) |
| `rights`, `stream`, `intro`, `sample`, `tune60` | the sounds | the series' clip rules (tests) |

Monochord's tools are held in `tests/music/test_business.py`; this part's claims and clips in `tests/music/test_music60.py`.

**Sounds.** Part 56's session, Part 38's piano, Part 40's kit, Part 9's bowed strings as a quartet, Part 8's voice, and
melodies by Part 14's model.

**What the models are, and are not.** *The terms* (a 30 % service share, 55 and 15 points to recording and composition, an
18 % royalty, a 25 % publisher share, 10 % society costs, three writers) are round illustrative numbers in the range
reported for 2020s US deals; real contracts vary widely. *The service* is a population built so that heavy listeners play
the charts and light listeners play niche artists; real services' data show the same direction with smaller shifts. *The
market* follows the design of the MusicLab experiment with a simple choice rule; its numbers are not the experiment's. *The
melody model* is an order-2 model of 54 folk tunes' pitches, without rhythm; real songwriting is freer, so its effective
numbers are a lower bound in spirit, not a measurement of popular music.

## Build

```bash
python -m videos.music.music60.compute                          # numbers and sounds (under a minute)
EXPLAINER_TTS=silent python tools/build.py music60 -q l --fps 15   # a silent-narration preview, with the sounds
python tools/qa_sound.py music60 --sync                         # the sound gates
python tools/dead_air.py renders/music60_480p.mp4 --sound music60  # no empty screen; no sound over a still one
python tools/lecture_length.py music60                          # 30 to 60 minutes, listening included
python tools/build.py music60                                   # 1080p30, narrated
python -m pytest -q tests/music                                 # Monochord against its references; this part's claims and clips
python -m videos.music.labs 60                                  # the lab (writes a figure and a short WAV)
```

## Problems, with solutions

1. **Compute.** A service pays rights holders 0.47 cents a stream; the label's royalty is 18 % of 55/70 of it. How many
   streams repay a 150,000-dollar account?

   *Solution.* The label receives 0.47 × 55/70 = 0.369 cents a stream; the artist is credited 18 % of that, 0.0665 cents.
   150,000 / 0.000665 ≈ 226 million streams. (The film's 228 million uses the unrounded simulated rate.)

2. **Prove.** Show that under user-centric division no account can be paid more in all than its owner's own fee.

   *Solution.* User u's fee f_u is divided among the artists u played in proportions s_ua / Σ_b s_ub, which are
   non-negative and sum to one; so the total any set of artists receives from u is at most f_u, and an artist played only
   by accounts A receives at most Σ_{u∈A} f_u. A bot farm is paid back at most its own fees. Pro rata, by contrast, an
   artist receives (Σ_u f_u) × (its share of all streams), which grows with its streams whatever its listeners paid.

3. **Ear.** The lab plays melodies from Part 14's model in pairs; say which pairs share an opening, then check.

   *Solution.* The lab prints the answers. Listen to the first six notes only; pairs that share them diverge at the
   seventh.

4. **Build.** Add a fourth social world with a ranking that ignores downloads; measure its Gini and unpredictability.

   *Where to look.* In `business.musiclab`, give each world its own influence (a list); a world with influence 0 is an
   independent world. Compare the Gini and the unpredictability of the influence-0 world with the others, over many
   seeds, and report intervals.

5. ★ **Can a model give a court a calibrated probability that a shared phrase arose by chance?**

   *Where the frontier is.* Train melody (and rhythm) models on large dated corpora, hold out the songs at issue, compute
   the probability of the shared material under independence, and test calibration on pairs known to be independent and
   pairs known to be copied (for example, documented covers and quotations).

## Sources

* D. S. Passman, *All You Need to Know About the Music Business* (11th ed., 2023); A. B. Krueger, *Rockonomics* (2019);
  D. Hesmondhalgh, "Is music streaming bad for musicians? Problems of evidence and argument", *New Media & Society* (2021).
* S. Rosen, "The economics of superstars", *American Economic Review* (1981); A. B. Krueger, "The economics of real
  superstars: the market for rock concerts in the material world", *Journal of Labor Economics* (2005).
* M. J. Salganik, P. S. Dodds and D. J. Watts, "Experimental study of inequality and unpredictability in an artificial
  cultural market", *Science* (2006).
* W. J. Baumol and W. G. Bowen, *Performing Arts: The Economic Dilemma* (1966).
* P. Lamere, "The skip" (Music Machinery, 2014); H. Léveillé Gauvin, "Drawing listener attention in popular music",
  *Musicae Scientiae* (2018).
* Cases (US unless noted): White-Smith Music v. Apollo (1908); Herbert v. Shanley (1917); Bright Tunes Music v. Harrisongs
  Music (1976); Grand Upright Music v. Warner Bros. Records (1991); Bridgeport Music v. Dimension Films (2005); Marya v.
  Warner/Chappell Music (2015); VMG Salsoul v. Ciccone (2016); Williams v. Gaye (2018); Pelham v. Hütter (CJEU, 2019);
  Skidmore v. Led Zeppelin (2020); Gray v. Hudson (2022); Structured Asset Sales v. Sheeran (2024); GEMA v. OpenAI (Munich
  Regional Court, 2025; under appeal). Dates of filings, settlements and statutes after 2023 should be checked against
  current sources.
