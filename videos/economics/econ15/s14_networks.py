from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403

ACOL = "#7EC8F5"
BCOL = "#F29E8E"


class Networks(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Networks and ideas", r"When joining makes a network more valuable to everyone in it, \ and an "
             r"idea can be used by all, \ what does the market get wrong?", "Chapter twelve. Networks and ideas.",
             lit={1974: r"Rohlfs", 1985: r"Katz and Shapiro; David", 1989: r"Arthur",
                  1993: r"Jaffe, Trajtenberg and Henderson"}, scale=("market", "world"), horizon=("a decade",))
        self.networks()
        self.lockin()
        self.ideas()

    def networks(self):
        rows = VGroup(
            label(r"a telephone is worth more \ the more people you can call with it", font_size=25),
            label(r"so each new subscriber makes everyone else's phone more valuable, \ unpaid: \ a positive spillover",
                  font_size=23, color=GOOD),
            label(r"Jeffrey Rohlfs, \ 1974: \ demand for a network can have more than one equilibrium", font_size=23,
                  color=GREY_A),
            label(r"a small network nobody joins, \ or a large one everyone does: \ which you get depends on how it "
                  r"starts", font_size=23, color=DEMAND),
            label(r"the same for languages, \ payment systems, \ software, \ social media, \ plugs and rail gauges",
                  font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Rohlfs, Bell Journal 5(1) (1974); \ Katz and Shapiro, AER 75(3) (1985)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Some spillovers come from joining. <bookmark mark='a'/> A telephone is worth more the more people you "
            "can call with it. <bookmark mark='b'/> So each new subscriber makes everyone else's telephone more "
            "valuable, and is not paid for it: a positive spillover, which economists call a network externality. "
            "<bookmark mark='c'/> In 1974 Jeffrey Rohlfs showed that demand for a network can have more than one "
            "equilibrium. <bookmark mark='d'/> A small network that nobody wants to join, because it is small, or a "
            "large one that everyone joins, because it is large: which one you get depends on how it starts. "
            "<bookmark mark='e'/> The same goes for languages, payment systems, software, social media, and even "
            "electric plugs and the gauge of a railway."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def lockin(self):
        L = load("lockin")
        n = L["adopters"]
        xs = np.arange(1, n + 1)
        ax = plane([0, n], [-0.05, 1.05], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.4, y_length=4.6,
                   xticks=[0, 200, 400, 600, 800], yticks=[0, 0.5, 1], xlabel=r"adopters, \ in order of arrival",
                   ylabel=r"share of the last 50 choosing A", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}")
        lines = VGroup(*[path(ax, xs, rc, color=ACOL if w == "A" else BCOL, width=2, smooth=False)
                         for rc, w in zip(L["recent"], L["winners"])])
        for ln in lines:
            ln.set_stroke(opacity=0.8)
        nA = sum(1 for w in L["winners"] if w == "A")
        side = VGroup(
            label(r"two technologies, \ A and B; \\ half of adopters prefer each", font_size=21),
            label(r"each also gains from every earlier adopter \\ who chose the same", font_size=21, color=GOOD),
            label(r"once one leads by ten, \\ everyone after picks it: \ locked in", font_size=21, color=DEMAND),
            label(rf"in {len(L['winners'])} runs of the same world, \\ A wins {nA}, \ B wins {len(L['winners']) - nA}: "
                  r"\\ the winner is history's accident", font_size=21, color=E.ACCENT),
            label(r"QWERTY? \ Paul David said yes, 1985; \\ Liebowitz and Margolis disputed it, 1990", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Arthur, EJ 99 (1989); \ David, AER 75(2) (1985); \ Liebowitz and Margolis, JLE 33(1) "
                            r"(1990); \ the runs: \ Agora", corner=DR, font_size=12)
        with self.voiceover(
            "In 1989 Brian Arthur showed what this does when two standards compete. <bookmark mark='a'/> Adopters "
            "arrive one at a time, and half of them, by taste, prefer technology A, half B. "
            "<bookmark mark='b'/> But each adopter also gains from every earlier adopter who chose the same, because "
            "of the network. <bookmark mark='c'/> Early on, adopters follow their tastes. Once one technology leads "
            "by enough, ten adopters here, everyone after picks it, whatever their taste. The market has locked in. "
            "<bookmark mark='d'/> Agora ran the same world twelve times. Which technology won was decided by the luck "
            "of who came first. <bookmark mark='e'/> Whether real markets lock into worse standards is disputed. Paul "
            "David argued in 1985 that the QWERTY keyboard was one; Stan Liebowitz and Stephen Margolis replied that "
            "the evidence for a better layout was weak. Part forty-four comes back to platforms."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.15), FadeIn(side[2]), run_time=4)
            for mk, r in zip("de", side[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def ideas(self):
        rows = VGroup(
            label(r"an idea is non-rival: \ my using it doesn't use it up", font_size=25, color=POT),
            label(r"and hard to exclude: \ others learn from it, \ copy it, \ build on it", font_size=24,
                  color=GOOD),
            label(r"so research pays society more than it pays the firm that does it: \ too little is done",
                  font_size=24, color=SOCIAL),
            label(r"Adam Jaffe, \ Manuel Trajtenberg and Rebecca Henderson, \ 1993: \ patents cite patents from "
                  r"nearby", font_size=22, color=GREY_A),
            label(r"the remedies: \ patents, \ which exclude for a while; \ subsidies and public research",
                  font_size=24, color=E.ACCENT),
            label(r"part twenty-one makes ideas the engine of growth", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Jaffe, Trajtenberg and Henderson, QJE 108(3) (1993)", corner=DR, font_size=13)
        with self.voiceover(
            "The largest spillover of all may be ideas. <bookmark mark='a'/> An idea is non-rival: my using the "
            "Pythagorean theorem leaves it whole for you. <bookmark mark='b'/> And it is hard to exclude others from: "
            "they learn from it, copy it and build on it. <bookmark mark='c'/> So research pays society more than it "
            "pays the firm that does it, and the market does too little. <bookmark mark='d'/> The spillovers can be "
            "traced. In 1993 Adam Jaffe, Manuel Trajtenberg and Rebecca Henderson showed that patents cite earlier "
            "patents from the same city far more often than chance would predict: ideas travel, but best over short "
            "distances. <bookmark mark='e'/> The remedies are Pigou's and Coase's again: a patent creates a property "
            "right that excludes others for a while; research grants and public laboratories subsidize. "
            "<bookmark mark='f'/> Part twenty-one makes ideas the engine of growth."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
