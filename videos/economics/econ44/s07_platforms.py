from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class Platforms(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Two-sided markets", r"Who should pay on a platform?",
             "Chapter six. Two-sided markets.", lit={2003: r"Rochet and Tirole", 2006: r"Armstrong"},
             scale=("firm", "market"), horizon=("a year",))
        self.examples()
        self.model()
        self.prices()
        self.antitrust()

    def examples(self):
        rows = VGroup()
        for left, plat, right, col in ((r"cardholders", r"a card network", r"merchants", FIRM1),
                                       (r"readers", r"a newspaper", r"advertisers", FIRM2),
                                       (r"players", r"a games console", r"game studios", PATIENT),
                                       (r"riders", r"a ride-hailing app", r"drivers", BUS)):
            a = label(left, font_size=21, color=FIRM1)
            b = RoundedRectangle(width=3.2, height=0.6, corner_radius=0.1, stroke_color=col, stroke_width=2,
                                 fill_color="#141821", fill_opacity=1)
            bl = label(plat, font_size=20, color=WHITE).move_to(b)
            c = label(right, font_size=21, color=FIRM2)
            g = VGroup(a, VGroup(b, bl), c).arrange(RIGHT, buff=0.9)
            arr = VGroup(DoubleArrow(a.get_right(), b.get_left(), buff=0.1, stroke_width=2, color=GREY_B,
                                     tip_length=0.15),
                         DoubleArrow(b.get_right(), c.get_left(), buff=0.1, stroke_width=2, color=GREY_B,
                                     tip_length=0.15))
            rows.add(VGroup(g, arr))
        rows.arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        head = label(r"platforms bring two groups together", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"each side values the other: \ the more merchants accept a card, \ the more it is worth "
                     r"carrying", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.55)
        tag = published_tag(tables.PLATFORMS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Some firms sell not a product but a meeting place. <bookmark mark='a'/> A card network brings "
            "cardholders and merchants together; <bookmark mark='b'/> a newspaper, readers and advertisers; "
            "<bookmark mark='c'/> a games console, players and studios; <bookmark mark='d'/> a ride-hailing app, "
            "riders and drivers. <bookmark mark='e'/> Each side values the other. The more merchants accept a card, "
            "the more it is worth carrying, and the more people carry it, the more it is worth accepting. "
            "Jean-Charles Rochet and Jean Tirole called these two-sided markets: what matters is not only the total "
            "price the platform charges, but how it is split between the two sides."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def model(self):
        P = TRUTH["platform"]
        lines = VGroup(
            MathTex(r"n_1 = a_1 + \alpha_1\, n_2 - p_1, \qquad n_2 = a_2 + \alpha_2\, n_1 - p_2", font_size=38),
            MathTex(r"\max_{p_1, p_2}\; (p_1 - c_1)\, n_1 + (p_2 - c_2)\, n_2", font_size=38, color=GREY_A),
            MathTex(r"p_1 \;=\; c_1 \;+\; \text{markup}_1 \;-\;", r"\alpha_2\, n_2", font_size=42, color=E.ACCENT),
        ).arrange(DOWN, buff=0.55).move_to(UP * 1.0)
        lines[2][1].set_color(FIRM2)
        notes = VGroup(
            label(r"$\alpha_1$: \ what a member of side 1 gains from each member of side 2", font_size=19,
                  color=FIRM1),
            label(r"$\alpha_2 n_2$: \ what side 1's members are worth to side 2, \ given back to them in a lower "
                  r"price", font_size=19, color=FIRM2),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Armstrong (2006), \ linear version; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Mark Armstrong's version makes the logic plain. <bookmark mark='a'/> Each side's membership rises with "
            "the size of the other side, at rate alpha, and falls with its own price. <bookmark mark='b'/> A "
            "monopoly platform chooses both prices to maximize its profit. <bookmark mark='c'/> The answer: each "
            "side pays its cost plus a markup, minus what its members are worth to the other side. A member of "
            "side one brings value alpha two to every member of side two, and the platform hands that value back "
            "as a lower price, because attracting side one is how it sells to side two."
        ) as vo:
            self.play(Write(lines[0]), FadeIn(tag), FadeIn(notes[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Write(lines[1]))
            vo.wait_until("c")
            self.play(Write(lines[2]), FadeIn(notes[1]))
        del P
        self.clear_scene()

    def prices(self):
        Pl = load("platform")
        al = np.array(Pl["alpha2"])
        ax = plane([0, 1.2], [-0.4, 1.4], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.3, 0.6, 0.9, 1.2], yticks=[-0.4, 0, 0.4, 0.8, 1.2],
                   xlabel=r"$\alpha_2$: \ side 1's value to each member of side 2", ylabel=r"price \ (cost 0)",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        zero = seg(ax, 0, 0, 1.2, 0, GREY_B, 1.6, dashed=True)
        l1 = path(ax, al, Pl["p1"], FIRM1, 3.2)
        l2 = path(ax, al, Pl["p2"], FIRM2, 3.2)
        side = VGroup(
            label(rf"side 1 values side 2 \\ at $\alpha_1$ = {Pl['alpha1']}", font_size=18, color=GREY_A),
            label(r"gold: \ side 1's price \\ falls as side 1 \\ becomes more valuable", font_size=18, color=FIRM1),
            label(r"blue: \ side 2 pays \\ more", font_size=18, color=FIRM2),
            label(r"beyond $\alpha_2$ = 1: \\ side 1 is paid \\ to join", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now let side one become more valuable to side two. <bookmark mark='a'/> Side one itself values side "
            f"two only a little, at {Pl['alpha1']}. <bookmark mark='b'/> As alpha two rises, side one's price "
            "falls, <bookmark mark='c'/> and side two's rises: the platform charges the side that gains the most. "
            "<bookmark mark='d'/> Past a point, side one's price turns negative: the platform pays it to join, as "
            "card networks pay rewards to cardholders out of the fees merchants pay, and newspapers give papers "
            "away to win advertisers. A price below cost on one side is not, by itself, a sign of predation."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(side[1]), run_time=1.8)
            vo.wait_until("c")
            self.play(Create(l2), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(l1, color=WHITE, scale_factor=1.0))
        self.clear_scene()

    def antitrust(self):
        cards = point_cards([
            (r"market definition", r"one market or two? \\ in 2018 the Supreme \\ Court treated a card \\ "
                                   r"network as one \\ (\emph{Ohio v. Amex})", FIRM1),
            (r"pricing tests", r"a price below cost \\ on one side can \\ be efficient", FIRM2),
            (r"evidence", r"Rysman: \ Yellow Pages \\ readers value ads, \\ advertisers value \\ readers", PATIENT),
            (r"competition", r"rival platforms fight \\ for the side that \\ others follow", BUS),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.1)
        head = label(r"what changes for antitrust", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.PLATFORMS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "This changes antitrust. <bookmark mark='a'/> Is a card network one market or two? In Ohio against "
            "American Express, in 2018, the Supreme Court treated it as one, so harm to merchants had to be weighed "
            "against benefits to cardholders. <bookmark mark='b'/> Pricing tests built for one-sided firms "
            "mislead: a price below cost on one side can be efficient. <bookmark mark='c'/> The effects are real "
            "and measurable: Marc Rysman found that Yellow Pages readers valued advertising and advertisers valued "
            "readers. <bookmark mark='d'/> And rival platforms fight hardest for the side the other side follows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
