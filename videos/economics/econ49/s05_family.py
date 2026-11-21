from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class Family(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The household as a small factory", r"What does a family make, and with what?",
             "Chapter four. The household as a small factory.", lit={1965: r"Becker", 1981: r"A Treatise"},
             scale=("household",), horizon=("a day", "a decade"))
        self.factory()
        self.split()
        self.record()

    def factory(self):
        chain = flow_chain([(r"goods \\ bought", MARKET), (r"time \\ at home", HOME),
                            (r"commodities: \\ meals, \ care, \\ rest, \ children", CHILD),
                            (r"what people \\ value", GAIN)],
                           notes=[r"paid for with \\ time at work", r"each hour priced \\ at the wage",
                                  r"made in the \\ household", r"the utility"], box_w=2.9, font_size=20,
                           note_size=17).move_to(UP * 1.2)
        eq = MathTex(r"\text{full income} \;=\; w \times T", r"\qquad", r"\text{price of a commodity} \;=\; p "
                     r"\cdot x \;+\; w \cdot t", font_size=40).move_to(DOWN * 1.4)
        eq[0].set_color(MARKET)
        eq[2].set_color(CHILD)
        foot = label(r"as wages rise, \ the time-intensive commodities get dearer", font_size=22,
                     color=E.ACCENT).next_to(eq, DOWN, buff=0.5)
        tag = published_tag(r"Becker, \ Economic Journal (1965)", corner=DR, font_size=11)
        with self.voiceover(
            "In 1965 Becker treated the household itself as a small factory. <bookmark mark='a'/> It buys goods "
            "with money earned at work, <bookmark mark='b'/> combines them with its own time at home, <bookmark "
            "mark='c'/> and produces what people actually want: meals, care, rest, the raising of children. "
            "<bookmark mark='d'/> Those commodities are what give utility. <bookmark mark='e'/> The idea has two "
            "consequences. A household's real budget is its full income, every hour valued at the wage, whether "
            "it is sold or not. And every commodity has a price that includes the time it takes. <bookmark "
            "mark='f'/> As wages rise, the commodities that take a lot of time, a home-cooked dinner, a large "
            "family, get dearer, and households shift toward those that take goods instead."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]), run_time=1.0)
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(Write(eq), run_time=2.0)
            vo.wait_until("f")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def split(self):
        H = load("household")
        w2 = np.array(H["w2"])
        ax = plane([0.3, 1.6], [0, 1.05], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.4,
                   xticks=[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"her wage, \ as a share of his", ylabel=r"share of each one's time at work for pay",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        him = path(ax, w2, H["market1"], MEN, 3.2, smooth=False)
        her = path(ax, w2, H["market2"], WOMEN, 3.2, smooth=False)
        k0 = int(np.argmax(np.array(H["market2"]) > 0))
        start = vline(ax, w2[k0], 0, 1.05, GREY_B)
        start_l = label(rf"she starts paid work \\ at {w2[k0]:.2f} of his wage", font_size=15, color=WOMEN).next_to(
            ax.ax.c2p(w2[k0], 0.55), RIGHT, buff=0.1)
        side = VGroup(
            label(r"two adults: \ he is \\ better paid, \ she is \\ better at home", font_size=17, color=WHITE),
            label(rf"home skills {H['h1']:.1f} and \\ {H['h2']:.1f}: \ she has the \\ comparative advantage",
                  font_size=17, color=HOME),
            label(r"blue: \ his paid time; \\ pink: \ hers", font_size=17, color=MEN),
            label(r"specialization by \\ comparative advantage, \\ not by any rule \\ about who does what",
                  font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        wt = ValueTracker(float(w2[0]))
        m2 = np.array(H["market2"])
        dot_w = always_redraw(lambda: Dot(ax.ax.c2p(wt.get_value(), float(np.interp(wt.get_value(), w2, m2))),
                                          radius=0.08, color=WHITE))
        read = always_redraw(lambda: label(rf"her wage {wt.get_value():.2f} of his: \ "
                                           rf"{100 * float(np.interp(wt.get_value(), w2, m2)):.0f}\% of her time "
                                           r"at paid work", font_size=19, color=WOMEN).to_edge(UP, buff=0.45))
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is an Island household of two adults. <bookmark mark='a'/> He earns more in the market; <bookmark "
            f"mark='b'/> she is more productive at home, {H['h2'] / H['h1']:.2f} times as productive, in the model. "
            "Who should do what? The answer is comparative advantage, the same as in trade between countries. "
            "<bookmark mark='c'/> While her wage is low, she specializes at home and he works for pay. As her wage "
            f"rises, past about {w2[k0]:.2f} of his, she starts paid work, and her share of time at work rises "
            "steadily. <bookmark mark='d'/> Nothing in the model says who should stay home; it is the ratio of wages "
            "to home skills that decides. Becker's critics pointed out that the home skills themselves are shaped "
            "by who was expected to stay home, and the model takes them as given."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(him), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.add(dot_w, read)
            self.play(wt.animate.set_value(float(w2[-1])), Create(her), run_time=8.0, rate_func=linear)
            self.play(Create(start), FadeIn(start_l))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(her, color=WHITE))
        self.clear_scene()

    def record(self):
        P = load("participation")
        y = np.array(P["year"])
        ax = plane([1946, 2026], [20, 95], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.8, y_length=4.4,
                   xticks=[1950, 1970, 1990, 2010], yticks=[20, 40, 60, 80], ylabel=r"in the labour force, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        w = path(ax, y, P["women"], WOMEN, 3.2, smooth=False)
        m = path(ax, y, P["men"], MEN, 3.2, smooth=False)
        pk = dot(ax, P["w_peak_year"], P["w_peak"], WOMEN, 0.08)
        side = VGroup(
            label(rf"women: \ {P['w_first']:.0f}\% in {P['first_year']}, \\ {P['w_peak']:.0f}\% at the peak \\ in "
                  rf"{P['w_peak_year']}, \ {P['w_last']:.0f}\% in {P['last_year']}", font_size=17, color=WOMEN),
            label(rf"men: \ {P['m_first']:.0f}\% to {P['m_last']:.0f}\%", font_size=17, color=MEN),
            label(r"behind it: \ women's \\ wages, \ fewer children, \\ machines at home, \\ the pill", font_size=17,
                  color=E.ACCENT),
            label(r"Goldin: \ also rules, \\ norms and the timing \\ of careers", font_size=17, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"BLS, \ Current Population Survey, \ via FRED \ (LNS11300002, \ LNS11300001)", corner=DL,
                       font_size=12)
        with self.voiceover(
            "The record of the twentieth century fits the model's direction. <bookmark mark='a'/> In America, "
            f"{P['w_first']:.0f} percent of women were in the labour force in {P['first_year']}. The share rose for "
            f"half a century, to {P['w_peak']:.0f} percent in {P['w_peak_year']}, and is {P['w_last']:.0f} percent "
            f"now. <bookmark mark='b'/> Men's fell, from {P['m_first']:.0f} to {P['m_last']:.0f}, as they stayed "
            "longer in school and retired earlier. <bookmark mark='c'/> In Becker's terms, women's wages rose, "
            "machines made housework take less time, and families had fewer children, which made time at home "
            "worth less and time at work worth more. <bookmark mark='d'/> Claudia Goldin, who won the Nobel prize "
            "in 2023 for this history, added what the model leaves out: rules that barred married women from many "
            "jobs, norms that changed slowly, and, as chapter six shows, the pill, which let women plan careers."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(w), FadeIn(side[0]), run_time=3.0)
            self.play(FadeIn(pk, scale=1.5))
            vo.wait_until("b")
            self.play(Create(m), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(w, color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(pk, color=WHITE, scale_factor=1.6))
        self.clear_scene()
