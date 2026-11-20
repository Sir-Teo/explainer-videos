from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ remote work and the climate", r"What could change the map?",
             "Chapter sixteen. Frontier: remote work and the climate.",
             lit={2020: r"the pandemic", 2021: r"Barrero, \ Bloom and Davis"}, scale=("household", "city"),
             horizon=("a decade", "a century"))
        self.home()
        self.questions()

    def home(self):
        W = load("wfh")
        t, v = np.array(W["t"]), np.array(W["v"])
        ax = plane([2019.5, 2027], [0, 70], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                   xticks=[2020, 2022, 2024, 2026], yticks=[0, 20, 40, 60],
                   ylabel=r"share of paid working days worked from home, \ \%", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=14)
        pre = dot(ax, 2019.6, W["pre"], GREY_B, 0.09)
        pl = label(rf"2019: \ {W['pre']:.0f}\%", font_size=16, color=GREY_B).next_to(ax.ax.c2p(2019.6, W["pre"]),
                                                                                  UR, buff=0.12)
        ln = path(ax, t[1:], v[1:], CITY, 3.2, smooth=False)
        side = VGroup(
            label(rf"May 2020: \ {W['peak']:.0f}\%", font_size=20, color=RENT),
            label(rf"the last year: \ {W['last12']:.0f}\%", font_size=20, color=CITY),
            label(r"nearly four times \\ the level of 2019, \\ and steady", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        tag = data_tag(r"Barrero, \ Bloom and Davis (SWAA), \ via FRED; \ 2019 from the ATUS", corner=DR,
                       font_size=12)
        with self.voiceover(
            "The frontier begins with the largest change in how people work in a century. "
            f"<bookmark mark='a'/> In 2019 about {W['pre']:.0f} percent of America's paid working days were worked "
            "from home. <bookmark mark='b'/> In May 2020, in the pandemic, about "
            f"{W['peak']:.0f} percent. <bookmark mark='c'/> And then it did not go back: over the last year of the "
            f"survey of José María Barrero, Nicholas Bloom and Steven Davis, about {W['last12']:.0f} percent, "
            "nearly four times the old level, and steady. Some people moved from city centres to the suburbs and "
            "smaller towns; office buildings lost value. Whether this loosens the hold of the big cities, or only "
            "lengthens the commutes of those who still come in two or three days a week, is being measured now."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(pre, scale=1.5), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()

    def questions(self):
        rows = VGroup(
            label(r"open questions", font_size=27, color=E.ACCENT),
            label(r"remote work: \ do ideas still need the face-to-face city?", font_size=21, color=CITY),
            label(r"the climate: \ heat, \ floods and rising seas on valuable land", font_size=21, color=RENT),
            label(r"density and emissions: \ do compact cities pollute less per person?", font_size=21, color=GAIN),
            label(r"sorting: \ how much of the big-city premium is the city?", font_size=21, color=WAGE),
            label(r"housing: \ how much output do tight cities really cost?", font_size=21, color=GOLD),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        tag = published_tag(r"Barrero, \ Bloom and Davis; \ Hsieh and Moretti (2019); \ Greaney (2026)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The frontier's open questions. <bookmark mark='a'/> Remote work: if ideas spread face to face, as "
            "Marshall thought, can a city's learning survive when its workers meet less? <bookmark mark='b'/> The "
            "climate: many of the world's most valuable places sit on coasts and river mouths; heat, floods and "
            "rising seas will reprice them, and someone must decide where to defend and where to retreat. "
            "<bookmark mark='c'/> Density and emissions: dense cities use less fuel per person, but they are also "
            "richer. <bookmark mark='d'/> Sorting: how much of the big-city premium is the city, and how much is "
            "who chooses to live there? <bookmark mark='e'/> And housing: how much output do tight cities cost the "
            "nation, a number that moved by two orders of magnitude in one comment."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
