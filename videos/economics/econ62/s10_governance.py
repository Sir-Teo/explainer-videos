from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


class Governance(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Agency and governance", r"When the owner is not the manager, \ who keeps the manager honest?",
             "Chapter eight. Agency and governance.", lit={1976: r"Jensen and Meckling", 2007: r"Bennedsen et al."},
             scale=("firm",), horizon=("a decade",))
        self.perks()
        self.watchers()

    def perks(self):
        P = load("perks")
        a, pk, val = np.array(P["alpha"]), np.array(P["perks"]), np.array(P["value"])
        ax = plane([0, 1], [0, 105], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.2, y_length=4.4,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 25, 50, 75, 100],
                   xlabel=r"the manager's share of the firm", ylabel=r"\$", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        pv = path(ax, a, val, OWN, 3.0)
        pp = path(ax, a, pk, COST, 3.0)
        side = VGroup(
            MathTex(r"\max_P\; \alpha\,(V - P) + k\ln(1 + P) \;\Rightarrow\; P = \frac{k}{\alpha} - 1", font_size=28,
                    color=WHITE),
            label(r"the manager owns a share $\alpha$ and enjoys perks $P$: \\ a jet, \ a grand office, \ a quiet "
                  r"life", font_size=19, color=GREY_A),
            label(r"red: \ perks; \ blue: \ what the firm is worth", font_size=19, color=COST),
            label(rf"own it all: \ perks {pk[-1]:.0f}; \ own 10\%: \ perks {np.interp(0.1, a, pk):.0f}", font_size=20,
                  color=WHITE),
            label(r"every dollar of perks costs the manager only $\alpha$ dollars: \\ the agency cost of selling "
                  r"shares to outsiders", font_size=19, color=OWN),
            label(r"the remedies: \ boards, \ large shareholders, \ takeovers, \ debt, \ pay tied to the share price",
                  font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = agora_tag(r"computed: \ agora.org.perks; \ a firm worth 100 before perks, \ k = 3", corner=DL,
                        font_size=12)
        with self.voiceover(
            "Michael Jensen and William Meckling's question in 1976: what happens when a firm's owner sells part of "
            "it and stays on as manager? <bookmark mark='a'/> The manager keeps a share alpha of the firm's value "
            "and enjoys perks: a jet, a grand office, a quiet life. <bookmark mark='b'/> Every dollar of perks "
            "costs the firm a dollar, but costs the manager only alpha dollars, so the manager takes perks until "
            "their value at the margin falls to alpha. <bookmark mark='c'/> Perks in red, the firm's value in "
            f"blue. <bookmark mark='d'/> Owning it all, the manager takes {pk[-1]:.0f}; owning ten percent, "
            f"{np.interp(0.1, a, pk):.0f}. <bookmark mark='e'/> The loss is the agency cost of separating ownership "
            "from control, and outside investors, knowing it, pay less for the shares. <bookmark mark='f'/> "
            "Corporate governance is the list of remedies: boards that can fire the manager, large shareholders "
            "who watch, the threat of a takeover, debt that must be paid, and pay tied to the share price."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(pp), Create(pv), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def watchers(self):
        cards = point_cards([
            (r"boards", r"directors chosen with the chief executive's help; \ stronger when independent and when a "
             r"large owner sits among them", OWN),
            (r"activists", r"investors who buy a stake to push for change: \ a board seat, \ a sale, \ a new "
             r"strategy", FIN),
            (r"family firms", r"Denmark: \ when a family member succeeds the chief executive, \ operating "
             r"profitability falls by at least four points \ (Bennedsen et al.)", COST),
            (r"the trick behind that number", r"the instrument: \ whether the departing CEO's first child was a "
             r"son, \ which makes a family successor likelier", MGR),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"who watches the manager", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Bennedsen, \ Nielsen, \ P\'erez-Gonz\'alez and Wolfenzon, \ QJE 122(2) (2007)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Who watches the manager in practice? <bookmark mark='a'/> Boards, though their members are often "
            "chosen with the chief executive's help; they are stronger when independent, and when a large owner "
            "sits among them, as chapter six's pay for luck showed. <bookmark mark='b'/> Activist investors, who "
            "buy a stake in order to push for change. <bookmark mark='c'/> And families, whose firms are most of "
            "the world's firms. Morten Bennedsen and colleagues studied Danish chief executive successions: when a "
            "family member took over, operating profitability fell by at least four percentage points. <bookmark "
            "mark='d'/> The trick behind that number is an instrument. Families that choose a successor are not "
            "random, so the authors used whether the departing chief executive's first child was a son, which "
            "makes a family successor likelier but has nothing else to do with the firm. Part four's tool, in "
            "the boardroom."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
