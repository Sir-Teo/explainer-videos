from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403
from explainer.psychology import capstone as C


class Power(VoiceoverScene):
    def construct(self):
        self.card()
        self.sesoi()
        self.telescopes()
        self.curve()

    def card(self):
        card = chapter_card(3, r"How big, \ and how many?", r"What effect would matter, \ and what can be detected?",
                            lit={2015: r"Simonsohn", 2022: r"Lakens"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter three. How big, and how many?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def sesoi(self):
        p = load("plans")
        head = heading(r"The smallest effect of interest")
        A = axes([0, 0.5], [0, 1], x_length=5.4, y_length=3.0, xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                 yticks=[0, 0.5, 0.8, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"true effect $d$",
                 ylabel=r"power", center=[-3.3, 0.5, 0], font_size=13)
        d = np.linspace(0.001, 0.5, 120)
        curves = VGroup()
        for n, c in ((47, AUTH), (200, PERSON), (1000, GOOD)):
            pw = np.array([C.power2(x, n, n) for x in d])
            curves.add(curve(A.ax, d, pw, c, stroke_width=3))
        key = VGroup(label(r"23 and 24 per group (the study the protocol followed)", font_size=12, color=AUTH),
                     label(r"200 per group", font_size=12, color=PERSON),
                     label(r"1{,}000 per group", font_size=12, color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        key.next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"Lakens, \ 2022: \ justify the sample size by the smallest effect that would matter, \ not by the effect "
             r"you hope for", WHITE),
            (rf"for ego depletion the plan sets $d = {p['ed_sesoi']:g}$: \ smaller would not matter in practice", AUTH),
            (rf"one study would need {num(p['ed_n95'])} people per group for 95\% power at it; \ only many labs "
             rf"together come close", MODEL),
            (rf"the study the protocol followed had {100 * p['ed_power_orig']:.0f}\% power even for $d = 0.2$", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{capstone.power2}, \ \texttt{n\_per\_group}; \ Lakens (2022)")
        with self.voiceover(
            "How big an effect should the study be able to see? <bookmark mark='a'/> In 2022 Daniel Lakens argued "
            "that a sample size should be justified by the smallest effect that would matter, not by the effect you "
            "hope for. <bookmark mark='b'/> For ego depletion, the plan sets that at zero point one. A smaller effect "
            "wouldn't matter in practice. <bookmark mark='c'/> A single study would need about two thousand six "
            "hundred people per group for ninety-five percent power at it. Only many labs together come close. "
            "<bookmark mark='d'/> And the study the protocol followed, with twenty-three and twenty-four people, had "
            "only about ten percent power, even for an effect twice that size."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(curves), run_time=2.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def telescopes(self):
        p = load("plans")
        head = heading(r"Small telescopes")
        rows = rows_of([
            (r"Simonsohn, \ 2015: \ a replication cannot prove an effect is zero; \ but it can show the effect is too "
             r"small for the original study to have seen", WHITE),
            (r"$d_{33}$: \ the effect the original had a 33\% chance to detect; \ if a replication rules out effects "
             r"that large, \ the original telescope was too small for what it claimed to see", MODEL),
            (rf"ego depletion's original, \ 23 and 24 people: \ $d_{{33}} = {p['ed_d33']:.2f}$", AUTH),
            (rf"verbal overshadowing's original, \ 44 and 44 people, \ {pct(p['vo_p0'])} correct without a "
             rf"description: \ $d_{{33}}$ = {100 * p['vo_d33']:.0f} fewer correct picks per 100", GOOD),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Simonsohn (2015)")
        with self.voiceover(
            "A second benchmark comes from astronomy. <bookmark mark='a'/> In 2015 Uri Simonsohn pointed out that a "
            "replication can't prove an effect is zero. But it can show the effect is too small for the original "
            "study to have seen. <bookmark mark='b'/> Call d thirty-three the effect the original study had a "
            "one-in-three chance to detect. If a replication rules out effects that large, the original telescope was "
            "too small to see what it claimed. <bookmark mark='c'/> For ego depletion's original, with twenty-three "
            "and twenty-four people, d thirty-three is about zero point four six. <bookmark mark='d'/> For verbal "
            "overshadowing's original, with forty-four people in each group, it's about sixteen fewer correct picks "
            "per hundred people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def curve(self):
        d = load("powercurve")
        p = load("plans")
        head = heading(r"Power, \ as a curve")
        A = axes([0, 0.8], [0, 1], x_length=5.6, y_length=3.4, xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[0, 0.5, 0.8, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"true effect $d$", ylabel=r"power",
                 center=[-3.3, 0.3, 0], font_size=13)
        c1 = curve(A.ax, d["d"], d["orig"], AUTH, stroke_width=4)
        c2 = curve(A.ax, d["d"], d["pooled"], MODEL, stroke_width=4)
        c3 = curve(A.ax, d["d"], d["big"], GOOD, stroke_width=4)
        key = VGroup(label(r"original, \ 23 and 24", font_size=13, color=AUTH),
                     label(rf"23 labs pooled, \ about {num(d['n_pool'])} per group", font_size=13, color=MODEL),
                     label(r"2{,}600 per group", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.3)
        key.next_to(A, UP, buff=0.3)
        rows = rows_of([
            (rf"the original study had {100 * p['ed_power_orig']:.0f}\% power for $d = 0.2$, \ and needed $d$ near "
             rf"0.75 for the conventional 80\%", AUTH),
            (r"so a significant result from it was always likely to overstate the effect: \ the winner's curse of Part 4",
             PERSON),
            (r"pooled across labs, \ the replication has good power down to about $d = 0.15$; \ for $d = 0.1$, \ "
             r"2{,}600 per group in one study", MODEL),
            (r"power is a curve, \ not a number: \ say which effect it is for", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{capstone.power2}, \ noncentral $t$")
        with self.voiceover(
            "Power is a curve, so draw it. <bookmark mark='a'/> The original depletion study had about ten percent power "
            "for an effect of zero point two, and needed an effect near zero point seven five for the usual eighty "
            "percent. <bookmark mark='b'/> So a significant result from it was always likely to overstate the effect: "
            "the winner's curse of Part 4. <bookmark mark='c'/> Pooled across its labs, the replication has good power "
            "down to effects of about zero point one five. For zero point one, one study would need two thousand six "
            "hundred people per group. <bookmark mark='d'/> Power is a curve, not a number. Always say which effect "
            "it's for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(c1))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(c2), Create(c3))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
