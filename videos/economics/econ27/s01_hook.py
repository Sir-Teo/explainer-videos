from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.coop()
        self.island()
        self.question()
        self.title()
        self.objectives()

    def coop(self):
        rows = VGroup(
            label(r"Capitol Hill, \ Washington, \ the 1970s", font_size=30, color=E.ACCENT),
            label(r"about 150 young couples run a babysitting co-operative", font_size=24, color=GREY_A),
            label(r"an evening of sitting is paid in coupons, \ the co-op's own money", font_size=24, color=COUPON),
            label(r"couples want a reserve of coupons for the evenings they will need later", font_size=24,
                  color=SAVE),
            label(r"so they stay in, \ and offer to sit", font_size=24, color=SAVE),
            label(r"nobody goes out, \ so nobody can earn: \ the co-op has a recession", font_size=26, color=PRICE),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Sweeney and Sweeney, \ JMCB 9(1) (1977): \ 86--89; \ retold by Krugman (1998)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "On Capitol Hill in Washington, in the 1970s, about a hundred and fifty young couples ran a "
            "babysitting co-operative. <bookmark mark='a'/> Instead of paying each other in dollars, they paid in "
            "coupons, the co-op's own money: sit for another couple's children, and you earn coupons; go out for an "
            "evening, and you pay them. <bookmark mark='b'/> Couples liked to keep a reserve of coupons for the "
            "evenings they would need later. <bookmark mark='c'/> So, to build up their reserves, they stayed in "
            "and offered to sit. <bookmark mark='d'/> But if everyone wants to sit, nobody is going out, and "
            "nobody can earn anything. The co-op had a recession: a whole economy with willing workers, willing "
            "customers and nothing broken, except that hardly anyone was buying."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def island(self):
        c = load("coop_path")
        ax = plane([0, c["weeks"]], [0, 0.3], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[0, 50, 100, 150, 200], yticks=[0, 0.1, 0.2, 0.3], xlabel=r"week",
                   ylabel=r"evenings out, \ per couple per week", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=16)
        pot = seg(ax, 0, c["potential"], c["weeks"], c["potential"], color=OUTPUT, width=2, dashed=True)
        before = path(ax, c["weeks_"][:c["print_at"]], c["smooth"][:c["print_at"]], color=PRICE, width=3,
                      smooth=False)
        after = path(ax, c["weeks_"][c["print_at"] - 1:], c["smooth"][c["print_at"] - 1:], color=OUTPUT, width=3,
                     smooth=False)
        printed = seg(ax, c["print_at"], 0, c["print_at"], 0.3, color=COUPON, width=2, dashed=True)
        side = VGroup(
            label(rf"the Island's co-op: \ {c['n']} couples, \\ each wanting {c['target']:.0f} coupons in reserve",
                  font_size=19, color=GREY_A),
            label(rf"with {c['start']:.0f} coupons a couple: \\ {c['before']:.2f} evenings a week", font_size=20,
                  color=PRICE),
            label(rf"week {c['print_at']}: \ the board prints, \\ to {c['print_to']:.0f} a couple", font_size=20,
                  color=COUPON),
            label(rf"then: \ {c['after']:.2f}, \\ close to the most it can do", font_size=20, color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island has a co-op too, and Agora can run it. <bookmark mark='a'/> A hundred and fifty couples, "
            f"each wanting {c['target']:.0f} coupons in reserve. The dashed line is how many evenings out it could "
            f"manage if everyone were happy with their reserve. <bookmark mark='b'/> It starts with only "
            f"{c['start']:.0f} coupons a couple, and it manages about {c['before']:.2f} evenings a couple each week, "
            f"barely half of what it could. <bookmark mark='c'/> In week {c['print_at']}, the board prints more "
            f"coupons, up to {c['print_to']:.0f} a couple. <bookmark mark='d'/> Evenings out rise to about "
            f"{c['after']:.2f}. Nobody became more skilful or more willing. The co-op simply had too little money "
            "for what its members wanted to hold, and more money cured it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(pot), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(before), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(printed), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(after), FadeIn(side[3]), run_time=2)
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why does output fall when nothing has destroyed the capacity to produce?", font_size=26,
                  color=PRICE),
            label(r"why do prices and wages not simply fall until everyone is employed?", font_size=26,
                  color=RATE),
            label(r"and what can a government or a central bank do about it?", font_size=26, color=GOV),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "In the 1930s the whole world asked the co-op's question. How can a whole economy be short of buyers? "
            "<bookmark mark='a'/> Why does output fall when no war or flood has destroyed the capacity to produce "
            "it? <bookmark mark='b'/> Why do prices and wages not simply fall until everyone who wants work has it? "
            "<bookmark mark='c'/> And what, if anything, can a government or a central bank do about it?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        c = load("coop_curve")
        mini = plane([0, 24], [0, 0.25], x_length=4.2, y_length=1.6)
        logo = VGroup(path(mini, c["coupons"], c["evenings"], COUPON, width=3),
                      path(mini, c["coupons"], c["sitters"], SAVE, width=2))
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 27 \ $\cdot$ \ The Keynesian Revolution", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part twenty-seven: the Keynesian revolution."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VI \ $\cdot$ \ Money and the Cycle", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"the Depression in data; \ hoard or spend? \ you choose; \ the co-op as a model",
            r"Keynes: \ effective demand, \ the multiplier, \ the paradox of thrift",
            r"IS--LM derived; \ the liquidity trap; \ Phillips's water machine",
            r"why wages do not fall; \ aggregate demand and supply",
            r"what ended the Depression; \ the critics; \ two dials; \ forecasting; \ supply shocks that cut demand",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> The Great Depression in the data, a choice for you, hoard or "
            "spend, and the co-op as a model of a whole economy. <bookmark mark='b'/> Then Keynes's answer: "
            "effective demand, the multiplier, and the paradox of thrift. <bookmark mark='c'/> The diagram that "
            "turned the book into a tool, the trap at zero interest, and a machine that ran the economy in "
            "coloured water. <bookmark mark='d'/> Why wages do not fall, and how demand and supply fit together. "
            "<bookmark mark='e'/> And what actually ended the Depression, Keynes's critics, two dials, the "
            "forecasting desk, and the newest twist: supply shocks that cut demand by more than themselves."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
