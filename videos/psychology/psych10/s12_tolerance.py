from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


class Tolerance(VoiceoverScene):
    def construct(self):
        self.card()
        self.opponent()
        self.ten()
        self.place()

    def card(self):
        card = chapter_card(11, r"Tolerance and withdrawal", r"What does the body do back?",
                            lit={1974: r"the opponent process"}, part=PART, scale=("neuron", "mind", "person"),
                            marr=("what", "how"))
        with self.voiceover(
            "Chapter eleven. Tolerance and withdrawal."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def opponent(self):
        d = load("tolerance")
        k = d["t"] < 23.95
        t, a, b, net = d["t"][k], d["a"][k], d["b"][k], d["net"][k]
        head = heading(r"The body answers back")
        A = axes([0, 24], [-0.6, 1.15], x_length=6.8, y_length=4.3, xticks=[0, 4, 8, 12, 16, 20, 24], yticks=[],
                 xlabel=r"hours after the first dose", ylabel=r"", center=[-3.2, -0.4, 0])
        ax = A.ax
        zero = Line(ax.c2p(0, 0), ax.c2p(24, 0), color=GREY_C, stroke_width=2)
        la = curve(ax, t, a, DRUG, stroke_width=3.5)
        lb = curve(ax, t, -b, OPP, stroke_width=3.5)
        ln = curve(ax, t, net, WHITE, stroke_width=5)
        ta = label(r"a: \ the drug's own effect", font_size=26, color=DRUG).next_to(ax.c2p(4.3, 1.0), RIGHT, buff=0.15)
        tb = label(r"b: \ the body's reply", font_size=26, color=OPP).move_to(ax.c2p(14, -0.42))
        tn = label(r"what is felt: \ a minus b", font_size=26, color=WHITE).next_to(ax.c2p(5.2, 0.62), RIGHT, buff=0.2)
        rows = rows_of([
            (r"a: \ on with the drug, \ off with it", DRUG),
            (r"b: \ opposite in sign, \ slow to rise, \ slow to fade", OPP),
            (r"felt: \ the full effect, \ then less as b catches up", WHITE),
            (r"and when the drug has gone, \ b runs on alone: \ the effect passes through zero to its opposite", THRESH),
        ], 5.0, 28, 0.28).move_to([4.35, -0.3, 0])
        keep_in_frame(rows)
        src = published_tag(archive.SOLOMON_CORBIT_1974.cite)
        tag = psyche_tag(r"computed: Psyche's opponent process (a model)")
        with self.voiceover(
            "The body isn't a passive container. In 1974 Richard Solomon and John Corbit proposed a "
            "simple account of what it does back, called the opponent process theory. "
            "<bookmark mark='a'/> A drug produces a direct effect. Call it process a. It comes on with "
            "the drug, and goes off with it. <bookmark mark='b'/> The nervous system defends its "
            "balance. It answers with an opposite process, b, which is slow to rise and slow to fade. "
            "<bookmark mark='c'/> What's felt is the difference. At first, the full effect. Then less, "
            "as b catches up. <bookmark mark='d'/> And when the drug is gone, b is still running, alone. "
            "So the effect doesn't return to zero. It passes through zero, to the opposite. After the "
            "lift, a low. After the calm, the jitters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), FadeIn(zero))
            vo.wait_until("a")
            self.play(Create(la), FadeIn(ta), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(lb), FadeIn(tb), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(ln), FadeIn(tn), FadeIn(rows[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def ten(self):
        d = load("tolerance")
        f0, f1 = d["felt_first"], d["felt_last"]
        w0, w1 = abs(d["after_first"]), abs(d["after_last"])
        sel = slice(None, None, 3)
        head = heading(r"Ten doses, \ one a day")
        A = axes([0, 264], [-1.2, 1.15], x_length=12.4, y_length=2.3, xticks=[], yticks=[], xlabel=r"", ylabel=r"",
                 center=[0, 1.45, 0])
        ax = A.ax
        zero = Line(ax.c2p(0, 0), ax.c2p(264, 0), color=GREY_C, stroke_width=2)
        net = curve(ax, d["t"][sel], d["net"][sel], WHITE, stroke_width=3)
        days = VGroup(*[label(rf"{n + 1}", font_size=22, color=GREY_A).move_to(ax.c2p(24 * n + 2, -1.2) + DOWN * 0.2)
                        for n in range(10)])
        dcap = label(r"dose", font_size=22, color=GREY_A).next_to(days, LEFT, buff=0.15)
        B = axes([0.5, 10.5], [-1.2, 1.0], x_length=5.0, y_length=2.4, xticks=[1, 4, 7, 10], yticks=[-1, 0, 1],
                 xlabel=r"dose", ylabel=r"", center=[-3.6, -1.75, 0])
        bx = B.ax
        bzero = Line(bx.c2p(0.5, 0), bx.c2p(10.5, 0), color=GREY_C, stroke_width=2)
        n = np.arange(1, 11)
        felt = VGroup(curve(bx, n, d["felt"], DRUG, stroke_width=4), *[Dot(bx.c2p(i, v), radius=0.07, color=DRUG)
                                                                      for i, v in zip(n, d["felt"])])
        low = VGroup(curve(bx, n, d["troughs"], OPP, stroke_width=4), *[Dot(bx.c2p(i, v), radius=0.07, color=OPP)
                                                                       for i, v in zip(n, d["troughs"])])
        fl = label(r"the effect felt", font_size=25, color=DRUG).move_to(bx.c2p(6.8, 0.68))
        wl = label(r"the low afterwards", font_size=25, color=OPP).move_to(bx.c2p(7.6, -0.62))
        rows = rows_of([
            (rf"the effect felt: \ ${f0:.2f}$ of the full effect, \ down to ${f1:.2f}$: \ tolerance", DRUG),
            (rf"the low afterwards: \ ${w0:.2f}$ below zero, \ down to ${w1:.2f}$: \ withdrawal", OPP),
            (r"one process, \ seen at two times", WHITE),
            (r"the first dose is taken to feel better than normal; \ the tenth, \ to get back up to normal", THRESH),
        ], 6.4, 28, 0.22).move_to([3.4, -1.75, 0])
        keep_in_frame(rows)
        src = published_tag(archive.SOLOMON_CORBIT_1974.cite)
        tag = psyche_tag(r"computed: Psyche's opponent process (a model)")
        with self.voiceover(
            "Now repeat the dose, once a day, for ten days. The theory makes one more assumption: the "
            "reply is strengthened by use. <bookmark mark='a'/> With each dose, b is larger. "
            f"<bookmark mark='b'/> So the effect that's felt shrinks: from {f0:.2f} of the full effect "
            f"on the first day, to {f1:.2f} on the tenth. That's tolerance. <bookmark mark='c'/> And the "
            f"low afterwards deepens: from {w0:.2f} below zero, to {w1:.2f}. That's withdrawal. "
            "<bookmark mark='d'/> They aren't two things. They're one process, seen at two times: while "
            "the drug is there, and after it has gone. <bookmark mark='e'/> And look at what the tenth "
            "dose is for. The first was taken to feel better than normal. The tenth is taken to get "
            "back up to normal. The theory was built for more than drugs, and Parts 28 and 41 will "
            "come back to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), FadeIn(zero), FadeIn(days), FadeIn(dcap))
            vo.wait_until("a")
            self.play(Create(net), run_time=6.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(bzero), FadeIn(felt, lag_ratio=0.1), FadeIn(fl), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(low, lag_ratio=0.1), FadeIn(wl), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def place(self):
        d = load("tolerance")
        s = archive.SIEGEL_1982.data
        pu, pn, p0 = (round(100 * float(v)) for v in d["published"])
        mu, mn, m0 = (round(100 * float(v)) for v in d["model"])
        head = heading(r"The same dose, \ in a different room")
        A = axes([0, 3], [0, 1.08], x_length=6.4, y_length=4.0, xticks=[], yticks=[0, 0.5, 1],
                 yfmt=lambda v: rf"{100 * v:.0f}\%", xlabel=r"", ylabel=r"rats that died", center=[-3.35, -0.2, 0])
        ax = A.ax
        unit = abs(ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1])
        names = [r"tolerant; \ the usual room", r"tolerant; \ a new room", r"no history of the drug"]
        bars = VGroup()
        for i in range(3):
            pv, mv = float(d["published"][i]), float(d["model"][i])
            pb = Rectangle(width=0.42, height=pv * unit, stroke_width=0, fill_color=DATA, fill_opacity=0.9)
            pb.move_to(ax.c2p(i + 0.32, 0), aligned_edge=DOWN)
            mb = Rectangle(width=0.42, height=mv * unit, stroke_width=0, fill_color=MODEL, fill_opacity=0.9)
            mb.move_to(ax.c2p(i + 0.68, 0), aligned_edge=DOWN)
            pl = label(rf"{100 * pv:.0f}\%", font_size=25, color=DATA).next_to(pb, UP, buff=0.06)
            ml = label(rf"{100 * mv:.0f}\%", font_size=25, color=MODEL).next_to(mb, UP, buff=0.06)
            nm = wrapped_label(names[i], 1.9, 24, WHITE).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.15)
            bars.add(VGroup(nm, VGroup(pb, pl), VGroup(mb, ml)))
        lg = legend([(DATA, r"published"), (MODEL, r"Psyche")], font_size=25).move_to(ax.c2p(0.55, 0.92))
        rows = rows_of([
            (rf"rats made tolerant to heroin, \ always in the same room; \ then one large dose "
             rf"({s['dose_mg_kg']} mg/kg)", WHITE),
            (r"same rats, \ same history, \ same dose, \ a different room: \ twice the deaths", BAD),
            (r"the room always came before the drug, \ so the room comes to switch the reply on in advance "
             r"(Pavlov: Part 16)", THRESH),
            (r"Psyche: \ the reply cancels three quarters of a lethal dose in the usual room, \ less than half in a new "
             r"one. \ Set to fit, so no test", MODEL),
            (r"some overdoses are the usual dose, \ in an unusual place", WHITE),
        ], 5.2, 27, 0.22).move_to([4.2, -0.3, 0])
        keep_in_frame(rows)
        src = published_tag(archive.SIEGEL_1982.cite)
        tag = psyche_tag(r"simulated: 100{,}000 model animals in each group")
        with self.voiceover(
            "And here's the part that makes this psychology, and not only pharmacology. The reply is "
            "partly learned. <bookmark mark='a'/> In 1982 Shepard Siegel made rats tolerant to heroin, "
            "always giving it in the same room. Then every rat got one large dose. Of rats with no "
            f"history of the drug, {p0} percent died. Of tolerant rats, dosed in the usual room: {pu} "
            f"percent. <bookmark mark='b'/> And of tolerant rats given the same dose in a different "
            f"room: {pn} percent. Same rats, same history, same dose. Twice the deaths. "
            "<bookmark mark='c'/> Siegel's account is Pavlov's, which Part 16 will build. The room has "
            "always come before the drug. So the room itself comes to switch on the body's reply, in "
            "advance. Take away the room, and part of the tolerance isn't there. <bookmark mark='d'/> "
            "In Psyche's version, the learned reply cancels three quarters of a lethal dose in the usual "
            f"room, and less than half in a new one, and the deaths come out at {mu}, {mn} and {m0} "
            "percent. Those settings were chosen to fit, so that's no test. It shows that the account "
            "hangs together. <bookmark mark='e'/> What it means outside the laboratory is grim, and "
            "practical. For an experienced user, some overdoses aren't a larger dose. They're the usual "
            "dose, in an unusual place."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), *[FadeIn(b_[0]) for b_ in bars], FadeIn(rows[0]))
            vo.wait_until("a")
            self.wait(7.0)
            self.play(FadeIn(bars[2][1], shift=UP * 0.1))
            self.wait(2.0)
            self.play(FadeIn(bars[0][1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(bars[1][1], shift=UP * 0.1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(*[FadeIn(b_[2], shift=UP * 0.1) for b_ in bars], FadeIn(lg), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()
