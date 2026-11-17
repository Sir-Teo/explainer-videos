"""The reading of *Music, Built*, as data: the textbooks the series covers, the theories it teaches, and each
part's reference card.  ``python -m videos.music.reading`` writes ``videos/music/READING.md`` from it;
``tests/music/test_reading.py`` checks that every book and theory listed is cited by the parts it names and that the
file is up to date.

Which parts cite a book or teach a theory is not typed in by hand: it is found by searching each part's scenes and
README (``cited_by``), so the map cannot claim a part covers something it does not mention.
"""

from __future__ import annotations

import ast
import re
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = range(1, 69)


def fold(s: str) -> str:
    """ASCII text with TeX and Unicode accents removed, so that M\\"uller, Müller and Muller all match."""
    s = re.sub(r"\\[`'\"^~=.]\{?([A-Za-z])\}?", r"\1", s)
    s = re.sub(r"\\[vu]\{([A-Za-z])\}", r"\1", s)
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def sources(part: int) -> str:
    d = HERE / f"music{part}"
    return fold("\n".join(p.read_text() for p in sorted(d.glob("s*.py")) + [d / "README.md"]))


_CACHE: dict[int, str] = {}


def cited_by(pattern: str) -> list[int]:
    """The parts whose scenes or README match ``pattern`` (a regex over accent-folded text)."""
    if not _CACHE:
        _CACHE.update({n: sources(n) for n in PARTS})
    return [n for n, t in _CACHE.items() if re.search(pattern, t)]


