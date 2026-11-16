from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 13, r"Frontier: \ what the notation does not settle", r"How much of this music do we actually know?")
        self.ficta()
        self.chant_rhythm()
        self.computing()

    # ------------------------------------------------------------------
    def ficta(self):
        d = load("census")["ficta"]
        kinds = sorted(d["kinds"].items(), key=lambda x: -x[1])
        bars = columns([v for _, v in kinds], [k.replace("♯", r"$\sharp$").replace("♭", r"$\flat$") for k, _ in kinds], width=5.0, height=2.6, color=EAR, fmt="{:.0f}", font_size=20)
        bars.move_to(LEFT * 3.7 + DOWN * 0.3)
        t = label(r"notes outside Guido's gamut, \ by name", font_size=20, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=24, color=c_) for s, c_ in (
            (rf"{d['outside']:,} of {d['notes']:,} notes \ ({100 * d['outside'] / d['notes']:.1f} in 100)".replace(",", "{,}"), WHITE),
            (r"outside the gamut: \ \textit{musica ficta}, \ `feigned music'", WHITE),
            (rf"{100 * d['rising'] / d['outside']:.0f} in 100 rise a semitone next: \ leading tones", TUNE),
            (r"mostly added by editors, \ by the singers' rules", EAR))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 6.4))
        side.move_to(RIGHT * 3.3 + DOWN * 0.2)
        with self.voiceover(
            "Everything counted in this part was counted in a modern edition, and an edition is an interpretation. "
            "<bookmark mark='a'/> Take the sharps. In the corpus, "
            f"{say(d['outside'])} of {say(d['notes'])} notes, about {100 * d['outside'] / d['notes']:.0f} in a hundred, are "
            "notes outside Guido's gamut: F sharp, C sharp, G sharp, E flat. <bookmark mark='b'/> Singers called them "
            "musica ficta, feigned music, because the system had no place for them. <bookmark mark='c'/> And "
            f"{say(round(100 * d['rising'] / d['outside']))} in a hundred of them rise a semitone to the very next note: "
            "they are leading tones. <bookmark mark='d'/> Many can reflect editorial additions, but this encoding does not by itself identify each accidental’s manuscript status. Singers added them by "
            "rule, for necessity, to avoid a tritone, and for beauty, to sharpen a cadence, and modern editors add them "
            "on the singers' behalf. Two editors can differ; the double leading-tone cadences counted in chapter ten "
            "are partly a count of editorial decisions."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chant_rhythm(self):
        items = [
            (r"chant's rhythm: \ the neumes show groups and nuances, \ not lengths", WHITE),
            (r"Solesmes, \ about 1900: \ equal notes, \ grouped in twos and threes \ (Pothier, \ Mocquereau)", WHITE),
            (r"Eugène Cardine's semiology, \ 1970: \ the earliest neumes show lengthenings and lightenings", WHITE),
            (r"others read chant in measured rhythm: \ the sources allow all three", WHITE),
            (r"the Winchester organa: \ shapes without pitches, \ reconstructed, \ never simply read", GREY_A),
        ]
        rows_scene(self, r"rhythm the page does not give", items,
                   "The chant itself has the same problem. <bookmark mark='b'/> Neumes show how notes group and where a "
                   "singer should lean, not how long each note lasts. <bookmark mark='c'/> The monks of Solesmes in "
                   "France, who restored the chant around 1900, sang equal notes in groups of two and three, and that is "
                   "how most people have heard chant since. <bookmark mark='d'/> In 1970 Eugène Cardine, also of "
                   "Solesmes, argued from the oldest neumes that singers lengthened and lightened notes in ways the "
                   "equal-note method erased. <bookmark mark='e'/> Others read chant in measured rhythm. The sources "
                   "allow all three. <bookmark mark='f'/> And the Winchester organa of chapter four can only be "
                   "reconstructed, never simply read. This part's chant, in plain equal notes, is one choice among "
                   "several.", marks="bcdef")

    # ------------------------------------------------------------------
    def computing(self):
        rows_ = VGroup(*[label(t, font_size=23, color=c_) for t, c_ in (
            (r"Cantus: \ a database of the chants in hundreds of medieval manuscripts, \ begun in the 1980s", WHITE),
            (r"mode classifiers trained on thousands of chants: \ right about nine times in ten", WHITE),
            (r"a wrong answer is a question: \ some chants sit in different modes in different sources", WHITE),
            (r"editions as data: \ ficta, \ text underlay, \ and rhythm become variables, \ not facts", TUNE),
            (r"$\bigstar$ \ research problem: \ learn the rules of \textit{musica ficta} from editions, \ and measure where editors disagree", EAR))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"computational chant and medieval studies", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Computation is changing this field. <bookmark mark='a'/> The Cantus database, begun in the 1980s, indexes "
            "the chants in hundreds of medieval manuscripts, so that a melody can be traced across Europe. "
            "<bookmark mark='b'/> Classifiers trained on thousands of chants, like the medieval rule of chapter one but "
            "learnt from the data, have reported mode-classification results that depend on corpus, labels and evaluation split; this film does not establish a general ninety-percent benchmark, <bookmark mark='c'/> and a wrong answer is a "
            "question worth asking, since some chants sit in different modes in different medieval sources. <bookmark mark='d'/> The bigger shift is "
            "to treat an edition as data with uncertain parts: the accidentals, the placing of the words, the rhythm. "
            "<bookmark mark='e'/> Here is a research problem: learn the rules of musica ficta from many editions, apply "
            "them to music no one has edited, and measure exactly where editors disagree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
