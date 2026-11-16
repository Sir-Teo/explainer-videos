from __future__ import annotations

from videos.music.music65.common import *  # noqa: F403


class Rules(SoundScene):
    def construct(self):
        chapter(self, 1, r"Dice, \ rules and chance", r"What did composing machines do before they could learn?")
        self.timeline()
        self.kinds()
        self.corpus()

    # ------------------------------------------------------------------
    def timeline(self):
        ev = [(1792, r"a minuet by dice, \ attributed to Mozart"), (1957, r"Hiller and Isaacson's Illiac Suite: \ draw, \ test against rules, \ draw again"),
              (1962, r"Xenakis: \ stochastic laws for masses of notes"), (1981, r"Cope begins EMI"),
              (2016, r"DeepBach: \ a network harmonizes chorales"), (2018, r"the Music Transformer")]
        line = Line(LEFT * 6, RIGHT * 6, color=GREY_B, stroke_width=2).move_to(DOWN * 0.2)
        x = lambda yr: -6 + 12 * (yr - 1780) / (2030 - 1780)
        g = VGroup()
        for i, (yr, t) in enumerate(ev):
            up = i % 2 == 0
            dot = Dot([x(yr), -0.2, 0], radius=0.07, color=TUNE)
            lab = VGroup(label(str(yr), font_size=17, color=TUNE), label(t, font_size=14, color=WHITE)).arrange(DOWN, buff=0.08)
            lab.move_to([x(yr), 1.1 if up else -1.6, 0])
            g.add(VGroup(dot, Line(dot.get_center(), lab.get_bottom() if up else lab.get_top(), color=GREY_D, stroke_width=1), lab))
        head = label(r"composing machines", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Composing machines are older than computers. <bookmark mark='a'/> In 1792 a game appeared, attributed to Mozart, "
            "that built a minuet from bars chosen by dice; Part 42 played one of ours. <bookmark mark='b'/> In 1957 Lejaren "
            "Hiller and Leonard Isaacson's Illiac Suite drew notes at random and tested each against rules of counterpoint, "
            "drawing again when one failed. <bookmark mark='c'/> Iannis Xenakis wrote laws of chance for whole clouds of "
            "notes. <bookmark mark='d'/> In 1981 David Cope began EMI. <bookmark mark='e'/> And then learning: DeepBach, a "
            "network that harmonizes chorales, in 2016, <bookmark mark='f'/> and the Music Transformer in 2018."
        ) as vo:
            self.play(FadeIn(head), Create(line))
            for mark, item in zip("abcdef", g):
                vo.wait_until(mark)
                self.play(FadeIn(item), run_time=0.6)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kinds(self):
        items = [
            (r"rules written by hand: \ the composer's knowledge, \ explicit; \ the machine only searches \ (Part 42)", WHITE),
            (r"chance shaped by a distribution: \ dice, \ urns, \ Xenakis's clouds", WHITE),
            (r"statistics learnt from music: \ what follows what, \ counted or fitted", WHITE),
            (r"the third kind learns from a corpus: \ it can only be as new as its model lets it be, \ and only as good as its corpus", TUNE),
        ]
        rows_scene(self, r"three kinds of machine", items,
                   "Three kinds of machine, then. <bookmark mark='b'/> Some follow rules written by hand: the composer's knowledge "
                   "made explicit, and the machine only searches, as in Part 42. <bookmark mark='c'/> Some shape chance with a "
                   "distribution: dice, urns, Xenakis's clouds. <bookmark mark='d'/> And some learn statistics from music, what "
                   "follows what, counted or fitted. <bookmark mark='e'/> This part is about the third kind. It learns from a "
                   "corpus, so it can only be as new as its model allows, and limited by its data, architecture and objective.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def corpus(self):
        d = load("corpus")
        c = clip("corpus.bach")
        rows_ = VGroup(
            label(rf"Bach's chorales in Part 17's table: \ {d['chorales']}", font_size=20, color=WHITE),
            label(rf"in major keys and in 4/4: \ {d['tunes']}, \ transposed to C; \ their soprano lines are the corpus", font_size=20, color=WHITE),
            label(rf"but only {d['hymn_tunes']} different hymn tunes: \ Bach harmonized many tunes more than once", font_size=20, color=EAR),
            label(rf"so split by tune: \ {d['train']} chorales to learn from, \ {d['test']} tunes never seen \ ({d['train_notes']:,} notes to learn from)", font_size=20, color=TUNE),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.6)
        head = label(r"the corpus", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        box = choice_boxes([rf"{bwv(d['example'])}, \ as Bach harmonized it"], width=5.2, height=0.8, size=18).move_to(UP * 2.0)
        with self.voiceover("The music to learn from: Bach's chorales, the hymns he harmonized for four voices. Here are the first two phrases of one held out from the melody generators."):
            self.play(FadeIn(head), FadeIn(box))
        with self.listen(c) as snd:
            window(snd, r"a chorale", kind="synthesized", detail=r"Bach, \ on Part 17's organ tones", corner=DL, tag_corner=DR)
            pulse(snd, box, 0.0, c.duration, buff=0.06)
        with self.voiceover(
            f"Part 17's table holds {say(d['chorales'])} chorales. <bookmark mark='a'/> The {say(d['tunes'])} in major keys and "
            "common time, transposed to C, give the corpus: their soprano lines, the hymn tunes. <bookmark mark='b'/> But "
            f"there are only {say(d['hymn_tunes'])} different tunes among them, because Bach set many tunes more than once. "
            "A test tune harmonized differently in the training set would be a test already seen. <bookmark mark='c'/> So the "
            f"split is by tune: {say(d['train'])} chorales to learn from, {say(d['test'])} tunes kept back, never seen in any "
            "harmonization."
        ) as vo:
            self.play(FadeIn(rows_[0]))
            for mark, r in zip("abc", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.6)
        self.clear_scene()
