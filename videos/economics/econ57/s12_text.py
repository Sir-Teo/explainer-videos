from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403

EVENTS = {"2025-04": r"tariffs", "2020-05": r"pandemic", "2020-11": r"election", "2011-08": r"debt ceiling",
          "2019-01": r"shutdown"}
# the close peaks of 2019-2020 get their labels set off in clear space, with a leader line to the dot
POS = {"2019-01": (2015.4, 300), "2020-05": (2016.2, 400), "2020-11": (2022.6, 400)}


class Text(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Text as data", r"Can newspapers, \ minutes and speeches be measured?",
             "Chapter ten. Text as data.", lit={2016: r"Baker, \ Bloom and Davis", 2018: r"Hansen, \ McMahon and Prat",
                                                2019: r"Gentzkow, \ Kelly and Taddy"},
             scale=("nation",), horizon=("a day", "a decade"))
        self.epu()
        self.beyond()

    def epu(self):
        E_ = load("epu")
        ks = E_["months"]
        t = np.array([int(k[:4]) + (int(k[5:7]) - 1) / 12 for k in ks])
        v = np.array(E_["value"])
        ax = plane([1984.5, 2027.5], [0, 500], center=LEFT * 0.4 + DOWN * 0.5, x_length=11.4, y_length=4.6,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0, 100, 200, 300, 400], xlabel=r"",
                   ylabel=r"economic policy uncertainty \ (1985--2009 average = 100)", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=13)
        line = path(ax, t, v, NOW, 1.8, smooth=False)
        eq = MathTex(r"\text{EPU}_t \propto \frac{\#\{\text{articles with }E \wedge P \wedge U\text{ terms}\}}"
                     r"{\#\{\text{articles}\}}", font_size=30, color=WHITE).to_edge(UP, buff=0.35)
        terms = label(r"E: \ economy, \ economic; \quad P: \ Congress, \ deficit, \ Federal Reserve, \ legislation, "
                      r"\ regulation, \ White House; \quad U: \ uncertain, \ uncertainty", font_size=16,
                      color=GREY_A).next_to(eq, DOWN, buff=0.2)
        peaks = VGroup()
        for p in E_["peaks"]:
            if p["month"] not in EVENTS:
                continue
            x = int(p["month"][:4]) + (int(p["month"][5:7]) - 1) / 12
            d = dot(ax, x, p["value"], E.ACCENT, 0.06)
            lab = label(rf"{EVENTS[p['month']]}, \ {p['month'][:4]}", font_size=14, color=E.ACCENT)
            if p["month"] in POS:
                lab.move_to(ax.ax.c2p(*POS[p["month"]]))
                end = lab.get_right() if POS[p["month"]][0] < x else lab.get_left()
                lead = Line(end + (RIGHT if POS[p["month"]][0] < x else LEFT) * 0.05, d.get_center(),
                            color=E.ACCENT, stroke_width=1, stroke_opacity=0.6)
                peaks.add(VGroup(d, lab, lead))
            else:
                lab.next_to(d, UP, buff=0.08)
                peaks.add(VGroup(d, lab))
        tag = data_tag(r"Baker, \ Bloom and Davis, \ policyuncertainty.com, \ via FRED \ (USEPUINDXM)", corner=DR,
                       font_size=12)
        top = E_["peaks"][0]
        with self.voiceover(
            "Words can be counted. <bookmark mark='a'/> Scott Baker, Nicholas Bloom and Steven Davis count, each "
            "month, the share of articles in ten leading American newspapers that use a word about the economy, a "
            "word about policy, and a word about uncertainty, all together, and scale it so that the 1985 to 2009 "
            "average is one hundred. <bookmark mark='b'/> The index jumps at the moments you would expect: the "
            "debt-ceiling standoff of 2011, the government shutdown of 2019, the pandemic and the election of 2020. "
            f"<bookmark mark='c'/> Its highest month in four decades is {top['month'][:4]}'s April, at "
            f"{top['value']:.0f}, when sweeping tariffs were announced. The index does more than describe: "
            "investment and hiring fall when it rises, in firms more exposed to government spending most of all."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(terms), run_time=2.0)
            self.play(FadeIn(ax), Create(line), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in peaks[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(peaks[0], scale=1.3))
        self.clear_scene()

    def beyond(self):
        cards = point_cards([
            (r"the Federal Reserve's own words", r"Stephen Hansen, \ Michael McMahon and Andrea Prat read the "
             r"transcripts of FOMC meetings with topic models: \ after 1993, \ when members knew the transcripts "
             r"would be published, \ newer members came better prepared, \ and also conformed more", GB),
            (r"from counts to meanings", r"text as data: \ word counts, \ then dictionaries, \ then topic models, "
             r"\ and now embeddings from language models, \ which place documents in a space of meanings", SPF),
            (r"the same rules", r"a measure built from text is still a measure: \ check it against the slow, \ "
             r"careful numbers, \ and beware of fitting the past", BENCH),
        ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.15)
        tag = published_tag(r"Baker, \ Bloom and Davis, \ QJE 131(4) (2016); \ Hansen, \ McMahon and Prat, \ QJE "
                            r"133(2) (2018); \ Gentzkow, \ Kelly and Taddy, \ JEL 57(3) (2019)", corner=DR,
                            font_size=11)
        with self.voiceover(
            "Text reaches further. <bookmark mark='a'/> Stephen Hansen, Michael McMahon and Andrea Prat read the "
            "transcripts of the Federal Reserve's policy meetings with topic models. After 1993, when members "
            "learned that the transcripts would be published, newer members came better prepared, citing more data, "
            "and also conformed more, disagreeing less: transparency changed the deliberation it revealed. "
            "<bookmark mark='b'/> The methods have moved "
            "from counting words to dictionaries, topic models, and now the embeddings of language models, which "
            "place documents in a space of meanings; Matthew Gentzkow, Bryan Kelly and Matt Taddy survey them. "
            "<bookmark mark='c'/> The old rules still apply: a measure built from text is a measure, to be checked "
            "against the careful numbers, and as easy to overfit as any other."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
