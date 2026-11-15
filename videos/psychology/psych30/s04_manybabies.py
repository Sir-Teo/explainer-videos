from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403

METHOD_COL = {"Central fixation": LOOK, "Eye tracking": MIND, "HPP": OBJ}
METHOD_NAME = {"Central fixation": r"central fixation", "Eye tracking": r"eye tracking", "HPP": r"head-turn preference"}


class ManyBabies(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.forest()
        self.moderators()

    def card(self):
        card = chapter_card(3, r"One effect, \ sixty-five laboratories", r"Does the instrument give the same answer "
                            r"everywhere?", lit={2017: r"ManyBabies founded", 2020: r"ManyBabies 1"},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter three. One effect, sixty-five laboratories."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def problem(self):
        head = heading(r"Why infant studies are fragile")
        rows = rows_of([
            (r"infants are hard to recruit and often fuss out: \ a typical study had a few dozen", LOST),
            (r"so a single study's estimate is noisy, \ and published ones are a filtered sample \ (Part 4)", LOST),
            (r"ManyBabies: \ a consortium of laboratories that agree a protocol in advance and all run it", NUM),
            (r"its first target: \ do infants prefer infant-directed speech, \ the sing-song way adults talk to "
             r"babies, \ to adult-directed speech?", WHITE),
            (r"chosen because it was thought robust: \ a test of the method, \ not of a fragile claim", LOOK),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"ManyBabies Consortium (2020)")
        with self.voiceover(
            "Before trusting looking times, ask how well they replicate. <bookmark mark='a'/> Infants are hard to "
            "recruit, and many fuss out before the end. A typical study has a few dozen. "
            "<bookmark mark='b'/> So one study's estimate is noisy, and the published ones are a filtered sample, "
            "the problem of Part 4. <bookmark mark='c'/> The response was ManyBabies, a consortium of laboratories "
            "that agree a protocol in advance and all run it. <bookmark mark='d'/> Its first target: do infants "
            "prefer infant-directed speech, the sing-song way adults talk to babies, to adult-directed speech? "
            "<bookmark mark='e'/> It was chosen because it was thought robust. This was a test of the method, not "
            "of a fragile claim."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def forest(self):
        d = load("manybabies")
        head = heading(r"Every laboratory and age group at once")
        k = int(d["k"])
        A = axes([-1.6, 2.2], [0, k + 4], x_length=6.0, y_length=5.2, xticks=[-1, 0, 1, 2], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"Cohen's $d$: \ infant-directed over adult-directed",
                 center=[-3.0, -0.4, 0], font_size=15)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, k + 4), color=GREY_B, stroke_width=2)
        lines = VGroup()
        for i, (y, se, m) in enumerate(zip(d["y"], d["se"], d["method_sorted"])):
            yy = i + 1
            col = METHOD_COL[m]
            lo, hi = max(y - 1.96 * se, -1.6), min(y + 1.96 * se, 2.2)
            lines.add(VGroup(Line(A.ax.c2p(lo, yy), A.ax.c2p(hi, yy), color=col, stroke_width=1.2, stroke_opacity=0.6),
                             Dot(A.ax.c2p(y, yy), radius=0.03, color=col)))
        pool = Polygon(A.ax.c2p(d["re_lo"], k + 2.5), A.ax.c2p(d["re"], k + 3.2), A.ax.c2p(d["re_hi"], k + 2.5),
                       A.ax.c2p(d["re"], k + 1.8), color=GOOD, fill_color=GOOD, fill_opacity=0.9, stroke_width=0)
        key = legend([(LOOK, r"central fixation"), (MIND, r"eye tracking"), (OBJ, r"head-turn preference")],
                     font_size=15).move_to(A.ax.c2p(1.45, 20))
        n_inf = num(d["infants"])
        rows = rows_of([
            (rf"the open table: \ {k} estimates from {d['labs']} laboratories, \ {n_inf} infants aged 3 to 15 "
             rf"months, \ in three methods", WHITE),
            (rf"pooled: \ $d = {d['re']:.2f}$ \ [{d['re_lo']:.2f}, \ {d['re_hi']:.2f}], \ the published value",
             GOOD),
            (r"smaller than the earlier literature suggested, \ and clearly not zero: \ the preference is real", NUM),
            (rf"$I^2 = {100 * d['I2']:.0f}\%$: \ most of the spread between laboratories is sampling noise", LOOK),
        ], 5.4, 21, 0.32).move_to([3.6, -0.1, 0])
        tag = published_tag(r"data: ManyBabies Consortium (2020), \ recomputed")
        n_infants = f"{d['infants']:,}"
        with self.voiceover(
            "The consortium released its data, and Psyche reads the table. <bookmark mark='a'/> There are "
            f"{k} estimates, one for each laboratory and age group, from {d['labs']} laboratories and "
            f"{n_infants} infants between three and fifteen months old, tested by three methods. Each line here is "
            f"one estimate. <bookmark mark='b'/> Pooled, the preference is a d of {d['re']:.2f}, with an interval "
            f"from {d['re_lo']:.2f} to {d['re_hi']:.2f}, which is the published value. "
            "<bookmark mark='c'/> That is smaller than the earlier literature suggested, and clearly not zero: the "
            f"preference is real. <bookmark mark='d'/> And the heterogeneity is low: I squared of "
            f"{100 * d['I2']:.0f} percent, so most of the spread between laboratories is the noise you'd expect from "
            "small samples."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.02), FadeIn(key), FadeIn(rows[0]),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(pool), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def moderators(self):
        d = load("manybabies")
        head = heading(r"What the effect depends on")
        A = axes([-0.6, 8.0], [0, 0.8], x_length=6.4, y_length=3.6, xticks=None, yticks=[0, 0.2, 0.4, 0.6, 0.8],
                 yfmt=lambda v: f"{v:g}", ylabel=r"pooled $d$", center=[-3.0, -0.2, 0], font_size=15)
        items = []
        for i, nm in enumerate(d["method_names"]):
            items.append((1.25 * i, d["method_est"][i], d["method_lo"][i], d["method_hi"][i], METHOD_COL[nm],
                          METHOD_NAME[nm]))
        for j, g in enumerate(d["group_names"]):
            items.append((3.9 + 1.1 * j, d["group_est"][j], d["group_lo"][j], d["group_hi"][j], NUM,
                          g.replace(" mo", r"\ mo")))
        marks = VGroup()
        for x, e, lo, hi, col, nm in items:
            marks.add(VGroup(Line(A.ax.c2p(x, max(lo, 0)), A.ax.c2p(x, min(hi, 0.8)), color=col, stroke_width=4),
                             Dot(A.ax.c2p(x, e), radius=0.08, color=col),
                             wrapped_label(nm, 0.85, 13, col).next_to(A.ax.c2p(x, 0), DOWN, buff=0.15)))
        gl = label(r"by method", font_size=17, color=GREY_B).move_to(A.ax.c2p(1.25, 0.75))
        al = label(r"by age", font_size=17, color=GREY_B).move_to(A.ax.c2p(5.55, 0.75))
        rows = rows_of([
            (rf"age: \ the preference grows by about {d['age_slope']:.2f} in $d$ per month \ (standard error "
             rf"{d['age_slope_se']:.2f}), \ from a meta-regression with method held fixed", NUM),
            (rf"method: \ the head-turn preference procedure gives the largest effect, \ about {d['hpp_b']:.2f} "
             rf"more than central fixation", OBJ),
            (rf"language: \ larger when the speech was the infants' own North American English \ "
             rf"({d['nae_est']:.2f} against {d['other_est']:.2f})", LOOK),
            (r"the lesson: \ an infant effect is a property of a method, \ an age and a stimulus, \ not only of "
             r"the infant", WHITE),
        ], 5.4, 21, 0.32).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{develop.meta\_regression}; \ data: ManyBabies Consortium (2020)")
        with self.voiceover(
            "With a hundred and eight estimates, the moderators can be measured. <bookmark mark='a'/> Age: in a "
            "meta-regression with method held fixed, the preference grows by about "
            f"{d['age_slope']:.2f} in d per month of age. <bookmark mark='b'/> Method: the head-turn preference "
            f"procedure gives the largest effect, about {d['hpp_b']:.2f} more than central fixation. "
            "<bookmark mark='c'/> And language: the effect is larger when the speech was the infants' own North "
            f"American English, {d['nae_est']:.2f} against {d['other_est']:.2f}. These match what the consortium "
            "reported. <bookmark mark='d'/> The lesson for the rest of this part: an infant effect is a property of "
            "a method, an age and a stimulus, not only of the infant."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(gl), FadeIn(al),
                      LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.15))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
