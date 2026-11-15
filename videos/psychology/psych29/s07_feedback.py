from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Feedback(VoiceoverScene):
    def construct(self):
        self.card()
        self.pen()
        self.rrr()
        self.meta()
        self.groups()
        self.smiles()

    def card(self):
        card = chapter_card(6, r"Facial feedback", r"Does smiling make you happier?",
                            lit={1988: r"Strack et al.", 2016: r"Wagenmakers et al.", 2018: r"Noah et al.",
                                 2019: r"Coles et al.", 2022: r"Many Smiles"},
                            part=PART, scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter six. Facial feedback."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def pen(self):
        head = heading(r"A pen held two ways")
        teeth = VGroup(face(0.55, 0.0, color=PLEAS, radius=0.7),
                       Line([-0.9, -0.28, 0], [0.9, -0.28, 0], color=COG, stroke_width=7))
        lips = VGroup(face(-0.35, -0.2, color=UNPL, radius=0.7),
                      Line([0, -0.25, 0], [0, -1.3, 0], color=COG, stroke_width=7))
        VGroup(teeth, lips).arrange(RIGHT, buff=1.6).move_to([-3.4, 0.5, 0])
        tl = label(r"in the teeth: \ a smile", font_size=19, color=PLEAS).next_to(teeth, DOWN, buff=0.35)
        ll = label(r"in the lips: \ a pout", font_size=19, color=UNPL).next_to(lips, DOWN, buff=0.35)
        rows = rows_of([
            (r"Fritz Strack, \ Leonard Martin and Sabine Stepper, \ 1988: \ a cover story about writing without "
             r"hands", WHITE),
            (r"holding the pen in the teeth forces the muscles of a smile; \ in the lips, \ it prevents them", COG),
            (r"while holding it, \ people rated cartoons from \emph{The Far Side}", FACE),
            (r"teeth: \ cartoons rated 0.82 points funnier on a 10-point scale", PLEAS),
        ], 5.6, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Strack, \ Martin \& Stepper (1988)")
        with self.voiceover(
            "If the body shapes feeling, then the face should too. <bookmark mark='a'/> In 1988 Fritz Strack, "
            "Leonard Martin and Sabine Stepper gave people a cover story about learning to write without hands. "
            "<bookmark mark='b'/> Holding a pen in the teeth forces the muscles of a smile; holding it in the lips "
            "prevents them. Nobody is told to smile. <bookmark mark='c'/> While holding the pen, people rated how "
            "funny cartoons from The Far Side were. <bookmark mark='d'/> With the pen in the teeth, the cartoons were "
            "rated 0.82 points funnier on a ten-point scale. It became one of the most cited demonstrations in "
            "psychology."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(teeth), FadeIn(lips), FadeIn(tl), FadeIn(ll))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def rrr(self):
        head = heading(r"Seventeen laboratories, \ 2016")
        A = axes([-0.4, 1.4], [0, 3], x_length=8.0, y_length=2.4, xticks=[0, 0.5, 1.0],
                 yticks=None, xfmt=lambda v: f"{v:g}", xlabel=r"how much funnier with the pen in the teeth \ "
                 r"(points of 10)", center=[0, 0.6, 0], font_size=16)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, 3), color=GREY_B, stroke_width=2)
        orig = Dot(A.ax.c2p(0.82, 2.2), radius=0.09, color=FACE)
        ol = label(r"1988: \ 0.82", font_size=18, color=FACE).next_to(orig, UP, buff=0.1)
        rep = VGroup(Line(A.ax.c2p(-0.11, 0.9), A.ax.c2p(0.16, 0.9), color=UNPL, stroke_width=4),
                     Dot(A.ax.c2p(0.03, 0.9), radius=0.09, color=UNPL))
        rl = label(r"2016, \ 17 laboratories: \ 0.03 \ [$-0.11$, \ 0.16]", font_size=18, color=UNPL).next_to(
            rep, UP, buff=0.12)
        rows = rows_of([
            (r"a Registered Replication Report led by Eric-Jan Wagenmakers: \ the same procedure, \ agreed with "
             r"Strack beforehand, \ in 17 laboratories", WHITE),
            (r"nine laboratories found a difference in the original direction, \ eight in the other; \ pooled, \ "
             r"essentially zero", UNPL),
            (r"Strack's objection: \ the replications filmed participants, \ and the cartoons were older", COG),
            (r"2018: \ Tom Noah, \ Yaacov Schul and Ruth Mayo tested exactly that; \ the effect appeared without "
             r"a camera, \ and vanished with one", FACE),
        ], 12.0, 22, 0.3).move_to([0, -2.1, 0])
        tag = published_tag(r"Wagenmakers et al.\ (2016); \ Noah, \ Schul \& Mayo (2018)")
        with self.voiceover(
            "In 2016 it was tested by seventeen laboratories at once. <bookmark mark='a'/> Eric-Jan Wagenmakers led "
            "a Registered Replication Report: the same procedure, agreed with Strack beforehand, in seventeen "
            "laboratories. <bookmark mark='b'/> Nine found a difference in the original direction and eight in the "
            "other. Pooled, the difference was 0.03 points, with an interval from minus 0.11 to 0.16: essentially "
            "zero, against the original 0.82. <bookmark mark='c'/> Strack objected that the replications had filmed "
            "participants, which the original had not, and used cartoons that had aged. "
            "<bookmark mark='d'/> In 2018 Tom Noah, Yaacov Schul and Ruth Mayo tested exactly that. The effect "
            "appeared without a camera, and vanished when people knew they were being filmed. That needs its own "
            "replication, but it is a lesson in how small details can carry an effect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero), FadeIn(orig), FadeIn(ol))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rep), FadeIn(rl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def meta(self):
        d = load("feedback")
        head = heading(r"Every study at once")
        k = d["k_studies"]
        A = axes([-1.5, 2.5], [0, k + 6], x_length=6.6, y_length=5.6, xticks=[-1, 0, 1, 2], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"Cohen's $d$, \ study by study", center=[-2.8, -0.35, 0],
                 font_size=15)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, k + 6), color=GREY_B, stroke_width=2)
        lines = VGroup()
        for i, (g, se) in enumerate(zip(d["g"], d["se"])):
            y = i + 5
            lo, hi = max(g - 1.96 * se, -1.5), min(g + 1.96 * se, 2.5)
            lines.add(Line(A.ax.c2p(lo, y), A.ax.c2p(hi, y), color=FACE, stroke_width=1, stroke_opacity=0.6))
            lines.add(Dot(A.ax.c2p(float(g), y), radius=0.025, color=FACE))
        dy = 2.0
        diamond = Polygon(A.ax.c2p(d["re_lo"], dy), A.ax.c2p(d["re"], dy + 1.6), A.ax.c2p(d["re_hi"], dy),
                          A.ax.c2p(d["re"], dy - 1.6), color=PLEAS, fill_opacity=0.9, stroke_width=0)
        rows = rows_of([
            (rf"Nicholas Coles, \ Jeff Larsen and Heather Lench, \ 2019: \ {d['k_effects']} effect sizes from "
             rf"{k} studies, \ published and unpublished", WHITE),
            (r"Psyche reads their table and pools each study's effects, \ then the studies", MODEL),
            (rf"pooled: \ $d = {d['re']:.2f}$ \ [{d['re_lo']:.2f}, \ {d['re_hi']:.2f}]: \ small, \ and real", PLEAS),
            (rf"and variable: \ $I^2 = {100 * d['I2']:.0f}\%$ of the spread is between studies, \ not chance",
             COG),
        ], 4.8, 20, 0.3).move_to([4.2, -0.1, 0])
        tag = published_tag(r"data: Coles, \ Larsen \& Lench (2019), \ recomputed")
        with self.voiceover(
            "One replication tests one procedure. A meta-analysis tests the idea. <bookmark mark='a'/> In 2019 "
            f"Nicholas Coles, Jeff Larsen and Heather Lench gathered {d['k_effects']} effect sizes from {k} studies "
            "of facial feedback, published and unpublished, and released their table. <bookmark mark='b'/> Psyche "
            "reads it, pools each study's effects, and then pools the studies; each line here is one study. "
            f"<bookmark mark='c'/> The pooled effect is a d of {d['re']:.2f}, with an interval from "
            f"{d['re_lo']:.2f} to {d['re_hi']:.2f}: small, and real. <bookmark mark='d'/> And variable: "
            f"{100 * d['I2']:.0f} percent of the spread is between studies rather than chance. Where it comes from "
            "is the next question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in lines], lag_ratio=0.005), FadeIn(rows[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(diamond, scale=0.5), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def groups(self):
        d = load("feedback")
        head = heading(r"Where the effect lives")
        names = d["group_names"]
        n = len(names)
        A = axes([-0.2, 0.7], [0, n + 2.5], x_length=5.2, y_length=4.2, xticks=[0, 0.2, 0.4, 0.6], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"pooled $d$, \ 95\% interval", center=[-0.8, -0.2, 0],
                 font_size=15)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, n + 2.5), color=GREY_B, stroke_width=2)
        rowsg = VGroup()
        for i, (nm, kk, e, lo, hi) in enumerate(zip(names, d["group_k"], d["group_est"], d["group_lo"],
                                                    d["group_hi"])):
            y = n - i + 1.5
            col = PLEAS if e > 0.3 else COG
            ln = Line(A.ax.c2p(max(lo, -0.2), y), A.ax.c2p(min(hi, 0.7), y), color=col, stroke_width=4)
            dt = Dot(A.ax.c2p(e, y), radius=0.08, color=col)
            t = label(rf"{nm} \ ({kk})", font_size=17, color=col).next_to(A.ax.c2p(-0.2, y), LEFT, buff=0.2)
            rowsg.add(VGroup(ln, dt, t))
        pub = rows_of([
            (rf"published: \ $d = {d['pub']:.2f}$; \ unpublished: \ $d = {d['unpub']:.2f}$", UNPL),
            (r"a contrast can belong to two groups: \ suppressing one face against posing another", GREY_B),
        ], 4.0, 19, 0.25).move_to([4.9, -1.6, 0])
        rows = rows_of([
            (r"posing an expression on purpose has the largest effect", PLEAS),
            (r"unobtrusive manipulations, \ like the pen, \ are smaller", COG),
        ], 4.0, 20, 0.3).move_to([4.9, 1.0, 0])
        tag = published_tag(r"data: Coles, \ Larsen \& Lench (2019), \ recomputed")
        with self.voiceover(
            "Split the effects by how the face was moved. <bookmark mark='a'/> Posing an expression on purpose has "
            f"the largest effect, about {d['group_est'][0]:.2f}. Suppressing or exaggerating one, and unobtrusive "
            "manipulations like the pen, are smaller. <bookmark mark='b'/> And the published studies show a larger "
            f"effect than the unpublished ones, {d['pub']:.2f} against {d['unpub']:.2f}, the file drawer of Part "
            "4. A contrast can belong to two groups here, suppressing one face against posing another, so the groups "
            "overlap."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero),
                      LaggedStart(*[FadeIn(r) for r in rowsg], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(rows))
            vo.wait_until("b")
            self.play(FadeIn(pub))
        self.clear_scene()

    def smiles(self):
        head = heading(r"The Many Smiles Collaboration, \ 2022")
        tasks = VGroup()
        for t, c in ((r"mimic a smiling face", PLEAS), (r"pull the corners of the mouth toward the ears", PLEAS),
                     (r"hold a pen in the teeth", COG)):
            tasks.add(word_chip(t, color=c, font_size=20, width=5.6))
        tasks.arrange(DOWN, buff=0.35).move_to([-3.6, 0.3, 0])
        rows = rows_of([
            (r"Coles and colleagues: \ 3{,}878 people in 19 countries, \ preregistered, \ three ways of "
             r"moving the face", WHITE),
            (r"mimicking smiles and posing them on instruction raised reported happiness", PLEAS),
            (r"the pen in the teeth gave inconclusive results", COG),
            (r"the Ledger: \ replicated, \ smaller; \ it depends on how the face is moved, \ and the classic "
             r"unobtrusive version is the weakest", WHITE),
        ], 5.6, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Coles et al.\ (2022)")
        with self.voiceover(
            "Then a large collaboration tested three versions at once. <bookmark mark='a'/> The Many "
            "Smiles Collaboration, led by Coles, ran a preregistered study with 3,878 people in nineteen countries, "
            "with three ways of moving the face: mimicking a smiling face, pulling the corners of the mouth toward "
            "the ears, and holding a pen in the teeth. <bookmark mark='b'/> Mimicking smiles and posing them on "
            "instruction raised reported happiness. <bookmark mark='c'/> The pen gave inconclusive results. "
            "<bookmark mark='d'/> So the Ledger records facial feedback as replicated, smaller. It depends on how "
            "the face is moved, and the famous unobtrusive version is the weakest of all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(t) for t in tasks], lag_ratio=0.3))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
