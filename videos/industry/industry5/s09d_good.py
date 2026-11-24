from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403


class Good(VoiceoverScene):
    def construct(self):
        card(self, 14, "Good for whom?", "Is a moat a reward for something better, or a toll on customers?",
             "Chapter fourteen. Good for whom?", lit=("moat", "who"))
        beam = Line(LEFT * 3.2, RIGHT * 3.2, stroke_color=STONE, stroke_width=6).move_to([0, 0.9, 0])
        post = Polygon([-0.35, -1.3, 0], [0.35, -1.3, 0], [0, 0.85, 0], stroke_width=0, fill_color=STONE,
                       fill_opacity=0.9)
        left_pan = VGroup(Line([-3.2, 0.9, 0], [-3.2, 0.1, 0], stroke_color=GREY_B, stroke_width=2),
                          Arc(radius=0.9, start_angle=PI, angle=PI, stroke_color=GREY_B, stroke_width=3).move_to(
                              [-3.2, -0.25, 0]))
        right_pan = left_pan.copy().shift(RIGHT * 6.4)
        scale = VGroup(beam, left_pan, right_pan)
        left_t = VGroup(tx("a reward", 26, RET, bold=True), tx("for being better or cheaper", 17, GREY_B)).arrange(
            DOWN, buff=0.06).move_to([-3.2, 2.1, 0])
        right_t = VGroup(tx("a toll", 26, COST_, bold=True), tx("charged because no one else can enter", 17, GREY_B)
                         ).arrange(DOWN, buff=0.06).move_to([3.2, 2.1, 0])
        goods = VGroup(tx("See's: chocolates people choose", 16, RET), tx("Costco: prices no one can beat", 16, RET),
                       tx("a patent: an invention, published", 16, RET)).arrange(DOWN, aligned_edge=LEFT,
                                                                                buff=0.08).move_to([-3.2, -1.9, 0])
        bads = VGroup(tx("a licence nobody else can get", 16, COST_), tx("a merger that removes the last rival", 16,
                                                                          COST_),
                      tx("customers locked in, then charged more", 16, COST_)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.08).move_to([3.2, -1.9, 0])
        weights = [Circle(radius=0.22, stroke_width=0, fill_color=RET, fill_opacity=0.9).move_to([-3.2, -0.4, 0]),
                   Circle(radius=0.22, stroke_width=0, fill_color=COST_, fill_opacity=0.9).move_to([3.2, -0.4, 0])]
        q = tx("The same high return can mean either.", 24, GOLD, bold=True).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Is a moat good for the rest of us? <bookmark mark='a'/> Weigh it up. On one side, a high return can be "
            "a reward for being better or cheaper. See's sells chocolates people choose to pay for. Costco's moat "
            "is that nobody can match its prices, which is a moat its customers are glad of. A patent rewards an "
            "invention in exchange for publishing how it works, so that others can use it when the patent runs "
            "out. <bookmark mark='b'/> On the other side, a high return can be a toll, charged only because no one "
            "else is allowed in or can get in: a licence the government hands to a few, a merger that removes the "
            "last real rival, customers locked in and then charged more. <bookmark mark='c'/> The accounts alone "
            "cannot tell the two apart. The same thirty percent return on capital can come from either. That is why "
            "competition authorities look not just at profits but at how they are earned, and why the same "
            "question, reward or toll, comes back in this series' parts on platforms, on medicines and on the "
            "industries that governments license."
        ) as vo:
            self.play(FadeIn(post), Create(scale))
            vo.wait_until("a")
            self.play(FadeIn(left_t), FadeIn(weights[0], shift=DOWN * 0.4))
            self.play(Rotate(VGroup(scale, weights[0]), angle=0.08, about_point=[0, 0.9, 0]))
            self.play(LaggedStart(*[FadeIn(g_) for g_ in goods], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("b")
            weights[1].move_to(right_pan[1].get_center() + DOWN * 0.15)
            self.play(FadeIn(right_t), FadeIn(weights[1], shift=DOWN * 0.4))
            self.play(Rotate(VGroup(scale, *weights), angle=-0.08, about_point=[0, 0.9, 0]))
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bads], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(q, shift=DOWN * 0.1))
        self.clear_scene()
        self.tests()

    def tests(self):
        rows = [("Could a newcomer get in?", "a reward survives a rival's attempt; a toll needs the door kept shut",
                 VGroup(draw.castle(0.6, color=STONE), draw.person(0.45, color=ENTRANT)).arrange(RIGHT, buff=0.1)),
                ("Are prices falling, or quality rising?", "a reward is usually shared with customers over time",
                 VGroup(Arrow(UP * 0.3, DOWN * 0.3, color=RET, buff=0, stroke_width=5), draw.coin(0.16)).arrange(
                     RIGHT, buff=0.1)),
                ("Would customers leave if they could?", "a reward keeps them by choice; a toll by lock-in",
                 VGroup(draw.crowd(4, 0.35, color=STONE, cols=4))),
                ("Where does the money go?", "into new products and lower costs, or into keeping rivals out",
                 VGroup(draw.factory(0.7, color=GREY_B), draw.coin(0.14)).arrange(RIGHT, buff=0.1))]
        cards = VGroup()
        for head, sub, pic in rows:
            pic.scale_to_fit_height(min(pic.height, 0.7))
            t_ = VGroup(tx(head, 23, WHITE, bold=True), tx(sub, 17, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            cards.add(VGroup(pic, t_).arrange(RIGHT, buff=0.4))
        cards.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.3, 0])
        for c_ in cards:
            c_[0].move_to([cards.get_left()[0] + 0.5, c_.get_y(), 0])
            c_[1].next_to(c_[0], RIGHT, buff=0.4).align_to(cards[0][1], LEFT)
        head = tx("Four questions that tell a reward from a toll", 26, GOLD, bold=True).to_edge(UP, buff=0.5)
        with self.voiceover(
            "So how do you tell them apart? Four questions help, and they are the ones competition authorities ask. "
            "<bookmark mark='a'/> Could a newcomer get in? A business that earns a reward can usually survive a "
            "rival's attempt to copy it; a toll depends on keeping the door shut. <bookmark mark='b'/> Are prices "
            "falling, or quality rising? A reward tends to be shared with customers over time, as costs fall. "
            "<bookmark mark='c'/> Would customers leave if they could? A business that keeps its customers by "
            "choice is earning a reward; one that keeps them by locking them in is charging a toll. "
            "<bookmark mark='d'/> And where does the money go: into new products and lower costs, or into lawyers, "
            "lobbying and buying up rivals before they grow?"
        ) as vo:
            self.play(FadeIn(head))
            for c_, m in zip(cards, "abcd"):
                vo.wait_until(m)
                self.play(FadeIn(c_[0], scale=0.8), FadeIn(c_[1], shift=RIGHT * 0.15))
        self.clear_scene()
