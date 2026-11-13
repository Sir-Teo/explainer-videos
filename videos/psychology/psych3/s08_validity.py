from __future__ import annotations

import numpy as np

from videos.psychology.psych3.common import *  # noqa: F403

INITIAL = {"conscientious": r"C", "neurotic": r"N", "extravert": r"E"}


class Validity(VoiceoverScene):
    def construct(self):
        self.card()
        self.kinds()
        self.network()
        self.matrix()

    def card(self):
        card = chapter_card(7, r"Does it measure what its name says?", r"A score is reliable. \ Of what?",
                            lit={1955: r"Cronbach \& Meehl: construct validity", 1959: r"Campbell \& Fiske's matrix"},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter seven. Does it measure what its name says?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def kinds(self):
        head = heading(r"Reliable is not yet valid")
        # a tape measure round a head: as reliable as you like
        skull = head_outline(height=2.6).move_to([-5.0, 1.0, 0])
        tape = Ellipse(width=1.75, height=0.5, color=P.ACCENT, stroke_width=5).move_to(skull.get_center() + UP * 0.55 + LEFT * 0.12)
        tape_l = VGroup(label(r"hat size", font_size=30, color=P.ACCENT),
                        label(r"measured twice: \ the same to the millimetre", font_size=26, color=GREY_A),
                        label(r"as a test of intelligence: \ nearly useless", font_size=26, color=ERRC))
        tape_l.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([-0.3, 1.25, 0])
        cards = VGroup()
        for title, q, ex, color in (
                (r"content", r"Do the questions cover the whole territory?",
                 r"an arithmetic test that only ever asks for sums", GROUP_A),
                (r"criterion", r"Does the score predict what it should?",
                 r"an entrance test, against the marks a year later", GROUP_B),
                (r"construct", r"Does the score behave as the attribute should?",
                 r"everything else in this chapter", TRUE)):
            body = VGroup(label(title, font_size=34, color=color), wrapped_label(q, 3.7, 27, WHITE),
                          wrapped_label(ex, 3.7, 24, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            box = panel(4.2, 2.75, color=color)
            body.move_to(box)
            cards.add(VGroup(box, body))
        cards.arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "So far we've asked how much of a score is error. Now the harder question. Suppose there's no error "
            "at all. What is the score a score of? <bookmark mark='a'/> Measure the size of someone's head with "
            "a tape. Do it again tomorrow, and you'll get the same answer to the millimetre. As a measurement "
            "it's nearly perfectly reliable. As a test of intelligence it's nearly useless, though in the "
            "nineteenth century people used it as one. Reliability tells you a number is repeatable. It doesn't tell you what the number "
            "is about. That second property is called validity, and there are three kinds of evidence for it. "
            "<bookmark mark='b'/> Content: do the questions cover the territory they claim to? "
            "<bookmark mark='c'/> Criterion: does the score predict something it ought to predict? "
            "<bookmark mark='d'/> And construct validity, the deepest of the three: does the score behave, in "
            "every way you can check, as the attribute it's named after would behave? For most of what "
            "psychology measures there's no criterion to compare against. There's no independent gauge of "
            "anxiety. So the third kind carries most of the weight."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(skull), Create(tape), FadeIn(tape_l[0]))
            self.play(FadeIn(tape_l[1]))
            self.wait(4.0)
            self.play(FadeIn(tape_l[2]))
            for m, c in zip("bcd", cards):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.2))
        self.clear_scene()

    def network(self):
        head = heading(r"A construct is known by its connections")
        hc = history_card(1955, r"Lee Cronbach and Paul Meehl", r"the ``nomological network'': \ a web of laws "
                          r"tying a construct to other constructs and to things you can observe", color=P.ARCHIVE,
                          width=5.4, font_size=24).move_to([-4.2, 1.7, 0])

        def construct(text, pos, color=TRUE):
            t = label(text, font_size=24, color=color)
            c = DashedVMobject(Ellipse(width=t.width + 0.6, height=0.85, color=color, stroke_width=3), num_dashes=30)
            return VGroup(c, t).move_to(pos)

        def observed(text, pos):
            t = label(text, font_size=22, color=OBS)
            return VGroup(SurroundingRectangle(t, color=OBS, buff=0.14, stroke_width=2), t).move_to(pos)

        centre = construct(r"conscientiousness", [1.6, 0.7, 0], P.ACCENT)
        others = [construct(r"achievement", [5.2, 2.1, 0]), construct(r"impulsiveness", [5.3, -0.6, 0]),
                  construct(r"intelligence", [1.6, 2.6, 0])]
        signs = [(r"$+$", TRUE), (r"$-$", ERRC), (r"$0$", GREY_B)]
        links = VGroup()
        for o, (sg, col) in zip(others, signs):
            ln = Line(centre.get_center(), o.get_center(), color=col, stroke_width=4, buff=0.75)
            links.add(VGroup(ln, label(sg, font_size=34, color=col).move_to(ln.get_center() + UP * 0.28 + LEFT * 0.1)))
        obs = [observed(r"questionnaire score", [-0.3, -1.55, 0]), observed(r"a friend's rating", [2.5, -2.2, 0]),
               observed(r"days late for work", [5.2, -2.45, 0])]
        down = VGroup(*[Arrow(centre.get_bottom(), o.get_top(), color=GREY_B, stroke_width=3, buff=0.1,
                              max_tip_length_to_length_ratio=0.1) for o in obs])
        key = VGroup(label(r"dashed: \ never seen", font_size=22, color=GREY_A),
                     label(r"boxed: \ what you can observe", font_size=22, color=OBS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-4.6, -0.2, 0])
        end = wrapped_label(r"A test is valid for a construct as far as the predicted pattern comes out: \ the "
                            r"links that should be there, and the ones that should not.", 4.3, 26, P.ACCENT)
        end.move_to([-4.6, -2.2, 0])
        tag = note(r"schematic").to_corner(UR, buff=0.2)
        with self.voiceover(
            "How can you check a measure against something nobody can see? In 1955 Lee Cronbach and Paul Meehl "
            "gave the answer the field still uses. <bookmark mark='a'/> An attribute like conscientiousness is "
            "never observed. But a theory of it says what it's connected to. <bookmark mark='b'/> It should go "
            "with achievement. It should go against impulsiveness. And, if the theory is any good, it should "
            "have nothing much to do with intelligence. <bookmark mark='c'/> It should also show up in things "
            "you can observe: in what people say about themselves, in what their friends say about them, in "
            "how often they turn up late. <bookmark mark='d'/> Cronbach and Meehl called this web the "
            "nomological network. A test is valid for a construct to the extent that the web comes out as "
            "predicted. Including the zeros: a test that correlates with everything measures nothing in "
            "particular. Notice that this makes validity an argument and never a number. And it ties the test "
            "and the theory together: if a prediction fails, either the test is bad or the theory is wrong, "
            "and the data alone won't say which."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(centre), FadeIn(key[0]))
            vo.wait_until("b")
            for o, ln in zip(others, links):
                self.play(FadeIn(o), FadeIn(ln), run_time=1.2)
                self.wait(1.2)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(o)) for a, o in zip(down, obs)], lag_ratio=0.5),
                      FadeIn(key[1]), run_time=3.5)
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.15))
        self.clear_scene()

    def matrix(self):
        d = load("validity")
        head = heading(r"Three traits, each measured three ways")
        r = np.asarray(d["r"])
        hm = heatmap(r, cell=0.6, font_size=18, diagonal=False).move_to([-3.5, -0.45, 0])
        labels = [(t, m) for t, m in d["labels"]]
        ticks = VGroup()
        for i, (t, m) in enumerate(labels):
            ticks.add(label(INITIAL[t], font_size=22, color=TRAIT[t]).next_to(hm.cells[i][0], LEFT, buff=0.12))
            ticks.add(label(INITIAL[t], font_size=22, color=TRAIT[t]).next_to(hm.cells[0][i], UP, buff=0.1))
        blocks = VGroup()
        for k, m in enumerate(d["methods"]):
            g = VGroup(*[hm.cells[0][3 * k + j] for j in range(3)])
            blocks.add(label(METHOD_NAME[m], font_size=22, color=GREY_A).next_to(g, UP, buff=0.42))
        key = VGroup(*[label(rf"{INITIAL[t]}: \ {TRAIT_NAME[t]}", font_size=24, color=TRAIT[t]) for t in d["traits"]])
        key.arrange(RIGHT, buff=0.45).next_to(hm, DOWN, buff=0.2)

        def frames(kind, color):
            out = VGroup()
            for i, (ti, mi) in enumerate(labels):
                for j, (tj, mj) in enumerate(labels):
                    if j >= i:
                        continue
                    if (kind == "convergent" and ti == tj) or (kind == "same_method" and ti != tj and mi == mj):
                        out.add(SurroundingRectangle(hm.cells[i][j], color=color, buff=0.0, stroke_width=4))
            return out

        conv, same = frames("convergent", WHITE), frames("same_method", GROUP_B)
        p = d["planted"]
        rows = VGroup(
            VGroup(label(r"same trait, different method", font_size=28, color=WHITE),
                   label(rf"{r2(p['convergent'])}", font_size=44, color=WHITE)),
            VGroup(label(r"different traits, same method", font_size=28, color=GROUP_B),
                   label(rf"{r2(p['same_method'])}", font_size=44, color=GROUP_B)),
            VGroup(label(r"different traits, different methods", font_size=28, color=GREY_A),
                   label(rf"{r2(p['neither'])}", font_size=44, color=GREY_A)),
        )
        for row in rows:
            row.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.7, 1.0, 0])
        sizes = label(r"(average sizes, ignoring the sign)", font_size=22, color=GREY_B)
        sizes.next_to(rows, DOWN, buff=0.2).align_to(rows, LEFT)
        verdict = wrapped_label(r"Each method leaves its own mark on every score it produces. \ Part of what a "
                                r"questionnaire measures is the filling-in of questionnaires.", 5.2, 26, P.ACCENT)
        verdict.next_to(sizes, DOWN, buff=0.35).align_to(rows, LEFT)
        keep_in_frame(verdict)
        tag = simulated_tag()
        with self.voiceover(
            "Four years later Donald Campbell, whom you met in Part 2, and Donald Fiske turned that idea into a "
            "table you can compute. <bookmark mark='a'/> Take three traits, and measure each of them three "
            "ways: by questionnaire, by a friend's rating, and from records. That's nine scores, and here are "
            "all their correlations. <bookmark mark='b'/> First, look at the same trait measured by different "
            f"methods. Those correlations average {p['convergent']:.2f}. If two methods are both measuring "
            "conscientiousness, they'd better agree. This is called convergent validity. "
            "<bookmark mark='c'/> Now the other side, which was the new idea. Look at different traits measured "
            f"by the same method. Those average {p['same_method']:.2f}, <bookmark mark='d'/> where different "
            f"traits measured by different methods give {p['neither']:.2f}. The gap is the method. A person "
            "who tends to agree with questionnaire items agrees with all of them, whatever they're about. In "
            "the Pool we planted that on purpose. In real data it's always there. <bookmark mark='e'/> So a "
            "measure has to pass two tests. It must agree with other measures of the same thing. And it must "
            "not agree too well with measures of other things that merely share its method. The second "
            "test is the one that's usually skipped."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hm, lag_ratio=0.01), FadeIn(ticks), FadeIn(blocks), FadeIn(key), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(conv), FadeIn(rows[0]), FadeIn(sizes))
            vo.wait_until("c")
            self.play(FadeOut(conv), Create(same), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeOut(same), FadeIn(verdict, shift=UP * 0.15))
        self.clear_scene()
