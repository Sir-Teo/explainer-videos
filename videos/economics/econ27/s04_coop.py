from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class Coop(VoiceoverScene):
    def construct(self):
        card(self, 3, r"The co-op as a model", r"What sets how much a whole economy produces?", "Chapter three. The "
             "co-op as a model.", lit={1977: r"Sweeney and Sweeney", 1998: r"Krugman"}, scale=("market",),
             horizon=("weeks",))
        self.rules()
        self.curve()
        self.lessons()

    def rules(self):
        c = load("coop_path")
        rows = VGroup(
            label(r"Agora's co-op: \ the rules", font_size=28, color=E.ACCENT),
            label(rf"each couple wants {c['target']:.0f} coupons in reserve", font_size=23, color=SAVE),
            label(rf"at its reserve, \ it wants to go out on {100 * c['p']:.0f}\% of weeks; \ with fewer coupons, "
                  r"\ less often", font_size=23, color=SPEND),
            label(r"below its reserve it is keen to sit; \ above it, \ less and less keen", font_size=23, color=SAVE),
            label(r"an evening needs one couple going out and one sitting: \ evenings $=$ the shorter queue",
                  font_size=23, color=OUTPUT),
            label(r"the number of coupons never changes, \ unless the board prints", font_size=23, color=COUPON),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the co-op as Agora runs it. <bookmark mark='a'/> Each couple wants "
            f"{c['target']:.0f} coupons in reserve. <bookmark mark='b'/> A couple at its reserve wants to go out "
            f"in about {100 * c['p']:.0f} percent of weeks, and less often when it is short. "
            "<bookmark mark='c'/> Below its reserve, it is keen to sit; above it, less and less keen. "
            "<bookmark mark='d'/> An evening needs a couple going out and a couple sitting, so the number of "
            "evenings is set by the shorter queue. <bookmark mark='e'/> And the number of coupons in the co-op "
            "never changes, unless the board prints more. Notice what is not in the model: no couple is lazy, no "
            "sitter is unskilled, and nobody's taste for evenings out ever changes."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def curve(self):
        c = load("coop_curve")
        ax = plane([0, 24], [0, 0.32], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[0, 4, 8, 12, 16, 20, 24], yticks=[0, 0.1, 0.2, 0.3], xlabel=r"coupons per couple",
                   ylabel=r"per couple per week", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=16)
        go = path(ax, c["coupons"], c["goers"], color=SPEND, width=3)
        sit = path(ax, c["coupons"], c["sitters"], color=SAVE, width=3)
        ev = path(ax, c["coupons"], c["evenings"], color=OUTPUT, width=5)
        tgt = seg(ax, c["target"], 0, c["target"], 0.32, color=GREY_B, width=2, dashed=True)
        side = VGroup(
            label(r"want to go out", font_size=20, color=SPEND),
            label(r"willing to sit", font_size=20, color=SAVE),
            label(r"evenings: \ the shorter queue", font_size=21, color=OUTPUT),
            label(r"left: \ too few coupons, \\ everyone hoards: \ a recession", font_size=20, color=PRICE),
            label(r"right: \ too many, \\ nobody will sit: \ excess demand", font_size=20, color=HOLD),
            label(rf"best near {c['best']:.0f} a couple: \\ {c['best_evenings']:.2f} evenings", font_size=20,
                  color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now run the co-op with different amounts of money, from one coupon a couple to twenty-four, and watch "
            "a few years of weeks at each. <bookmark mark='a'/> In blue, the share of couples who want to go out "
            "each week. It rises with the coupons they hold. <bookmark mark='b'/> In violet, the share willing to "
            "sit. It falls as their reserves fill. <bookmark mark='c'/> In green, the evenings that actually "
            "happen: the shorter of the two queues. <bookmark mark='d'/> On the left, with too few coupons, "
            "everyone hoards and the co-op is in recession. More money raises output one for one with the "
            "willingness to spend. <bookmark mark='e'/> On the right, with too many coupons, nobody needs to sit, "
            "and evenings are scarce because sitters are: the co-op's version of an economy running too hot. "
            f"<bookmark mark='f'/> In between, near {c['best']:.0f} coupons a couple, it manages about "
            f"{c['best_evenings']:.2f} evenings a couple a week, as many as its members want. Output is set by "
            "demand on the left, and by capacity on the right."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(tgt), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(go), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(sit), FadeIn(side[1]), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(ev), FadeIn(side[2]), run_time=1.5)
            for mk, r_ in zip("def", side[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def lessons(self):
        rows = VGroup(
            label(r"three lessons the co-op teaches", font_size=28, color=E.ACCENT),
            label(r"1. \ \ a general glut is possible when people want to hold more money than there is",
                  font_size=23, color=SAVE),
            label(r"2. \ \ output can be set by spending, \ not by what the economy could produce", font_size=23,
                  color=OUTPUT),
            label(r"3. \ \ the cure need not be a change in anyone's character: \ more money will do", font_size=23,
                  color=COUPON),
            label(r"the real co-op first tried rules, \ obliging members to go out; \ more coupons worked",
                  font_size=21, color=GREY_A),
            label(r"and a co-op cannot cut the price of an evening: \ a real economy can, \ slowly (chapter 9)",
                  font_size=21, color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> First, a general glut is possible after all: when people want to "
            "hold more money than there is, they try to sell more than they buy, and everyone fails at once. "
            "<bookmark mark='b'/> Second, output can be set by spending, not by what the economy is able to "
            "produce. <bookmark mark='c'/> Third, the cure need not change anyone's character or skills. More money "
            "will do. <bookmark mark='d'/> The real co-op, by Krugman's account, first tried rules obliging members "
            "to go out, and recovered when more coupons were issued. <bookmark mark='e'/> One difference matters. "
            "The co-op fixed the price of an evening in coupons. In a real economy, prices and wages could fall, "
            "making each coupon worth more. Chapter nine asks why they fall so slowly."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
