from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class Antitrust(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Antitrust's standards", r"What is competition law for?",
             "Chapter eleven. Antitrust's standards.",
             lit={1911: r"\emph{Standard Oil}", 1978: r"Bork", 2001: r"\emph{Microsoft}", 2024: r"\emph{Google}"},
             scale=("market", "nation"), horizon=("a decade", "a century"))
        self.timeline()
        self.views()
        self.cases()

    def timeline(self):
        events = [(1890, r"the Sherman Act", WHITE), (1911, r"Standard Oil \\ broken up", FIRM1),
                  (1978, r"Bork: \\ consumer welfare", PATIENT), (2001, r"Microsoft: \\ liable, \ not split", FIRM2),
                  (2017, r"Khan: \ `Amazon's \\ Antitrust Paradox'", LOSS), (2024, r"Google: \\ a monopolist", BUS)]
        x0, x1 = -6.0, 6.0
        line = Line(np.array([x0, 0, 0]), np.array([x1, 0, 0]), color=GREY_B, stroke_width=2)

        def X(y):
            return x0 + (x1 - x0) * (y - 1880) / (2030 - 1880)
        marks = VGroup()
        for k, (y, t, col) in enumerate(events):
            d = Dot(np.array([X(y), 0, 0]), radius=0.08, color=col)
            yl = label(str(y), font_size=17, color=col).next_to(d, DOWN if k % 2 else UP, buff=0.15)
            tl = label(t, font_size=17, color=col).next_to(yl, DOWN if k % 2 else UP, buff=0.1)
            marks.add(VGroup(d, yl, tl))
        head = label(r"a century of American antitrust, \ in six marks", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.ANTITRUST.tag, corner=DR, font_size=11)
        with self.voiceover(
            "What is competition law for? Its answer has changed. <bookmark mark='a'/> The Sherman Act of 1890 "
            "outlawed monopolization and restraints of trade. <bookmark mark='b'/> In 1911 the Supreme Court broke "
            "up Standard Oil. <bookmark mark='c'/> From the late 1970s, led by Robert Bork's book, the courts came "
            "to judge cases by their effect on consumers: higher prices, lower output, worse products. "
            "<bookmark mark='d'/> In 2001 an appeals court upheld the finding that Microsoft had illegally "
            "maintained its monopoly in operating systems, but threw out the order to split the company. "
            "<bookmark mark='e'/> In 2017 Lina Khan argued that a standard focused on prices misses the power of "
            "firms like Amazon, which keep prices low while gaining control of markets. <bookmark mark='f'/> And in "
            "August 2024 a federal judge found that Google had illegally monopolized general search."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(line))
            for mk, m in zip("abcdef", marks):
                vo.wait_until(mk)
                self.play(FadeIn(m, shift=UP * 0.1))
        self.clear_scene()

    def views(self):
        cols = VGroup()
        cw = [r"harm means higher prices, \\ lower output or quality", r"measurable, \ predictable, \\ grounded in "
              r"economics", r"risk: \ misses harm that \\ does not show in prices"]
        nb = [r"harm includes \\ concentrated power itself", r"structure, \ dependence, \\ gatekeeping",
              r"risk: \ vague standards, \\ protecting rivals, \ not rivalry"]
        for title, rows, col in ((r"the consumer-welfare standard", cw, PATIENT), (r"the neo-Brandeisian view", nb,
                                                                                  LOSS)):
            t = label(title, font_size=23, color=col)
            body = VGroup(*[label(r_, font_size=19, color=WHITE if k < 2 else HOLD) for k, r_ in enumerate(rows)])
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
            cols.add(VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.4))
        cols.arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to(DOWN * 0.1)
        head = label(r"each side's best case", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.ANTITRUST.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Each side has a strong case. <bookmark mark='a'/> The consumer-welfare standard asks one question: "
            "are consumers worse off, through higher prices, lower output or worse products? Its strength is that "
            "the tools of this part can answer it, so cases are predictable. Its weakness is that some harms, to "
            "innovation, to quality, to the choices of the future, may not show up in today's prices. "
            "<bookmark mark='b'/> The neo-Brandeisian view treats concentrated power as a harm in itself, "
            "especially when a platform both runs a market and competes in it. Its strength is that it looks at "
            "structure and dependence. Its weakness is that vague standards can end up protecting rivals rather than "
            "rivalry."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("ab", cols):
                vo.wait_until(mk)
                self.play(FadeIn(c[0]), LaggedStart(*[FadeIn(r_) for r_ in c[1]], lag_ratio=0.5), run_time=2.0)
        self.clear_scene()

    def cases(self):
        cards = point_cards([
            (r"the conduct", r"Google paid to be \\ the default search \\ engine on phones \\ and browsers", BUS),
            (r"the finding", r"August 2024: \\ an illegal monopoly \\ in general search", LOSS),
            (r"the remedy", r"September 2025: \\ no sale of Chrome; \\ no exclusive deals; \\ some data shared",
             PATIENT),
            (r"the question", r"do defaults decide \\ markets? \ (Part 42's \\ lesson, \ for firms)", E.ACCENT),
        ], width=12.8, cols=4, font_size=17).move_to(DOWN * 0.1)
        head = label(r"\emph{United States v. Google}", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.ANTITRUST.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The Google case shows the economics at work. <bookmark mark='a'/> Google paid phone makers and browser "
            "makers to make it the default search engine. <bookmark mark='b'/> In August 2024 Judge Amit Mehta "
            "found that those deals helped maintain an illegal monopoly in general search. "
            "<bookmark mark='c'/> In September 2025 he declined to order Google to sell its Chrome browser, but "
            "barred exclusive distribution contracts and required some search data to be shared with rivals. "
            "<bookmark mark='d'/> Underneath is a question this series met in Part forty-two: how much do defaults "
            "decide? If people rarely change them, buying the default is buying the market."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
