from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403

A_COL, B_COL = "#F28FB8", "#7EC8F5"
KIND = {0: GREY_C, 1: A_COL, 2: THRESH, 3: GREY_B}


class Logic(VoiceoverScene):
    def construct(self):
        self.card()
        self.single()
        self.double()
        self.noise()
        self.licence()

    def card(self):
        card = chapter_card(4, r"The logic of dissociation", r"When does damage show that two things are separate?",
                            lit=(), part=PART, scale=("brain", "mind"), marr=("how",))
        with self.voiceover(
            "Chapter four. The logic of dissociation."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _curves(self, d, center, x_length=6.4):
        A = axes([0, 1], [0, 1.05], x_length=x_length, y_length=3.9, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{100 * v:.0f}", yfmt=lambda v: f"{v:.1f}",
                 xlabel=r"how much of the one resource the lesion leaves (\%)", ylabel=r"score", center=center)
        ax = A.ax
        ca = curve(ax, d["resource"], d["curve_a"], A_COL, stroke_width=4)
        cb = curve(ax, d["resource"], d["curve_b"], B_COL, stroke_width=4)
        la = label(r"task A", font_size=26, color=A_COL).next_to(ax.c2p(0.66, 0.82), RIGHT, buff=0.1)
        lb = label(r"task B", font_size=26, color=B_COL).next_to(ax.c2p(0.3, 0.42), LEFT, buff=0.15)
        return A, ax, ca, cb, la, lb

    def single(self):
        d = load("dissociation")
        head = heading(r"One patient fails A and passes B. \ What follows?")
        A, ax, ca, cb, la, lb = self._curves(d, [-3.2, -0.6, 0])
        r0 = 0.45
        ia, ib = (float(np.interp(r0, d["resource"], d[k])) for k in ("curve_a", "curve_b"))
        patient = VGroup(DashedLine(ax.c2p(r0, 0), ax.c2p(r0, 1.05), color=THRESH, stroke_width=2.5),
                         Dot(ax.c2p(r0, ia), radius=0.1, color=A_COL), Dot(ax.c2p(r0, ib), radius=0.1, color=B_COL),
                         label(r"this patient", font_size=22, color=THRESH).next_to(ax.c2p(r0, 1.05), UP, buff=0.05))
        side = VGroup(
            wrapped_label(r"the tempting reading: \ A and B are done by different parts, \ and the part for A "
                          r"is damaged", 5.6, 30, WHITE),
            wrapped_label(r"another reading: \ one part does both, \ and A needs more of it", 5.6, 30, P.ACCENT),
            wrapped_label(rf"here the patient scores {r2(ia)} on A and {r2(ib)} on B, \ with one resource", 5.6, 30,
                          THRESH),
            wrapped_label(r"A single dissociation cannot tell the two readings apart.", 5.6, 31, LESION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([3.95, -0.3, 0])
        keep_in_frame(side)
        tag = psyche_tag()
        # the case, before any theory: two tasks and one patient's scores
        case = VGroup()
        for name, v, col, word in ((r"task A: \ recognizing faces", 0.2, A_COL, r"impaired"),
                                   (r"task B: \ recognizing objects", 0.8, B_COL, r"normal")):
            case.add(VGroup(label(name, font_size=32, color=col), score_bar(v, col, 3.6, 0.45),
                            label(word, font_size=28, color=LESION if v < 0.5 else SPARED)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.14))
        case.arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([-3.6, -0.3, 0])
        with self.voiceover(
            "Let's make the reasoning exact. A patient with brain damage does badly on task A and normally on "
            "task B. Say A is recognizing faces, and B is recognizing objects. <bookmark mark='a'/> The "
            "tempting reading is that faces and objects are handled by different parts of the brain, and the "
            "part for faces is damaged. <bookmark mark='b'/> Here's another reading. One part does both "
            "jobs, and faces simply need more of it. Draw each task's score against how much of that single "
            "resource a lesion leaves. Task A falls off first. <bookmark mark='c'/> Now take a patient who "
            f"has lost about half. They score {ia:.2f} on A and {ib:.2f} on B. Impaired on one task, "
            "nearly normal on the other, and there's only one resource in this model. <bookmark mark='d'/> "
            "So a single dissociation can't tell you that two functions are separate. It may only tell you "
            "that one task is harder than the other. Half of the claims you'll read about what some brain "
            "region is for rest on exactly this pattern."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.15) for c_ in case], lag_ratio=0.8), run_time=4.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeOut(case), FadeIn(side[1]))
            self.play(FadeIn(A))
            self.play(Create(cb), FadeIn(lb), Create(ca), FadeIn(la), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(patient), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()

    def double(self):
        d = load("dissociation")
        head = heading(r"A second patient, with the opposite pattern")
        A, ax, ca, cb, la, lb = self._curves(d, [-3.2, -0.6, 0])
        band = Rectangle(width=np.linalg.norm(ax.c2p(1, 0) - ax.c2p(0, 0)), height=0.5, stroke_width=0,
                         fill_color=LESION, fill_opacity=0.0)
        table = VGroup()
        colx = [1.6, 3.9, 5.9]
        for j, h in enumerate([r"", r"task A", r"task B"]):
            table.add(label(h, font_size=31, color=[WHITE, A_COL, B_COL][j]).move_to([colx[j], 1.6, 0]))
        for i, (name, cells) in enumerate(((r"patient 1", (False, True)), (r"patient 2", (True, False)))):
            y = 0.85 - 0.8 * i
            table.add(label(name, font_size=32, color=WHITE).move_to([colx[0], y, 0]))
            for j, ok in enumerate(cells):
                table.add(label(r"normal" if ok else r"impaired", font_size=32, color=SPARED if ok else LESION).move_to(
                    [colx[j + 1], y, 0]))
        keep_in_frame(table)
        notes = VGroup(
            wrapped_label(r"On these curves B is never below A. \ No amount of one resource gives patient 2.", 5.8,
                          30, P.ACCENT),
            wrapped_label(r"So there are at least two resources, \ and each can be damaged without the other: \ a "
                          r"double dissociation.", 5.8, 30, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.95, -1.75, 0])
        keep_in_frame(notes)
        tag = psyche_tag()
        with self.voiceover(
            "What would settle it? <bookmark mark='a'/> A second patient, with the opposite pattern. "
            "Impaired on B, and normal on A. <bookmark mark='b'/> Look at the curves again. In a "
            "one-resource world, B is the easier task at every level of damage. There's no amount of the "
            "resource that leaves you worse at B than at A. So the second patient is impossible. "
            "<bookmark mark='c'/> If you find one, the one-resource account is dead. There must be at least "
            "two resources, and each can be damaged without the other. That's a double dissociation, and "
            "it's exactly what Broca's and Wernicke's patients gave us for speaking and understanding. It's "
            "the strongest argument that damage can make. And notice what kind of argument it is. It tests a "
            "diagram of the mind. It says nothing yet about where in the brain anything is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(VGroup(ca, cb, la, lb)))
            vo.wait_until("a")
            self.play(FadeIn(table, lag_ratio=0.1), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), Indicate(cb, color=WHITE, scale_factor=1.02))
            vo.wait_until("c")
            self.play(FadeIn(notes[1], shift=UP * 0.1))
        self.clear_scene()

    def noise(self):
        d = load("dissociation")
        k = int(np.argmin(np.abs(d["noises"] - 0.05)))
        head = heading(r"Now make the tests as noisy as real tests are")
        A = axes([0, 1.15], [0, 1.15], x_length=4.7, y_length=4.7, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"score on task A",
                 ylabel=r"score on task B", center=[-4.25, -0.6, 0])
        ax = A.ax
        pts = d["cloud_one"]
        kinds = d["cloud_one_kind"]
        dots = VGroup(*[Dot(ax.c2p(float(np.clip(a, 0, 1.15)), float(np.clip(b, 0, 1.15))), radius=0.04 if kk != 2 else 0.09,
                            color=KIND[int(kk)], fill_opacity=0.8) for (a, b), kk in zip(pts, kinds)])
        cuts = VGroup(DashedLine(ax.c2p(d["cut_a"], 0), ax.c2p(d["cut_a"], 1.15), color=A_COL, stroke_width=2),
                      DashedLine(ax.c2p(0, d["cut_b"]), ax.c2p(1.15, d["cut_b"]), color=B_COL, stroke_width=2))
        corner = label(r"B impaired, A normal", font_size=22, color=THRESH).move_to(ax.c2p(0.98, 0.4))
        B = axes([0, 200], [0, 1.05], x_length=5.6, y_length=2.5, xticks=[0, 50, 100, 150, 200], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"patients screened", ylabel=r"chance of finding both patterns",
                 center=[2.9, -0.2, 0])
        bx = B.ax
        n = d["screened"]
        c_quiet = curve(bx, n, d["chance_quiet"], GREY_B, stroke_width=3)
        c_typ = curve(bx, n, d["chance_typical"], THRESH, stroke_width=4)
        c_noisy = curve(bx, n, d["chance_noisy"], LESION, stroke_width=3)
        lg = legend([(LESION, r"tests twice as noisy"), (THRESH, r"tests as noisy as controls vary"),
                     (GREY_B, r"perfect tests")], font_size=21)
        lg.next_to(bx.c2p(200, 0.04), UL, buff=0.08)
        at100 = float(d["chance_typical"][99])
        side = VGroup(
            wrapped_label(rf"one resource, 300 patients: \ {pct(d['one_a_only'][k])} fail only A; \ "
                          rf"{pct(d['one_b_only'][k], 1)} fail only B", 6.6, 28, WHITE),
            wrapped_label(rf"screen 100 patients: \ a {pct(at100)} chance of a ``double dissociation'' that is "
                          r"not there", 6.6, 27, THRESH),
            wrapped_label(r"and it is the striking case that gets written up", 6.6, 27, P.ACCENT),
        )
        side[0].move_to([3.1, 2.35, 0])
        side[1].move_to([3.1, -2.5, 0])
        side[2].next_to(side[1], DOWN, buff=0.15).align_to(side[1], LEFT)
        keep_in_frame(side)
        tag = psyche_tag(r"simulated patients: Psyche")
        with self.voiceover(
            "That argument assumed something we should doubt after Part 3: that a test score is the truth. "
            "It isn't. A patient tested on a bad morning scores lower. <bookmark mark='a'/> So here is the "
            "one-resource model again, with three hundred simulated patients, and tests whose error is as "
            "large as the spread among healthy people. Each dot is a patient: the score on A across, the "
            "score on B upwards. The dashed lines are the cutoffs for impaired. <bookmark mark='b'/> Most "
            "patients behave. But a few land in the forbidden corner: impaired on B, normal on A. They "
            f"aren't real. They're noise. Only {100 * d['one_b_only'][k]:.1f} percent of patients, in the "
            "long run. <bookmark mark='c'/> But neuropsychologists don't see one patient. A clinic sees "
            "hundreds. Screen a hundred patients from this one-resource world, and the chance that you find "
            f"both patterns is {100 * at100:.0f} percent. With noisier tests it's nearly certain. "
            "<bookmark mark='d'/> And which patients get written up in a journal? The striking ones. You've "
            "seen this before. It's Part 4's file drawer, with patients in place of studies. A double "
            "dissociation found by searching is not the same as one that was predicted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(A), Create(cuts), FadeIn(dots, lag_ratio=0.005), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(corner), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(B), FadeIn(lg))
            self.play(Create(c_quiet), Create(c_typ), Create(c_noisy), run_time=4.0)
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()

    def licence(self):
        head = heading(r"What each pattern lets you say")
        rows = VGroup(
            VGroup(label(r"a single dissociation", font_size=36, color=A_COL),
                   wrapped_label(r"one task may only be harder. \ Nothing yet about separate parts.", 12.4, 31,
                                 WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"a double dissociation", font_size=36, color=B_COL),
                   wrapped_label(r"at least two resources, \ if the tests are reliable, the difference is large, "
                                 r"and the reverse case has been found more than once", 12.4, 31, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"a lesion and a loss", font_size=36, color=LESION),
                   wrapped_label(r"the damaged tissue was \emph{needed} for the task. \ It does not follow that the "
                                 r"task is done there, or only there.", 12.4, 31, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"and always", font_size=36, color=P.ACCENT),
                   wrapped_label(r"the answer depends on the task you chose. \ Lashley's maze and Broca's patient "
                                 r"were both real.", 12.4, 31, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.35, 0])
        with self.voiceover(
            "So here are the rules, and we'll use them for the rest of this part. <bookmark mark='a'/> A "
            "single dissociation. One task may simply be harder. It tells you nothing yet about separate "
            "parts. <bookmark mark='b'/> A double dissociation. At least two resources, provided the tests "
            "are reliable, the differences are large and not just either side of a cutoff, and the reverse "
            "case has turned up more than once. <bookmark mark='c'/> A lesion together with a loss. The "
            "damaged tissue was needed for the task. That's necessity. It doesn't follow that the task is "
            "done there, or only there. Cut the power cable and the radio stops. The music wasn't in the "
            "cable. <bookmark mark='d'/> And always, the answer depends on the task you chose. Lashley's "
            "maze and Broca's patient were both real. One task could be done six ways, and one couldn't."
        ) as vo:
            self.play(FadeIn(head))
            for k, mark_ in enumerate("abcd"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()
