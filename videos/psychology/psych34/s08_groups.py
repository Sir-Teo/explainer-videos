from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403


class Groups(VoiceoverScene):
    def construct(self):
        self.card()
        self.polarization()
        self.groupthink()
        self.minority()
        self.hidden()

    def card(self):
        card = chapter_card(7, r"Groups deciding", r"Are groups wiser, \ or just more extreme?",
                            lit={1969: r"Moscovici", 1972: r"Janis", 1985: r"Stasser \& Titus"}, part=PART,
                            scale=("group",), marr=("what", "how"))
        with self.voiceover("Chapter seven. Groups deciding."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def polarization(self):
        head = heading(r"Discussion makes a group more of what it was")
        A = axes([-3.2, 3.2], [0, 1.0], x_length=6.0, y_length=2.6, xticks=[-3, 0, 3], yticks=None,
                 xfmt=lambda v: {-3: "against", 0: "neutral", 3: "for"}[int(v)], xlabel=r"attitude",
                 center=[-3.0, 0.3, 0], font_size=15)
        xs = np.linspace(-3.2, 3.2, 200)
        before = np.exp(-0.5 * ((xs - 0.8) / 0.9) ** 2)
        after = np.exp(-0.5 * ((xs - 1.6) / 0.6) ** 2)
        cb = curve(A.ax, xs, before, CROWD, stroke_width=4)
        ca = curve(A.ax, xs, after, AUTH, stroke_width=4)
        key = legend([(CROWD, r"members before"), (AUTH, r"after discussing")], font_size=16)
        key.next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"Stoner, \ 1961, \ a master's thesis: \ groups chose riskier options than their members had alone, \ "
             r"the ``risky shift''", WHITE),
            (r"but later studies found groups also shifted toward caution, \ when their members leaned that way", CROWD),
            (r"Moscovici and Zavalloni, \ 1969: \ French students who liked their president and disliked Americans "
             r"felt both more strongly after discussing them", AUTH),
            (r"group polarization: \ discussion moves a group further in the direction it already leaned", YOU),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = historical_tag(r"Stoner (1961); \ Moscovici \& Zavalloni (1969)")
        with self.voiceover(
            "Do groups decide better than their members? <bookmark mark='a'/> In 1961 a master's student, James "
            "Stoner, found that groups chose riskier options than their members had chosen alone. It was called "
            "the risky shift. <bookmark mark='b'/> But later studies found groups shifting toward caution too, when "
            "their members leaned that way. <bookmark mark='c'/> In 1969 Moscovici and Zavalloni showed "
            "the general rule. French students who liked their president and disliked Americans felt both more "
            "strongly after discussing them. <bookmark mark='d'/> Group polarization: discussion moves a group "
            "further in the direction it already leaned. Chapter ten's model adds why: people mostly hear "
            "arguments from those who already agree with them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(cb), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(TransformFromCopy(cb, ca), FadeIn(key[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def groupthink(self):
        head = heading(r"Groupthink, \ and its evidence")
        rows = rows_of([
            (r"Janis, \ 1972: \ case studies of American foreign-policy fiascos: \ a cohesive "
             r"group, \ insulated, \ under a strong leader, \ seeks agreement and stops testing its plan", WHITE),
            (r"the idea spread through business schools and government, \ and into everyday speech", CROWD),
            (r"experiments rarely found its predicted pattern: \ reviews in 1998 called it weakly supported, \ and "
             r"one called it virtually devoid of support after a quarter of a century", AUTH),
            (r"Baron, \ 2005: \ the symptoms appear in many groups without Janis's conditions, \ so they are not "
             r"explained by them", MODEL),
            (r"what survives: \ groups often suppress dissent and share too little; \ the next two studies show "
             r"both", YOU),
        ], 12.4, 22, 0.34).move_to([0, -0.3, 0])
        tag = historical_tag(r"Janis (1972); \ Fuller \& Aldag (1998); \ Baron (2005)")
        with self.voiceover(
            "The most famous idea about groups came from history, not experiments. <bookmark mark='a'/> In 1972 "
            "Janis studied American foreign-policy fiascos. A cohesive group, insulated, "
            "under a strong leader, seeks agreement, and stops testing its plan. He called it groupthink. "
            "<bookmark mark='b'/> The idea spread through business schools and governments, and into everyday "
            "speech. <bookmark mark='c'/> But experiments rarely found the pattern it predicts. Reviews in 1998 "
            "called it weakly supported, and one said it was virtually devoid of support after a quarter of a "
            "century. <bookmark mark='d'/> In 2005 Baron argued that its symptoms appear in many groups "
            "without Janis's conditions, so the conditions don't explain them. <bookmark mark='e'/> What survives "
            "is narrower: groups often suppress dissent, and share too little of what they know. The next two "
            "studies show both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def minority(self):
        head = heading(r"A consistent minority")
        slides = VGroup(*[Square(side_length=0.42, stroke_width=1, stroke_color=GREY_B, fill_color="#3B6FD8",
                                 fill_opacity=1) for _ in range(36)]).arrange_in_grid(4, 9, buff=0.08)
        slides.move_to([-3.4, 1.5, 0])
        A = axes([-0.6, 2.6], [0, 10], x_length=4.6, y_length=2.6, xticks=None, yticks=[0, 4, 8],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"answers of ``green''", center=[-3.4, -1.5, 0], font_size=14)
        b = bars(A.ax, [0, 1, 2], [0.25, 1.25, 8.4], [GREY_B, CROWD, GOOD], width=0.6)
        names = VGroup(*[label(t, font_size=14, color=c).next_to(A.ax.c2p(k, 0), DOWN, buff=0.12) for k, (t, c) in
                         enumerate(((r"no confederates", GREY_B), (r"inconsistent", CROWD), (r"consistent", GOOD)))])
        rows = rows_of([
            (r"Moscovici, \ Lage and Naffrechoux, \ 1969: \ groups of six, \ two of them confederates, \ named the "
             r"colour of 36 blue slides", WHITE),
            (r"when the two said ``green'' every time, \ about 8\% of the real participants' answers were green; \ "
             r"with no confederates, \ almost none", GOOD),
            (r"when the two said green only sometimes, \ they had almost no effect", CROWD),
            (r"a minority moves a majority by being consistent, \ and its influence often shows later, \ in "
             r"private, \ more than in public", YOU),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = historical_tag(r"Moscovici, \ Lage \& Naffrechoux (1969)")
        with self.voiceover(
            "Influence doesn't only flow from the many to the few. <bookmark mark='a'/> In 1969 Moscovici and his "
            "colleagues showed groups of six thirty-six slides, all of them blue. Two of the six were confederates. "
            "<bookmark mark='b'/> When the two said green every time, about eight percent of the real participants' "
            "answers were green. With no confederates, almost none were. <bookmark mark='c'/> When the two said "
            "green only some of the time, they had almost no effect. <bookmark mark='d'/> A minority moves a "
            "majority by being consistent, and its influence often shows later and in private more than in public."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(slides), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[0], DOWN), GrowFromEdge(b[2], DOWN), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def hidden(self):
        d = load("impact")
        head = heading(r"The hidden profile")
        A = axes([0.5, 5.5], [0, 1.0], x_length=5.6, y_length=3.6, xticks=[1, 2, 3, 4, 5], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"members who know a fact",
                 ylabel=r"chance it is mentioned", center=[-3.0, -0.4, 0], font_size=15)
        k, m = np.asarray(d["k"]), np.asarray(d["mention"])
        b = bars(A.ax, k, m, [AUTH] + [CROWD] * 4, width=0.6)
        rows = rows_of([
            (r"Stasser and Titus, \ 1985: \ each member of a group read part of the information about political "
             r"candidates; \ pooled, \ it favoured one, \ but each member's share favoured another", WHITE),
            (r"groups discussed what everyone already knew, \ and rarely found the best candidate", AUTH),
            (r"their sampling model: \ if each person who knows a fact mentions it with chance $p$, \ a fact known "
             r"to $k$ comes up with chance $1 - (1 - p)^k$", MODEL),
            (r"shared facts win the discussion by arithmetic alone: \ ask members to write down what they know "
             r"first", YOU),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{social.mentions}; \ Stasser \& Titus (1985)")
        with self.voiceover(
            "The second weakness of groups is subtler. <bookmark mark='a'/> In 1985 Stasser and Titus "
            "gave each member of a group part of the information about political candidates. Pooled, the information "
            "favoured one candidate; but each member's share, on its own, favoured another. <bookmark mark='b'/> "
            "Groups spent their time on what everyone already knew, and rarely found the best candidate. "
            "<bookmark mark='c'/> Their explanation was a sampling model. If each person who knows a fact mentions "
            "it with some chance, a fact known to more people is simply more likely to come up. "
            "<bookmark mark='d'/> Shared facts win the discussion by arithmetic alone. The remedy is cheap: ask "
            "members to write down what they know before anyone talks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b], lag_ratio=0.3), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
