from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


class Cooperate(VoiceoverScene):
    def construct(self):
        self.card()
        self.routes()
        self.tournament()

    def card(self):
        card = chapter_card(3, r"Why cooperate?", r"How can helping a stranger pay?",
                            lit={1964: r"Hamilton", 1980: r"Axelrod"}, part=PART, scale=("gene", "group"),
                            marr=("why",))
        with self.voiceover("Chapter three. Why cooperate?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def routes(self):
        head = heading(r"Four routes to cooperation")
        items = [
            (r"kin", r"help relatives, \ who share your genes: \ Hamilton's rule \ (1964), \ help when $rB > C$, \ with $r$ "
             r"the relatedness", GOOD),
            (r"reciprocity", r"help those who will help you back: \ works when you meet again \ (Trivers's "
             r"reciprocal altruism, \ 1971)", CROWD),
            (r"reputation", r"help, \ and others see it, \ and help you: \ works when others are watching", PERSON),
            (r"punishment", r"make cheating costly, \ even at a cost to yourself: \ works when someone will pay to "
             r"punish", AUTH),
        ]
        rows = VGroup()
        for what, how, c in items:
            rows.add(VGroup(word_chip(what, color=c, font_size=20, width=3.0), wrapped_label(how, 8.8, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "If defecting pays, why does anyone cooperate? Biology and economics found four routes. "
            "<bookmark mark='a'/> Kin: helping relatives, who share your genes. William Hamilton's rule, from 1964, says help when the "
            "benefit times your relatedness exceeds the cost. A sibling counts half, a cousin an eighth. "
            "<bookmark mark='b'/> Reciprocity: help those who'll help you back, which works when you'll meet "
            "again; Robert Trivers called it reciprocal altruism, in 1971. <bookmark mark='c'/> Reputation: help, be seen helping, and be helped by others, which works "
            "when people are watching. <bookmark mark='d'/> And punishment: make cheating costly, even at a cost to "
            "yourself, which works when someone is willing to pay to punish."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def tournament(self):
        d = load("tournament")
        head = heading(r"A tournament of strategies")
        names = d["names"]
        A = axes([-0.6, len(names) - 0.4], [1.5, 2.8], x_length=9.6, y_length=2.6, xticks=None,
                 yticks=[1.5, 2, 2.5], yfmt=lambda v: f"{v:g}", ylabel=r"average points per move",
                 center=[-0.6, 1.0, 0], font_size=14)
        xs = np.arange(len(names))
        clean = bars(A.ax, xs - 0.18, d["clean_score"], CROWD, width=0.34)
        noisy = bars(A.ax, xs + 0.18, d["noisy_score"], AUTH, width=0.34)
        lab = VGroup(*[wrapped_label(n, 1.25, 14, GREY_A).next_to(A.ax.c2p(k, 1.5), DOWN, buff=0.12)
                       for k, n in enumerate(names)])
        key = legend([(CROWD, r"exact moves"), (AUTH, r"5\% of moves flipped")], font_size=14).next_to(A, RIGHT,
                                                                                                    buff=0.2)
        best_c = names[int(np.argmax(d["clean_score"]))]
        best_n = names[int(np.argmax(d["noisy_score"]))]
        rows = rows_of([
            (r"Axelrod, \ 1980: \ strategies submitted by scientists played each other for 200 moves; \ the "
             r"simplest, \ Tit for Tat, \ submitted by Anatol Rapoport, \ scored most, \ and won a second "
             r"tournament too", WHITE),
            (rf"Psyche's own round-robin of seven strategies: \ with exact moves, \ {best_c} scores most; \ with "
             rf"noise, \ {best_n}", MODEL),
            (r"the strategies that do well are nice, \ retaliate, \ and forgive; \ which one wins depends on who "
             r"else is in the tournament, \ and on noise", YOU),
        ], 12.4, 20, 0.26).move_to([0, -2.45, 0])
        tag = psyche_tag(r"\texttt{social.ipd\_tournament}; \ Axelrod (1980)")
        with self.voiceover(
            "Reciprocity can be studied as a contest. <bookmark mark='a'/> In 1980 Robert Axelrod invited scientists "
            "to submit strategies for a repeated prisoner's dilemma, and had them play each other for two hundred "
            "moves. The simplest, Tit for Tat, submitted by Anatol Rapoport, scored the most: cooperate first, then "
            "copy what the other did last. It won a second tournament too. <bookmark mark='b'/> Here's Psyche's own "
            f"round-robin of seven strategies. With exact moves, {best_c} scores most. When five percent of moves "
            f"are flipped by mistake, {best_n} does best. <bookmark mark='c'/> The strategies that do well are "
            "nice, retaliate and forgive. Which one wins depends on who else is in the tournament, and on noise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lab))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(clean), FadeIn(noisy), FadeIn(key), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
