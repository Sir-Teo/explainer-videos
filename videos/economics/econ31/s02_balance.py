from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Balance(VoiceoverScene):
    def construct(self):
        card(self, 1, r"The balance sheet: \ reserves, \ a corridor and a floor", r"How does a central bank set "
             r"an interest rate?", "Chapter one. The balance sheet: reserves, a corridor and a floor.",
             lit={1694: r"the Bank of England", 2008: r"interest on reserves"}, scale=("market", "nation"),
             horizon=("a day",))
        self.accounts()
        self.corridor()
        self.floor_()
        self.data()

    def accounts(self):
        cbk = tacct(r"the central bank", CB, [(r"government bonds", BOND), (r"loans to banks", CB)],
                    [(r"currency", PRICE), (r"reserves: \ banks' accounts", RES)], width=5.4)
        bank = tacct(r"a commercial bank", OUTPUT, [(r"reserves", RES), (r"loans", OUTPUT), (r"bonds", BOND)],
                     [(r"deposits", OUTPUT), (r"capital", GREY_B)], width=5.4)
        VGroup(cbk, bank).arrange(RIGHT, buff=1.0).move_to(UP * 0.9)
        arrow = Arrow(cbk.right[1].get_right() + RIGHT * 0.1, bank.left[0].get_left() + LEFT * 0.1, color=RES,
                      buff=0.05, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        rows = VGroup(
            label(r"reserves are the money banks pay each other with", font_size=22, color=RES),
            label(r"the overnight rate: \ what one bank charges another for reserves until tomorrow", font_size=22,
                  color=RATE),
            label(r"the central bank sets that price, \ because it alone can make more reserves", font_size=22,
                  color=CB),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Part 25; \ the Federal Reserve's H.4.1 statement", corner=DR, font_size=12)
        with self.voiceover(
            "Start with a central bank's balance sheet, as a T-account: what it owns on the left, what it owes on "
            "the right. It owns government bonds and loans to banks. It owes two kinds of money: currency, and "
            "reserves, which are the accounts banks keep with it. <bookmark mark='a'/> A commercial bank holds "
            "reserves as an asset, alongside its loans and bonds, and owes its depositors. <bookmark mark='b'/> "
            "Reserves are the money banks pay one another with. <bookmark mark='c'/> A bank short of reserves at "
            "the end of the day borrows them overnight from one that has spare, and the price of that loan is the "
            "overnight rate: in America, the federal funds rate. <bookmark mark='d'/> The central bank can set that "
            "price because it alone can create reserves, or take them away."
        ) as vo:
            self.play(FadeIn(cbk), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bank))
            vo.wait_until("b")
            self.play(Create(arrow), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def _axes(self):
        return plane([0, 400], [0, 3.6], center=LEFT * 2.0 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                     xticks=[0, 100, 200, 300, 400], yticks=[0, 1, 2, 3], xlabel=r"reserves in the system",
                     ylabel=r"overnight rate, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                     font_size=15)

    def corridor(self):
        R = load("reserves")
        C = R["curve"]
        ax = self._axes()
        dem = path(ax, C["R"], C["i"], RES, 3.5)
        ceil = seg(ax, 0, C["ceiling"], 400, C["ceiling"], RATE, 2, dashed=True)
        flo = seg(ax, 0, C["floor"], 400, C["floor"], CB, 2, dashed=True)
        cl = label(r"lending rate: \ the ceiling", font_size=16, color=RATE).next_to(ax.ax.c2p(400, C["ceiling"]), UP,
                                                                                    buff=0.08).shift(LEFT * 1.3)
        fl = label(r"rate paid on reserves: \ the floor", font_size=16, color=CB)
        fl.next_to(ax.ax.c2p(400, C["floor"]), UP, buff=0.08).shift(LEFT * 1.6)
        supply = seg(ax, C["corridor_R"], 0, C["corridor_R"], 3.6, PRICE, 3)
        pt = dot(ax, C["corridor_R"], C["corridor_i"], PRICE, 0.09)
        shift_ = seg(ax, C["corridor_R"] + 10, 0, C["corridor_R"] + 10, 3.6, PRICE, 2, dashed=True)
        new_i = float(cb.reserve_demand(C["corridor_R"] + 10, C["floor"], C["ceiling"], 50, 15))
        side = VGroup(
            label(r"blue: \ banks' demand for reserves", font_size=19, color=RES),
            label(r"no bank lends below the floor: \\ it can earn that at the central bank", font_size=19, color=CB),
            label(r"no bank pays above the ceiling: \\ it can borrow there", font_size=19, color=RATE),
            label(r"gold: \ reserves supplied, \ scarce: \\ a corridor", font_size=19, color=PRICE),
            label(rf"add 10 units: \ the rate falls \\ from {C['corridor_i']:.1f}\% to {new_i:.2f}\%", font_size=19,
                  color=PRICE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the market for reserves. <bookmark mark='a'/> The blue curve is banks' demand: the scarcer "
            "reserves are, the more a bank will pay to borrow them overnight. <bookmark mark='b'/> The central bank "
            "pays interest on reserves, here one percent, so no bank lends them for less: that is a floor. "
            "<bookmark mark='c'/> And it lends to any sound bank against collateral at three percent, so no bank "
            "pays more: a ceiling. <bookmark mark='d'/> Before 2008 the Federal Reserve kept reserves scarce, in "
            "the steep part of the curve, and set the rate within the corridor by adding or draining small amounts "
            f"every morning. <bookmark mark='e'/> Add ten units, and the rate falls from {C['corridor_i']:.0f} "
            f"percent to {say_num(new_i, 2)}."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(dem), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(flo), FadeIn(fl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ceil), FadeIn(cl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(supply), GrowFromCenter(pt), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(shift_), pt.animate.move_to(ax.ax.c2p(C["corridor_R"] + 10, new_i)), FadeIn(side[4]))
        self.clear_scene()

    def floor_(self):
        R = load("reserves")
        C = R["curve"]
        ax = self._axes()
        dem = path(ax, C["R"], C["i"], RES, 3.5)
        ceil = seg(ax, 0, C["ceiling"], 400, C["ceiling"], RATE, 2, dashed=True)
        flo = seg(ax, 0, C["floor"], 400, C["floor"], CB, 2, dashed=True)
        sup = seg(ax, C["floor_R"], 0, C["floor_R"], 3.6, PRICE, 3)
        sup2 = seg(ax, C["floor_R"] - 60, 0, C["floor_R"] - 60, 3.6, PRICE, 2, dashed=True)
        pt = dot(ax, C["floor_R"], C["floor_i"], PRICE, 0.09)
        lift = seg(ax, 0, C["floor"] + 0.75, 400, C["floor"] + 0.75, CB, 2.5, dashed=True)
        lifted = path(ax, C["R"], np.array(C["i"]) * 0 + np.maximum(np.array(C["i"]), C["floor"] + 0.75), RES, 2.2)
        side = VGroup(
            label(r"gold: \ reserves abundant: \ a floor", font_size=19, color=PRICE),
            label(r"the rate sits at the rate on reserves, \\ whatever the quantity", font_size=19, color=CB),
            label(r"to raise it: \ raise the rate paid \\ on reserves", font_size=19, color=CB),
            label(r"quantity and price come apart: \\ the balance sheet becomes \\ a separate tool", font_size=19,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now flood the system with reserves. <bookmark mark='a'/> On the flat part of the curve, banks have "
            "more than they need, <bookmark mark='b'/> and the overnight rate sits on the floor, the rate the "
            "central bank pays on reserves. Take a sixth of the reserves away, and nothing happens to the rate. "
            "<bookmark mark='c'/> To raise the rate, the central bank simply raises what it pays on reserves, and "
            "the market rate rises with it. <bookmark mark='d'/> In a floor system the quantity of reserves and the "
            "interest rate come apart. The rate is set by an announcement; the size of the balance sheet becomes a "
            "second, separate tool."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(dem), FadeIn(ceil), FadeIn(flo), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(sup), GrowFromCenter(pt), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            self.play(Create(sup2), run_time=0.8)
            vo.wait_until("c")
            self.play(Create(lift), Transform(dem, lifted), pt.animate.move_to(ax.ax.c2p(C["floor_R"],
                                                                                        C["floor"] + 0.75)),
                      FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def data(self):
        R = load("reserves")
        t = np.array(R["t"])
        ax = plane([2003, 2027], [0, 9.5], center=LEFT * 3.4 + DOWN * 0.3, x_length=5.8, y_length=4.6,
                   xticks=[2005, 2010, 2015, 2020, 2025], yticks=[0, 2, 4, 6, 8],
                   ylabel=r"trillions of dollars", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        ax2 = plane([2003, 2027], [0, 6], center=RIGHT * 3.4 + DOWN * 0.3, x_length=5.8, y_length=4.6,
                    xticks=[2005, 2010, 2015, 2020, 2025], yticks=[0, 2, 4, 6], ylabel=r"percent",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        assets = path(ax, t, R["assets"], CB, 3, smooth=False)
        res = path(ax, t, R["reserves"], RES, 3, smooth=False)
        ff = path(ax2, t, R["ff"], RATE, 3, smooth=False)
        ior = DashedVMobject(path(ax2, R["ior_t"], R["ior"], CB, 2.4, smooth=False), num_dashes=80)
        k1 = VGroup(label(r"green: \ the Fed's assets", font_size=16, color=CB),
                    label(r"blue: \ reserves", font_size=16, color=RES)).arrange(DOWN, aligned_edge=LEFT,
                                                                                buff=0.1)
        k1.next_to(ax, UP, buff=0.15)
        k2 = VGroup(label(r"pink: \ the federal funds rate", font_size=16, color=RATE),
                    label(r"dashed: \ the rate paid on reserves", font_size=16, color=CB)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax2, UP, buff=0.15)
        foot = label(rf"August 2008: \ reserves \${R['reserves_pre']:.0f} billion; \ "
                     rf"{R['reserves_peak_date'][:4]}: \ \${R['reserves_peak']:.1f} trillion", font_size=20,
                     color=E.ACCENT).to_edge(DOWN, buff=0.3)
        tag = data_tag(r"Federal Reserve Board: \ H.4.1 and H.15, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "This is what America did. <bookmark mark='a'/> Before the crisis the Federal Reserve's assets were "
            f"about {R['assets_pre']:.1f} trillion dollars, and banks' reserves were tiny: about "
            f"{R['reserves_pre']:.0f} billion dollars in August 2008. <bookmark mark='b'/> In October 2008 the Fed "
            "began paying interest on reserves, and then bought bonds on an enormous scale. Reserves peaked at "
            f"{R['reserves_peak']:.1f} trillion dollars in {R['reserves_peak_date'][:4]}. <bookmark mark='c'/> On the "
            "right, the federal funds rate, and the rate paid on reserves in dashes. Since 2008 the market rate has "
            "followed the administered rate, a little below it: the Federal Reserve moved from a corridor to a "
            "floor, and in 2019 said it would stay there."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ax2), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(assets), Create(res), FadeIn(k1), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(Create(ff), Create(ior), FadeIn(k2), run_time=2)
        self.clear_scene()
