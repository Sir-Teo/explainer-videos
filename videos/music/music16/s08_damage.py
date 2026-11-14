from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403


class Damage(SoundScene):
    def construct(self):
        chapter(self, 7, r"Remove a rule", r"What goes wrong without each rule?")
        self.table()
        self.hear()

    # ------------------------------------------------------------------
    def table(self):
        d = load("damage")
        rows = {r["rule"]: r for r in d["rows"]}
        show = [("consonance", "dissonant", r"dissonant notes against the cantus"), ("direct", "fused", r"fused moments: \ perfect intervals reached together"),
                ("melodic", "big", r"leaps larger than a fifth"), ("recovery", "move", r"average move, \ in semitones"), ("unison", "unison", r"unisons in the middle"),
                ("repeat", "move", r"average move \ (repeated notes count as none)")]
        head = VGroup(label(r"rule removed", font_size=22, color=GREY_B), label(r"lines", font_size=22, color=GREY_B), label(r"what goes wrong in them, \ measured", font_size=22, color=GREY_B),
                      label(r"with", font_size=22, color=GREY_B), label(r"without", font_size=22, color=GREY_B))
        xs = (-6.4, -3.0, -1.6, 4.4, 5.6)
        for h, x in zip(head, xs):
            h.move_to([x, 2.7, 0], aligned_edge=LEFT)
        table = VGroup()
        for k, (rule, key, what) in enumerate(show):
            r = rows[rule]
            y = 2.0 - 0.75 * k
            fmt = (lambda v: f"{100 * v:.0f}\\%") if key != "move" else (lambda v: f"{v:.1f}")
            table.add(VGroup(label(rule, font_size=26, color=TUNE).move_to([xs[0], y, 0], aligned_edge=LEFT),
                             label(rf"$\times {r['factor']:.0f}$" if r["factor"] >= 2 else rf"$\times {r['factor']:.1f}$", font_size=24, color=WHITE).move_to([xs[1], y, 0], aligned_edge=LEFT),
                             label(what, font_size=20, color=GREY_A).move_to([xs[2], y, 0], aligned_edge=LEFT),
                             label(fmt(d["base"][key]), font_size=24, color=GREY_A).move_to([xs[3], y, 0], aligned_edge=LEFT),
                             label(fmt(r[key]), font_size=24, color=EAR).move_to([xs[4], y, 0], aligned_edge=LEFT)))
        with self.voiceover(
            "Now take the rules away one at a time, and measure the damage. For each rule, count the "
            "lines that obey all the others, draw three hundred of them at random, and measure what "
            "has gone wrong in them. <bookmark mark='a'/> Without the rule of consonance there are a "
            f"hundred and eighty times as many lines, and {say(100 * rows['consonance']['dissonant'])} "
            "notes in a hundred clash with the cantus. <bookmark mark='b'/> Without the rule against "
            f"similar motion into perfect intervals, {say(100 * rows['direct']['fused'])} moves in a "
            "hundred land on a fused interval with both voices moving together: the organum effect "
            "returns. <bookmark mark='c'/> Without the rules of melody, leaps larger than a fifth "
            f"triple. Without the rule of recovery, the line wanders: its moves grow. Without the rule "
            "against unisons, the two voices meet in the middle and vanish into each other. Each rule "
            "repairs one specific way of losing a voice."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(table[0]))
            vo.wait_until("b")
            self.play(FadeIn(table[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in table[2:]], lag_ratio=0.5), run_time=4.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("damage")
        c = clip("damage.broken")
        cfn = load("fux")["cf"]
        cf = [(p, 4.0 * k, 4.0) for k, p in enumerate(cfn)]
        g1 = duet([[(p, 4.0 * k, 4.0) for k, p in enumerate(d["direct_line"])], cf], width=5.4, height=2.6, lo=58, hi=82, thick=0.13, bar=4.0).move_to(LEFT * 3.3 + UP * 0.2)
        g2 = duet([[(p, 4.0 * k, 4.0) for k, p in enumerate(d["dissonant_line"])], cf], width=5.4, height=2.6, lo=58, hi=82, thick=0.13, bar=4.0).move_to(RIGHT * 3.3 + UP * 0.2)
        l1 = label(r"without the rule on similar motion", font_size=24, color=GREY_A).next_to(g1, UP, buff=0.25)
        l2 = label(r"without the rule of consonance", font_size=24, color=GREY_A).next_to(g2, UP, buff=0.25)
        la = label(r"A", font_size=40, color=GREY_A).next_to(g1, UP, buff=0.25)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(g2, UP, buff=0.25)
        card = listen_card(r"Two lines over Fux's cantus, \ each obeying every rule but one. \ One clashes; \ in the other the voices merge for a moment. \ Which clashes: \ A or B?", width=10.0)
        with self.voiceover(
            "Hear two of them. Each obeys every rule but one. In one, some notes clash with the cantus; "
            "in the other, the two voices arrive together on an octave or a fifth. Which one clashes, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        self.play(FadeOut(card), FadeIn(g1), FadeIn(la), FadeIn(g2), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing_voice(snd, g1.notes[0], d["times"]["direct"][0], base=UP_C)
            sing_voice(snd, g2.notes[0], d["times"]["dissonant"][0], base=UP_C)
            pulse(snd, la, d["starts"]["direct"], d["starts"]["dissonant"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["dissonant"], c.duration, buff=0.1)
        for k in d["direct_at"]:
            g1.notes[0][k].set_fill(EAR)
        for k in d["dissonant_at"]:
            g2.notes[0][k].set_fill(EAR)
        with self.voiceover(
            "B clashes: it breaks the rule of consonance, at the pink notes. A breaks the rule on "
            "similar motion, and at its pink notes the two voices fuse."
        ):
            self.play(ReplacementTransform(la, l1), ReplacementTransform(lb, l2), *[Indicate(g1.notes[0][k], color=EAR) for k in d["direct_at"]],
                      *[Indicate(g2.notes[0][k], color=EAR) for k in d["dissonant_at"]])
        with self.voiceover(
            "Neither is a catastrophe. A loses its independence for a moment, twice, as the "
            "voices arrive together on an octave or a fifth. B is harsher, and in a style "
            "where every note is held for a whole bar, the clashes have nowhere to go. In the species "
            "that follow, dissonance comes back, on purpose, in places where it can go somewhere."
        ):
            self.wait(0.2)
        self.wait(0.4)
        self.clear_scene()
