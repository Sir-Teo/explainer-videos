from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403

CASES = {"0.15": TARIFF, "0.20": PRICE, "0.30": FREE}


class Infant(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Industrial policy, \ the old case", r"When is it worth protecting an industry while it "
             r"learns?", "Chapter eight. Industrial policy, the old case.",
             lit={1791: "Hamilton", 1841: "List"}, scale=("nation", "firm"), horizon=("a decade",))
        self.history()
        self.learning()
        self.tests()

    def history(self):
        cards = VGroup(
            history_card(r"1791", r"Hamilton's \emph{Report on Manufactures}", r"a young country's industries "
                         r"cannot compete with Britain's established ones at first; \ protect and encourage them "
                         r"until they can", color=US, width=11.4, font_size=21),
            history_card(r"1841", r"List's \emph{National System}", r"Britain climbed the ladder behind tariffs, "
                         r"\ then preached free trade: \ it kicked away the ladder", color=ROW, width=11.4,
                         font_size=21),
            history_card(r"the economics", r"learning by doing", r"costs fall with cumulative output: \ a firm "
                         r"that produces today is cheaper tomorrow", color=STATE, width=11.4, font_size=21),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        with self.voiceover(
            "Industrial policy is older than free trade theory's victory. <bookmark mark='a'/> In 1791 Alexander "
            "Hamilton told Congress that a young country's manufacturers could not compete at first with Britain's "
            "established ones, and should be protected and encouraged until they could. <bookmark mark='b'/> Fifty "
            "years later Friedrich List added that Britain itself had climbed behind tariffs and then preached free "
            "trade, kicking away the ladder. <bookmark mark='c'/> The economics behind the argument is learning by "
            "doing: an industry's costs fall as it produces, so a firm that starts today is cheaper tomorrow."
        ) as vo:
            for mk, c in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def learning(self):
        I = load("infant")
        C = I["cases"]
        any_ = C["0.20"]
        prot, pw, tar = any_["protect"], any_["p_world"], any_["tariff"]
        ax = plane([0, 30], [0.5, 1.75], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.6, y_length=4.8,
                   xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[0.6, 0.8, 1.0, 1.2, 1.4, 1.6],
                   xlabel=r"years", ylabel=r"unit cost, \ world price = 1", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        world = seg(ax, 0, pw, 30, pw, GREY_B, 2.2, dashed=True)
        wl = label(r"the world price", font_size=14, color=GREY_B).next_to(ax.ax.c2p(24, pw), UP, buff=0.06)
        shield = seg(ax, 0, pw * (1 + tar), prot, pw * (1 + tar), TARIFF, 2.2, dashed=True)
        sl = label(rf"behind a {100 * tar:.0f}\% tariff, \ {prot} years", font_size=14, color=TARIFF).next_to(
            ax.ax.c2p(prot / 2, pw * (1 + tar)), UP, buff=0.06)
        end = vline(ax, prot, 0.5, 1.75, GREY_C)
        curves = {}
        for k, col in CASES.items():
            rows = C[k]["rows"]
            ts = [r["t"] for r in rows if r["t"] <= 30 and (r["t"] < prot or r["q"] > 0 or r["t"] == prot)]
            cs = [r["cost"] for r in rows if r["t"] in ts]
            curves[k] = path(ax, ts, cs, col, 3.0, smooth=False)
        key = legend_rows([(CASES[k], f"costs fall {100 * (1 - 2 ** -float(k)):.0f}% each time output doubles")
                           for k in CASES], font_size=14).next_to(
            ax.ax, RIGHT, buff=0.3).shift(UP * 1.4)
        if key.width > 4.4:
            key.scale_to_fit_width(4.4).next_to(ax.ax, RIGHT, buff=0.3).shift(UP * 1.4)
        tag = island_tag(r"a model: \ agora.tradewar.infant\_industry", corner=DL, font_size=12)
        with self.voiceover(
            "Here is a model of it. <bookmark mark='a'/> An industry starts with costs sixty percent above the world "
            f"price. Behind a {100 * tar:.0f} percent tariff for {prot} years, it can sell at home, and as it "
            "produces, its costs fall. After that the tariff goes, and it survives only if it can beat the world "
            "price. <bookmark mark='b'/> With slow learning, in red, costs fall, but not far enough: when the "
            "tariff goes, the industry dies. <bookmark mark='c'/> With faster learning, in gold, it just makes it. "
            "<bookmark mark='d'/> With fast learning, in green, it ends well below the world price, and exports."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(world), FadeIn(wl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(shield), FadeIn(sl), FadeIn(end))
            for mk, k in zip("bcd", CASES):
                vo.wait_until(mk)
                self.play(Create(curves[k]), FadeIn(key[list(CASES).index(k)]), run_time=1.8)
        self.clear_scene()

    def tests(self):
        I = load("infant")
        C = I["cases"]
        head = VGroup(label(r"learning", font_size=20, color=GREY_A), label(r"Mill's test", font_size=20,
                                                                           color=GREY_A),
                      label(r"Bastable's test", font_size=20, color=GREY_A)).arrange(RIGHT, buff=1.2)
        rows = VGroup()
        for k, col in CASES.items():
            c = C[k]
            m = r"passes" if c["mill"] else r"fails"
            b = r"passes" if c["bastable"] else r"fails"
            r = VGroup(label(rf"{100 * (1 - 2 ** -float(k)):.0f}\% per doubling", font_size=20, color=col),
                       label(m, font_size=20, color=FREE if c["mill"] else TARIFF),
                       label(rf"{b}: \ {c['pv_gain']:.2f} against {c['pv_cost']:.2f}", font_size=20,
                             color=FREE if c["bastable"] else TARIFF))
            rows.add(r)
        table = VGroup(head, *rows)
        for i, r in enumerate(table):
            for j, item in enumerate(r):
                item.move_to([(-5.2, -1.4, 1.6)[j], 2.0 - 0.65 * i, 0], aligned_edge=LEFT)
        notes = VGroup(
            label(r"Mill: \ the industry must survive without protection", font_size=19, color=GREY_A),
            label(r"Bastable: \ the discounted gains must exceed the discounted costs \ (here at 10\%)",
                  font_size=19, color=GREY_A),
            label(r"and a third test: \ if the learning stays in the firm, \ a bank should lend for it; \ policy "
                  r"is needed only if it spills over", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(table, DOWN, buff=0.6)
        tag = published_tag(r"Mill (1848); \ Bastable (1891); \ Baldwin, \ JPE 77(3) (1969)", corner=DL, font_size=12)
        with self.voiceover(
            "Economists have two old tests. <bookmark mark='a'/> John Stuart Mill's: the protected industry must "
            "eventually survive without protection. The slow learner fails it. <bookmark mark='b'/> Charles "
            "Bastable's is stricter: the gains, once the industry beats the world price, must outweigh the costs "
            "of protecting it while it learned, both discounted. The middle case survives, but at a ten percent "
            "discount rate its gains do not repay what it cost. Only the fast learner passes both. <bookmark "
            "mark='c'/> And Robert Baldwin added a third. If the learning stays inside the firm, the firm could "
            "borrow to pay for its early losses, and needs no tariff. Policy is justified only when the learning "
            "spills over, to other firms, workers or suppliers, which no lender can be repaid for. Which raises "
            "the empirical question: has it ever worked?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1][:2]), FadeIn(rows[2][:2]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(r[2]) for r in rows], FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.clear_scene()
