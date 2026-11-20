from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


class Accelerator(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The financial accelerator", r"Why does a firm's net worth change what it can invest?",
             "Chapter four. The financial accelerator.", lit={1979: r"Townsend", 1999: r"Bernanke, Gertler and "
                                                                                      r"Gilchrist"},
             scale=("firm", "nation"), horizon=("a year",))
        self.contract()
        self.premium()
        self.loop()

    def contract(self):
        B = load("bgg")
        rows = VGroup(
            label(r"a firm with net worth $N$ wants capital $K$; \ it borrows $K - N$", font_size=25, color=WHITE),
            label(r"its return is $\omega R^k K$, \ and only the firm sees $\omega$ for free", font_size=25,
                  color=HOUSE),
            label(r"a lender who wants to check \ (when the firm says it cannot pay) \ loses a share $\mu$ of what "
                  r"is left", font_size=23, color=CRISIS),
            label(r"the best contract: \ standard debt, \ with a premium over the safe rate", font_size=25,
                  color=RATE),
            label(rf"the Island's lenders: \ $\sigma = {B['sigma']:.2f}$, \ $\mu = {B['mu']:.2f}$: \ at leverage 2, \ "
                  rf"a premium of {100 * (B['at2']['premium'] - 1):.1f}\% \ and {100 * B['at2']['default']:.1f}\% "
                  r"of firms default", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Townsend, \ \emph{JET} 21(2) (1979); \ Bernanke, \ Gertler and Gilchrist, \ "
                            r"\emph{Handbook of Macroeconomics} 1C (1999)", corner=DR, font_size=12)
        head = label(r"borrowing when only the borrower sees the outcome", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.5)
        with self.voiceover(
            "Markets in which borrowers know more than lenders were the subject of Part thirteen. Here is the "
            "version that macroeconomics built on. <bookmark mark='a'/> A firm with net worth N wants capital K, so "
            "it borrows the difference. <bookmark mark='b'/> What the capital returns depends on luck, omega, which "
            "the firm sees and the lender does not. <bookmark mark='c'/> A lender can check, but only at a cost, "
            "a share mu of what is left, as in a bankruptcy. Robert Townsend showed in 1979 that the best contract "
            "is then ordinary debt: a fixed repayment, and an inspection only when the firm says it cannot pay. "
            "<bookmark mark='d'/> Because some firms do fail and checking them is costly, lenders charge a premium "
            "over the safe rate, and the premium is larger the more the firm borrows against its own stake. "
            "<bookmark mark='e'/> On the Island, with returns that vary as much as small firms' do and a "
            f"bankruptcy cost of {100 * B['mu']:.0f} percent, a firm that borrows as much as it owns pays "
            f"{100 * (B['at2']['premium'] - 1):.1f} percent over the safe rate, and "
            f"{100 * B['at2']['default']:.1f} percent of such firms default each year."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def premium(self):
        B = load("bgg")
        lev = np.array(B["leverage"])
        prem = 100 * (np.array(B["premium"]) - 1)
        ax = plane([1, 4], [0, 8], center=LEFT * 3.3 + DOWN * 0.4, x_length=5.6, y_length=4.4,
                   xticks=[1, 2, 3, 4], yticks=[0, 2, 4, 6, 8], xlabel=r"leverage, \ $K/N$",
                   ylabel=r"the premium, \ \% a year", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        curve = path(ax, lev, prem, RATE, 3.5, xr=(1, 4), yr=(0, 8))
        Ks = np.array(B["K"])
        ax2 = plane([1.5, 2.5], [1, 4], center=RIGHT * 3.3 + DOWN * 0.4, x_length=5.6, y_length=4.4,
                    xticks=[1.5, 2.0, 2.5], yticks=[1, 2, 3, 4], xlabel=r"capital, \ $K$",
                    ylabel=r"\% a year over the safe rate", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}",
                    font_size=14)
        dem = path(ax2, Ks, 100 * (np.array(B["demand"]) - 1), OUTPUT, 3.2, xr=(1.5, 2.5), yr=(1, 4))
        sup = path(ax2, Ks, 100 * (np.array(B["supply"]) - 1), RATE, 3.2, xr=(1.5, 2.5), yr=(1, 4))
        sup2 = path(ax2, Ks, 100 * (np.array(B["supply_low"]) - 1), CRISIS, 3.2, xr=(1.5, 2.5), yr=(1, 4))
        e0 = dot(ax2, B["base"]["K"], 100 * (B["base"]["premium"] - 1), WHITE)
        e1 = dot(ax2, B["low"]["K"], 100 * (B["low"]["premium"] - 1), CRISIS)
        k1 = label(r"the premium rises with leverage", font_size=17, color=RATE).next_to(ax, UP, buff=0.1)
        k2 = VGroup(label(r"green: \ what capital earns", font_size=16, color=OUTPUT),
                    label(r"pink: \ the premium at net worth 1", font_size=16, color=RATE),
                    label(rf"red: \ net worth {100 * B['N_fall']:.0f}\% lower", font_size=16, color=CRISIS)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).next_to(ax2, UP, buff=0.1)
        foot = label(rf"a {100 * B['N_fall']:.0f}\% loss of net worth cuts investment {abs(B['K_fall']):.1f}\%; \ "
                     r"without the friction, \ by nothing", font_size=22, color=WHITE).to_edge(DOWN, buff=0.3)
        tag = island_tag(corner=DR, font_size=13)
        with self.voiceover(
            "On the left, the premium against leverage, computed from the optimal contract. <bookmark mark='a'/> "
            "It is near zero for a firm that borrows little, and climbs as the firm's own stake shrinks. "
            "<bookmark mark='b'/> On the right, a firm deciding how much capital to hold. In green, what capital "
            "earns, falling as the firm adds more. In pink, what the firm must pay over the safe rate, given its net "
            "worth. It invests where they cross. <bookmark mark='c'/> Now a recession cuts its net worth by ten "
            "percent, with nothing else changed: same projects, same safe rate. Every level of capital now means "
            f"more leverage, so the premium curve shifts up, and investment falls {abs(B['K_fall']):.1f} percent. "
            "<bookmark mark='d'/> In a world without the friction, net worth would not matter at all: this is the "
            "Modigliani and Miller benchmark of Part twenty-three. With the friction, a firm's balance sheet is "
            "part of the economy's machinery."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ax2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(k1), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(dem), Create(sup), FadeIn(k2[:2]), FadeIn(e0), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(sup2), FadeIn(k2[2]), FadeIn(e1), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def loop(self):
        chain = flow_chain([(r"a loss: \ output or asset prices fall", CRISIS), (r"net worth falls", CREDIT),
                            (r"the premium rises", RATE), (r"investment and spending fall", OUTPUT),
                            (r"asset prices and profits fall further", HOUSE)], box_w=2.4, box_h=1.3, buff=0.45,
                           font_size=21).move_to(UP * 0.4)
        back = CurvedArrow(chain.boxes[-1].get_bottom() + DOWN * 0.1, chain.boxes[1].get_bottom() + DOWN * 0.1,
                           angle=-TAU / 6, color=CRISIS, stroke_width=3)
        lab = label(r"the accelerator: \ the loop runs again", font_size=22, color=CRISIS).next_to(back, DOWN,
                                                                                                 buff=0.15)
        top = label(r"the financial accelerator", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"in Bernanke, \ Gertler and Gilchrist's model, \ the loop makes shocks bigger and longer; \ "
                     r"in 2008 it ran through banks too", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Put that inside an economy and it becomes a loop. <bookmark mark='a'/> A loss, say a fall in output "
            "or in asset prices, <bookmark mark='b'/> lowers firms' net worth, <bookmark mark='c'/> which raises "
            "the premium they pay, <bookmark mark='d'/> which cuts investment and spending, <bookmark mark='e'/> "
            "which lowers profits and asset prices further, <bookmark mark='f'/> which lowers net worth again. Ben "
            "Bernanke, Mark Gertler and Simon Gilchrist built this into the New Keynesian model of Part thirty, and "
            "found that it makes shocks larger and longer-lived. In 2008 the same loop ran through the balance "
            "sheets of banks themselves."
        ) as vo:
            self.play(FadeIn(top))
            for mk, k in zip("abcde", range(5)):
                vo.wait_until(mk)
                anims = [FadeIn(chain.boxes[k], shift=RIGHT * 0.1)]
                if k:
                    anims.append(GrowArrow(chain.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("f")
            self.play(Create(back), FadeIn(lab))
            self.play(FadeIn(foot))
        self.clear_scene()
