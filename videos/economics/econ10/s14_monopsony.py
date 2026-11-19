from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403

SUP = "#7EC8F5"
MCL = "#F2A65A"
MRP = "#7BD88F"


class Monopsony(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Monopsony: \ one employer", r"What happens when there is only one buyer, of labour?",
             "Chapter twelve. Monopsony: one employer.", lit={1933: r"Robinson names monopsony"},
             scale=("firm", "market"))
        self.diagram()

    def diagram(self):
        m = load("monopsony")
        ax = plane([0, 250], [0, 40], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.4, y_length=5.0,
                   xticks=[0, 50, 100, 150, 200, 250], yticks=[0, 10, 20, 30, 40], xlabel=r"shipwrights",
                   ylabel=r"\$ a day", font_size=17)
        a = ax.ax
        Ls = np.linspace(0, 250, 100)
        sup = path(ax, Ls, m["w0"] + m["slope"] * Ls, color=SUP, width=3.5, smooth=False, yr=(0, 40))
        mcl = path(ax, Ls, m["w0"] + 2 * m["slope"] * Ls, color=MCL, width=3.5, smooth=False, yr=(0, 40))
        mrp = DashedLine(a.c2p(0, m["mrp"]), a.c2p(250, m["mrp"]), color=MRP, stroke_width=2.5)
        mo, co, mn = m["monopsony"], m["competitive"], m["minimum"]
        Pm = Dot(a.c2p(mo["L"], mo["w"]), radius=0.09, color=SUP)
        Pc = Dot(a.c2p(co["L"], co["w"]), radius=0.08, color=GREY_A)
        mw = DashedLine(a.c2p(0, mn["w"]), a.c2p(250, mn["w"]), color=E.ACCENT, stroke_width=2)
        Pw = Dot(a.c2p(mn["L"], mn["w"]), radius=0.09, color=E.ACCENT)
        names = VGroup(label(r"labour supply", font_size=17, color=SUP).next_to(a.c2p(60, 10.5), DR, buff=0.05),
                       label(r"marginal cost of labour", font_size=17, color=MCL).next_to(a.c2p(165, 38), LEFT,
                                                                                         buff=0.1),
                       label(r"what a shipwright adds", font_size=17, color=MRP).next_to(a.c2p(4, 25), UR,
                                                                                         buff=0.06))
        side = VGroup(
            label(r"Crusoe's yard is the only employer: \\ to hire more he must raise everyone's wage", font_size=22),
            label(r"so an extra worker costs more than the wage", font_size=22, color=MCL),
            label(rf"he hires {mo['L']:.0f}, \ at \${mo['w']:.0f} a day, \ though each adds \${m['mrp']:.0f}", font_size=22,
                  color=SUP),
            label(rf"competition would hire {co['L']:.0f} at \${co['w']:.0f}", font_size=22, color=GREY_A),
            label(rf"a minimum wage of \${mn['w']:.0f}: \ {mn['L']:.0f} hired, \ at a higher wage", font_size=22,
                  color=E.ACCENT),
            label(r"in monopsony, \ a minimum wage can raise employment: \\ whether it does is Part 38's question",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Market power works on the buying side too. Joan Robinson called a single buyer a monopsonist. "
            "<bookmark mark='a'/> Suppose Crusoe's yard is the only employer on the Island, and to hire more "
            "shipwrights it must raise the wage, for everyone. <bookmark mark='b'/> So the cost of one more worker is "
            "more than the wage he is paid: it includes the raise for all the others. <bookmark mark='c'/> Crusoe "
            "hires where that marginal cost meets what a shipwright adds, twenty-five dollars a day: a hundred "
            "shipwrights, at fifteen dollars. <bookmark mark='d'/> A competitive labour market would employ two "
            "hundred, at twenty-five. <bookmark mark='e'/> Now impose a minimum wage of eighteen dollars. The "
            "yard no longer has to raise the wage to hire, so the marginal cost of a worker is just eighteen, and it "
            "hires a hundred and thirty: more workers, and higher pay. <bookmark mark='f'/> Whether real minimum "
            "wages do this is one of the great empirical questions of labour economics, in Part thirty-eight."
        ) as vo:
            self.play(FadeIn(ax), Create(sup), FadeIn(names[0]), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(mcl), FadeIn(names[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(mrp), FadeIn(names[2]), FadeIn(Pm), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(Pc), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(mw), FadeIn(Pw), FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()
