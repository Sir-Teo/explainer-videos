from __future__ import annotations

import numpy as np

from videos.music.music42.common import *  # noqa: F403

RULE_SHORT = {"range": r"range", "tritone": r"tritone", "seventh": r"seventh or wider", "repeat": r"three repeats",
              "recover": r"leap not recovered", "end": r"ending"}


class Illiac(SoundScene):
    def construct(self):
        chapter(self, 7, r"Generate and test: \ the \textit{Illiac Suite}", r"What did the first computer composer do?")
        self.history()
        self.rules()
        self.draws()
        self.hear()
        self.stats()
        self.experiments()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"Lejaren Hiller and Leonard Isaacson, \ University of Illinois, \ on the ILLIAC I computer", WHITE),
            (r"the \textit{Illiac Suite} for string quartet \ (1957): \ four `experiments', \ printed and played by humans", WHITE),
            (r"method: \ choose a note at random, \ test it against rules, \ keep it or draw again", WHITE),
            (r"published as \textit{Experimental Music} \ (1959): \ composing as choice among possibilities", TUNE),
            (r"the dice game reversed: \ the generator is dumb, \ the rules do the composing", GREY_A),
        ]
        rows_scene(self, r"Illinois, \ 1956 to 1957", items,
                   "In 1956 and 1957 Lejaren Hiller and Leonard Isaacson, at the University of Illinois, programmed the ILLIAC I "
                   "computer to compose. <bookmark mark='b'/> The result, the Illiac Suite for string quartet of 1957, has four "
                   "movements they called experiments, printed as a score and played by humans. <bookmark mark='c'/> The method: "
                   "choose a note at random, test it against rules, and keep it or draw again. <bookmark mark='d'/> Their book, "
                   "Experimental Music of 1959, describes composing as choice among possibilities. <bookmark mark='e'/> It is the "
                   "dice game reversed: the generator is dumb, and the rules do the composing.", marks="bcde")

    # ------------------------------------------------------------------
    def rules(self):
        d = load("illiac")
        rs = d["rules"]
        rows_ = text_rows([(rf"{k}: \ " + v, TUNE if k == "end" else WHITE) for k, v in rs.items()], font_size=23)
        head = label(r"our rules, \ in the spirit of the first experiment", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"each note is drawn from the eight white keys C4 to C5; \ after 50 failures in a row, \ the line backs up one note", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Their first experiment wrote short melodies like cantus firmi under rules from counterpoint. Ours are in the same "
            "spirit. Stay within an octave of middle C; no melodic tritone; no seventh or wider leap; no note three times "
            "running; after a leap larger than a fourth, a step back; and end on C, approached by step. Each note is drawn "
            "from the eight white keys of that octave, and after fifty failures in a row the line backs up one note."
        ):
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def draws(self):
        d = load("illiac")
        draws = d["draws"]
        nn = ["C", "D", "E", "F", "G", "A", "B"]
        def name(m):
            return nn[[0, 2, 4, 5, 7, 9, 11].index(m % 12)] + (r"$'$" if m >= 72 else "")
        cells = VGroup()
        for k, (m, why, pos) in enumerate(draws[:22]):
            ok = why is None
            col = TUNE if ok else GREY_D
            box = RoundedRectangle(width=1.05, height=0.62, corner_radius=0.08, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.15)
            t = label(name(m), font_size=20, color=WHITE if ok else GREY_B)
            w = label(r"kept" if ok else RULE_SHORT[why], font_size=11, color=TUNE if ok else EAR)
            cells.add(VGroup(box, VGroup(t, w).arrange(DOWN, buff=0.04).move_to(box)))
        cells.arrange_in_grid(rows=3, cols=8, buff=(0.22, 0.3)).move_to(UP * 0.1)
        line = label(r"the line: \ " + r" \ ".join(name(m) for m in d["line"]), font_size=22, color=TUNE).to_edge(DOWN, buff=0.9)
        head = label(r"one run, \ draw by draw", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        o = d["one"]
        with self.voiceover(
            "Watch one run, draw by draw. The line starts on C. Each box is a draw: gold if the note was kept, grey with the "
            f"rule it broke if not. <bookmark mark='a'/> This run needed {say(o['draws'])} draws for twelve notes, and most "
            "of its failures came at the very end, where only a C reached by step will do."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.15), run_time=4.0)
            vo.wait_until("a")
            self.play(FadeIn(line))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("illiac")
        c = clip("illiac.line")
        mel = [[m, float(i), 1.0 if i < len(d["line"]) - 1 else 2.0] for i, m in enumerate(d["line"])]
        g = scored(mel, None, width=10.0, height=2.0, lo=58, hi=74, bars=4, beats=4.0).move_to(UP * 0.3)
        head = label(r"the line, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"every note survived every rule: \ correct, \ and not much more", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover("Here is the line that survived."):
            self.play(FadeIn(head), FadeIn(g))
        with self.listen(c) as snd:
            window(snd, r"a line by generate and test", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g.roll.notes, [n[1] * 0.5 for n in mel], hot=WHITE, base=TUNE)
        with self.voiceover(
            "It breaks no rule. It is correct, and not much more: the rules say what to avoid, and nothing about what to aim "
            "for. That gap is what the critics of chapter nine try to fill."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stats(self):
        d = load("illiac")
        rej = d["rejected"]
        tot = sum(rej.values())
        order = sorted(rej, key=lambda k: -rej[k])
        x0, W = -2.0, 6.5
        mx = max(rej.values())
        bars = VGroup()
        for i, k in enumerate(order):
            w = W * rej[k] / mx
            y = 1.3 - 0.62 * i
            bars.add(VGroup(label(RULE_SHORT[k], font_size=19, color=WHITE).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT),
                            Rectangle(width=w, height=0.4, stroke_width=0, fill_color=EAR, fill_opacity=0.85).move_to([x0 + w / 2, y, 0]),
                            label(rf"{100 * rej[k] / tot:.0f}\%", font_size=17, color=WHITE).move_to([x0 + w + 0.4, y, 0])))
        head = label(rf"{d['runs']} runs: \ {d['mean_draws']:.0f} draws for twelve notes, \ on average", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"which rule rejected the draws: \ the ending dominates, \ then recovering from leaps", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            f"Run it {say(d['runs'])} times. <bookmark mark='a'/> On average a twelve-note line costs "
            f"{say(d['mean_draws'])} draws. The ending rejects the most, {say(100 * rej['end'] / tot)} per cent of all "
            "rejections, then the rule that a leap must be recovered. Blind generation wastes most of its effort on the few "
            "places where the rules are tight; better generators, like the dice game's table, put the knowledge in before "
            "the draw."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experiments(self):
        items = [
            (r"experiment 1: \ cantus firmi, \ then two and four voices in first-species counterpoint", WHITE),
            (r"experiment 2: \ four-part counterpoint, \ adding Fux's rules one by one", WHITE),
            (r"experiment 3: \ rhythm, \ dynamics and playing techniques; \ chromatic writing", WHITE),
            (r"experiment 4: \ Markov chains, \ each note chosen by probabilities that depend on the last", TUNE),
            (r"chapter 8: \ chains, \ grammars and evolution", GREY_A),
        ]
        rows_scene(self, r"the four experiments", items,
                   "The suite's four experiments climb in ambition. <bookmark mark='b'/> The first writes cantus firmi and then "
                   "two and four voices in first-species counterpoint. <bookmark mark='c'/> The second builds four-part "
                   "counterpoint, adding Fux's rules one at a time, so you can hear the music become more correct. "
                   "<bookmark mark='d'/> The third generates rhythms, dynamics and playing techniques, and chromatic writing. "
                   "<bookmark mark='e'/> And the fourth uses Markov chains: each note chosen by probabilities that depend on the "
                   "notes before. <bookmark mark='f'/> Chapter eight takes up chains, grammars and evolution.", marks="cdef")
