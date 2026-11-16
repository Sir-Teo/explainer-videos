from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403

ORDER = ["unison", "second", "third", "fourth", "fifth", "sixth", "seventh", "octave", "ninth"]


class Canons(SoundScene):
    def construct(self):
        chapter(self, 2, r"Canon at every interval", r"How rare is a melody that makes a canon?", extra=((1741, r"the \textit{Goldberg Variations}"),))
        self.goldberg()
        self.solver()
        self.counts()
        self.below()
        self.hear()

    # ------------------------------------------------------------------
    def goldberg(self):
        cells = VGroup()
        for k, name in enumerate(ORDER):
            box = RoundedRectangle(width=1.25, height=1.0, corner_radius=0.1, stroke_color=TUNE if k in (0, 4, 7) else GREY_B, stroke_width=2)
            t = VGroup(label(rf"Var.\ {3 * (k + 1)}", font_size=18, color=GREY_A), label(name, font_size=20, color=WHITE)).arrange(DOWN, buff=0.12).move_to(box)
            cells.add(VGroup(box, t))
        cells.arrange(RIGHT, buff=0.12).move_to(UP * 0.6)
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"a canon: \ a second voice copies the first, \ later, \ and at a fixed interval", WHITE),
            (r"a round is a canon at the unison \ (or octave) \ that goes round", WHITE),
            (r"Bach, \ 1741: \ every third Goldberg variation is a canon, \ at the unison, \ then the second, \ ... \ the ninth", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.next_to(cells, DOWN, buff=0.6)
        with self.voiceover(
            "A round is the simplest case of a canon: a second voice copies the first, entering later. "
            "<bookmark mark='a'/> But the copy need not start on the same note. It can enter a second higher, or a "
            "fifth lower, at any interval, keeping the shape of the line within the scale. <bookmark mark='b'/> In "
            "1741 Bach published the Goldberg Variations, thirty variations on one bass, and made every third "
            "variation a canon: the third at the unison, the sixth at the second, the ninth at the third, and so on "
            "up to the twenty-seventh, a canon at the ninth. <bookmark mark='c'/> Is that a feat, or is any interval as "
            "easy as any other?"
        ) as vo:
            self.play(FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.15), FadeIn(rows_[2]), run_time=3.0)
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def solver(self):
        d = load("canons")
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (rf"a leader of {d['n']} notes, \ one a beat, \ in C major, \ from C to C", WHITE),
            (rf"the follower: \ the same line, \ {d['delay']} beats later, \ some number of scale steps away", WHITE),
            (r"from the follower's entry: \ every beat consonant, \ no parallel fifths or octaves \ (Part 16)", WHITE),
            (r"moves: \ steps, \ thirds, \ fourths, \ fifths, \ octaves; \ no repeated notes", WHITE),
            (r"count them all exactly: \ keep only the leader's last three notes, \ and add up", TUNE))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.4))
        rows_.move_to(DOWN * 0.1)
        head = label(r"a canon solver", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Ask a program. <bookmark mark='a'/> A leader of twelve notes, one a beat, in C major, beginning and ending "
            "on C. <bookmark mark='b'/> The follower plays the same line two beats later, a chosen number of scale steps "
            "away. <bookmark mark='c'/> From the follower's entry, every beat must be consonant, and no two beats in a "
            "row may make parallel fifths or octaves, Part 16's rules. <bookmark mark='d'/> The leader moves by steps "
            "and by the usual leaps. <bookmark mark='e'/> Whether the next note is allowed depends only on the leader's "
            "last three notes, the two the follower is copying and the one before. So the program never lists the "
            "melodies: it counts, for every three-note ending, how many ways there are to reach it, and adds up. "
            "Hundreds of millions of melodies are counted in a compact dynamic-programming search."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counts(self):
        d = load("canons")
        vals = [d["counts"][k] / 1000 for k in ORDER]
        ch = columns(vals, ORDER, width=11.0, height=2.8, color=WEAK, hot=(3, 6), hot_color=EAR, fmt="{:.0f}", font_size=19).move_to(DOWN * 0.6)
        t = label(rf"canons of {d['n']} notes, \ follower {d['delay']} beats later and above, \ in thousands", font_size=22, color=GREY_A).next_to(ch, UP, buff=0.4)
        tot = d["total_melodies"]
        cap = label(rf"of {tot / 1e6:.0f} million melodies: \ about 1 in {tot / d['counts']['fifth']:.0f} at the fifth, \ 1 in {tot / d['counts']['fourth']:.0f} at the fourth", font_size=23, color=TUNE).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            f"Here are the counts. Every interval works: there are hundreds of thousands of canons at each. <bookmark mark='a'/> But they are rare. Of about {say(round(tot / 1000000.0))} million melodies the leader could sing, about one in {say(round(tot / d['counts']['fifth']))} makes a canon at the fifth or the octave. <bookmark mark='b'/> The fourth and the seventh are hardest, about one in {say(round(tot / d['counts']['fourth']))} at the fourth: a fourth is dissonant over the bass, and a seventh copies every consonance onto a dissonance a step away. Bach’s canons also use rhythmic and tonal freedoms absent from this restricted count; these rankings do not measure his compositional difficulty."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(t))
            vo.wait_until("a")
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(Indicate(ch.bars[3], color=EAR), Indicate(ch.bars[6], color=EAR))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def below(self):
        d = load("canons")
        names = ORDER[1:]
        up = [d["counts"][k] / 1000 for k in names]
        dn = [d["counts_below"][k] / 1000 for k in names]
        top = max(up + dn)
        a = columns(up, names, width=5.6, height=2.4, color=WEAK, hot=(), hot_color=TUNE, fmt="{:.0f}", font_size=16, top=top)
        b = columns(dn, names, width=5.6, height=2.4, color=BLUE, hot=(), hot_color=TUNE, fmt="{:.0f}", font_size=16, top=top)
        ta = label(r"follower above", font_size=24, color=GREY_A).next_to(a, UP, buff=0.35)
        tb = label(r"follower below", font_size=24, color=BLUE).next_to(b, UP, buff=0.35)
        g = VGroup(VGroup(ta, a), VGroup(tb, b)).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.2)
        cap = label(r"thousands of canons; \ the octave is the same either way, \ every other interval changes", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Does it matter whether the follower enters above or below? <bookmark mark='a'/> At the octave it makes no "
            "difference: the counts are identical, since an octave above and an octave below make the same intervals. "
            f"At every other interval it does. The ninth below allows only {say(round(d['counts_below']['ninth'] / 1000))} "
            f"thousand canons against {say(round(d['counts']['ninth'] / 1000))} thousand above, and the second below "
            f"{say(round(d['counts_below']['second'] / 1000))} thousand against {say(round(d['counts']['second'] / 1000))}. "
            "The major scale is not symmetric, its steps a pattern of tones and semitones that reads differently "
            "upwards and downwards, so a copy above and a copy below are different problems."
        ) as vo:
            self.play(FadeIn(g[0]), FadeIn(g[1]))
            vo.wait_until("a")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("canons")
        c = clip("canons.three")
        ex = d["examples"]
        names = {"unison": r"at the unison", "second": r"at the second", "fifth": r"at the fifth below"}
        cells = VGroup()
        for k in ("unison", "second", "fifth"):
            g = voices_roll([ex[k]["leader"], ex[k]["follower"]], width=3.9, height=2.4, lo=50, hi=82, total=14.0)
            cells.add(VGroup(label(names[k], font_size=22, color=TUNE), g).arrange(DOWN, buff=0.3))
        cells.arrange(RIGHT, buff=0.4).move_to(DOWN * 0.1)
        with self.voiceover(
            "Three of the canons the solver found, heard: at the unison, at the second, and at the fifth below. In "
            "each, the pink voice copies the gold one two beats later. Not one sampled beat violates this consonance check."
        ):
            self.play(FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"three canons from the solver", detail=r"a plucked string", corner=DL, tag_corner=DR)
            for j, k in enumerate(("unison", "second", "fifth")):
                sing_voices(snd, cells[j][1], [ex[k]["leader"], ex[k]["follower"]], start=ex[k]["start"])
                pulse(snd, cells[j][0], ex[k]["start"], ex[k]["start"] + 14 * BEAT, buff=0.08)
        with self.voiceover(
            "They are correct, and they are not Bach. The rules constrain sampled vertical intervals and parallels; they say nothing about "
            "shape, direction or a climax. The solver shows how much room there is. The art is in choosing."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()
