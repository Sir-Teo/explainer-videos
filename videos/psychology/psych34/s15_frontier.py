from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.twins()
        self.amplification()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ influence at scale",
                            r"Can influence be measured in networks of millions?",
                            lit={2011: r"Shalizi \& Thomas", 2017: r"Becker et al.", 2022: r"Husz\'ar et al."},
                            part=PART, scale=("society",), marr=("what", "how"))
        with self.voiceover("Chapter fourteen. Frontier: influence at scale."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def twins(self):
        d = load("twins")
        head = heading(r"Contagion, \ or birds of a feather?")
        A = axes([-0.6, 3.6], [0, 0.7], x_length=6.0, y_length=3.4, xticks=None, yticks=[0, 0.2, 0.4, 0.6],
                 yfmt=lambda v: f"{v:g}", ylabel=r"chance a friend adopts", center=[-3.0, -0.4, 0], font_size=15)
        pc, ph = d["p_contagion"], d["p_homophily"]
        b = bars(A.ax, [0, 1, 2.4, 3.4], [pc[0], pc[1], ph[0], ph[1]], [AUTH, GREY_B, AUTH, GREY_B], width=0.55)
        names = VGroup(label(r"world 1: \ influence", font_size=16, color=CROWD).next_to(A.ax.c2p(0.5, 0), DOWN,
                                                                                        buff=0.45),
                       label(r"world 2: \ a shared hidden trait", font_size=16, color=MODEL)
                       .next_to(A.ax.c2p(2.9, 0), DOWN, buff=0.45))
        sub = VGroup(*[label(t, font_size=13, color=GREY_A).next_to(A.ax.c2p(x, 0), DOWN, buff=0.12)
                       for x, t in ((0, r"you adopted"), (1, r"you did not"), (2.4, r"you adopted"),
                                    (3.4, r"you did not"))])
        rows = rows_of([
            (rf"two simulated worlds of 4{{,}}000 pairs of friends with the same correlation in what they do: \ "
             rf"{d['r_contagion']:.2f} and {d['r_homophily']:.2f}", WHITE),
            (r"in the first, \ one friend's adoption causes the other's; \ in the second, \ nobody influences anyone: "
             r"\ friends share a trait that makes both adopt", MODEL),
            (r"Shalizi and Thomas, \ 2011: \ from observational network data, \ influence and hidden homophily are "
             r"generically confounded, \ and cannot be told apart without strong assumptions", AUTH),
            (r"which is why chapter thirteen's evidence came from randomized experiments", YOU),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"simulated; \ Shalizi \& Thomas (2011)")
        with self.voiceover(
            "The frontier is measuring influence at scale. The first problem is old. <bookmark mark='a'/> Here are "
            "two simulated worlds of four thousand pairs of friends, with the same correlation in what they do. "
            "<bookmark mark='b'/> In the first, one friend's adoption causes the other's. In the second, nobody "
            "influences anyone: friends share a trait that makes both of them adopt. <bookmark mark='c'/> In 2011 "
            "Cosma Shalizi and Andrew Thomas proved that, from observational network data, influence and hidden "
            "homophily are generically confounded. Without strong assumptions, they can't be told apart. "
            "<bookmark mark='d'/> Which is why the evidence in chapter thirteen came from randomized experiments."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def amplification(self):
        head = heading(r"When the network is an algorithm")
        rows = rows_of([
            (r"Husz\'ar and colleagues, \ 2022, \ \emph{PNAS}: \ Twitter had kept a randomized control group of "
             r"nearly two million accounts on a reverse-chronological feed", WHITE),
            (r"against it, \ the ranking algorithm amplified the mainstream political right more than the left in "
             r"six of seven countries; \ Germany was the exception", AUTH),
            (r"it did not amplify the far left or far right over moderates", CROWD),
            (r"the same randomized logic as Salganik's music market, \ run by a platform on its own users", MODEL),
            (r"who sees whose opinions is now partly set by a ranking system: \ chapter ten's ``who listens to "
             r"whom'', \ chosen by code", YOU),
        ], 12.4, 22, 0.34).move_to([0, -0.3, 0])
        tag = published_tag(r"Husz\'ar et al.\ (2022)")
        with self.voiceover(
            "The second problem is new. Much of who hears whom is now chosen by a ranking algorithm. "
            "<bookmark mark='a'/> In 2022 Huszár and colleagues used a randomized control group Twitter had "
            "kept: nearly two million accounts that saw their feed in reverse chronological order. "
            "<bookmark mark='b'/> Against it, the ranking algorithm amplified the mainstream political right more "
            "than the left in six of seven countries. Germany was the exception. <bookmark mark='c'/> It did not "
            "amplify the far left or far right over moderates. <bookmark mark='d'/> It's the same randomized logic "
            "as the music market, run by a platform on its own users. <bookmark mark='e'/> Who listens to whom, the "
            "parameter that decided chapter ten's camps, is now partly set by code."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"how much of the famous obedience and conformity effects survives procedures that cannot be "
             r"disbelieved?", AUTH),
            (r"how can influence be separated from homophily outside experiments?", MODEL),
            (r"what network structures keep crowds wise, \ and can platforms be designed for them?", CROWD),
            (r"when does a norm message change behaviour, \ and where does it backfire?", GOOD),
            (r"who should run experiments on millions of people, \ and with what consent?", YOU),
        ], 12.4, 24, 0.46).move_to([0, -0.2, 0])
        with self.voiceover(
            "So, open questions. <bookmark mark='a'/> How much of the famous obedience and conformity effects "
            "survives procedures that can't be disbelieved? <bookmark mark='b'/> How can influence be separated from "
            "homophily outside experiments? <bookmark mark='c'/> Which network structures keep crowds wise, and can "
            "platforms be designed for them? <bookmark mark='d'/> When does a norm message change behaviour, and "
            "where does it backfire? <bookmark mark='e'/> And who should run experiments on millions of people, and "
            "with what consent?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