# (area, short name, the book, the pattern that finds it in a part)
SPINE = [
 ("Acoustics and instruments", "Helmholtz", "H. von Helmholtz, *On the Sensations of Tone* (1863; tr. A. J. Ellis, 1875)", r"Helmholtz.{0,40}Sensations"),
 ("Acoustics and instruments", "Rayleigh", "Lord Rayleigh, *The Theory of Sound* (1877)", r"Theory of Sound"),
 ("Acoustics and instruments", "Fletcher–Rossing", "N. H. Fletcher and T. D. Rossing, *The Physics of Musical Instruments* (2nd ed., 1998)", r"Physics of Musical Instruments"),
 ("Acoustics and instruments", "Benade", "A. H. Benade, *Fundamentals of Musical Acoustics* (1976)", r"Benade"),
 ("Acoustics and instruments", "Rossing–Moore–Wheeler", "T. D. Rossing, F. R. Moore and P. A. Wheeler, *The Science of Sound* (3rd ed., 2002)", r"Science of Sound"),
 ("Acoustics and instruments", "Kinsler", "L. E. Kinsler and others, *Fundamentals of Acoustics* (4th ed., 2000)", r"Kinsler"),
 ("Acoustics and instruments", "Pierce", "A. D. Pierce, *Acoustics* (3rd ed., 2019)", r"A\. D\. Pierce"),
 ("Acoustics and instruments", "Chaigne–Kergomard", "A. Chaigne and J. Kergomard, *Acoustics of Musical Instruments* (2016)", r"Kergomard"),
 ("Acoustics and instruments", "Campbell–Greated", "D. M. Campbell and C. A. Greated, *The Musician's Guide to Acoustics* (1987)", r"Greated"),
 ("Acoustics and instruments", "Roederer", "J. G. Roederer, *The Physics and Psychophysics of Music* (4th ed., 2008)", r"Roederer"),
 ("Acoustics and instruments", "Sundberg", "J. Sundberg, *The Science of the Singing Voice* (1987)", r"Singing Voice"),
 ("Acoustics and instruments", "Bilbao", "S. Bilbao, *Numerical Sound Synthesis* (2009)", r"Numerical Sound Synthesis"),
 ("Hearing and psychoacoustics", "Moore", "B. C. J. Moore, *An Introduction to the Psychology of Hearing* (6th ed., 2012)", r"Psychology of Hearing"),
 ("Hearing and psychoacoustics", "Plack", "C. J. Plack, *The Sense of Hearing* (3rd ed., 2018)", r"Sense of Hearing"),
 ("Hearing and psychoacoustics", "Zwicker–Fastl", "E. Zwicker and H. Fastl, *Psychoacoustics: Facts and Models* (3rd ed., 2007)", r"Zwicker and H\. Fastl"),
 ("Hearing and psychoacoustics", "Hartmann", "W. M. Hartmann, *Signals, Sound, and Sensation* (1997)", r"Signals, Sound"),
 ("Hearing and psychoacoustics", "Blauert", "J. Blauert, *Spatial Hearing* (rev. ed., 1997)", r"Spatial Hearing"),
 ("Hearing and psychoacoustics", "Bregman", "A. S. Bregman, *Auditory Scene Analysis* (1990)", r"Auditory Scene Analysis"),
 ("Tuning", "Barbour", "J. M. Barbour, *Tuning and Temperament* (1951)", r"Barbour"),
 ("Tuning", "Sethares", "W. A. Sethares, *Tuning, Timbre, Spectrum, Scale* (2nd ed., 2005)", r"Tuning, Timbre"),
 ("Tuning", "Partch", "H. Partch, *Genesis of a Music* (1949; 2nd ed., 1974)", r"Genesis of a Music"),
 ("Theory and aural skills", "Fux", "J. J. Fux, *Gradus ad Parnassum* (1725; tr. A. Mann)", r"Gradus"),
 ("Theory and aural skills", "Rameau", "J.-P. Rameau, *Traité de l'harmonie* (1722)", r"Trait.{0,4}de l.harmonie"),
 ("Theory and aural skills", "Piston", "W. Piston, *Harmony* (1941; 5th ed., rev. M. DeVoto, 1987)", r"Piston"),
 ("Theory and aural skills", "Aldwell–Schachter", "E. Aldwell and C. Schachter, *Harmony and Voice Leading* (4th ed., 2011)", r"Aldwell"),
 ("Theory and aural skills", "Kostka–Payne", "S. Kostka and D. Payne, *Tonal Harmony* (8th ed., 2018)", r"Kostka"),
 ("Theory and aural skills", "Laitz", "S. G. Laitz, *The Complete Musician* (4th ed., 2015)", r"Laitz"),
 ("Theory and aural skills", "Clendinning–Marvin", "J. P. Clendinning and E. W. Marvin, *The Musician's Guide to Theory and Analysis* (4th ed., 2021)", r"Clendinning"),
 ("Theory and aural skills", "Open Music Theory", "M. Gotham and others, *Open Music Theory* (2nd ed., 2021)", r"Open Music Theory"),
 ("Theory and aural skills", "Karpinski", "G. S. Karpinski, *Aural Skills Acquisition* (2000)", r"Karpinski"),
 ("Theory and aural skills", "Jeppesen", "K. Jeppesen, *Counterpoint* (1931) and *The Style of Palestrina and the Dissonance* (1927)", r"Jeppesen"),
 ("Theory and aural skills", "Gjerdingen", "R. O. Gjerdingen, *Music in the Galant Style* (2007)", r"Galant Style"),
 ("Theory and aural skills", "Caplin", "W. E. Caplin, *Classical Form* (1998)", r"Classical Form"),
 ("Theory and aural skills", "Hepokoski–Darcy", "J. Hepokoski and W. Darcy, *Elements of Sonata Theory* (2006)", r"Sonata Theory"),
 ("Theory and aural skills", "Schenker", "H. Schenker, *Der freie Satz* (1935)", r"freie Satz"),
 ("Theory and aural skills", "Cadwallader–Gagné", "A. Cadwallader and D. Gagné, *Analysis of Tonal Music: A Schenkerian Approach*", r"Cadwallader"),
 ("Theory and aural skills", "Lerdahl–Jackendoff", "F. Lerdahl and R. Jackendoff, *A Generative Theory of Tonal Music* (1983)", r"Generative Theory of Tonal Music"),
 ("Theory and aural skills", "Lerdahl", "F. Lerdahl, *Tonal Pitch Space* (2001)", r"Tonal Pitch Space"),
 ("Theory and aural skills", "Rosen", "C. Rosen, *The Classical Style* (1971) and *Sonata Forms* (1980)", r"C\. Rosen"),
 ("Post-tonal and mathematical theory", "Forte", "A. Forte, *The Structure of Atonal Music* (1973)", r"Structure of Atonal Music"),
 ("Post-tonal and mathematical theory", "Straus", "J. N. Straus, *Introduction to Post-Tonal Theory* (4th ed., 2016)", r"Post-Tonal Theory"),
 ("Post-tonal and mathematical theory", "Lewin", "D. Lewin, *Generalized Musical Intervals and Transformations* (1987)", r"Generalized Musical Intervals"),
 ("Post-tonal and mathematical theory", "Cohn", "R. Cohn, *Audacious Euphony* (2012)", r"Audacious Euphony"),
 ("Post-tonal and mathematical theory", "Tymoczko", "D. Tymoczko, *A Geometry of Music* (2011)", r"Geometry of Music"),
 ("Post-tonal and mathematical theory", "Amiot", "E. Amiot, *Music Through Fourier Space* (2016)", r"Fourier Space"),
 ("Post-tonal and mathematical theory", "Toussaint", "G. Toussaint, *The Geometry of Musical Rhythm* (2013; 2nd ed., 2019)", r"Geometry of Musical Rhythm"),
 ("Post-tonal and mathematical theory", "Benson", "D. J. Benson, *Music: A Mathematical Offering* (2006)", r"Mathematical Offering"),
 ("Post-tonal and mathematical theory", "Xenakis", "I. Xenakis, *Formalized Music* (1963; rev. 1992)", r"Formalized Music"),
 ("History", "Taruskin", "R. Taruskin, *The Oxford History of Western Music* (2005)", r"Oxford History of Western Music"),
 ("History", "Burkholder–Grout–Palisca", "J. P. Burkholder, D. J. Grout and C. V. Palisca, *A History of Western Music* (10th ed., 2019)", r"Grout"),
 ("History", "Hoppin", "R. H. Hoppin, *Medieval Music* (1978)", r"Hoppin"),
 ("History", "Atlas", "A. W. Atlas, *Renaissance Music* (1998)", r"Renaissance Music"),
 ("History", "Bukofzer", "M. Bukofzer, *Music in the Baroque Era* (1947)", r"Bukofzer"),
 ("History", "Dahlhaus", "C. Dahlhaus, *Nineteenth-Century Music* (1980; tr. 1989)", r"Dahlhaus"),
 ("History", "Ross", "A. Ross, *The Rest Is Noise* (2007)", r"Rest Is Noise"),
 ("History", "Kelly", "T. F. Kelly, *Capturing Music: The Story of Notation* (2014)", r"Capturing Music"),
 ("Cognition and emotion", "Meyer", "L. B. Meyer, *Emotion and Meaning in Music* (1956)", r"Emotion and Meaning"),
 ("Cognition and emotion", "Krumhansl", "C. L. Krumhansl, *Cognitive Foundations of Musical Pitch* (1990)", r"Cognitive Foundations"),
 ("Cognition and emotion", "Deutsch", "D. Deutsch (ed.), *The Psychology of Music* (3rd ed., 2013)", r"Psychology of Music"),
 ("Cognition and emotion", "Huron", "D. Huron, *Sweet Anticipation* (2006) and *Voice Leading* (2016)", r"Sweet Anticipation"),
 ("Cognition and emotion", "Temperley", "D. Temperley, *Music and Probability* (2007)", r"Music and Probability"),
 ("Cognition and emotion", "London", "J. London, *Hearing in Time* (2nd ed., 2012)", r"Hearing in Time"),
 ("Cognition and emotion", "Juslin–Sloboda", "P. N. Juslin and J. A. Sloboda (eds.), *Handbook of Music and Emotion* (2010)", r"Handbook of Music and Emotion"),
 ("Cognition and emotion", "Patel", "A. D. Patel, *Music, Language, and the Brain* (2008)", r"Language, and the Brain"),
 ("Cognition and emotion", "Kivy", "P. Kivy, *The Corded Shell* (1980)", r"Corded Shell"),
 ("Ethnomusicology and world musics", "Merriam", "A. P. Merriam, *The Anthropology of Music* (1964)", r"Anthropology of Music"),
 ("Ethnomusicology and world musics", "Blacking", "J. Blacking, *How Musical Is Man?* (1973)", r"How Musical Is Man"),
 ("Ethnomusicology and world musics", "Nettl", "B. Nettl, *The Study of Ethnomusicology* (3rd ed., 2015)", r"Study of Ethnomusicology"),
 ("Ethnomusicology and world musics", "Titon", "J. T. Titon (ed.), *Worlds of Music* (6th ed., 2017)", r"Worlds of Music"),
 ("Ethnomusicology and world musics", "Jairazbhoy", "N. A. Jairazbhoy, *The Rāgs of North Indian Music* (1971)", r"Jairazbhoy"),
 ("Ethnomusicology and world musics", "Clayton", "M. Clayton, *Time in Indian Music* (2000)", r"Time in Indian Music"),
 ("Ethnomusicology and world musics", "Touma", "H. H. Touma, *The Music of the Arabs* (1996)", r"Music of the Arabs"),
 ("Ethnomusicology and world musics", "Tenzer", "M. Tenzer, *Gamelan Gong Kebyar* (2000)", r"Gong Kebyar"),
 ("Ethnomusicology and world musics", "Arom", "S. Arom, *African Polyphony and Polyrhythm* (1991)", r"African Polyphony"),
 ("Ethnomusicology and world musics", "Agawu", "K. Agawu, *Representing African Music* (2003)", r"Representing African Music"),
 ("Ethnomusicology and world musics", "Kubik", "G. Kubik, *Africa and the Blues* (1999)", r"Africa and the Blues"),
 ("Jazz and popular music", "Schuller", "G. Schuller, *Early Jazz* (1968) and *The Swing Era* (1989)", r"Swing Era"),
 ("Jazz and popular music", "Berliner", "P. F. Berliner, *Thinking in Jazz* (1994)", r"Thinking in Jazz"),
 ("Jazz and popular music", "Levine", "M. Levine, *The Jazz Theory Book* (1995)", r"Jazz Theory Book"),
 ("Jazz and popular music", "Gioia", "T. Gioia, *The History of Jazz* (3rd ed., 2021)", r"History of Jazz"),
 ("Jazz and popular music", "Everett", "W. Everett, *The Foundations of Rock* (2009)", r"Foundations of Rock"),
 ("Jazz and popular music", "Moore (song)", "A. F. Moore, *Song Means* (2012)", r"Song Means"),
 ("Jazz and popular music", "Temperley (rock)", "D. Temperley, *The Musical Language of Rock* (2018)", r"Musical Language of Rock"),
 ("Craft: orchestration, composition, performance, media", "Berlioz", "H. Berlioz, *Treatise on Instrumentation* (1844)", r"Treatise on Instrumentation"),
 ("Craft: orchestration, composition, performance, media", "Adler", "S. Adler, *The Study of Orchestration* (4th ed., 2016)", r"Study of Orchestration"),
 ("Craft: orchestration, composition, performance, media", "Schoenberg", "A. Schoenberg, *Fundamentals of Musical Composition* (1967)", r"Fundamentals of Musical Composition"),
 ("Craft: orchestration, composition, performance, media", "Cook", "N. Cook, *Beyond the Score* (2013)", r"Beyond the Score"),
 ("Craft: orchestration, composition, performance, media", "Gorbman", "C. Gorbman, *Unheard Melodies* (1987)", r"Unheard Melodies"),
 ("Craft: orchestration, composition, performance, media", "Chion", "M. Chion, *Audio-Vision* (1990; tr. 1994)", r"Audio-Vision"),
 ("Craft: orchestration, composition, performance, media", "Collins", "K. Collins, *Game Sound* (2008)", r"Game Sound"),
 ("Signal processing and synthesis", "Oppenheim–Schafer", "A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing* (3rd ed., 2010)", r"Discrete-Time Signal Processing"),
 ("Signal processing and synthesis", "Smith", "J. O. Smith, the four CCRMA books (*Mathematics of the DFT*, *Introduction to Digital Filters*, *Physical Audio Signal Processing*, *Spectral Audio Signal Processing*)", r"J\. O\. Smith"),
 ("Signal processing and synthesis", "Pohlmann", "K. C. Pohlmann, *Principles of Digital Audio* (6th ed., 2010)", r"Principles of Digital Audio"),
 ("Signal processing and synthesis", "Zölzer", "U. Zölzer (ed.), *DAFX: Digital Audio Effects* (2nd ed., 2011)", r"DAFX"),
 ("Signal processing and synthesis", "Roads", "C. Roads, *The Computer Music Tutorial* (2nd ed., 2023) and *Microsound* (2001)", r"Computer Music Tutorial"),
 ("Signal processing and synthesis", "Dodge–Jerse", "C. Dodge and T. A. Jerse, *Computer Music* (2nd ed., 1997)", r"Dodge and T\. A\. Jerse"),
 ("Signal processing and synthesis", "Puckette", "M. Puckette, *The Theory and Technique of Electronic Music* (2007)", r"Theory and Technique of Electronic Music"),
 ("Signal processing and synthesis", "Holmes", "T. Holmes, *Electronic and Experimental Music* (6th ed., 2020)", r"Electronic and Experimental Music"),
 ("Studio, room and stage", "Eargle", "J. Eargle, *The Microphone Book* (2nd ed., 2004)", r"Microphone Book"),
 ("Studio, room and stage", "Toole", "F. E. Toole, *Sound Reproduction* (3rd ed., 2018)", r"Sound Reproduction"),
 ("Studio, room and stage", "Kuttruff", "H. Kuttruff, *Room Acoustics* (6th ed., 2016)", r"Room Acoustics"),
 ("Studio, room and stage", "Beranek", "L. Beranek, *Concert Halls and Opera Houses* (2nd ed., 2004)", r"Concert Halls"),
 ("Studio, room and stage", "Everest–Pohlmann", "F. A. Everest and K. C. Pohlmann, *Master Handbook of Acoustics* (7th ed., 2021)", r"Master Handbook"),
 ("Studio, room and stage", "Izhaki", "R. Izhaki, *Mixing Audio* (3rd ed., 2018)", r"Izhaki"),
 ("Studio, room and stage", "Moylan", "W. Moylan, *Understanding and Crafting the Mix* (3rd ed., 2015)", r"Crafting the Mix"),
 ("Studio, room and stage", "Katz", "B. Katz, *Mastering Audio* (3rd ed., 2015)", r"Mastering Audio"),
 ("Studio, room and stage", "Bosi–Goldberg", "M. Bosi and R. E. Goldberg, *Introduction to Digital Audio Coding and Standards* (2003)", r"Digital Audio Coding"),
 ("Studio, room and stage", "McCarthy", "B. McCarthy, *Sound Systems: Design and Optimization* (3rd ed., 2016)", r"Design and Optimization"),
 ("Studio, room and stage", "Passman", "D. S. Passman, *All You Need to Know About the Music Business* (11th ed., 2023)", r"Passman"),
 ("Music information retrieval and generation", "Müller", "M. Müller, *Fundamentals of Music Processing* (2nd ed., 2021)", r"Fundamentals of Music Processing"),
 ("Music information retrieval and generation", "Klapuri–Davy", "A. Klapuri and M. Davy (eds.), *Signal Processing Methods for Music Transcription* (2006)", r"Music Transcription"),
 ("Music information retrieval and generation", "Lerch", "A. Lerch, *An Introduction to Audio Content Analysis* (2nd ed., 2022)", r"Audio Content Analysis"),
 ("Music information retrieval and generation", "Knees–Schedl", "P. Knees and M. Schedl, *Music Similarity and Retrieval* (2016)", r"Music Similarity and Retrieval"),
 ("Music information retrieval and generation", "Vincent–Virtanen–Gannot", "E. Vincent, T. Virtanen and S. Gannot (eds.), *Audio Source Separation and Speech Enhancement* (2018)", r"Audio Source Separation"),
 ("Music information retrieval and generation", "Briot–Hadjeres–Pachet", "J.-P. Briot, G. Hadjeres and F.-D. Pachet, *Deep Learning Techniques for Music Generation* (2020)", r"Deep Learning Techniques"),
 ("Musicology and method", "Kerman", "J. Kerman, *Contemplating Music* (1985)", r"Contemplating Music"),
 ("Musicology and method", "Goehr", "L. Goehr, *The Imaginary Museum of Musical Works* (1992)", r"Imaginary Museum"),
 ("Musicology and method", "Small", "C. Small, *Musicking* (1998)", r"Musicking"),
 ("Musicology and method", "Clarke–Cook", "E. Clarke and N. Cook (eds.), *Empirical Musicology* (2004)", r"Empirical Musicology"),
 ("Musicology and method", "Grier", "J. Grier, *The Critical Editing of Music* (1996)", r"Critical Editing"),
]

