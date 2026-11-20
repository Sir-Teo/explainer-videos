from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Borders(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Borders as experiments", r"When a border cuts through one people, \ what does it do to their "
             r"incomes?", "Chapter ten. Borders as experiments.",
             lit={1573: r"the mita", 2010: r"Dell", 2012: r"Why Nations Fail"}, scale=("city", "nation"),
             horizon=("a century",))
        self.cases()
        self.rd()

    def cases(self):
        rows = VGroup(
            label(r"the two Koreas \ (Part 20): \ one people, \ split in 1945; \ 26 to 1 by 2022", font_size=23,
                  color=OUTPUT),
            label(r"Nogales, \ Arizona, \ and Nogales, \ Sonora: \ one town, \ a fence through the middle", font_size=23,
                  color=INST),
            label(r"the average household on the American side: \ about \$30{,}000 a year; \ on the Mexican side, \ "
                  r"about a third of that", font_size=21, color=GREY_A),
            label(r"same climate, \ same diseases, \ much the same culture: \ different institutions", font_size=23,
                  color=E.ACCENT),
            label(r"but a border also changes laws, \ markets, \ money and schools at once", font_size=21,
                  color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Acemoglu and Robinson, \emph{Why Nations Fail} (2012), \ ch.\ 1", corner=DR,
                            font_size=12)
        with self.voiceover(
            "A cleaner test is a border that cuts through one people. <bookmark mark='a'/> Part twenty began with "
            "the cleanest of all: the two Koreas, one people split in 1945, now twenty-six to one apart. "
            "<bookmark mark='b'/> Acemoglu and Robinson open their book, Why Nations Fail, with another: Nogales, "
            "a town cut in half by the border between Arizona and the Mexican state of Sonora. "
            "<bookmark mark='c'/> The average household on the American side, they write, earns about thirty "
            "thousand dollars a year; on the Mexican side, about a third of that. <bookmark mark='d'/> The climate, "
            "the diseases and much of the culture are the same. The institutions are not. "
            "<bookmark mark='e'/> But a border changes many things at once, laws, markets, money and schools, so a "
            "border alone cannot say which institution matters."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def rd(self):
        rng = np.random.default_rng(1573)
        xs = rng.uniform(-100, 100, 220)
        jump = np.where(xs > 0, 0.0, -0.25)
        ys = 5.0 + 0.0015 * xs + jump + rng.normal(0, 0.12, len(xs))
        ax = plane([-100, 100], [4.3, 5.6], center=LEFT * 1.5 + DOWN * 0.5, x_length=8.6, y_length=4.6,
                   xticks=[-100, -50, 0, 50, 100], yticks=[4.5, 5.0, 5.5],
                   xlabel=r"distance from the mita boundary, \ km \ (inside $<$ 0 $<$ outside)",
                   ylabel=r"log household consumption", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                   font_size=15)
        dots = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.04, color=MORT if a < 0 else INST).set_opacity(0.8)
                        for a, b in zip(xs, ys)])
        left = Line(ax.ax.c2p(-100, 5.0 - 0.15 - 0.25), ax.ax.c2p(0, 5.0 - 0.25), color=MORT, stroke_width=4)
        right = Line(ax.ax.c2p(0, 5.0), ax.ax.c2p(100, 5.15), color=INST, stroke_width=4)
        brace = DoubleArrow(ax.ax.c2p(4, 4.75), ax.ax.c2p(4, 5.0), buff=0, color=E.ACCENT, stroke_width=3)
        bl = label(r"about $-25\%$", font_size=19, color=E.ACCENT).next_to(brace, RIGHT, buff=0.1)
        side = VGroup(
            label(r"Melissa Dell, \ 2010", font_size=24, color=E.ACCENT),
            label(r"the mita, \ 1573--1812: \\ forced labour in the silver \\ and mercury mines", font_size=19,
                  color=GREY_A),
            label(r"inside its boundary today: \\ household consumption about 25\% lower; \\ stunting about 6 points "
                  r"higher", font_size=19, color=MORT),
            label(r"through land tenure \\ and public goods \ (roads)", font_size=19, color=INST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = illustrative_tag(r"illustrative points; \ the jump is Dell's estimate", corner=DL, font_size=13)
        ptag = published_tag(r"Dell, Econometrica 78(6) (2010): \ 1863--1903, \ abstract", corner=DR, font_size=12)
        with self.voiceover(
            "Melissa Dell found a sharper border inside Peru. <bookmark mark='a'/> From 1573 to 1812 the Spanish "
            "required communities within a boundary to send a seventh of their adult men to work the silver mines "
            "of Potosí and the mercury mines of Huancavelica: the mita. Just outside the boundary, the same "
            "geography and the same peoples were exempt. <bookmark mark='b'/> She compared households on either side "
            "of the line, a regression discontinuity, the method of part four. Two centuries after the mita "
            "ended, household consumption inside it is about twenty-five percent lower, and stunting among children "
            "about six percentage points higher. <bookmark mark='c'/> The channels she found are land tenure and "
            "public goods: the mita discouraged large estates, which later lobbied for roads, and mita districts "
            "are still less connected to them. The points here are illustrative; the jump is hers."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ptag), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.005), run_time=2)
            vo.wait_until("b")
            self.play(Create(left), Create(right), GrowFromCenter(brace), FadeIn(bl), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
