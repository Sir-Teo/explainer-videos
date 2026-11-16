from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


class Attraction(VoiceoverScene):
    def construct(self):
        self.card()
        self.proximity()
        self.exposure()
        self.similar()

    def card(self):
        card = chapter_card(7, r"Attraction", r"Who comes to like whom?",
                            lit={1950: r"Festinger et al.", 1968: r"Zajonc", 1989: r"Bornstein"}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter seven. Attraction."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def proximity(self):
        head = heading(r"Who lives nearby")
        doors = VGroup(*[Rectangle(width=0.7, height=1.0, stroke_color=GREY_B, fill_color="#14181F", fill_opacity=1)
                         for _ in range(5)]).arrange(RIGHT, buff=0.15).move_to([-3.6, 1.0, 0])
        me = Dot(doors[0].get_center(), radius=0.15, color=PERSON)
        arcs = VGroup(*[ArcBetweenPoints(doors[0].get_top(), doors[k].get_top(), angle=-0.8, color=GOOD,
                                         stroke_width=6 - k) for k in (1, 2, 4)])
        stair = label(r"stairs", font_size=15, color=GREY_A).next_to(doors[0], DOWN, buff=0.15)
        rows = rows_of([
            (r"Festinger, \ Schachter and Back, \ 1950: \ friendships among married students in a new housing "
             r"project at MIT", WHITE),
            (r"friends were overwhelmingly near neighbours: \ physical distance, \ and functional distance, \ such "
             r"as living by the stairs or the mailboxes, \ predicted who befriended whom", GOOD),
            (r"proximity works through chance encounters, \ and through familiarity", CROWD),
        ], 6.2, 20, 0.38).move_to([3.2, -0.2, 0])
        tag = historical_tag(r"Festinger, \ Schachter \& Back (1950)")
        with self.voiceover(
            "Now the closest bargains: who comes to like whom. <bookmark mark='a'/> In 1950 Festinger, Stanley "
            "Schachter and Kurt Back mapped friendships among married students in a new housing project at MIT. "
            "<bookmark mark='b'/> Friends were overwhelmingly near neighbours. Physical distance, and functional "
            "distance, like living by the stairs or the mailboxes, predicted who befriended whom. "
            "<bookmark mark='c'/> Proximity works through chance encounters, and through familiarity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(doors), FadeIn(me), FadeIn(stair))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(arcs), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def exposure(self):
        head = heading(r"Mere exposure")
        A = axes([0, 25], [0, 1.0], x_length=5.0, y_length=3.0, xticks=[0, 5, 10, 25], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"number of exposures", ylabel=r"liking", center=[-3.4, -0.2, 0],
                 font_size=15)
        x = np.linspace(0, 25, 100)
        y = 0.25 + 0.6 * (x / 10) * np.exp(1 - x / 10)
        c = curve(A.ax, x, y, PERSON)
        note = label(r"a schematic of the reported shape", font_size=14, color=GREY_B).next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"Zajonc, \ 1968: \ repeated exposure to a stimulus, \ even a meaningless one, \ increases liking for it",
             WHITE),
            (r"Bornstein, \ 1989: \ a meta-analysis of 208 experiments: \ a reliable effect, \ about $r = .26$", GOOD),
            (r"Montoya and colleagues, \ 2017: \ 268 curves from 81 articles: \ liking rises and then falls with "
             r"many exposures, \ an inverted U", CROWD),
            (r"familiarity breeds liking, \ up to a point", YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.2, 0])
        tag = historical_tag(r"Zajonc (1968); \ Bornstein (1989); \ Montoya et al.\ (2017)")
        with self.voiceover(
            "Familiarity on its own makes a difference. <bookmark mark='a'/> In 1968 Zajonc showed that "
            "repeated exposure to a stimulus, even a meaningless one, increases liking for it. "
            "<bookmark mark='b'/> In 1989 Bornstein pooled two hundred and eight experiments and found a "
            "reliable effect, a correlation of about point two six. <bookmark mark='c'/> In 2017 Montoya and "
            "colleagues fitted two hundred and sixty-eight curves from eighty-one articles. Liking rises, and with "
            "many exposures falls again: an inverted U. <bookmark mark='d'/> Familiarity breeds liking, up to a "
            "point."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(rows[1]), run_time=2)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def similar(self):
        d = load("market")
        head = heading(r"Similarity, \ reciprocity, \ matching")
        panels = VGroup()
        for k, (tag, title, c) in enumerate((("best", r"everyone wants the most attractive", PERSON),
                                              ("alike", r"everyone wants someone like themselves", CROWD))):
            A = axes([-3, 3], [-3, 3], x_length=2.5, y_length=2.5, xticks=None, yticks=None,
                     xlabel=r"one partner", ylabel=r"the other", center=[-5.0 + 3.2 * k, -0.6, 0], font_size=13)
            pts = scatter(A.ax, np.clip(d[f"{tag}_a"], -2.9, 2.9), np.clip(d[f"{tag}_b"], -2.9, 2.9), c,
                          radius=0.03, opacity=0.8)
            t = wrapped_label(title, 2.7, 14, c).next_to(A, UP, buff=0.2)
            rr = label(rf"$r = {d[f'{tag}_median']:.2f}$", font_size=18, color=c).next_to(A, DOWN, buff=0.5)
            panels.add(VGroup(A, pts, t, rr))
        rows = rows_of([
            (r"similarity: \ people like those who share their attitudes and backgrounds", CROWD),
            (r"reciprocity: \ people like those who like them", GOOD),
            (r"matching: \ couples resemble each other in attractiveness, \ education and much else", PERSON),
            (r"Psyche's marriage market, \ 200 people a side, \ attractiveness on both axes: \ the same match "
             r"appears whether people seek it or all chase the same few; \ Kalick and Hamilton made this point "
             r"in 1986", MODEL),
            (r"Part 34's lesson again: \ a pattern in who ends up together does not show what each person wanted",
             YOU),
        ], 5.6, 19, 0.3).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{social.stable\_matching}, \ deferred acceptance; \ median of 50 markets")
        with self.voiceover(
            "Three more classic regularities. <bookmark mark='a'/> Similarity: people like those who share their "
            "attitudes and backgrounds. <bookmark mark='b'/> Reciprocity: people like those who like them. "
            "<bookmark mark='c'/> And matching: couples tend to resemble each other in attractiveness, education "
            "and much else. But why? <bookmark mark='d'/> Here's Psyche's marriage market, two hundred people on "
            "each side, paired off so that no two people would rather leave their partners for each other. On the "
            "left, everyone wants the most attractive partner they can get, with a little private taste. Couples "
            f"end up matched, with a correlation of {d['best_median']:.2f}. <bookmark mark='e'/> On the right, "
            "everyone wants someone like themselves. The correlation is about the same. Kalick and Hamilton made "
            "this point with a simulation in 1986. <bookmark mark='f'/> It's a lesson from Part 34's networks. A "
            "pattern in who ends up together doesn't show what each person wanted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(panels[0][0]), FadeIn(panels[0][2]))
            self.play(FadeIn(panels[0][1], lag_ratio=0.01), run_time=1.5)
            self.play(FadeIn(panels[0][3]))
            vo.wait_until("e")
            self.play(FadeIn(panels[1][0]), FadeIn(panels[1][2]))
            self.play(FadeIn(panels[1][1], lag_ratio=0.01), run_time=1.5)
            self.play(FadeIn(panels[1][3]))
            vo.wait_until("f")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
