from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.gym()
        self.island()
        self.question()
        self.title()
        self.objectives()

    def gym(self):
        T = tables.GYM_2006.data
        chain = flow_chain([(rf"a monthly contract: \\ over \${T['fee']}", GYM),
                            (rf"{T['visits']} visits \\ a month", DO),
                            (rf"over \${T['per_visit']} \\ a visit", LOSS)],
                           notes=[r"unlimited visits, \\ paid in advance", r"on average, \\ members on it",
                                  r"what each visit \\ really cost"], box_w=3.2, font_size=24, note_size=18)
        chain.move_to(UP * 1.2)
        alt = VGroup(
            RoundedRectangle(width=3.2, height=1.1, corner_radius=0.12, stroke_color=GAIN, stroke_width=2.2,
                             fill_color=GAIN, fill_opacity=0.14),
            label(rf"a ten-visit pass: \\ \${T['pass']} a visit", font_size=24, color=WHITE),
        )
        alt[1].move_to(alt[0])
        alt.next_to(chain.boxes[2], DOWN, buff=1.6)
        vs = label(r"on offer at the same clubs", font_size=18, color=GAIN).next_to(alt, DOWN, buff=0.15)
        arr = Arrow(chain.boxes[2].get_bottom() + DOWN * 0.75, alt.get_top(), buff=0.08, color=GREY_B,
                    stroke_width=2.5)
        who = label(rf"{T['members']:,} members \\ of {T['clubs']} American \\ health clubs, \\ over three years",
                    font_size=19, color=GREY_A).to_edge(LEFT, buff=0.5).shift(DOWN * 1.6)
        tag = published_tag(tables.GYM_2006.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 2006 two economists, Stefano DellaVigna and Ulrike Malmendier, published the attendance records of "
            f"{T['members']:,} members of three American health clubs, over three years. <bookmark mark='a'/> Many "
            f"members bought a monthly contract, for over {T['fee']} dollars a month, with unlimited visits. "
            f"<bookmark mark='b'/> They then went, on average, {T['visits']} times a month. <bookmark mark='c'/> "
            f"Each visit cost them over {T['per_visit']} dollars. <bookmark mark='d'/> The same clubs sold a "
            f"ten-visit pass, at {T['pass']} dollars a visit. The members would have paid less, for the same visits, "
            "with the pass. They were paying not to go to the gym."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(who), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(chain.arrows[0]), FadeIn(chain.boxes[1]), FadeIn(chain.notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(chain.arrows[1]), FadeIn(chain.boxes[2]), FadeIn(chain.notes[2]))
            vo.wait_until("d")
            self.play(GrowArrow(arr), FadeIn(alt), FadeIn(vs))
        self.clear_scene()

    def island(self):
        G = load("gym")
        ax = plane([0, 25], [0, 15], center=LEFT * 2.0 + DOWN * 0.4, x_length=6.6, y_length=4.8,
                   xticks=[0, 5, 10, 15, 20, 25], yticks=[0, 5, 10, 15],
                   xlabel=r"visits a month, \ forecast at sign-up",
                   ylabel=r"visits a month, \ made", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        diag = seg(ax, 0, 0, 15, 15, GREY_B, 1.6, dashed=True)
        dl = label(r"as planned", font_size=15, color=GREY_B).next_to(ax.ax.c2p(13, 13.6), UL, buff=0.05)
        pts = VGroup(*[dot(ax, f, v, NAIF, 0.05) for f, v in zip(G["sample_forecast"], G["sample_visits"])
                       if f <= 25 and v <= 15])
        side = VGroup(
            label(rf"the Island's gym: \\ \${G['fee']:.0f} a month, \\ or \${G['per_visit']:.0f} a visit", font_size=19,
                  color=WHITE),
            label(rf"monthly members \\ forecast {G['forecast']:.1f} visits", font_size=19, color=PLAN),
            label(rf"and make {G['visits']:.1f}", font_size=19, color=DO),
            label(rf"\${G['price_per_visit']:.2f} a visit; \\ {100 * G['regret_share']:.0f}\% would have paid \\ "
                  r"less with the pass", font_size=19, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island has a gym too, with the same two prices. <bookmark mark='a'/> When members sign up, they "
            "forecast how often they will go: each dot is a monthly member, with the forecast across and the visits "
            "made up the side. If people went as often as they planned, the dots would sit on the dashed line. "
            f"<bookmark mark='b'/> On average, monthly members expect {G['forecast']:.1f} visits a month. "
            f"<bookmark mark='c'/> They make {G['visits']:.1f}. <bookmark mark='d'/> So they pay "
            f"{money_words(G['price_per_visit'])} a visit, and {100 * G['regret_share']:.0f} percent of them would "
            "have done better with the pass. Nobody here is short of information, or bad at arithmetic. They are "
            "wrong about something else: their own future selves."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(diag), FadeIn(dl), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.01), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 36, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"which of Part 5's assumptions fail, \ and how would we know?", font_size=26, color=PLAN),
            label(r"how do economists measure a bias in the field, \ not just in the laboratory?", font_size=26,
                  color=GYM),
            label(r"what do markets, \ and the firms in them, \ do with people's biases?", font_size=26, color=FIRM),
            label(r"if choices are not always in people's interest, \ what is welfare?", font_size=26, color=NUDGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "So this part asks what changes in economics when people are not the agents of Part five, who knew "
            "what they wanted and chose it. <bookmark mark='a'/> Which of those assumptions fail, and how would we "
            "know? <bookmark mark='b'/> How do economists measure a bias in real decisions, not only in the "
            "laboratory? <bookmark mark='c'/> What do markets, and the firms in them, do with people's biases? "
            "<bookmark mark='d'/> And if choices are not always in people's interest, what does it mean to make "
            "someone better off?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1959, 2026.5], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, GYM, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 45 \ $\cdot$ \ Behavioural Economics", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part forty-five: behavioural economics."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IX \ $\cdot$ \ The Fields", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"three departures; \ a mug to sell; \ reference points in the lab and in the field",
            r"present bias, \ naifs and sophisticates; \ commitment; \ defaults",
            r"inattention; \ fairness; \ what markets do with biases",
            r"behavioural welfare; \ nudges at scale; \ models of limited minds",
            r"three dials; \ the people who use this; \ the frontier",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> Three ways people depart from the textbook, a mug for you to "
            "sell, and reference points, in the laboratory and in marathons, golf and housing. "
            "<bookmark mark='b'/> Present bias, the difference between knowing it and not, what people do to bind "
            "themselves, and the power of defaults. <bookmark mark='c'/> Inattention, fairness, and whether markets "
            "cure biases or feed on them. <bookmark mark='d'/> What welfare means when choices conflict, what nudges "
            "do at scale, and models of minds with limits. <bookmark mark='e'/> Three dials, the people who use "
            "these ideas, and the frontier."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