THEORIES = [
 ("Consonance", "Pythagorean ratios", "the Pythagoreans; Nicomachus (c. 100)", r"Pythagor"),
 ("Consonance", "roughness and beats", "Helmholtz (1863); Plomp and Levelt (1965)", r"Plomp"),
 ("Consonance", "spectral (timbre-dependent) consonance", "Sethares (1993)", r"Sethares"),
 ("Consonance", "harmonicity and virtual pitch", "Terhardt (1974); Parncutt (1989)", r"Terhardt"),
 ("Consonance", "consonance as culture", "McDermott and others (2016)", r"McDermott"),
 ("Hearing", "place and temporal theories of pitch", "Békésy; Wever's volley; Licklider (1951)", r"Licklider"),
 ("Hearing", "the residue, or missing fundamental", "Seebeck (1841); Schouten (1940)", r"Schouten|missing fundamental"),
 ("Hearing", "critical bands", "Fletcher (1940); Zwicker (1961); Glasberg and Moore (1990)", r"critical band"),
 ("Hearing", "psychophysical laws", "Fechner (1860); Stevens (1936, 1957)", r"Fechner"),
 ("Hearing", "auditory scene analysis", "Bregman (1990)", r"Bregman"),
 ("Theory", "fundamental bass", "Rameau (1722)", r"fundamental bass"),
 ("Theory", "harmonic function", "Riemann (1893)", r"Riemann"),
 ("Theory", "species counterpoint", "Fux (1725)", r"Fux"),
 ("Theory", "voice leading from perception", "Huron (2001)", r"Tone and voice"),
 ("Theory", "galant schemata and partimenti", "Gjerdingen (2007); Sanguinetti (2012)", r"partimento"),
 ("Theory", "Schenkerian reduction", "Schenker (1935)", r"Schenker"),
 ("Theory", "generative grammar of tonal music", "Lerdahl and Jackendoff (1983); Rohrmeier (2011)", r"Rohrmeier"),
 ("Theory", "formal functions and sonata theory", "Caplin (1998); Hepokoski and Darcy (2006)", r"Hepokoski"),
 ("Theory", "topics", "Ratner (1980)", r"Ratner"),
 ("Theory", "key profiles", "Krumhansl and Kessler (1982)", r"Kessler"),
 ("Post-tonal", "pitch-class set theory", "Forte (1973)", r"Forte"),
 ("Post-tonal", "twelve-tone combinatoriality", "Schoenberg; Babbitt (1955)", r"Babbitt"),
 ("Post-tonal", "transformational and neo-Riemannian theory", "Lewin (1987); Cohn (1998)", r"Lewin"),
 ("Post-tonal", "voice-leading geometry", "Tymoczko (2006)", r"Tymoczko"),
 ("Post-tonal", "well-formed and maximally even scales", "Carey and Clampitt (1989); Clough and Douthett (1991)", r"Clampitt"),
 ("Post-tonal", "Euclidean rhythms", "Bjorklund; Toussaint (2005)", r"Euclidean rhythm|Euclid's algorithm|Bjorklund"),
 ("Post-tonal", "rhythmic tiling canons", "Vuza (1991)", r"Vuza"),
 ("Post-tonal", "just intonation as a system", "Partch (1949)", r"Partch"),
 ("Cognition", "expectation", "Meyer (1956); Narmour (1990); Huron's ITPRA (2006)", r"Narmour"),
 ("Cognition", "statistical learning", "Saffran and others (1999); Pearce's IDyOM (2005)", r"Saffran"),
 ("Cognition", "musical meter as entrainment", "Povel and Essens (1985); London (2004); Large", r"Povel"),
 ("Cognition", "emotion mechanisms", "Juslin and Västfjäll (2008)", r"Juslin"),
 ("Cognition", "the contour theory of expression", "Kivy (1980)", r"Kivy"),
 ("Cognition", "formalism", "Hanslick (1854)", r"Hanslick"),
 ("Cognition", "predictive coding of music", "Vuust and others (2009, 2022)", r"Vuust"),
 ("Origins", "statistical universals", "Savage and others (2015); Mehr and others (2019)", r"Savage"),
 ("Origins", "humanly organized sound", "Blacking (1973)", r"humanly organized"),
 ("Origins", "credible signalling and social bonding", "Mehr and others (2020); Savage and others (2021)", r"credible signal"),
 ("Origins", "sexual selection", "Darwin (1871)", r"Darwin"),
 ("Media", "added value and synchresis", "Chion (1990)", r"synchresis"),
 ("Media", "the classical film score", "Gorbman (1987)", r"Gorbman"),
 ("Signal processing", "the sampling theorem", "Nyquist (1928); Shannon (1949)", r"sampling theorem|Nyquist"),
 ("Signal processing", "Fourier analysis", "Fourier (1822); Cooley and Tukey (1965)", r"Cooley"),
 ("Signal processing", "the time-frequency limit", "Gabor (1946)", r"Gabor"),
 ("Signal processing", "artificial reverberation", "Schroeder (1962); Jot (1991)", r"Schroeder"),
 ("Signal processing", "frequency modulation synthesis", "Chowning (1973)", r"Chowning"),
 ("Signal processing", "perceptual coding", "Johnston (1988); Brandenburg", r"Johnston"),
 ("Signal processing", "loudness measurement", "ITU-R BS.1770; EBU R 128", r"1770"),
 ("Machines", "fingerprinting", "Wang (2003)", r"A\. Wang"),
 ("Machines", "non-negative matrix factorization", "Smaragdis and Brown (2003)", r"Smaragdis"),
 ("Machines", "beat tracking by dynamic programming", "Ellis (2007)", r"Beat tracking by dynamic programming"),
 ("Machines", "neural audio and language models", "WaveNet (2016); Music Transformer (2019); MusicLM (2023)", r"WaveNet"),
 ("Musicology", "the work-concept", "Goehr (1992)", r"work-concept|fixed musical work|fixed `work'"),
 ("Musicology", "musicking", "Small (1998)", r"musicking|Musicking"),
 ("Musicology", "bi-musicality", "Hood (1960)", r"bi-musicality"),
]


