from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Kant(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Kant's question", r"How are synthetic judgments a priori possible?",
                            lit=(1781, 1783), part=PART)
        with self.voiceover("Chapter nine. Kant's question."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.slumber()
        self.grid()
        self.copernicus()

    def slumber(self):
        q = quote_card(r"I freely admit that the remembrance of David Hume was the very thing that many years ago first "
                       r"interrupted my dogmatic slumber.", r"Immanuel Kant", r"\textit{Prolegomena}, \ 1783",
                       width=9.6, font_size=28).move_to([0, 1.2, 0])
        rows = VGroup(label(r"Hume: \ necessity is not in experience, \ so it is only habit", font_size=24,
                            color=SENSE),
                      label(r"but mathematics and physics are necessary, \ and about the world", font_size=24,
                            color=REASON),
                      label(r"so where does their necessity come from?", font_size=26, color=GOAL)).arrange(
            DOWN, buff=0.3).move_to([0, -1.5, 0])
        with self.voiceover(
            "In Königsberg, on the Baltic, a professor who never travelled more than a few miles from home read "
            "Hume, and it changed his life's work. <bookmark mark='a'/>I freely admit, Immanuel Kant wrote, that the "
            "remembrance of David Hume was the very thing that many years ago first interrupted my dogmatic slumber. "
            "<bookmark mark='b'/>Hume had shown that necessity cannot be found in experience. <bookmark mark='c'/>Yet "
            "mathematics and Newton's physics seemed both necessary and about the world. <bookmark mark='d'/>So where "
            "does their necessity come from, if not from experience, and not from mere definitions?"
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def grid(self):
        d = load("grid")["rows"]
        head = label(r"Two distinctions, \ four boxes", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        W, H = 3.9, 2.1
        o = np.array([0.3, -0.95, 0])
        boxes = {}
        for i, a in enumerate(("a priori", "a posteriori")):
            for j, s_ in enumerate(("analytic", "synthetic")):
                r = Rectangle(width=W, height=H, stroke_color=GREY_C, stroke_width=2,
                              fill_color=[REASON, KANT, "#333", SENSE][2 * j + i], fill_opacity=0.08)
                r.move_to(o + np.array([(i - 0.5) * W, (0.5 - j) * H, 0]))
                boxes[(s_, a)] = r
        colh = VGroup(label(r"a priori", font_size=24, color=REASON).next_to(boxes[("analytic", "a priori")], UP,
                                                                             buff=0.15),
                      label(r"a posteriori", font_size=24, color=SENSE).next_to(boxes[("analytic", "a posteriori")],
                                                                                 UP, buff=0.15))
        rowh = VGroup(label(r"analytic", font_size=24, color=GREY_A).next_to(boxes[("analytic", "a priori")], LEFT,
                                                                             buff=0.15),
                      label(r"synthetic", font_size=24, color=GREY_A).next_to(boxes[("synthetic", "a priori")], LEFT,
                                                                              buff=0.15))
        gl = VGroup(label(r"analytic: \ the predicate is contained in the subject", font_size=20, color=GREY_A),
                    label(r"a priori: \ known independently of experience", font_size=20, color=GREY_A),
                    label(r"the empty box: \ analytic a posteriori", font_size=20, color=GREY_B)).arrange(
            DOWN, buff=0.12).move_to([0, 2.42, 0])
        items = VGroup()
        slots = {}
        for text, s_, a, who in d:
            if "Kripke" in who or "1915" in who:
                continue
            key = (s_, a)
            slots.setdefault(key, 0)
            m = label(text.replace("°", r"$^\circ$"), font_size=19, color=WHITE)
            m.move_to(boxes[key].get_top() + DOWN * (0.45 + 0.42 * slots[key]))
            slots[key] += 1
            items.add(m)
        tri = label(r"a triangle's angles sum to 180$^\circ$", font_size=19, color=WHITE).move_to(
            boxes[("synthetic", "a priori")].get_top() + DOWN * (0.45 + 0.42 * slots[("synthetic", "a priori")]))
        kantq = label(r"Kant: \ mathematics, \ and the principles of physics, \ live in the bottom-left box", font_size=22,
                      color=KANT).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Kant's question rests on two distinctions. <bookmark mark='a'/>A judgment is analytic if its predicate is "
            "already contained in its subject, like all bachelors are unmarried, or Kant's example, all bodies are "
            "extended. Otherwise it is synthetic. <bookmark mark='b'/>And it is a priori if it is known independently "
            "of experience, a posteriori if only through it. <bookmark mark='c'/>Two distinctions make four boxes. "
            "Analytic truths are a priori: we need only understand the words. Some bodies are heavy is synthetic a "
            "posteriori: we must lift them. Nothing is analytic and a posteriori. <bookmark mark='d'/>The interesting "
            "box is the last. Kant put there seven plus five equals twelve; every event has a cause; and the angles of "
            "a triangle sum to two right angles. They are about the world, yet known with necessity. "
            "<bookmark mark='e'/>How are such synthetic judgments a priori possible? That is the question of the "
            "Critique."
        ) as vo:
            self.play(FadeIn(head), *[Create(b) for b in boxes.values()], FadeIn(colh), FadeIn(rowh))
            vo.wait_until("a")
            self.play(FadeIn(gl[0]))
            vo.wait_until("b")
            self.play(FadeIn(gl[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m) for m in items[:3]], lag_ratio=0.4), FadeIn(gl[2]), run_time=3)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(m) for m in items[3:]], lag_ratio=0.5), FadeIn(tri), run_time=3)
            vo.wait_until("e")
            self.play(Indicate(boxes[("synthetic", "a priori")], color=KANT), FadeIn(kantq))
        self.clear_scene()

    def copernicus(self):
        head = label(r"Kant's Copernican revolution", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        left = VGroup(label(r"before", font_size=26, color=GREY_A),
                      label(r"our knowledge must conform to objects", font_size=23),
                      label(r"then necessity is impossible:", font_size=21, color=GREY_A),
                      label(r"we cannot know in advance what objects will be like", font_size=21,
                            color=GREY_A)).arrange(DOWN, buff=0.15)
        right = VGroup(label(r"Kant", font_size=26, color=KANT),
                       label(r"objects must conform to our knowledge", font_size=23),
                       label(r"we know a priori", font_size=21, color=GREY_A),
                       label(r"what we ourselves put into experience", font_size=21, color=GREY_A)).arrange(
            DOWN, buff=0.15)
        for c in (left, right):
            for m in c:
                if m.width > 5.8:
                    m.width = 5.8
            c.arrange(DOWN, buff=0.15)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.0).move_to([0, 1.55, 0])

        def orbit(centre_col, mover_col, x):
            c = Dot([x, -0.75, 0], radius=0.16, color=centre_col)
            ring = Circle(radius=0.95, color=GREY_D, stroke_width=1.5).move_to(c)
            m = Dot(ring.point_at_angle(0), radius=0.11, color=mover_col)
            return VGroup(ring, c, m)
        geo = orbit(REASON, GOAL, left.get_x())
        helio = orbit(GOAL, REASON, right.get_x())
        keys = VGroup(label(r"the stars turn round the observer", font_size=19, color=GREY_B).next_to(geo, DOWN,
                                                                                                buff=0.15),
                      label(r"the observer turns", font_size=19, color=GREY_B).next_to(helio, DOWN, buff=0.15))
        tail = VGroup(label(r"like Copernicus, \ who moved the observer instead of the stars \ (B xvi)", font_size=22,
                            color=GREY_B),
                      label(r"the mind supplies the form: \ space, \ time, \ and the categories", font_size=26,
                            color=GOAL)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Kant's answer turns the problem upside down. <bookmark mark='a'/>Up to now, he wrote, it has been assumed "
            "that all our knowledge must conform to objects. On that assumption, knowledge in advance of experience is "
            "impossible: how could we know beforehand what objects will be like? <bookmark mark='b'/>So let us try "
            "assuming that objects must conform to our knowledge. Then we can know a priori whatever we ourselves "
            "contribute to experience. <bookmark mark='c'/>He compared the move to Copernicus, who explained the "
            "motions of the heavens by letting the observer move instead of the stars. <bookmark mark='d'/>What does "
            "the mind contribute? The forms of all experience: space, time, and the categories."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(geo), FadeIn(helio), FadeIn(keys), FadeIn(tail[0]))
            self.play(Rotate(geo[2], TAU, about_point=geo[1].get_center()),
                      Rotate(helio[2], TAU, about_point=helio[1].get_center()), run_time=3, rate_func=smooth)
            vo.wait_until("d")
            self.play(FadeIn(tail[1]))
        self.clear_scene()
