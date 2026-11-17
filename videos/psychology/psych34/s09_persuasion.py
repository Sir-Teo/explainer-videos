from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403

PRINCIPLES = [r"reciprocity", r"commitment and consistency", r"social proof", r"authority", r"liking", r"scarcity"]


class Persuasion(VoiceoverScene):
    def construct(self):
        self.card()
        self.yale()
        self.routes()
        self.principles()
        self.towels()

    def card(self):
        card = chapter_card(8, r"Persuasion", r"What changes a mind, \ and does it last?",
                            lit={1953: r"Hovland et al.", 1981: r"Petty et al.", 2008: r"Goldstein et al."},
                            part=PART, scale=("person", "society"), marr=("what", "how"))
        with self.voiceover("Chapter eight. Persuasion."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def yale(self):
        head = heading(r"Who says what to whom")
        boxes = VGroup()
        for t, c in ((r"the communicator", AUTH), (r"the message", PERSON), (r"the audience", CROWD),
                     (r"the response", GOOD)):
            boxes.add(word_chip(t, color=c, font_size=22, width=3.0))
        boxes.arrange(RIGHT, buff=0.35).move_to([0, 1.9, 0])
        arrows = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.05, color=GREY_B,
                                stroke_width=2, max_tip_length_to_length_ratio=0.3) for k in range(3)])
        rows = rows_of([
            (r"Hovland, \ Janis and Kelley, \ 1953: \ the Yale programme broke persuasion into the communicator, \ "
             r"the message, \ the audience and its response, \ and tested each", WHITE),
            (r"Hovland and Weiss, \ 1951: \ an article from a doubtful source persuaded less at first, \ but its "
             r"effect grew over weeks, \ as the source came apart from the message: \ the sleeper effect", CROWD),
            (r"later work found the sleeper effect fragile, \ and a 2004 meta-analysis found it real under the right "
             r"conditions", MODEL),
        ], 12.4, 22, 0.36).move_to([0, -1.0, 0])
        tag = historical_tag(r"Hovland \& Weiss (1951); \ Hovland, \ Janis \& Kelley (1953)")
        with self.voiceover(
            "The experimental science of persuasion grew up at Yale. "
            "<bookmark mark='a'/> In 1953 Carl Hovland, Janis and Kelley broke persuasion into four "
            "parts: who says it, what is said, to whom, and how they respond. They tested each. "
            "<bookmark mark='b'/> In 1951 Hovland and Weiss had found something strange. An article from a "
            "doubtful source persuaded less at first, but its effect grew over the following weeks, as the source "
            "came apart from the message in memory. They called it the sleeper effect. <bookmark mark='c'/> Later "
            "work found it fragile, and a 2004 meta-analysis found it real under the right conditions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(b_) for b_ in boxes], lag_ratio=0.3),
                      FadeIn(arrows))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def routes(self):
        head = heading(r"Two routes")
        panels = VGroup()
        for k, (title, strong, weak, src) in enumerate((
                (r"the exam would apply to them", (0.85, 0.75), (0.25, 0.35), False),
                (r"the exam would not apply to them", (0.6, 0.62), (0.55, 0.58), True))):
            A = axes([-0.6, 1.6], [0, 1.0], x_length=3.8, y_length=2.8, xticks=None, yticks=None,
                     ylabel=r"agreement" if k == 0 else "", center=[-4.5 + 4.3 * k, 0.4, 0], font_size=14)
            xs = [0, 1]
            lines = VGroup(curve(A.ax, xs, [weak[0], strong[0]], AUTH, stroke_width=4),
                           curve(A.ax, xs, [weak[1], strong[1]], GOOD, stroke_width=4))
            if src:
                lines = VGroup(curve(A.ax, xs, [0.3, 0.38], AUTH, stroke_width=4),
                               curve(A.ax, xs, [0.75, 0.82], GOOD, stroke_width=4))
            names = VGroup(label(r"weak arguments", font_size=14, color=GREY_A).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                           label(r"strong", font_size=14, color=GREY_A).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15))
            t = wrapped_label(title, 3.8, 17, WHITE).next_to(A, UP, buff=0.15)
            panels.add(VGroup(A, lines, names, t))
        key = legend([(AUTH, r"a non-expert source"), (GOOD, r"an expert source")], font_size=15)
        key.next_to(panels, DOWN, buff=0.35)
        rows = rows_of([
            (r"Petty, \ Cacioppo and Goldman, \ 1981: \ students read a case for a senior exam, \ with strong or weak "
             r"arguments, \ from an expert or not", WHITE),
            (r"when the exam would affect them, \ argument quality decided their attitude; \ when it would not, \ the "
             r"source's expertise did", PERSON),
            (r"the elaboration likelihood model: \ a central route through the arguments, \ when people are able and "
             r"motivated to think, \ and a peripheral route through cues", MODEL),
            (r"the pattern of the result, \ drawn schematically", GREY_B),
        ], 4.2, 18, 0.3).move_to([4.8, -0.2, 0])
        tag = historical_tag(r"Petty, \ Cacioppo \& Goldman (1981)")
        with self.voiceover(
            "Why does a source matter sometimes and not others? <bookmark mark='a'/> In 1981 Petty, Cacioppo and "
            "Goldman had students read a proposal for a new senior exam. The arguments were "
            "strong or weak, and came from an expert or not. <bookmark mark='b'/> When the exam would affect the "
            "students themselves, the quality of the arguments decided their attitude. When it wouldn't, the "
            "source's expertise did. <bookmark mark='c'/> Their elaboration likelihood model has two routes: a "
            "central one, through the arguments, when people are able and motivated to think; and a peripheral one, "
            "through cues like who is speaking. <bookmark mark='d'/> The charts show the pattern of the result, "
            "drawn schematically."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(p[0]) for p in panels], *[FadeIn(p[2]) for p in panels],
                      *[FadeIn(p[3]) for p in panels])
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[Create(p[1]) for p in panels], FadeIn(key), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def principles(self):
        head = heading(r"Six principles, \ from the field")
        chips = VGroup(*[word_chip(p, color=c, font_size=22, width=4.2) for p, c in zip(
            PRINCIPLES, (GOOD, PERSON, CROWD, AUTH, MODEL, YOU))]).arrange_in_grid(2, 3, buff=(0.4, 0.35))
        chips.move_to([0, 1.5, 0])
        rows = rows_of([
            (r"Cialdini, \ \emph{Influence}, \ 1984: \ drawing on the work of salespeople, \ fund-raisers and "
             r"recruiters, \ he sorted their tactics into six principles", WHITE),
            (r"social proof is this part's subject seen from the seller's side: \ people do what they see others do",
             CROWD),
            (r"the principles are well supported as tendencies; \ how large each effect is in a given campaign is a "
             r"question for field experiments, \ Part 55's subject", YOU),
        ], 12.4, 22, 0.36).move_to([0, -1.3, 0])
        tag = historical_tag(r"Cialdini (1984)")
        with self.voiceover(
            "Meanwhile, persuasion was being studied in the field. <bookmark mark='a'/> In his 1984 book Influence, "
            "Cialdini drew on the work of salespeople, fund-raisers and recruiters, and sorted their tactics "
            "into six principles: reciprocity, commitment and consistency, social proof, authority, liking and "
            "scarcity. <bookmark mark='b'/> Social proof is this part's subject seen from the seller's side: people "
            "do what they see others do. <bookmark mark='c'/> The principles are well supported as tendencies. How "
            "large each effect is in a given campaign is a question for field experiments, Part 55's subject."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(c_) for c_ in chips], lag_ratio=0.2))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def towels(self):
        head = heading(r"Norms on a hotel door")
        A = axes([-0.6, 1.6], [0, 50], x_length=4.4, y_length=3.6, xticks=None, yticks=[0, 25, 50],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"guests who reused towels", center=[-3.9, -0.3, 0],
                 font_size=15)
        b = bars(A.ax, [0, 1], [35.1, 44.1], [CROWD, GOOD], width=0.6)
        names = VGroup(label(r"``help the environment''", font_size=14, color=CROWD).next_to(A.ax.c2p(0, 0), DOWN,
                                                                                              buff=0.2),
                       label(r"``most guests reuse''", font_size=14, color=GOOD).next_to(A.ax.c2p(1, 0), DOWN,
                                                                                         buff=0.2))
        tops = VGroup(label(r"35.1\%", font_size=17, color=CROWD).next_to(A.ax.c2p(0, 35.1), UP, buff=0.1),
                      label(r"44.1\%", font_size=17, color=GOOD).next_to(A.ax.c2p(1, 44.1), UP, buff=0.1))
        rows = rows_of([
            (r"Goldstein, \ Cialdini and Griskevicius, \ 2008: \ cards in hotel rooms, \ 1{,}058 chances to reuse "
             r"a towel", WHITE),
            (r"saying that most guests reused their towels beat the standard environmental appeal, \ 44.1\% to "
             r"35.1\%; \ ``most guests in this room'' did best of all", GOOD),
            (r"Bohner and Schl\"uter, \ 2014: \ two German hotels: \ both messages raised reuse above no message, \ "
             r"but the norm message did no better than the standard one", AUTH),
            (r"descriptive norms work in some places and not in others: \ a reason to test in the place you mean to "
             r"use them", YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.3, 0])
        tag = published_tag(r"Goldstein et al.\ (2008); \ Bohner \& Schl\"uter (2014)")
        with self.voiceover(
            "Here is social proof in a field experiment. <bookmark mark='a'/> In 2008 Goldstein, Cialdini and "
            "Griskevicius put cards in hotel rooms, and counted one thousand and fifty-eight "
            "chances to reuse a towel. <bookmark mark='b'/> A card saying that most guests reused their towels beat "
            "the standard appeal to help the environment, forty-four percent to thirty-five. A card about guests "
            "who'd stayed in that very room did best of all. <bookmark mark='c'/> In 2014 Bohner and Schlüter ran "
            "the study again in two German hotels. Both messages raised reuse above no message at all, but the norm "
            "did no better than the standard appeal. <bookmark mark='d'/> Descriptive norms work in some places and "
            "not in others, which is a reason to test them in the place you mean to use them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[0], DOWN), GrowFromEdge(b[1], DOWN), FadeIn(tops), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
