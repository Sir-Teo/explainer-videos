from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


class Time(VoiceoverScene):
    def construct(self):
        self.card()
        self.curves()
        self.reversal()
        self.betadelta()

    def card(self):
        card = chapter_card(9, r"Choice over time", r"Why do plans made for later fall apart now?",
                            lit={1975: r"Ainslie", 1987: r"Mazur", 1995: r"Kirby \& Herrnstein", 1997: r"Laibson"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter nine. Choice over time."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def curves(self):
        d = load("time")
        head = heading(r"Two ways to discount the future")
        A = axes([0, 52], [0, 1.0], x_length=6.2, y_length=3.8, xticks=[0, 13, 26, 39, 52], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"delay, \ weeks",
                 ylabel=r"weight of a reward this far away", center=[-3.0, -0.2, 0], font_size=16)
        ce = curve(A.ax, d["t"], d["exp"], NORM, 4)
        ch = curve(A.ax, d["t"], d["hyp"], TIME, 4)
        key = legend([(NORM, rf"exponential: \ ${d['delta']}^D$"), (TIME, rf"hyperbolic: \ $1/(1 + {d['k']}D)$")],
                     font_size=18).move_to(A.ax.c2p(36, 0.85))
        rows = rows_of([
            (r"exponential: \ every week costs the same share, \ wherever it falls; \ the only discounting that "
             r"never changes its mind", NORM),
            (r"hyperbolic: \ steep near now, \ shallow far away; \ Ainslie, \ 1975; \ Mazur, \ 1987, \ in pigeons "
             r"and people", TIME),
            (r"asked how much later money must be, \ people demand far higher rates for short delays than for long "
             r"ones", GREY_A),
        ], 5.4, 22, 0.32).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{choice.discount}")
        with self.voiceover(
            "Choices are spread in time as well as in risk. Money now or more money later, cake now or health "
            "later. <bookmark mark='a'/> The standard model discounts the future exponentially: each week of delay "
            "shrinks a reward by the same fraction, wherever that week falls. It has a special property. It's the "
            "only discounting that never changes its mind: if you prefer the larger, later reward when both are far "
            "away, you still prefer it when the smaller one is at hand. <bookmark mark='b'/> Animals, and people, "
            "discount differently. George Ainslie and James Mazur found that pigeons and people discount "
            "hyperbolically: steeply near the present, shallowly far away. <bookmark mark='c'/> Asked how much "
            "money they'd need later to give up a sum now, people demand far higher rates of interest over short "
            "delays than over long ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(ce), FadeIn(key[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ch), FadeIn(key[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def reversal(self):
        d = load("time")
        head = heading(rf"{d['small']:.0f} sooner, \ or {d['large']:.0f} four weeks later?")
        A = axes([0, 52], [20, 105], x_length=6.2, y_length=4.0, xticks=[0, 13, 26, 39, 52], yticks=[25, 50, 75, 100],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"weeks until the sooner reward", ylabel=r"discounted value today, \ hyperbolic",
                 center=[-3.0, -0.2, 0], font_size=16)
        cs = curve(A.ax, d["t"], d["hyp_small"], SURE, 4)
        cl = curve(A.ax, d["t"], d["hyp_large"], RISKY, 4)
        star = d["star"]
        vline = DashedLine(A.ax.c2p(star, 20), A.ax.c2p(star, 105), color=GREY_B, stroke_width=2)
        slab = label(rf"{star:.0f} weeks", font_size=18, color=GREY_B).next_to(A.ax.c2p(star, 105), RIGHT, buff=0.1)
        key = legend([(SURE, rf"{d['small']:.0f} sooner"), (RISKY, rf"{d['large']:.0f} four weeks later")],
                     font_size=18).move_to(A.ax.c2p(42, 90))
        near = label(r"take the sooner", font_size=19, color=SURE).move_to(A.ax.c2p(9, 60))
        far = label(r"wait for more", font_size=19, color=RISKY).move_to(A.ax.c2p(38, 55))
        rows = rows_of([
            (r"far away, \ the extra four weeks look cheap: \ you plan to wait", RISKY),
            (r"as the date approaches, \ the curves cross, \ and the same person takes the sooner reward", SURE),
            (r"Kirby and Herrnstein, \ 1995: \ such reversals with real money, \ and real waits", WHITE),
            (r"an exponential discounter's curves never cross: \ with weekly weight 0.97 it takes the sooner reward "
             r"at every distance", NORM),
        ], 5.4, 22, 0.3).move_to([3.6, -0.1, 0])
        tag = psyche_tag(rf"\texttt{{choice.reversal\_delay}}: \ $k = {d['k']}$ a week")
        assert np.all(d["exp_small"] > d["exp_large"])
        with self.voiceover(
            f"Here's what hyperbolic discounting does. {d['small']:.0f} dollars at some date, or "
            f"{d['large']:.0f} dollars four weeks after it. <bookmark mark='a'/> Plot both rewards' value today "
            "against how far away the sooner one is. When both are far off, the extra four weeks barely register, "
            "and the larger reward is worth more. So today you plan to wait. <bookmark mark='b'/> But as the date "
            f"approaches the curves cross, at {star:.0f} weeks here, and the same person, with the same "
            "preferences, now takes the smaller, sooner reward. A plan made for later falls apart when later "
            "becomes now. <bookmark mark='c'/> Kris Kirby and Richard Herrnstein showed such reversals in 1995 with "
            "real money and real waiting. <bookmark mark='d'/> An exponential discounter can't do this. Its curves "
            "never cross; with these numbers it takes the sooner reward at every distance, and never regrets it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cs), Create(cl), FadeIn(key), run_time=2)
            self.play(FadeIn(far), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(vline), FadeIn(slab), FadeIn(near), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def betadelta(self):
        d = load("time")
        head = heading(r"Beta and delta: \ present bias")
        eq = MathTex(r"U = u_0 + \beta \sum_{t \ge 1} \delta^{t}\, u_t", font_size=44, color=TIME).move_to([0, 1.9, 0])
        A = axes([0, 52], [0, 1.05], x_length=5.4, y_length=3.0, xticks=[0, 26, 52], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"delay, \ weeks", ylabel=r"weight",
                 center=[-3.4, -1.0, 0], font_size=16)
        cb = curve(A.ax, d["t"][1:], d["bd"][1:], TIME, 4)
        now = Dot(A.ax.c2p(0, 1.0), color=TIME, radius=0.08)
        rows = rows_of([
            (r"Phelps and Pollak, \ 1968; \ Laibson, \ 1997: \ everything later is cut by $\beta$ at once, \ then "
             r"discounted exponentially", WHITE),
            (r"$\beta < 1$ is present bias: \ the self who plans is patient, \ the self who acts is not", TIME),
            (r"a sophisticated chooser who knows it binds the future self: \ commitment savings accounts, \ deadlines, "
             r"\ Ulysses at the mast", GAIN),
        ], 5.8, 22, 0.32).move_to([3.4, -0.9, 0])
        tag = psyche_tag(r"\texttt{choice.discount(kind=``beta\_delta'')}: \ $\beta = 0.7$, \ $\delta = 0.995$")
        with self.voiceover(
            "Economists adopted a simpler form of the same idea. <bookmark mark='a'/> In the beta-delta model, "
            "from Edmund Phelps and Robert Pollak in 1968 and David Laibson in 1997, anything not immediate is cut "
            "at once by a factor beta, and after that discounted exponentially. <bookmark mark='b'/> Beta below one "
            "is present bias. The self who plans for next month is patient; the self who has to act today is not, "
            "and the two disagree. <bookmark mark='c'/> The model also says what a person who knows this should do: "
            "bind the future self, as Ulysses had himself tied to the mast. Commitment savings accounts, deadlines "
            "and pre-paid gym memberships are all ways of doing it, with mixed success, as Part 55 will show."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(now), Create(cb), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
