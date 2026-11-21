from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403

CHOICES = ("energy", "chips", "services", "retail")
LETTERS = ("A", "B", "C", "D")
COLS = (LINK, NODE, GDP, PEOPLE)


def pct_loss(x: float) -> float:
    """A change in log GDP as a percentage fall."""
    return 100 * (1 - np.exp(x))


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Play it: \ which failure costs most?", r"A disaster takes two fifths of one sector's "
             r"productivity for a year: \ which one should the Island fear most?",
             "Chapter three. Play it: which failure costs most?", scale=("market", "nation"), horizon=("a year",))
        self.stage()
        self.reveal()

    def stage(self):
        P = load("playit")
        T = load("table")
        names = T["sectors"]
        lam = {r["sector"]: r["domar"] for r in P["rows"]}
        up = dict(zip(names, T["upstreamness"]))
        links = dict(zip(names, P["links"]))
        facts = {
            "energy": rf"sells to all {links['energy']} sectors; \ {up['energy']:.1f} steps from households",
            "chips": rf"in every machine and car; \ sells to {links['chips']} sectors",
            "services": rf"the biggest seller: \ {lam['services']:.2f} per dollar of GDP",
            "retail": r"closest to the household: \ one step",
        }
        rows = VGroup(*[label(rf"{ltr} \ \ {s}: \ {facts[s]}", font_size=23, color=c)
                        for ltr, s, c in zip(LETTERS, CHOICES, COLS)]).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        rows.move_to(UP * 0.2)
        head = label(r"inputs are hard to replace for a year: \ elasticity of substitution 0.15", font_size=21,
                     color=GREY_A).to_edge(UP, buff=0.5)
        tag = island_tag(r"the Island: \ agora.network.which\_failure", corner=DL, font_size=12)
        with self.voiceover(
            "Your turn. A disaster takes two fifths of one sector's productivity for a year. For that year, firms "
            "cannot easily switch to other inputs. Which sector's failure should the Island fear most? <bookmark "
            "mark='a'/> A: energy, which sells to every sector and sits nearly three steps from the household. "
            "<bookmark mark='b'/> B: chips, which go into every machine and car. <bookmark mark='c'/> C: services, "
            "the biggest seller of all, mostly straight to households. <bookmark mark='d'/> D: retail, the last "
            "step before the household. <bookmark mark='e'/> Which costs the most GDP?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
            vo.wait_until("e")
        ring = countdown().scale(0.6).next_to(rows, DOWN, buff=0.5)
        self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=7.0, rate_func=linear)
        self.play(FadeOut(ring), Indicate(rows[2], color=WHITE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def reveal(self):
        P = load("playit")
        R = {r["sector"]: r for r in P["rows"]}
        loss = [pct_loss(R[s]["loss"]) for s in CHOICES]
        hult = [pct_loss(R[s]["hulten"]) for s in CHOICES]
        ax = plane([-0.6, 3.6], [0, 32], center=LEFT * 2.7 + DOWN * 0.3, x_length=6.6, y_length=4.8, xticks=[],
                   yticks=[0, 10, 20, 30], ylabel=r"GDP's fall for the year, \ \%", yfmt=lambda v: f"{v:.0f}",
                   font_size=15)
        b = bars(ax, range(4), loss, COLS, width=0.5)
        marks = VGroup(*[seg(ax, k - 0.32, h, k + 0.32, h, WHITE, 3.0) for k, h in enumerate(hult)])
        vl = VGroup(*[label(f"{v:.1f}", font_size=15, color=c).next_to(x, UP, buff=0.08)
                      for v, c, x in zip(loss, COLS, b)])
        labs = VGroup(*[label(rf"{ltr}: \ {s}", font_size=15, color=c).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.12)
                        for k, (ltr, s, c) in enumerate(zip(LETTERS, CHOICES, COLS))])
        e, s_ = CHOICES.index("energy"), CHOICES.index("services")
        side = VGroup(
            label(r"bars: \ the computed loss; \ white lines: \ Hulten's rule", font_size=19, color=WHITE),
            label(rf"C, \ services: \ {loss[s_]:.0f}\%, \ by far the most", font_size=20, color=GDP),
            label(rf"energy: \ {loss[e]:.1f}\%, \ nearly a third more than its sales predict", font_size=20,
                  color=LINK),
            label(r"sales decide the ranking; \\ hard-to-replace inputs add a premium upstream", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ CES technologies, \ elasticity 0.15; \ agora.network.which\_failure",
                         corner=DL, font_size=12)
        with self.voiceover(
            "Here is what the Island computes. <bookmark mark='a'/> The bars are the loss of GDP for the year; the "
            "white lines are what Hulten's rule predicts from each sector's sales alone. <bookmark mark='b'/> C. "
            f"Services cost {loss[s_]:.0f} percent of GDP, far more than any other, because they are by far the "
            "largest seller: the network's links do not rescue the upstream sectors from being smaller. <bookmark "
            f"mark='c'/> But look at energy. Its sales predict a loss of {hult[e]:.1f} percent; the model computes "
            f"{loss[e]:.1f}. When inputs are hard to replace, losing an input that everyone needs costs more than "
            "its sales share, and the gap grows with the size of the shock. <bookmark mark='d'/> So sales decide "
            "the ranking, and Hulten is a good first answer. The premium for being upstream and hard to replace is "
            "the second answer, and chapter five is about when it becomes the first."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(x, DOWN) for x in b], FadeIn(vl), FadeIn(side[0]))
            self.play(FadeIn(marks))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(b[s_], color=WHITE, scale_factor=1.0))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(b[e], color=WHITE, scale_factor=1.0))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
