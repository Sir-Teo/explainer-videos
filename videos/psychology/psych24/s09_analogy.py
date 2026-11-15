from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


class Analogy(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.mapping()

    def card(self):
        card = chapter_card(8, r"Analogy", r"Why do people miss an answer they have already seen?",
                            lit={1980: r"Gick \& Holyoak", 1983: r"Gentner"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter eight. Analogy."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def problem(self):
        head = heading(r"The radiation problem")
        tumour = Circle(radius=0.35, color=LOST, fill_opacity=0.6).move_to([-3.6, 0.3, 0])
        body = Ellipse(width=4.4, height=3.0, color=GREY_B, stroke_width=2).move_to([-3.6, 0.3, 0])
        rays = VGroup(*[Line([-3.6 + 2.6 * np.cos(a), 0.3 + 2.0 * np.sin(a), 0], tumour.get_center()
                             + 0.38 * np.array([np.cos(a), np.sin(a), 0]), color=CONTENT, stroke_width=2)
                        for a in np.linspace(0, 2 * np.pi, 7)[:-1]])
        big = Line([-6.4, 0.3, 0], tumour.get_left(), color=CONTENT, stroke_width=10)
        lt = label(r"a tumour, \ healthy tissue around it", font_size=21, color=GREY_A).next_to(body, DOWN, buff=0.2)
        rows = rows_of([
            (r"Duncker's problem: \ rays strong enough to destroy the tumour destroy the tissue they pass through; "
             r"\ weak rays are harmless, \ and useless", WHITE),
            (r"the answer: \ many weak rays from different directions, \ meeting at the tumour", CONTENT),
            (r"Gick \& Holyoak, \ 1980: \ about one person in ten finds it unaided", GREY_A),
            (r"after reading a story with the same solution, \ about three in ten", INSIGHT),
            (r"told that the story might help, \ about three in four", MODEL),
        ], 5.8, 23, 0.34).move_to([3.5, 0.0, 0])
        story = label(r"the story: \ a general splits his army to converge on a fortress by many roads", font_size=21,
                      color=INSIGHT).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Duncker (1945); \ Gick \& Holyoak (1980)")
        with self.voiceover(
            "Here's another of Duncker's problems. <bookmark mark='a'/> A patient has a tumour that can be "
            "destroyed by rays. But rays strong enough to destroy it also destroy the healthy tissue they pass "
            "through, and weak rays do no harm, and no good. <bookmark mark='b'/> The answer is to send many weak "
            "rays from different directions, meeting at the tumour. <bookmark mark='c'/> In 1980 Mary Gick and Keith "
            "Holyoak found that about one person in ten finds this unaided. <bookmark mark='d'/> Before the problem "
            "they had people read a story: a general captures a fortress by splitting his army and sending it down "
            "many roads at once. After the story, about three people in ten solved the radiation problem. "
            "<bookmark mark='e'/> Told that the story might help, about three in four did. People had the answer "
            "and didn't see that it applied."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(body), FadeIn(tumour), FadeIn(lt))
            vo.wait_until("a")
            self.play(Create(big), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeOut(big), LaggedStart(*[Create(r) for r in rays], lag_ratio=0.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(story), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def mapping(self):
        d = load("analogy")
        head = heading(r"Structure mapping, \ computed")
        pairs = [(str(a), str(b)) for a, b in d["pairs"]]
        left = VGroup(*[word_chip(a, INSIGHT, 26) for a, _ in pairs]).arrange(DOWN, buff=0.35).move_to([-4.6, 0.4, 0])
        right = VGroup(*[word_chip(b, CONTENT, 26) for _, b in pairs]).arrange(DOWN, buff=0.35).move_to(
            [-1.4, 0.4, 0])
        links = VGroup(*[Arrow(l_.get_right(), r_.get_left(), buff=0.1, color=MODEL, stroke_width=3)
                         for l_, r_ in zip(left, right)])
        hl = label(r"fortress story", font_size=24, color=INSIGHT).next_to(left, UP, buff=0.3)
        hr = label(r"radiation problem", font_size=24, color=CONTENT).next_to(right, UP, buff=0.3)
        rel = label(r"$\text{cause}(\text{divide}(x),\ \text{converge}(x, y))$", font_size=24, color=MODEL)
        rel.next_to(VGroup(left, right), DOWN, buff=0.45)
        rows = rows_of([
            (r"Gentner, \ 1983: \ an analogy maps \emph{relations}, \ not appearances; \ objects correspond if "
             r"they play the same roles", WHITE),
            (r"and a mapping that keeps a connected system of relations, \ causes over effects, \ is preferred: "
             r"\ \emph{systematicity}", LOGIC),
            (rf"Psyche tries every one-to-one mapping of the objects and keeps the one that matches the most "
             rf"relations: \ {d['n_matched']} matched, \ score {d['score']}", MODEL),
            (r"armies do not look like rays: \ that is why the story is missed, \ and why a hint is enough", GREY_A),
        ], 5.6, 23, 0.36).move_to([3.7, 0.0, 0])
        tag = psyche_tag(r"\texttt{reason.structure\_map}")
        with self.voiceover(
            "What does it take to see an analogy? <bookmark mark='a'/> Dedre Gentner proposed in 1983 that an "
            "analogy maps relations, not appearances. Objects correspond when they play the same roles. "
            "<bookmark mark='b'/> And the best mapping keeps a connected system of relations, with causes linking "
            "events, which she called systematicity. <bookmark mark='c'/> Psyche writes both stories as relations: "
            "dividing a force causes it to converge on a target, which causes the target's capture. Then it tries "
            "every one-to-one mapping of the objects and keeps the one that matches the most relations. The army "
            "maps to the rays, the fortress to the tumour, the general to the doctor. <bookmark mark='d'/> Nothing "
            "about an army looks like a ray. That's why people miss the analogy, and why a single hint is enough "
            "to make them look at the relations instead."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(hl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(right), FadeIn(hr), LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.3),
                      FadeIn(rel), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