def reference_cards() -> dict[int, tuple[list[str], list[str]]]:
    """Each part's on-screen reference card: (books, papers), as TeX strings."""
    out = {}
    for n in PARTS:
        for f in sorted((HERE / f"music{n}").glob("s*.py")):
            for node in ast.walk(ast.parse(f.read_text())):
                if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "reference_card":
                    out[n] = (ast.literal_eval(node.args[0]), ast.literal_eval(node.args[1]))
    return out


def tex_to_md(s: str) -> str:
    s = re.sub(r"\\=\{?\\i\}? ?", "ī", s)  # a control word eats the space after it
    s = re.sub(r"\\textit\{([^}]*)\}", r"*\1*", s)
    s = re.sub(r"\\textsc\{([^}]*)\}", r"\1", s)
    for a, b in (("\\ ", " "), ("``", "\""), ("''", "\""), ("`", "'"), ("--", "–"), ("\\&", "&"), ("~", " ")):
        s = s.replace(a, b)
    accents = {"\"": "\u0308", "'": "\u0301", "`": "\u0300", "^": "\u0302", "~": "\u0303", "=": "\u0304", "c": "\u0327",
               "v": "\u030c", "u": "\u0306", ".": "\u0307"}
    s = re.sub(r"\\([\"'`^~=.])\{?([A-Za-z])\}?", lambda m: unicodedata.normalize("NFC", m.group(2) + accents[m.group(1)]), s)
    s = re.sub(r"\\([cvu])\{([A-Za-z])\}", lambda m: unicodedata.normalize("NFC", m.group(2) + accents[m.group(1)]), s)
    for a, b in (("\\,", ""), ("\\ldots", "…"), ("\\alpha", "α"), ("\\_", "_"), ("\\i", "i")):
        s = s.replace(a, b)
    s = s.replace("{", "").replace("}", "").replace("$", "")
    return re.sub(r"\s+", " ", s).strip()


