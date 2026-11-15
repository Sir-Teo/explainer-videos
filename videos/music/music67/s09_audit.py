from __future__ import annotations

import numpy as np

from videos.music.music67.common import *  # noqa: F403


class Audit(SoundScene):
    def construct(self):
        chapter(self, 8, r"The series audits itself", r"Do this series' own verdicts survive a new seed?")
        self.idea()
        self.table()
        self.query()
        self.order()
        self.errata()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"every number in this series came from one run: \ one split, \ one seed, \ one stretch of music", WHITE),
            (r"a verdict that depends on the seed is not a verdict", WHITE),
            (r"so re-run five of them: \ Parts 61, \ 63, \ 64, \ 65 and 66", WHITE),
            (r"with new seeds and splits, \ and report the spread", TUNE),
        ]
        rows_scene(self, r"one run is not enough", items,
                   "Every number in this series came from one run: one split, one seed, one stretch of music. "
                   "<bookmark mark='c'/> A verdict that changes with the seed is not a verdict. <bookmark mark='d'/> So re-run five of "
                   "them: Part 61's pitch tracker, Part 63's fingerprinter, Part 64's median filter, Part 65's best order, and Part "
                   "66's watermark detector. "
                   "<bookmark mark='e'/> With new seeds and new splits, and report the spread.", marks="cde")

    # ------------------------------------------------------------------
    def table(self):
        d = load("audit")
        y, h, o, w = d["p61_yin_0db"], d["p64_hpss_tonal"], d["p65_best_order"], d["p66_false_alarms"]
        rows = [(r"Part 61: \ YIN's gross errors at 0 dB, \ 9\%", rf"{100 * y['lo']:.0f} to {100 * y['hi']:.0f}\% over 10 noises", r"holds", TUNE),
                (r"Part 64: \ median filtering, \ tonal stems 7.8 dB", rf"{h['lo']:.1f} to {h['hi']:.1f} dB over 3 stretches", r"holds", TUNE),
                (r"Part 65: \ order 2 predicts new tunes best", rf"best in {round(10 * o['share'])} of 10 splits; \ order 1 in the rest", r"weaker than said", EAR),
                (r"Part 66: \ a score above 5 means a mark", rf"{w['above5']} of 60 unmarked phrases above 5 \ (largest {w['max']:.1f})", r"holds", TUNE)]
        a63 = load("audit63")
        v63 = a63["values"]
        rows.insert(2, (r"Part 63: \ 61\% named at 0 dB in a bar", rf"{100 * min(v63):.0f} to {100 * max(v63):.0f}\% over 3 new noises", r"holds" if abs(np.mean(v63) - 0.61) < 0.08 else r"differs", TUNE if abs(np.mean(v63) - 0.61) < 0.08 else EAR))
        g = VGroup()
        for claim, spread, verdict, col in rows:
            g.add(VGroup(label(claim, font_size=17, color=WHITE), label(spread, font_size=17, color=GREY_A), label(verdict, font_size=18, color=col)))
        g.arrange(DOWN, buff=0.38)
        for r in g:
            r[0].set_x(-3.4)
            r[1].set_x(2.0)
            r[2].set_x(5.4)
        g.move_to(DOWN * 0.3)
        head = label(r"five verdicts, \ re-run", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here they are. <bookmark mark='a'/> Part 61 said YIN gets nine per cent of frames grossly wrong at nought decibels; "
            f"over ten new noises, {say(round(100 * y['lo']))} to {say(round(100 * y['hi']))} per cent. It holds, with a "
            f"spread worth stating. <bookmark mark='b'/> Part 64's median filter: {say(h['lo'], 1)} to {say(h['hi'], 1)} "
            "decibels over three stretches of the session; it holds. Part 63's fingerprinter, said to name sixty-one per cent "
            f"of queries level with a bar's noise: {say(round(100 * min(a63['values'])))} to {say(round(100 * max(a63['values'])))} "
            "per cent over three new noises. <bookmark mark='c'/> Part 65 said order two predicts new "
            f"tunes best. Over ten splits by tune it is best in {say(round(10 * o['share']))}, and order one in the rest: the "
            "claim was true for the split shown, and weaker than it sounded. <bookmark mark='d'/> Part 66's detector fired on "
            f"{say(w['above5'])} of sixty unmarked phrases; it holds."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abbcd", g):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def order(self):
        d = load("audit")["p65_best_order"]
        vals = d["values"]
        cells = VGroup(*[VGroup(Square(side_length=0.8, stroke_color=TUNE if v == 2 else EAR, fill_color=TUNE if v == 2 else EAR, fill_opacity=0.3),
                                label(str(v), font_size=22, color=WHITE)).arrange(ORIGIN) for v in vals]).arrange(RIGHT, buff=0.2).move_to(UP * 0.4)
        lab = label(r"the best order, \ split by split", font_size=17, color=GREY_A).next_to(cells, UP, buff=0.3)
        note = VGroup(label(rf"order 2's bits per note range from {d['bits2_lo']:.2f} to {d['bits2_hi']:.2f} across splits:", font_size=18, color=WHITE),
                      label(r"the split moves the score more than the order does", font_size=20, color=TUNE),
                      label(r"Part 65's README now says so", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.6)
        head = label(r"one verdict, \ looked at closely", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Look closer at the one that weakened. <bookmark mark='a'/> Split by split, the best order is two, two, one, two, "
            "and so on: order one and order two are close, and which wins depends on which tunes happen to be held out. "
            f"<bookmark mark='b'/> Order two's own score ranges from {say(d['bits2_lo'], 2)} to {say(d['bits2_hi'], 2)} bits "
            "across splits: the choice of test tunes moves the number more than the choice of order does. That is the "
            "ordinary situation in small-data research, and the fix is ordinary too: report the spread, not one run."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lab), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.1), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(note[:2]))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def errata(self):
        items = [
            (r"Part 61: \ a quantizer with one tempo put 1 of 14 rubato onsets right; \ replaced by one whose tempo drifts \ (14 of 14)", WHITE),
            (r"Part 63: \ a classifier split by excerpt looked better than chance; \ split by clip, \ it is at chance", WHITE),
            (r"Part 64: \ a network trained on phrases the test repeats; \ retrained without them, \ and the leak shown", WHITE),
            (r"Part 65: \ `order 2 is best' \ holds in 7 of 10 splits; \ the notes now give the spread", WHITE),
            (r"Part 38: \ a piano note's force stopped abruptly, \ a click; \ fixed, \ but earlier parts' stored sounds keep it", TUNE),
        ]
        rows_scene(self, r"errata", items,
                   "An honest audit ends in errata, and this series has some. <bookmark mark='b'/> In Part 61 a quantizer with one "
                   "tempo put one rubato onset in fourteen in the right place; it was replaced by one whose tempo may drift, which "
                   "puts all fourteen there. <bookmark mark='c'/> In Part 63 a classifier split by excerpt looked better than "
                   "chance; split by clip, it is at chance. <bookmark mark='d'/> In Part 64 a network was trained on phrases the "
                   "test repeats; it was retrained without them, and the leak is shown. <bookmark mark='e'/> Part 65's best order "
                   "holds in seven splits of ten, and its notes now give the spread. <bookmark mark='f'/> And Part 38's piano cut "
                   "each note's string force off abruptly, a faint click; it is fixed, but sounds stored by earlier parts keep it. "
                   "Every one was found by checking, not by luck.", marks="bcdef")

    # ------------------------------------------------------------------
    def query(self):
        d = load("auditheard")
        c = clip("audit.one")
        box = choice_boxes([r"a query, \ in new noise"], width=4.0, height=0.8, size=18).move_to(UP * 0.8)
        res = label((rf"named: \ {d['found'].split('/')[1]}" if d["ok"] else rf"missed: \ the best match was {d['found'].split('/')[1]}, \ with {d['votes']} votes"), font_size=19, color=TUNE if d["ok"] else EAR).next_to(box, DOWN, buff=0.7)
        head = label(r"one audited query, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is one of the audit's queries, a Variation in a new draw of the bar's noise, the music no louder than the noise."):
            self.play(FadeIn(head), FadeIn(box))
        with self.listen(c) as snd:
            window(snd, r"a query", kind="physical model", detail=r"Part 63's bar noise", corner=DL, tag_corner=DR)
            pulse(snd, box, 0.0, c.duration, buff=0.06)
        with self.voiceover(
            ("The fingerprinter named it. " if d["ok"] else f"This one was missed: the index's best guess, with {say(d['votes'])} votes, was another clip. ")
            + "An audit is made of cases like this one, many times over; a single case, right or wrong, shows only what one "
            "trial looks like."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()
