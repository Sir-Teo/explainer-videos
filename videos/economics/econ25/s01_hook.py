from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403

STONE = "#C8C2B4"


def rai(radius: float = 0.6) -> VGroup:
    """A stone wheel of Yap: a limestone disc with a hole for the carrying pole."""
    disc = Annulus(inner_radius=radius * 0.22, outer_radius=radius, fill_color=STONE, fill_opacity=0.9,
                   stroke_color=GREY_B, stroke_width=2)
    return VGroup(disc)


class Hook(VoiceoverScene):
    def construct(self):
        self.yap()
        self.seabed()
        self.basement()
        self.question()
        self.title()
        self.objectives()

    def yap(self):
        stones = VGroup(rai(0.9), rai(0.6), rai(1.2), rai(0.5)).arrange(RIGHT, buff=0.6, aligned_edge=DOWN)
        stones.move_to(UP * 1.0)
        ground = Line(LEFT * 6.5, RIGHT * 6.5, color=GREY_D, stroke_width=2).next_to(stones, DOWN, buff=0.05)
        rows = VGroup(
            label(r"Yap, \ in the western Pacific, \ around 1900", font_size=28, color=E.ACCENT),
            label(r"the money: \ wheels of limestone quarried on Palau, \ hundreds of miles away, \ some taller than "
                  r"a person", font_size=22, color=GREY_A),
            label(r"too heavy to move: \ when one is spent, \ it stays where it is, \ and everyone remembers who "
                  r"owns it", font_size=22, color=MONEY),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Furness, \emph{The Island of Stone Money} (1910); \ Friedman, Hoover WP E-91-3 (1991)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "In 1903 an American doctor, William Henry Furness, visited the island of Yap in the western Pacific. "
            "<bookmark mark='a'/> Its money was stone: wheels of limestone, quarried on Palau hundreds of miles away "
            "and brought back by canoe and raft, some of them taller than a person. <bookmark mark='b'/> The big ones "
            "were too heavy to move. When one changed hands, it stayed where it was. Everyone simply remembered "
            "who owned it now."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.2) for s_ in stones], lag_ratio=0.2), Create(ground),
                      FadeIn(rows[0]), FadeIn(tag), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def seabed(self):
        sea = Rectangle(width=14.5, height=3.6, fill_color="#123A5A", fill_opacity=0.55, stroke_width=0)
        sea.move_to(DOWN * 1.6)
        waves = VGroup(*[Arc(radius=0.35, start_angle=PI, angle=-PI, color=FISH, stroke_width=2).move_to(
            [-6.5 + 0.7 * k, sea.get_top()[1], 0]) for k in range(20)])
        raft = Rectangle(width=2.0, height=0.25, fill_color=COCO, fill_opacity=0.9, stroke_width=0).move_to(
            sea.get_top() + UP * 0.2 + LEFT * 2.5)
        stone = rai(0.8).move_to(raft.get_top() + UP * 0.8)
        rows = VGroup(
            label(r"a great stone was lost overboard in a storm, \ on the way home from Palau", font_size=22,
                  color=GREY_A),
            label(r"its owners' family was still counted among the richest on the island", font_size=24,
                  color=MONEY),
            label(r"when German officials wanted the paths repaired, \ they painted black crosses on the most "
                  r"valuable stones", font_size=21, color=PRICE),
            label(r"the islanders went to work; \ when the crosses were removed, \ they were rich again",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22).to_edge(UP, buff=0.4)
        cross = VGroup(Line(UL * 0.35, DR * 0.35, color=BLACK, stroke_width=10),
                       Line(UR * 0.35, DL * 0.35, color=BLACK, stroke_width=10))
        other = rai(0.7).move_to(RIGHT * 3.5 + UP * 0.6)
        cross.move_to(other)
        with self.voiceover(
            "Furness was told a stranger story. <bookmark mark='a'/> Generations earlier, a great stone had been lost "
            "overboard in a storm, on the way home from Palau. It sank to the bottom of the sea. "
            "<bookmark mark='b'/> Its owners' family was still counted among the richest on the island. Nobody had "
            "seen the stone for years, but everyone agreed it was theirs, and it could still be spent. "
            "<bookmark mark='c'/> When Yap became a German colony, the officials wanted the island's paths repaired, "
            "and nobody would do it. So they painted black crosses on the most valuable stones, to show the "
            "government had claimed them. <bookmark mark='d'/> The islanders went to work at once. When the paths "
            "were done, the crosses were removed, and everyone was rich again."
        ) as vo:
            self.play(FadeIn(sea), Create(waves), FadeIn(raft), FadeIn(stone), FadeIn(rows[0]), FadeIn(other),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(stone.animate.move_to(sea.get_center() + DOWN * 0.9 + LEFT * 2.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(cross))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeOut(cross))
        self.clear_scene()

    def basement(self):
        rows = VGroup(
            label(r"Milton Friedman, \ 1991: \ is that so different from us?", font_size=27, color=E.ACCENT),
            label(r"in the early 1930s, \ the Bank of France felt richer because drawers of gold in a New York "
                  r"basement", font_size=22, color=MONEY),
            label(r"were marked as its own: \ the gold never moved", font_size=22, color=MONEY),
            label(r"money is what people agree to accept, \ and keep track of", font_size=26, color=WHITE),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.3)
        tag = published_tag(r"Friedman, \ ``The Island of Stone Money'', \ Hoover Institution WP E-91-3 (1991)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Milton Friedman retold the story in 1991 and asked whether it is so different from us. "
            "<bookmark mark='a'/> In the early 1930s, he pointed out, the Bank of France felt richer, and America's "
            "position weaker, because some gold in a basement in New York had been marked as belonging to France. "
            "<bookmark mark='b'/> The gold never moved. <bookmark mark='c'/> On Yap and in Paris alike, money was "
            "what people agreed to accept, and kept track of."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why would anyone accept a thing they do not want, \ only to pass it on?", font_size=26,
                  color=MONEY),
            label(r"why does printing more of it raise prices, \ and sometimes destroy it?", font_size=26,
                  color=PRICE),
            label(r"and where does today's money, \ mostly bank deposits, \ come from?", font_size=26, color=BANK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: what is money, and what happens when there is too much of it? "
            "<bookmark mark='a'/> Why would anyone accept a thing they do not want, only to pass it on? "
            "<bookmark mark='b'/> Why does printing more of it raise prices, and why does printing far too much "
            "destroy it? <bookmark mark='c'/> And where does today's money, which is mostly bank deposits, come from?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        f = load("film")
        mini = plane([1959, 2027], [0, np.log10(120)], x_length=4.2, y_length=1.6)
        logo = VGroup(path(mini, f["t"], np.log10(f["base"]), CB, width=3, smooth=False),
                      path(mini, f["t"], np.log10(f["m2"]), BANK, width=3, smooth=False),
                      path(mini, f["t"], np.log10(f["cpi"]), PRICE, width=3, smooth=False))
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 25 \ $\cdot$ \ Money", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part twenty-five: money."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VI \ $\cdot$ \ Money and the Cycle", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"barter and its double coincidence; \ money as memory",
            r"which good becomes money: \ you choose, \ then Kiyotaki and Wright",
            r"the quantity theory on a century of data; \ hyperinflations and their ends",
            r"money demand; \ how banks create money; \ the Fisher equation",
            r"the optimum quantity of money; \ a dial; \ payments; \ stablecoins",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part opens Act Six, money and the business cycle. <bookmark mark='a'/> You'll see why barter "
            "fails, and why money is a kind of memory. <bookmark mark='b'/> You'll choose which good becomes money "
            "on the Island, and then watch a model of search decide it. <bookmark mark='c'/> You'll test the "
            "quantity theory on the world's data, and see how hyperinflations start and how they end. "
            "<bookmark mark='d'/> Then why people hold money at all, how a bank creates it by lending, and how "
            "interest rates carry inflation. <bookmark mark='e'/> And how much money there should be, one dial, the "
            "payment systems, and the new private moneys."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