def short_parts(ps: list[int]) -> str:
    """[3, 4, 5, 7] -> '3–5, 7'."""
    out, i = [], 0
    while i < len(ps):
        j = i
        while j + 1 < len(ps) and ps[j + 1] == ps[j] + 1:
            j += 1
        out.append(str(ps[i]) if j == i else f"{ps[i]}–{ps[j]}")
        i = j + 1
    return ", ".join(out)


def render() -> str:
    from explainer.music import PARTS as TITLES

    lines = [
        "# Music, Built: textbooks, theories and papers",
        "",
        "The series' reading in one place, written by `python -m videos.music.reading` from",
        "[`reading.py`](reading.py) and the parts themselves; `tests/music/test_reading.py` fails when it is out of",
        "date. Section 1 is the textbook spine, area by area: the books a music, music-technology or",
        "music-cognition degree is taught from, with the parts that cite each. Section 2 maps the major theories to",
        "the parts that teach them. Section 3 is every part's reference card, as it appears on screen.",
        "",
        "The *Parts* columns are found, not typed: a part is listed when its scenes or its README cite the book or",
        "name the theory. Fuller notes (editions, chapters, what each source was used for) are in each part's",
        "README, under *Sources*.",
        "",
        "## 1. The textbook spine",
        "",
    ]
    area = None
    for a, short, book, rx in SPINE:
        if a != area:
            if area is not None:
                lines.append("")
            lines += [f"### {a}", "", "| Short name | Book | Parts |", "|---|---|---|"]
            area = a
        lines.append(f"| {short} | {book} | {short_parts(cited_by(rx))} |")
    lines += ["", "## 2. Theories and where they are taught", ""]
    area = None
    for a, theory, who, rx in THEORIES:
        if a != area:
            if area is not None:
                lines.append("")
            lines += [f"### {a}", "", "| Theory | Who, when | Parts |", "|---|---|---|"]
            area = a
        lines.append(f"| {theory} | {who} | {short_parts(cited_by(rx))} |")
    lines += ["", "## 3. Every part's reference card", ""]
    cards = reference_cards()
    for n in PARTS:
        books, papers = cards[n]
        lines.append(f"**Part {n}, *{tex_to_md(TITLES[n])}*.** Books: " + "; ".join(tex_to_md(b) for b in books)
                     + ". Papers: " + "; ".join(tex_to_md(p) for p in papers) + ".")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    (HERE / "READING.md").write_text(render())
    print("wrote", HERE / "READING.md")
