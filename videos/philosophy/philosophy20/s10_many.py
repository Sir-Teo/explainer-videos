from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Many(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"The problem of the many", r"How many clouds are in the sky?", lit=(1980, 1993),
                            part=PART)
        with self.voiceover("Chapter nine. The problem of the many."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.cloud()
        self.price()
        self.persons()

    def cloud(self):
        head = label(r"One cloud, \ or a thousand?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rng = np.random.default_rng(1980)
        c = np.array([-3.8, -0.2, 0])
        pts = []
        for _ in range(420):
            r = abs(rng.normal(0, 1.0))
            a = rng.uniform(0, 2 * PI)
            pts.append(c + np.array([1.4 * r * np.cos(a), 0.9 * r * np.sin(a), 0]))
        drops = VGroup(*[Dot(p, radius=0.03, color=GREY_A, fill_opacity=max(0.2, 1 - np.linalg.norm(
            (p - c) / [1.4, 0.9, 1]) / 2.4)) for p in pts])
        outlines = VGroup(*[Ellipse(width=2 * 1.4 * s, height=2 * 0.9 * s, color=col, stroke_width=2).move_to(
            c + np.array([dx, dy, 0])) for s, col, dx, dy in ((1.5, UNIV, 0, 0), (1.55, WHOLE, 0.08, -0.05),
                                                             (1.45, NOM, -0.06, 0.04), (1.6, PARTC, 0.03, 0.06))])
        rows = stack([(r"a cloud's edge is a gradual thinning of droplets", WHITE),
                      (r"many aggregates of droplets, \ differing by a few at the edge, \ each an equally good "
                       r"candidate", GOAL),
                      (r"each candidate is cloud-shaped, \ cloud-sized, \ made of water: \ each seems to be a cloud", BAD),
                      (r"Unger \ (1980); \ Geach \ (1980): \ so there are many clouds, \ or none", GREY_A)],
                     font_size=20, aligned_edge=LEFT, width=6.2).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "Peter Unger and Peter Geach found a problem in every ordinary object. <bookmark mark='a'/>Look at a "
            "cloud. Its edge is not a line; the droplets simply thin out. <bookmark mark='b'/>So there are many "
            "aggregates of droplets that differ by a few droplets at the edge, and each is an equally good candidate "
            "to be the cloud. <bookmark mark='c'/>Each candidate is cloud-shaped, cloud-sized and made of water. Each "
            "seems to be a cloud. <bookmark mark='d'/>So either there are thousands of clouds where we see one, or, as "
            "Unger concluded, there are no clouds at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(drops))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(o) for o in outlines], lag_ratio=0.3), FadeIn(rows[1]))
            for mk, r in zip("cd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def price(self):
        d = load("many")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mcs"] == [["M1"], ["M2"], ["M3"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.9, width=3.9, font_size=20,
                       center=[0, -0.5, 0], title=r"The Price List: \ the problem of the many")
        positions = [(("M1",), r"Unger; \ or Williamson", r"no candidate is a cloud \ (nihilism), \ or exactly one "
                                                          r"is, \ unknowably \ (epistemicism)"),
                     (("M2",), r"Geach; \ Lewis \ (1993)", r"they are the same cloud \ (relative identity), \ or "
                                                           r"`many, \ but almost one'"),
                     (("M3",), r"many clouds", r"there really are many, \ overlapping almost entirely; \ we count "
                                              r"loosely")]
        with self.voiceover(
            "The problem of the many is a Price List. <bookmark mark='a'/>Each candidate in the crowd is a cloud, "
            "since they are equally good. The candidates are many, since they differ by droplets. And there is "
            "exactly one cloud in the sky. <bookmark mark='b'/>The three cannot all be true. <bookmark mark='c'/>Deny "
            "the first: Unger says no candidate is a cloud, because there are none; Timothy Williamson's "
            "epistemicism says exactly one is, though we can never know which. <bookmark mark='d'/>Deny the second: "
            "Geach says the candidates are different aggregates but the same cloud; Lewis says they are many but "
            "almost one, overlapping so much that we may count them as one. <bookmark mark='e'/>Or deny the third: "
            "there really are many clouds, and our counting is loose."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def persons(self):
        head = label(r"The problem comes home", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"cats", r"Tibbles loses a hair: \ Tibbles and Tibbles-minus-a-hair, \ two cats on the mat? \ (Geach, "
                      r"\ Wiggins)", NOM),
            (r"you", r"many slightly different aggregates of your particles: \ are there many of you thinking this "
                     r"thought?", BAD),
            (r"supervaluation", r"`cloud' is vague: \ on each sharpening exactly one candidate is the cloud, \ so "
                                r"`there is one cloud' is supertrue", UNIV),
            (r"onward", r"identity over time, \ fission and what matters: \ Part 21", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "The problem does not stay in the sky. <bookmark mark='a'/>A cat, Tibbles, is about to lose a hair. "
            "Before it falls, Tibbles and Tibbles-minus-that-hair are both cat-shaped, both made of cat. Are there "
            "two cats on the mat? <bookmark mark='b'/>And you: there are many slightly different aggregates of your "
            "particles. Are there many of you, all thinking this thought? <bookmark mark='c'/>The supervaluationist "
            "says the word cloud, or cat, is vague. On each way of making it precise, exactly one candidate qualifies, "
            "so there is one cloud is true on every sharpening, though no candidate is determinately the cloud. "
            "<bookmark mark='d'/>What makes you the same person over time is the topic of Part 21."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
