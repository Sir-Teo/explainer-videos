from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403


class Persist(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Why bad institutions persist", r"Why would an elite ever give up power?",
             "Chapter nine. Why bad institutions persist.", lit={2000: r"Acemoglu and Robinson"}, scale=("nation",),
             horizon=("a century",))
        self.commitment()
        self.island()
        self.franchise()

    def commitment(self):
        chain = flow_chain([(r"an elite rules; \\ the many are poor", ELITE), (r"a crisis: \\ the poor could revolt",
                                                                               LOSS),
                            (r"the elite promises \\ to share", ELITE), (r"but promises end \\ with the crisis",
                                                                         HOLD)],
                           notes=[r"and could tax \\ the rich", r"a war, \ a slump, \\ a harvest failure",
                                  r"lower taxes on \\ the poor, \ schools", r"so the poor \\ do not believe them"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.9)
        foot = label(r"giving the poor the vote is a promise the elite cannot take back: \ it commits", font_size=22,
                     color=E.ACCENT).to_edge(DOWN, buff=1.0)
        tag = published_tag(tables.FRANCHISE_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Why do institutions that make most people poorer survive, and why do they sometimes change? Daron "
            "Acemoglu and James Robinson put the problem as one of commitment. <bookmark mark='a'/> An elite "
            "rules, and most people are poor. <bookmark mark='b'/> Now and then, in a war, a slump or a bad "
            "harvest, the poor could organize and overthrow it. <bookmark mark='c'/> The elite can promise to "
            "share: lower taxes for the poor, schools, land. <bookmark mark='d'/> But once the crisis passes, the "
            "elite holds power again and can take the promise back, and the poor know it. <bookmark mark='e'/> "
            "Extending the vote solves this. Once the poor can vote, redistribution no longer depends on the "
            "elite's word. That is why, they argue, elites in nineteenth-century Europe extended the franchise "
            "when the threat of unrest was high."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def island(self):
        F = load("franchise")
        ex = F["examples"]
        lo, hi = ex["0.1"], ex["0.9"]
        rows = [(r"revolution", lo["V_revolution"], LOSS), (r"promises, \\ crises rare", lo["V_promise"], ELITE),
                (r"promises, \\ crises frequent", hi["V_promise"], ELITE), (r"the vote", lo["V_democracy"], DEM)]
        ax = plane([0, 4], [0, 12], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.0, y_length=4.6, xticks=[],
                   yticks=[0, 3, 6, 9, 12], ylabel=r"what the poor expect, \ present value",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        bars = VGroup()
        for i, (nm, v, col) in enumerate(rows):
            p0, p1 = ax.ax.c2p(0.5 + i - 0.3, 0), ax.ax.c2p(0.5 + i + 0.3, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=14, color=WHITE).next_to(ax.ax.c2p(0.5 + i, 0), DOWN, buff=0.12),
                            label(rf"{v:.1f}", font_size=16, color=WHITE).next_to(r, UP, buff=0.05)))
        rev = DashedLine(ax.ax.c2p(0, lo["V_revolution"]), ax.ax.c2p(4, lo["V_revolution"]), color=LOSS,
                         stroke_width=1.6)
        side = VGroup(
            label(rf"the richest {100 * F['elite']:.0f}\% earn \\ {100 * F['elite_income']:.0f}\% of income",
                  font_size=18,
                  color=WHITE),
            label(r"a revolution costs \\ the poor 60\% of \\ the economy", font_size=18, color=LOSS),
            label(r"rare crises: \\ promises fall short, \\ so the elite extends \\ the vote", font_size=18,
                  color=DEM),
            label(r"frequent crises: \\ promises recur, \\ and suffice", font_size=18, color=ELITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Here it is on the Island. The richest {100 * F['elite']:.0f} percent earn "
            f"{100 * F['elite_income']:.0f} percent of income. <bookmark mark='a'/> A revolution would destroy "
            "sixty percent of the economy, but the poor would keep the rest, forever: the red line is what that is "
            "worth to them. <bookmark mark='b'/> If crises come one year in ten, the elite's promises, honoured "
            f"only during crises, are worth {lo['V_promise']:.1f}, less than revolution. <bookmark mark='c'/> If "
            f"crises come nine years in ten, the promises keep being renewed, and are worth {hi['V_promise']:.1f}, "
            f"enough. <bookmark mark='d'/> The vote, which makes redistribution permanent, is worth "
            f"{lo['V_democracy']:.1f}. So where crises are rare, an elite facing one must give up the vote to "
            "survive; where they are frequent, it can get by on promises. The paradox: it is the elite that is "
            "only occasionally threatened that democratizes."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), *[FadeIn(b[1]) for b in bars], run_time=1.0)
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][2]), Create(rev), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][2]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[3][0], DOWN), FadeIn(bars[3][2]), FadeIn(side[2]))
        self.clear_scene()

    def franchise(self):
        F = load("franchise")
        q, mu, grid = np.array(F["q"]), np.array(F["mu"]), np.array(F["grid"])
        ax = plane([0, 1], [0.4, 0.95], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.0, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0.4, 0.55, 0.7, 0.85],
                   xlabel=r"how often crises come, \ $q$", ylabel=r"how costly a revolution is, \ $\mu$",
                   xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        cols = {0: ELITE, 1: DEM, 2: LOSS}
        dq, dm = q[1] - q[0], mu[1] - mu[0]
        cells = VGroup()
        for i, m in enumerate(mu):
            for j, qq in enumerate(q):
                p0, p1 = ax.ax.c2p(qq - dq / 2, m - dm / 2), ax.ax.c2p(qq + dq / 2, m + dm / 2)
                cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0,
                                    fill_color=cols[int(grid[i][j])], fill_opacity=0.55).move_to((p0 + p1) / 2))
        side = VGroup(
            label(r"red: \ revolution", font_size=19, color=LOSS),
            label(r"green: \ the elite \\ extends the vote", font_size=19, color=DEM),
            label(r"purple: \ promises \\ are enough", font_size=19, color=ELITE),
            label(r"Britain extended the \\ vote in steps: \\ 1832, \ 1867, \ 1884", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The whole picture, across how often crises come and how costly a revolution is. <bookmark mark='a'/> "
            "Where revolution is cheap, nothing the elite can offer stops it. <bookmark mark='b'/> Where it is "
            "costlier, but crises are rare, the elite extends the vote. <bookmark mark='c'/> Where crises are "
            "frequent, or revolution very costly, promises are enough, and the old institutions survive. "
            "<bookmark mark='d'/> Acemoglu and Robinson read Britain's reform acts of 1832, 1867 and 1884, each "
            "passed amid unrest, this way. The model also explains why reforms that would make everyone richer "
            "are blocked: an elite that cannot be compensated credibly for what it would lose will resist them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.002), run_time=2.0)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
