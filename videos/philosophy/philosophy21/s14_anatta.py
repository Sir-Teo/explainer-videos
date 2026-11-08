from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Anatta(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"No self: \ the chariot and the bundle", r"Is there a self at all?",
                            lit=(-150, 1739), part=PART)
        with self.voiceover("Chapter thirteen. No self: the chariot and the bundle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.chariot()
        self.hume()
        self.views()
        self.middle()
        self.modern()

    def chariot(self):
        head = label(r"The chariot \ (\textit{Milindapañha})", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        wheel = VGroup(Circle(radius=0.55, color=WHOLE, stroke_width=4).move_to([-4.0, -0.3, 0]),
                       *[Line([-4.0, -0.3, 0], [-4.0 + 0.55 * np.cos(a), -0.3 + 0.55 * np.sin(a), 0], color=WHOLE,
                              stroke_width=2) for a in np.linspace(0, PI, 4)[:-1]],
                       *[Line([-4.0, -0.3, 0], [-4.0 + 0.55 * np.cos(a), -0.3 + 0.55 * np.sin(a), 0], color=WHOLE,
                              stroke_width=2) for a in np.linspace(PI, 2 * PI, 4)[:-1]])
        pieces = [
            Line([-3.25, 0.35, 0], [-1.0, 0.65, 0], color=WHOLE, stroke_width=6),                        # pole
            Line([-4.35, -0.3, 0], [-3.65, -0.3, 0], color=GREY_A, stroke_width=8),                       # axle
            wheel,                                                                                       # wheels
            Rectangle(width=1.5, height=0.65, color=WHOLE, fill_opacity=0.3).move_to([-4.0, 0.6, 0]),    # frame
            VGroup(Line([-4.6, 0.9, 0], [-4.6, 2.25, 0], color=GREY_A, stroke_width=3),
                   Polygon([-4.6, 2.25, 0], [-3.85, 2.05, 0], [-4.6, 1.85, 0], color=NOM, fill_opacity=0.7)),  # banner
            Line([-1.1, 0.35, 0], [-1.1, 1.0, 0], color=WHOLE, stroke_width=6),                          # yoke
            ArcBetweenPoints([-3.45, 1.0, 0], [-1.15, 0.95, 0], angle=-0.6, color=UNIV, stroke_width=2.5),  # reins
            Line([-3.6, 0.95, 0], [-2.95, 2.05, 0], color=GREY_B, stroke_width=2),                       # goad
        ]
        parts = [r"pole", r"axle", r"wheels", r"frame", r"banner", r"yoke", r"reins", r"goad"]
        chariot = VGroup(*pieces)
        tags = VGroup()
        targets = []
        for i, nm in enumerate(parts):
            c = np.array([-5.9 + 1.3 * (i % 4), 1.5 - 1.6 * (i // 4), 0])
            targets.append(c)
            tags.add(label(nm, font_size=19, color=PARTC).move_to(c + DOWN * 0.62))
        q = label(r"is the chariot any of these? \ \ all of them? \ \ something else?", font_size=20,
                  color=GOAL).move_to([-3.6, -1.75, 0])
        rows = stack([(r"King Milinda asks the monk Nāgasena his name", WHITE),
                      (r"`Nāgasena' is only a designation; \ no person is found", NOM),
                      (r"the chariot: \ not the pole, \ not the axle, \ not their sum taken as a thing", PARTC),
                      (r"`chariot' is a convenient name for parts in dependence", GOAL),
                      (r"two truths: \ conventionally there are chariots and persons; \ ultimately, \ parts and "
                       r"events", UNIV)], font_size=20, aligned_edge=LEFT, width=6.2).move_to([3.75, -0.2, 0])
        with self.voiceover(
            "Buddhist philosophers denied that there is a self at all. <bookmark mark='a'/>In the Milindapañha, the "
            "Questions of King Milinda, the Greek-descended king asks the monk Nāgasena his name. "
            "<bookmark mark='b'/>Nāgasena answers that Nāgasena is only a designation, and no person is found in it. "
            "<bookmark mark='c'/>The king objects, and Nāgasena asks him how he came: by chariot. Then what is the "
            "chariot? Is it the pole, the axle, the wheels? None of these. Is it something apart from them? No. "
            "<bookmark mark='d'/>Chariot is a convenient name for parts in a certain dependence, and so is Nāgasena. "
            "<bookmark mark='e'/>Two truths: conventionally, there are chariots and persons; ultimately, there are "
            "only parts and events in causal series."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[Create(pc) for pc in pieces], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(*[pc.animate.scale(min(1.0, 1.0 / max(pc.width, pc.height))).move_to(t)
                        for pc, t in zip(pieces, targets)], FadeIn(rows[2]), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.1), FadeIn(q))
            for mk, r in zip("de", rows[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def hume(self):
        hc = history_card(1739, r"David Hume", r"\textit{Treatise}, \ 1.4.6, \ `Of Personal Identity'", width=6.6,
                          color=HIST).to_corner(UL, buff=0.3)
        q = quote_card(r"I never can catch \textit{myself} at any time without a perception, \ and never can observe "
                       r"any thing but the perception.", r"David Hume", r"\textit{Treatise} 1.4.6", width=9.0,
                       font_size=22).move_to([0.8, 0.8, 0])
        rows = stack([(r"`a bundle or collection of different perceptions'", NOM),
                      (r"the self is like a commonwealth: \ members change, \ the republic remains", WHOLE),
                      (r"in the Appendix, \ Hume confessed himself unsatisfied: \ what binds the bundle?", BAD)],
                     font_size=20, aligned_edge=LEFT, width=10.4).move_to([0.4, -1.8, 0])
        with self.voiceover(
            "Two thousand years later, David Hume reached a similar view by introspection. "
            "<bookmark mark='a'/>When I enter most intimately into what I call myself, he wrote, I always stumble on "
            "some particular perception. I never catch myself without a perception, and never observe anything but "
            "the perception. <bookmark mark='b'/>The self is a bundle or collection of different perceptions. "
            "<bookmark mark='c'/>It is like a commonwealth, whose members change while the republic remains. "
            "<bookmark mark='d'/>But in the Appendix Hume confessed that he could not explain what binds the bundle "
            "together, and was unsatisfied with his own account."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def views(self):
        head = label(r"Buddhist reductionism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"five aggregates", r"form, \ feeling, \ perception, \ volition, \ consciousness: \ the skandhas", PARTC),
            (r"Vasubandhu", r"\textit{Abhidharmakośa}, \ ch. 9: \ the self is a conceptual fiction over a causal "
                            r"series", NOM),
            (r"Parfit", r"`my view is close to the Buddha's': \ reductionism about persons", GOAL),
            (r"Siderits \ (2007)", r"\textit{Buddhism as Philosophy}: \ the two truths as a mereological nihilism "
                                   r"\ (Part 20)", UNIV),
            (r"the ethical turn", r"if no self is deeply real, \ the line between my future and others' matters "
                                  r"less \ (Part 36)", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "The Buddhist tradition developed this into a systematic reductionism. <bookmark mark='a'/>A person is "
            "five aggregates: form, feeling, perception, volition and consciousness, in causal sequence. "
            "<bookmark mark='b'/>Vasubandhu, around the fourth century, argued in the ninth chapter of the "
            "Abhidharmakośa that the self is a conceptual fiction laid over a causal series. "
            "<bookmark mark='c'/>Parfit noticed that his view was close to the Buddha's. <bookmark mark='d'/>Mark "
            "Siderits reads the doctrine of two truths as a kind of mereological nihilism, of the sort Part 20 "
            "considered. <bookmark mark='e'/>And both traditions draw ethical conclusions: if the self is not deeply "
            "real, the line between my future and other people's matters less, a theme of Part 36."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def middle(self):
        head = label(r"The self debated in India", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Nyāya", r"there must be a self: \ memory and recognition need one subject who saw then and sees now",
             NOM),
            (r"the Buddhist reply", r"a causal series of momentary states suffices, \ as a flame passes along a wick",
             PARTC),
            (r"Nāgārjuna \ (c. 150)", r"the middle way: \ the self neither exists ultimately nor is nothing; \ it is "
                                      r"empty, \ dependently arisen", ABS),
            (r"Śāntideva \ (c. 700)", r"if no self owns pain, \ my future pain and yours are on a par: \ so remove "
                                      r"all pain alike", GOAL),
            (r"Parfit again", r"the same inference, \ from reductionism to impartiality", UNIV),
        ]
        g = rows_table(rows, top=2.1, gap=0.42, width=8.8, x_text=-2.4, label_size=21)
        candles, flames = VGroup(), VGroup()
        for i in range(6):
            x = -4.6 + 1.45 * i
            candles.add(VGroup(Rectangle(width=0.28, height=0.6, stroke_color=GREY_B, stroke_width=1.5,
                                         fill_color=WHITE, fill_opacity=0.75).move_to([x, -3.15, 0]),
                               Line([x, -2.85, 0], [x, -2.74, 0], color=GREY_C, stroke_width=2)))
            flames.add(Ellipse(width=0.2, height=0.38, color=GOAL, fill_opacity=0.9).move_to([x, -2.55, 0]))
        cap = label(r"each flame lit by the last: \ nothing travels", font_size=18, color=PARTC).move_to(
            [4.9, -2.9, 0])
        with self.voiceover(
            "In India the question was argued for centuries. <bookmark mark='a'/>Nyāya philosophers held that there "
            "must be a self: memory and recognition need a single subject who saw then and sees now. "
            "<bookmark mark='b'/>Buddhists replied that a causal series of momentary states suffices, as a flame "
            "passes along a wick without any flame-substance travelling with it. <bookmark mark='c'/>Nāgārjuna's "
            "middle way: the self neither exists ultimately nor is simply nothing; it is empty, dependently arisen. "
            "<bookmark mark='d'/>Śāntideva drew the ethical conclusion around the year 700: if no self owns pain, my "
            "future pain and yours are on a par, so we should remove all pain alike. <bookmark mark='e'/>Parfit drew "
            "the same inference, from reductionism towards impartiality."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]), FadeIn(candles), FadeIn(flames[0], scale=0.5))
            for i in range(1, 6):
                self.play(FadeIn(flames[i], scale=0.5), flames[i - 1].animate.set_opacity(0.15), run_time=0.55)
            self.play(FadeIn(cap))
            for mk, r in zip("cde", g[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def modern(self):
        head = label(r"The self as a model", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Dennett \ (1992)", r"the self as `a centre of narrative gravity': \ real as an abstraction, \ like a "
                                  r"centre of mass", UNIV),
            (r"Metzinger \ (2003)", r"\textit{Being No One}: \ no one has ever been or had a self; \ there is a "
                                    r"self-model the brain cannot see as a model", NOM),
            (r"neuroscience", r"depersonalization; \ split-brain patients; \ the rubber-hand illusion: \ the sense of self "
                              r"can come apart", BAD),
            (r"Strawson \ (1997)", r"the self as a brief subject of experience, \ lasting moments", WHOLE),
            (r"Zahavi \ (2005)", r"a minimal self: \ the first-person givenness of experience \ (Part 29)", ABS),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Modern philosophy of mind has given the bundle new forms. <bookmark mark='a'/>Daniel Dennett called the "
            "self a centre of narrative gravity: real as an abstraction, like a centre of mass, but nothing inside the "
            "head. <bookmark mark='b'/>Thomas Metzinger's Being No One argues that no one has ever had a self; there is "
            "only a self-model, which the brain cannot recognise as a model. <bookmark mark='c'/>Neuroscience shows "
            "the sense of self coming apart: in depersonalization, in split-brain patients, in the rubber-hand "
            "illusion. <bookmark mark='d'/>Galen Strawson defends selves as brief subjects of experience, lasting "
            "moments. <bookmark mark='e'/>And Dan Zahavi, from phenomenology, a minimal self: the first-person way "
            "experience is given, which Part 29 explores."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
