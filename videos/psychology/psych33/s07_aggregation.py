from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403


class Aggregation(VoiceoverScene):
    def construct(self):
        self.card()
        self.many()
        self.situations()
        self.signatures()

    def card(self):
        card = chapter_card(6, r"Many acts", r"What resolved the person-situation debate?",
                            lit={1979: r"Epstein", 1983: r"Funder \& Ozer", 1995: r"Mischel \& Shoda", 2001: r"Fleeson"},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter six. Many acts."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def many(self):
        d = load("acts")
        head = heading(r"Average the acts")
        A = axes([0, 17], [0, 1.0], x_length=6.2, y_length=4.0, xticks=[1, 2, 4, 8, 16], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"situations averaged",
                 ylabel=r"consistency (correlation)", center=[-2.9, -0.4, 0], font_size=15)
        sb = curve(A.ax, d["k"], d["sb"], MODEL, stroke_width=3)
        obs = scatter(A.ax, d["k"], d["observed"], PERSON, radius=0.09)
        key = legend([(PERSON, r"Psyche's people"), (MODEL, r"Spearman-Brown, \ from one act")], font_size=16)
        key.move_to(A.ax.c2p(11.5, 0.2))
        rows = rows_of([
            (r"Seymour Epstein, \ 1979: \ record behaviour and feelings day by day for weeks; \ single days barely "
             r"agree, \ but averages over many days agree closely with averages over others", WHITE),
            (rf"Psyche: \ one act against one act, \ {d['observed'][0]:.2f}; \ the average of 16 situations against "
             rf"16 others, \ {d['observed'][-1]:.2f}", PERSON),
            (r"exactly Part 3's Spearman-Brown formula: \ a trait is measured by many acts, \ as a test is by many "
             r"items", MODEL),
            (r"Mischel's .30 was the reliability of one act, \ not the reality of the trait", YOU),
        ], 5.6, 20, 0.34).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{personality.aggregate\_curve}")
        with self.voiceover(
            "The answer came from measurement. <bookmark mark='a'/> In 1979 Seymour Epstein had people record their "
            "behaviour and feelings day by day for weeks. Single days barely agreed with each other, but averages "
            "over many days agreed closely with averages over other days. <bookmark mark='b'/> Psyche shows the "
            f"same. One act against one act gives {d['observed'][0]:.2f}. The average of sixteen situations against "
            f"the average of sixteen others gives {d['observed'][-1]:.2f}. That's your second number. "
            "<bookmark mark='c'/> And the curve is exactly Part 3's Spearman-Brown formula, predicted from the "
            "single act. A trait is measured by many acts, as a test is measured by many items. "
            "<bookmark mark='d'/> Mischel's point three was the reliability of one act, not the reality of the "
            "trait."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(o, scale=0.5) for o in obs], lag_ratio=0.3), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(sb), FadeIn(key), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def situations(self):
        head = heading(r"How large are situations?")
        A = axes([-0.6, 1.6], [0, 0.5], x_length=4.2, y_length=3.6, xticks=None, yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                 yfmt=lambda v: f"{v:g}", ylabel=r"effect, \ as a correlation", center=[-4.0, -0.4, 0], font_size=15)
        b = VGroup(Line(A.ax.c2p(0, 0.30), A.ax.c2p(0, 0.30), color=PERSON),
                   bars(A.ax, [0], [0.30], PERSON, width=0.6),
                   Rectangle(width=abs(A.ax.c2p(1.3, 0)[0] - A.ax.c2p(0.7, 0)[0]),
                             height=A.ax.c2p(0, 0.42)[1] - A.ax.c2p(0, 0.36)[1], stroke_width=0, fill_color=SITUATION,
                             fill_opacity=0.85).move_to(A.ax.c2p(1, 0.39)))
        names = VGroup(label(r"a trait, \ one act", font_size=16, color=PERSON).next_to(A.ax.c2p(0, 0), DOWN, buff=0.2),
                       label(r"classic situations", font_size=16, color=SITUATION).next_to(A.ax.c2p(1, 0), DOWN,
                                                                                          buff=0.2))
        rows = rows_of([
            (r"David Funder and Daniel Ozer, \ 1983: \ take the most famous situational effects in social psychology, "
             r"\ including Milgram's obedience, \ and convert them to correlations", WHITE),
            (r"they come to about .36 to .42: \ the same size as the trait coefficient everyone had called small", SITUATION),
            (r"so neither the person nor the situation dominates one act: \ both matter, \ and both are modest", YOU),
        ], 6.8, 21, 0.38).move_to([2.8, -0.2, 0])
        tag = published_tag(r"Funder \& Ozer (1983)")
        with self.voiceover(
            "And how large are the effects of situations? <bookmark mark='a'/> In 1983 David Funder and Daniel Ozer "
            "took some of the most famous situational effects in social psychology, including Milgram's obedience "
            "study, which is Part 34's story, and converted them to correlations. <bookmark mark='b'/> They came to "
            "about point three six to point four two: the same size as the trait coefficient everyone had called "
            "small. <bookmark mark='c'/> So neither the person nor the situation dominates a single act. Both "
            "matter, and both are modest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(b[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(b[2]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def signatures(self):
        d = load("acts")
        head = heading(r"Traits as distributions, \ and if-then signatures")
        S = len(d["p1"])
        A = axes([0.5, S + 0.5], [-3.5, 4.0], x_length=6.0, y_length=3.6, xticks=list(range(1, S + 1)), yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"situation", ylabel=r"behaviour", center=[-2.9, -0.4, 0],
                 font_size=15)
        xs = np.arange(1, S + 1)
        p1 = VGroup(curve(A.ax, xs, d["p1"], PERSON, stroke_width=4), scatter(A.ax, xs, d["p1"], PERSON, radius=0.07))
        p2 = VGroup(curve(A.ax, xs, d["p2"], O_, stroke_width=4), scatter(A.ax, xs, d["p2"], O_, radius=0.07))
        m1 = DashedLine(A.ax.c2p(0.5, float(np.mean(d["p1"]))), A.ax.c2p(S + 0.5, float(np.mean(d["p1"]))),
                        color=WHITE, stroke_width=2)
        key = legend([(PERSON, r"person 1"), (O_, r"person 2"), (WHITE, r"their shared average")], font_size=16)
        key.move_to(A.ax.c2p(6.4, -2.85))
        rows = rows_of([
            (r"William Fleeson, \ 2001: \ sampling people's behaviour several times a day for weeks, \ the typical "
             r"person showed nearly every level of every trait; \ their averages were almost perfectly stable", WHITE),
            (r"a trait is the centre of a distribution of states, \ not a fixed behaviour", PERSON),
            (r"Walter Mischel and Yuichi Shoda, \ 1995: \ what is stable is also each person's profile across "
             r"situations, \ an if-then signature: \ two people with the same average can differ in where they rise "
             r"and fall", O_),
        ], 5.6, 20, 0.34).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{personality.act\_world}")
        with self.voiceover(
            "Two more ideas finished the debate. <bookmark mark='a'/> In 2001 William Fleeson sampled people's "
            "behaviour several times a day for weeks. The typical person showed nearly every level of every trait, "
            "but each person's average was almost perfectly stable. <bookmark mark='b'/> A trait is the centre of a "
            "distribution of states, not a fixed behaviour. <bookmark mark='c'/> And in 1995 Mischel himself, with "
            "Yuichi Shoda, argued that each person's profile across situations is stable too: an if-then signature. "
            "Here are two of Psyche's people with the same average over eight situations. Where they rise and fall "
            "differs, and it repeats when the situations come round again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(p1[0]), FadeIn(p1[1]), Create(p2[0]), FadeIn(p2[1]), Create(m1), FadeIn(key),
                      FadeIn(rows[2]))
        self.clear_scene()
