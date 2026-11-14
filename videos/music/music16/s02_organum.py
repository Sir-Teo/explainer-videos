from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403


class Organum(SoundScene):
    def construct(self):
        chapter(self, 1, r"One voice, \ made thicker", r"What did the first written polyphony want?", extra=((900, r"\textit{Musica enchiriadis}"),))
        self.history()
        self.listen_two()
        self.stages()
        self.after()

    # ------------------------------------------------------------------
    def history(self):
        card = history_card(900, r"\textit{Musica enchiriadis}, \ a handbook from northern France", r"a chant sung against itself, \ a fourth or a fifth below; \ the voices may be doubled at the octave", width=10.0, font_size=26).to_edge(UP, buff=0.4)
        names = VGroup(label(r"vox principalis: \ the chant", font_size=28, color=CF_C), label(r"vox organalis: \ the same, \ a fifth lower", font_size=28, color=UP_C)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 0.6)
        with self.voiceover(
            "The oldest surviving instructions for singing in more than one part come from a handbook "
            "written in northern France around the year 900, the Musica enchiriadis. It describes a "
            "practice called organum. <bookmark mark='a'/> One singer has the chant, the principal "
            "voice. A second sings the same chant, a fourth or a fifth lower, the organal voice, moving "
            "exactly with it. Then either voice may be doubled at the octave, for more singers."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(names))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listen_two(self):
        d = load("organum")
        c = clip("organum.two")
        b = d["beats"]
        on = np.concatenate([[0.0], np.cumsum(b)])[:-1]
        mk = lambda ps: [(p, a, w) for p, a, w in zip(ps, on, b)]               # noqa: E731
        g1 = duet([mk(d["tune"]), mk(d["fifth"])], colors=(CF_C, UP_C), width=5.4, height=3.0, lo=40, hi=82, thick=0.13).move_to(LEFT * 3.3 + DOWN * 0.2)
        g2 = duet([mk(v) for v in d["composite"]], colors=(UP_C, CF_C, UP_C, UP_C), width=5.4, height=3.0, lo=40, hi=82, thick=0.13).move_to(RIGHT * 3.3 + DOWN * 0.2)
        l1 = label(r"simple: \ a fifth below", font_size=26, color=GREY_A).next_to(g1, UP, buff=0.3)
        l2 = label(r"composite: \ doubled at the octaves", font_size=26, color=GREY_A).next_to(g2, UP, buff=0.3)
        with self.voiceover(
            "Here is the Tune's first phrase treated that way, on sustained organ tones. First the "
            "simple form, the Tune and a fifth below it. Then the composite form, with both voices "
            "doubled at the octave: four parts."
        ):
            self.play(FadeIn(g1), FadeIn(l1), FadeIn(g2), FadeIn(l2))
        with self.listen(c) as snd:
            window(snd, r"organum, \ simple and composite", kind="synthesized", detail=r"organ tones", corner=DL, tag_corner=DR)
            for j, nts in enumerate(g1.notes):
                sing_voice(snd, nts, d["times"]["simple"], base=(CF_C, UP_C)[j])
            for j, nts in enumerate(g2.notes):
                sing_voice(snd, nts, d["times"]["composite"], base=(UP_C, CF_C, UP_C, UP_C)[j])
            pulse(snd, l1, d["starts"]["simple"], d["starts"]["composite"] - 0.4, buff=0.1)
            pulse(snd, l2, d["starts"]["composite"], c.duration, buff=0.1)
        cap = label(r"four parts, \ and still one melody", font_size=32, color=TUNE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Four parts, and still one melody. That was the point. Organum did not want independence. "
            "It wanted a single line, made splendid: one voice for the whole church, as wide as the "
            "building. Parallel fifths and octaves were not a fault in it. They were the means, "
            "precisely because they fuse."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stages(self):
        d = load("more")["stages"]
        c = clip("more.stages")
        b = d["beats"]
        on = np.concatenate([[0.0], np.cumsum(b)])[:-1]
        mk = lambda ps: [(p, a, w) for p, a, w in zip(ps, on, b)]               # noqa: E731
        names = ("parallel", "oblique", "free")
        titles = {"parallel": r"about 900: \ parallel, \ a fifth below", "oblique": r"about 1026: \ at the fourth, \ never below C; \ meeting at the end",
                  "free": r"about 1100: \ free: \ against the chant"}
        rows = VGroup()
        for k, name in enumerate(names):
            g = duet([mk(d["tune"]), mk(d["voices"][name])], colors=(CF_C, UP_C), width=7.6, height=1.35, lo=51, hi=71, thick=0.11)
            ind = d["independence"][name]
            t = label(titles[name], font_size=22, color=GREY_A)
            m = VGroup(label(rf"fused: \ {100 * ind['fused']:.0f}\%", font_size=22, color=MOTION_C["parallel"] if ind["fused"] > 0 else GREY_B),
                       label(rf"contrary: \ {100 * ind['contrary']:.0f}\%", font_size=22, color=MOTION_C["contrary"] if ind["contrary"] > 0 else GREY_B)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            row = VGroup(t, g, m)
            g.move_to(LEFT * 1.3 + UP * (2.05 - 2.25 * k))
            t.next_to(g, UP, buff=0.12).align_to(g, LEFT)
            m.next_to(g, RIGHT, buff=0.5)
            rows.add(row)
        with self.voiceover(
            "Hear how the second voice won its freedom, on the whole Tune. <bookmark mark='a'/> First, "
            "parallel organum at the fifth, as in the handbook. <bookmark mark='b'/> Then the kind the "
            "handbook itself prefers for the fourth, and Guido describes: the organal voice may not go "
            "below a boundary note, here C, so at the start it waits on C while the chant rises, follows "
            "in parallel fourths, and at the end holds C again until the chant comes down to meet it in "
            "a unison. <bookmark mark='c'/> Then free organum, as in a treatise of about 1100: here "
            "every interval is still an octave, fifth, fourth or unison, as most were then, but the "
            "organal voice moves against the chant wherever it can. Monochord chose that voice by dynamic programming, rewarding contrary motion."
        ) as vo:
            for mark, row in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(row[0]), FadeIn(row[1]))
        with self.listen(c) as snd:
            window(snd, r"parallel, \ oblique, \ free", kind="synthesized", detail=r"organ tones", corner=DL, tag_corner=DR)
            for k, name in enumerate(names):
                g = rows[k][1]
                for j, nts in enumerate(g.notes):
                    sing_voice(snd, nts, d["times"][name][j], base=(CF_C, UP_C)[j])
                pulse(snd, rows[k][0], d["starts"][name], d["starts"][names[k + 1]] - 0.4 if k < 2 else c.duration, buff=0.08)
        f, o, fr = (d["independence"][n] for n in names)
        with self.voiceover(
            f"Measure each the way this part will measure everything: at each move, are the voices "
            f"moving together onto a fused interval, and are they moving in opposite directions? "
            f"Parallel organum: fused at every move, contrary at none. The oblique kind: fused at "
            f"{say(100 * o['fused'])} moves in a hundred, the rest standing still. Free organum: never "
            f"fused, and contrary {say(100 * fr['contrary'])} times in a hundred, using only the "
            "intervals that fuse most. It is the first sign of the rule Fux would write down: perfect "
            "intervals are safe only if the voices reach them from opposite directions."
        ):
            self.play(LaggedStart(*[FadeIn(r[2]) for r in rows], lag_ratio=0.4), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def after(self):
        steps = VGroup(label(r"about 1026: \ Guido of Arezzo prefers the voices to meet at the ends of phrases", font_size=26, color=WHITE),
                       label(r"about 1100: \ free organum: \ the voices move in contrary motion", font_size=26, color=WHITE),
                       label(r"about 1200: \ Notre-Dame: \ a fast new voice over long notes of chant \ (Part 23)", font_size=26, color=WHITE),
                       label(r"by 1500: \ parallel fifths and octaves avoided", font_size=26, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.2)
        cap = label(r"the change was in what the music wanted", font_size=30, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "So over the next five centuries the goal changed. <bookmark mark='a'/> Around 1026 Guido "
            "of Arezzo, whom Part 10 met inventing the staff, wanted the voices to come back together at "
            "the ends of phrases. <bookmark mark='b'/> By about 1100, in free organum, the voices move "
            "against each other. "
            "<bookmark mark='c'/> By about 1200, in Paris, a new voice runs freely over the long held "
            "notes of a chant: Part 23 tells that story. <bookmark mark='d'/> And by about 1500, "
            "composers were avoiding exactly what organum had been built on. The ear had not changed. "
            "What the music wanted had: two voices, heard as two."
        ) as vo:
            for mark, s in zip("abcd", steps):
                vo.wait_until(mark)
                self.play(FadeIn(s))
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
