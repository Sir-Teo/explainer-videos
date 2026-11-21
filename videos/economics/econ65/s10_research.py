from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403


class Research(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Growth with automated research", r"If machines can do research, \ can growth accelerate "
             r"without limit?", "Chapter eight. Growth with automated research.",
             lit={2019: "Aghion, Jones and Jones", 1967: "Baumol"}, scale=("world",), horizon=("a century",))
        self.ideas()
        self.bottleneck()
        self.baumol()
        self.debate()

    def ideas(self):
        eq = MathTex(r"\dot A_t", r"=", r"\theta\, S_t^{\lambda} A_t^{\phi}", font_size=48).to_edge(UP, buff=0.6)
        g = MathTex(r"g_A = \frac{\lambda\, n}{1-\phi}", font_size=44).next_to(eq, DOWN, buff=0.4)
        rows = VGroup(
            label(r"ideas come from researchers $S$, \ helped by the stock of ideas $A$", font_size=21, color=IDEA),
            label(r"but ideas are getting harder to find: \ $\phi < 1$", font_size=21, color=NAIVE),
            label(r"Moore's law now takes more than 18 times the researchers of the early 1970s", font_size=21,
                  color=GREY_A),
            label(r"so growth is tied to the growth of researchers, \ $n$: \ semi-endogenous growth \ (Part 21)",
                  font_size=21, color=WORK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, DOWN, buff=0.5)
        tag = published_tag(r"Jones, \ JPE 103(4) (1995); \ Bloom, \ Jones, \ Van Reenen and Webb, \ AER 110(4) "
                            r"(2020)", corner=DL, font_size=12)
        with self.voiceover(
            "Chapter six's arithmetic treats AI as a cheaper way to do today's tasks. The bigger question is "
            "whether it changes how fast we invent. Recall the model of ideas from Part twenty-one. <bookmark "
            "mark='a'/> New ideas come from researchers, S, standing on the shoulders of the ideas already found, "
            "A. <bookmark mark='b'/> But ideas get harder to find: phi is below one. <bookmark mark='c'/> Nicholas "
            "Bloom, Charles Jones, John Van Reenen and Michael Webb found that keeping Moore's law going now takes "
            "more than eighteen times as many researchers as in the early nineteen-seventies. <bookmark mark='d'/> "
            "So in the long run, growth is tied to the growth of the number of researchers, which is tied to the "
            "growth of the population. Now suppose machines can be researchers."
        ) as vo:
            self.play(FadeIn(tag), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Write(g), FadeIn(rows[3]))
        self.clear_scene()

    def bottleneck(self):
        G = load("growth")
        P = G["paths"]["0.90"]
        yrs = np.array(P["year"])
        axl = plane([0, 200], [0, 25], center=LEFT * 3.5 + DOWN * 0.2, x_length=5.6, y_length=4.4,
                    xticks=[0, 50, 100, 150, 200], yticks=[0, 5, 10, 15, 20, 25], xlabel=r"years",
                    ylabel=r"growth, \ \% a year", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                    font_size=13)
        axr = plane([0, 200], [0, 1], center=RIGHT * 3.3 + DOWN * 0.2, x_length=5.6, y_length=4.4,
                    xticks=[0, 50, 100, 150, 200], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"years",
                    ylabel=r"people's share of research costs", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=13)
        gl = path(axl, yrs, [100 * x for x in P["growth"]], IDEA, 3.0)
        sl = path(axr, yrs, P["people_share"], WORK, 3.0)
        head = label(r"90\% of research tasks automated", font_size=24, color=IDEA).to_edge(UP, buff=0.4)
        eqn = MathTex(r"R = \Big[\beta^{\frac1\sigma} K_R^{\frac{\sigma-1}{\sigma}} + (1-\beta)^{\frac1\sigma} "
                      r"S^{\frac{\sigma-1}{\sigma}}\Big]^{\frac{\sigma}{\sigma-1}}, \quad \sigma < 1",
                      font_size=30).next_to(head, DOWN, buff=0.2)
        tag = published_tag(r"Aghion, \ Jones and Jones, \ in \emph{The Economics of Artificial Intelligence} "
                            r"(2019); \ agora.automation.ideas\_growth", corner=DL, font_size=12)
        half = next((y for y, s_ in zip(P["year"], P["people_share"]) if s_ >= 0.5), None)
        with self.voiceover(
            "Philippe Aghion, Benjamin Jones and Charles Jones wrote this down. <bookmark mark='a'/> Research is "
            "a set of tasks, a share beta done by machines and the rest by people, combined with an elasticity "
            "below one. <bookmark mark='b'/> Automate ninety percent, and growth booms, as in the Play-it: to "
            f"about {100 * max(P['growth']):.0f} percent a year. <bookmark mark='c'/> Now watch where the money "
            "goes. At first, the machines' tasks are most of the cost of research, and the people's ten percent is "
            "almost nothing. But machines multiply, their tasks get cheap, and the people's tasks, which cannot be "
            f"skipped, take over the cost: by year {half} they are half of it, and soon nearly all. <bookmark "
            "mark='d'/> From then on, research grows only as fast as the people doing the last tasks, and growth "
            "falls back. This is William Baumol's cost disease, from 1967, in the laboratory: the tasks that are "
            "hard to improve end up determining the pace."
        ) as vo:
            self.play(FadeIn(axl), FadeIn(axr), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eqn))
            vo.wait_until("b")
            self.play(Create(gl), run_time=2.2)
            vo.wait_until("c")
            self.play(Create(sl), run_time=2.2)
            vo.wait_until("d")
            self.play(Indicate(sl, color=WORK, scale_factor=1.0))
        self.clear_scene()

    def baumol(self):
        B = load("baumol")
        t = np.array(B["t"])
        axl = plane([0, 100], [0, 0.6], center=LEFT * 3.5 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                    xticks=[0, 25, 50, 75, 100], yticks=[0, 0.2, 0.4, 0.6], xlabel=r"years",
                    ylabel=r"the automated sector's share of spending", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=13)
        axr = plane([0, 100], [0, 4], center=RIGHT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                    xticks=[0, 25, 50, 75, 100], yticks=[0, 1, 2, 3, 4], xlabel=r"years",
                    ylabel=r"growth of real output, \ \% a year", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:.0f}", font_size=13)
        sl = path(axl, t, B["share_fast"], MACH, 3.0)
        gl = path(axr, t, [100 * x for x in B["growth"]], GDP, 3.0)
        slow = seg(axr, 0, 100 * B["g_slow"], 100, 100 * B["g_slow"], WORK, 2.0, dashed=True)
        slab = label(r"the slow sector's growth", font_size=13, color=WORK).next_to(
            axr.ax.c2p(70, 100 * B["g_slow"]), UP, buff=0.08)
        head = label(rf"two goods, \ complements; \ one sector's productivity grows {100 * B['g_fast']:.0f}\% a "
                     rf"year, \ the other's {100 * B['g_slow']:.1f}\%", font_size=20, color=GREY_A).to_edge(
            UP, buff=0.4)
        tag = published_tag(r"Baumol, \ AER 57(3) (1967); \ Nordhaus, \ B.E. Journal of Macroeconomics 8(1) (2008); "
                            r"\ agora.automation.baumol", corner=DL, font_size=12)
        with self.voiceover(
            "The same logic applies to the whole economy. <bookmark mark='a'/> Two goods that people want "
            "together, like food and haircuts. Automate the making of one, so its productivity grows "
            f"{100 * B['g_fast']:.0f} percent a year, while the other's grows {100 * B['g_slow']:.1f}. <bookmark "
            "mark='b'/> The automated good gets cheaper and cheaper, and because people do not want ever more of "
            f"it, its share of spending falls, from half to {100 * B['share_fast'][-1]:.0f} percent in a century. "
            "<bookmark mark='c'/> Aggregate growth is the average of the two sectors' growth, weighted by spending, "
            f"so it slides from {100 * B['growth'][0]:.1f} percent towards the slow sector's "
            f"{100 * B['g_slow']:.1f}. Agriculture and manufacturing went this way: brilliant productivity, "
            "shrinking shares of GDP. William Nordhaus found the pattern across American industries. Automation "
            "that leaves an essential task to people can make that task the economy's pace-setter."
        ) as vo:
            self.play(FadeIn(axl), FadeIn(axr), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(sl), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(gl), FadeIn(slow), FadeIn(slab), run_time=2.0)
        self.clear_scene()

    def debate(self):
        cards = point_cards([
            (r"the case for an explosion", r"if AI can do every task in research, \ including its own improvement, "
             r"\ ideas feed ideas: \ growth that accelerates", IDEA),
            (r"the bottlenecks", r"experiments in the physical world, \ compute and energy, \ data, \ regulation, "
             r"\ and the tasks still left to people", NAIVE),
            (r"what to watch", r"whether the share of tasks automated, \ in research above all, \ approaches "
             r"one, \ or stalls", GDP),
            (r"the stakes", r"a century of Part 21's two percent, \ or a world economy that doubles in a few "
             r"years: \ the models allow both", E.ACCENT),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"explosion or bottleneck?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "So which is it? <bookmark mark='a'/> The case for explosive growth is the Play-it's last line: if AI "
            "can do every task in research, including improving AI, ideas produce the machines that produce ideas, "
            "and growth accelerates. <bookmark mark='b'/> The case against is the bottleneck: experiments in the "
            "physical world take time, compute needs chips and power, regulation moves slowly, and any task still "
            "left to people sets the pace. <bookmark mark='c'/> The models agree on what to watch: whether the "
            "share of tasks automated, in research above all, approaches one, or stalls short of it. <bookmark "
            "mark='d'/> The stakes are the difference between Part twenty-one's two percent a year and a world "
            "economy that doubles in a few years. The models allow both. The data have to decide."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
