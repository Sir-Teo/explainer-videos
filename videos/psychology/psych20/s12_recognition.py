from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403


class Recognition(VoiceoverScene):
    def construct(self):
        self.card()
        self.butcher()
        self.rocs()
        self.debate()

    def card(self):
        card = chapter_card(11, r"Knowing and remembering", r"Is recognising a face one process or two?",
                            lit={1980: r"Mandler", 1985: r"Tulving", 1994: r"Yonelinas", 2007: r"Wixted"},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter eleven. Knowing and remembering."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def butcher(self):
        head = heading(r"The butcher on the bus")
        rows = rows_of([
            (r"a face on a bus is familiar: \ you know you know it, \ and nothing more", CUE),
            (r"then it comes: \ the butcher, \ from the shop on the corner \ (Mandler, \ 1980)", WORD),
            (r"familiarity: \ a graded sense of having met something before; \ fast", CUE),
            (r"recollection: \ bringing back the episode, \ where and when and what else; \ slower, \ all or none",
             WORD),
            (r"Tulving, \ 1985: \ people can say which: \ ``I remember'' against ``I just know''", MODEL),
            (r"recall needs recollection; \ recognition can run on either", GREY_A),
        ], 12.4, 27, 0.38).move_to([0, -0.2, 0])
        tag = historical_tag(r"Mandler (1980); \ Tulving (1985)")
        with self.voiceover(
            "So far we've asked people to recall. Recognising is different, and George Mandler gave the classic "
            "example. <bookmark mark='a'/> You see a man on a bus, and his face is familiar. You know you know him, "
            "and that is all you know. <bookmark mark='b'/> Then it comes to you: he's the butcher from the shop on "
            "the corner. <bookmark mark='c'/> Two things happened. First familiarity, a graded feeling of having "
            "met something before, which arrives quickly. <bookmark mark='d'/> Then recollection: the episode "
            "itself, where and when, comes back, all at once or not at all. <bookmark mark='e'/> Tulving found in "
            "1985 that people can report which they have. Asked about each word they recognise, they can say "
            "I remember seeing it, or I just know it was there. <bookmark mark='f'/> Recall needs recollection. "
            "Recognition, it seems, can run on either."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def rocs(self):
        d = load("recognition")
        head = heading(r"Two models, \ one ROC")
        A = axes([0, 1], [0, 1], x_length=3.9, y_length=3.9, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xlabel=r"false alarms", ylabel=r"hits", center=[-4.4, -0.25, 0], font_size=17,
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}")
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_C, stroke_width=2)
        dp = curve_in(ax, d["F_dp"], d["H_dp"], WORD, 4)
        uv = curve_in(ax, d["F_uv"], d["H_uv"], CUE, 4)
        B = axes([-2.5, 2.5], [-2.5, 3.0], x_length=3.9, y_length=3.9, xticks=[-2, 0, 2], yticks=[-2, 0, 2],
                 xlabel=r"$z$(false alarms)", ylabel=r"$z$(hits)", center=[0.4, -0.25, 0], font_size=17,
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        bx = B.ax
        keep_dp = (np.abs(d["zF_dp"]) < 2.4) & (d["zH_dp"] < 2.9)
        keep_uv = (np.abs(d["zF_uv"]) < 2.4) & (d["zH_uv"] < 2.9)
        zdp = curve_in(bx, d["zF_dp"][keep_dp], d["zH_dp"][keep_dp], WORD, 4)
        zuv = curve_in(bx, d["zF_uv"][keep_uv], d["zH_uv"][keep_uv], CUE, 4)
        key = legend([(WORD, r"dual process: \ recollection 0.3, \ familiarity $d' = 1$"),
                      (CUE, r"one process: \ old items more variable, \ s.d.\ 1.25")], font_size=18)
        key.move_to([-2.0, 2.75, 0])
        rows = rows_of([
            (r"Yonelinas, \ 1994: \ recollection is a threshold, \ familiarity is graded", WORD),
            (r"the ROC: \ raised at the left, \ where only recollection can produce hits", WORD),
            (r"the rival: \ one graded strength, \ with more spread for studied items", CUE),
            (r"in ROC space the two are almost the same curve", GREY_A),
            (r"in $z$ space: \ a straight line of slope 0.8, \ against a slight bend", MODEL),
            (r"telling them apart needs many confidence levels, \ many trials, \ and care", LOST),
        ], 4.2, 20, 0.28).move_to([4.75, -0.3, 0])
        ptag = psyche_tag(r"\texttt{memory.dual\_process\_roc}, \ \texttt{memory.uvsd\_roc}")
        with self.voiceover(
            "Can you see two processes in the data? Part 12 drew receiver operating characteristics for "
            "recognition, by asking for confidence. <bookmark mark='a'/> Andrew Yonelinas's dual-process model "
            "treats recollection as a threshold: some studied items are simply remembered, and the rest are judged by "
            "familiarity, a graded signal of the kind Part 12 described. <bookmark mark='b'/> That lifts the left "
            "end of the curve, because recollection produces hits without any false alarms. "
            "<bookmark mark='c'/> The rival model has only one graded strength, but studied items vary more in "
            "strength than new ones, the unequal-variance model, whose z-transformed slope of about 0.8 Part 12's "
            "Ledger entered as replicated. <bookmark mark='d'/> Draw both, and in ROC space they are almost the same "
            "curve. <bookmark mark='e'/> Transform to z scores and the difference shows: a straight line for one "
            "process, and a slight bend for two. <bookmark mark='f'/> A slight bend is hard to measure. Telling the "
            "models apart needs many confidence levels and many trials, and this is one of the longest-running "
            "arguments in memory research."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(diag), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(Create(dp), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(key[1]))
            vo.wait_until("d")
            self.play(Create(uv), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(B), Create(zdp), Create(zuv), FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def debate(self):
        head = heading(r"Where are the two processes?")
        rows = rows_of([
            (r"one view: \ the hippocampus recollects, \ the nearby perirhinal cortex signals familiarity", WORD),
            (r"evidence: \ some patients with damage limited to the hippocampus lose recollection and keep "
             r"familiarity", WORD),
            (r"the other view (Wixted, \ Squire): \ both depend on the hippocampus; \ ``remember'' is just "
             r"stronger memory", CUE),
            (r"evidence: \ remember and know responses behave like high and low confidence on one scale", CUE),
            (r"the same lesson as the last chapter: \ a dissociation needs tests matched for difficulty", LOST),
            (r"and the same tool as Part 12: \ a model of the decision makes the argument testable", MODEL),
        ], 12.4, 26, 0.36).move_to([0, -0.2, 0])
        tag = historical_tag(r"Yonelinas et al.\ (2002); \ Wixted (2007); \ Squire et al.\ (2007)")
        with self.voiceover(
            "The argument extends into the brain. <bookmark mark='a'/> On one view, the hippocampus does "
            "recollection and the perirhinal cortex beside it signals familiarity. <bookmark mark='b'/> Some "
            "patients whose damage is limited to the hippocampus seem to have lost recollection while keeping "
            "familiarity. <bookmark mark='c'/> On the other view, argued by John Wixted and Larry Squire, the "
            "hippocampus supports both, and remembering, as opposed to knowing, is simply what strong memory feels "
            "like. <bookmark mark='d'/> They point out that remember and know judgments behave very much like high "
            "and low confidence on a single scale. <bookmark mark='e'/> The lesson is the one from the last "
            "chapter. A dissociation is only as good as the match between the two tests. "
            "<bookmark mark='f'/> And the tool is the one from Part 12: a model of the decision, which turns a "
            "debate about words into one about curves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
