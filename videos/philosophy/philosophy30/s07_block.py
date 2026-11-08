from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


class Block(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Blockhead and the China brain", r"Does it matter how the behaviour is produced?",
                            lit=(1978, 1981), part=PART)
        with self.voiceover("Chapter six. Blockhead and the China brain."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.blockhead()
        self.size()
        self.leibniz()
        self.china()

    def blockhead(self):
        hc = history_card(1981, r"Ned Block", r"`Psychologism and Behaviorism'", width=5.6, color=HIST).to_corner(
            UL, buff=0.3)
        rows = stack([(r"store, \ for every possible conversation so far, \ one sensible next reply", SYM),
                      (r"programmed by people who thought of every sensible reply in advance", GREY_A),
                      (r"it would pass any Turing test of that length, \ by looking things up", OK),
                      (r"yet it is no more intelligent than a jukebox: \ intelligence depends on \textit{how} behaviour "
                       r"is produced", BAD)], font_size=22, aligned_edge=LEFT, width=12.0, buff=0.35).move_to(
            [0, -0.3, 0])
        with self.voiceover(
            "In 1981 Ned Block imagined a machine built to pass the Turing test by brute force. "
            "<bookmark mark='a'/>For every possible conversation up to some length, it stores one sensible next "
            "reply. <bookmark mark='b'/>Its programmers, working in advance, thought of every sensible reply to "
            "everything that could be typed. <bookmark mark='c'/>It would pass any test of that length, by looking up "
            "the conversation so far and printing what it finds. <bookmark mark='d'/>Yet, Block argued, it has the "
            "intelligence of a jukebox. Intelligence depends on how behaviour is produced, not only on what the "
            "behaviour is. He called this view psychologism."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def size(self):
        d = load("blockhead")
        head = label(r"Blockhead's table, \ measured", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows_d = d["rows"]
        assert d["alphabet"] == 27 and d["chars_per_minute"] == 300 and d["log10_atoms"] == 80
        assert [r["log10_entries"] for r in rows_d] == [429.4, 4294.1, 25764.5]
        eq = MathTex(r"\text{entries} \;\geq\; 27^{\,\text{characters}}", font_size=32, color=SYM).move_to([0, 2.1, 0])
        scale = 10.0 / 25764.5
        bars = VGroup()
        items = [(r"atoms in the observable universe", 80, PHYS)] + [
            (rf"{r['minutes']} min \ ({r['chars']:,} characters)".replace(",", r"\,"), r["log10_entries"], SYM)
            for r in rows_d]
        for i, (name, v, col) in enumerate(items):
            y = 1.0 - 0.85 * i
            w = max(0.04, v * scale)
            bar = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [-5.0 + w / 2, y, 0])
            t = label(name, font_size=17, color=col).next_to([-5.0, y, 0], UP, buff=0.26).align_to([-5.0, 0, 0], LEFT)
            n = MathTex(rf"10^{{{v:g}}}", font_size=22, color=col).next_to(bar, RIGHT, buff=0.15)
            bars.add(VGroup(bar, t, n))
        xl = label(r"bar length: \ the number of digits", font_size=16, color=GREY_A).move_to([0, -2.4, 0])
        foot = label(r"an hour's table outnumbers the atoms by more than 25\,000 orders of magnitude", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How big would Blockhead be? <bookmark mark='a'/>It needs an entry for every string the interrogator "
            "might type: at least twenty-seven to the power of the number of characters, counting letters and the "
            "space. <bookmark mark='b'/>The observable universe holds about ten to the eighty atoms. "
            "<bookmark mark='c'/>A one-minute test, at three hundred characters a minute, needs about ten to the four "
            "hundred and twenty-nine entries. Ten minutes, ten to the four thousand two hundred and ninety-four. An "
            "hour, ten to the twenty-five thousand seven hundred and sixty-four. <bookmark mark='d'/>Here each bar's "
            "length is the number of digits. The universe is a sliver at the top. Blockhead is logically possible and "
            "physically absurd, which is Block's point: the test can be passed in principle by something that "
            "plainly does not think, so passing it cannot be what thinking is."
        ) as vo:
            self.play(FadeIn(head), Write(eq))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(bars[0]))
            vo.wait_until("c")
            for b in bars[1:]:
                self.play(GrowFromEdge(b[0], LEFT), FadeIn(b[1]), FadeIn(b[2]), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(xl), FadeIn(foot))
        self.clear_scene()

    def leibniz(self):
        q = quote_card(r"Imagine there were a machine whose structure produced thought, \ feeling and perception; \ we "
                       r"can conceive of its being enlarged \dots\ so that one could go into it as into a mill. \ "
                       r"Suppose this done; \ then if we inspect the interior we shall find there nothing but parts "
                       r"which push one against another, \ and never anything by which to explain a perception.",
                       r"Leibniz", r"\textit{Monadology} \ (1714), \ \S 17", width=10.8, font_size=22).move_to(
            [0, 0.4, 0])
        foot = label(r"Leibniz's mill: \ the ancestor of every argument in this chapter", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The worry behind Blockhead is old. <bookmark mark='a'/>In 1714 Leibniz wrote: imagine a machine whose "
            "structure produced thought, feeling and perception, enlarged so that one could walk into it as into a "
            "mill. Inside, we would find nothing but parts pushing one against another, and never anything by which "
            "to explain a perception. <bookmark mark='b'/>Leibniz's mill is the ancestor of every argument in this "
            "chapter."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def china(self):
        hc = history_card(1978, r"Ned Block", r"`Troubles with Functionalism'", width=5.4, color=HIST).to_corner(UL,
                                                                                                         buff=0.3)
        rng = np.random.default_rng(1978)
        people = VGroup(*[Dot([x, y, 0], radius=0.05, color=FUNC) for x, y in
                          zip(rng.uniform(-5.6, -0.6, 160), rng.uniform(-2.2, 1.4, 160))])
        links = VGroup(*[Line(people[i].get_center(), people[j].get_center(), color=FUNC, stroke_width=0.6,
                              stroke_opacity=0.4) for i, j in zip(rng.integers(0, 160, 120), rng.integers(0, 160, 120))])
        body = VGroup(Circle(radius=0.3, color=PHYS), Line([0, -0.3, 0], [0, -1.2, 0], color=PHYS),
                      Line([-0.5, -0.6, 0], [0.5, -0.6, 0], color=PHYS)).move_to([1.4, -0.2, 0])
        radio = DashedLine([-0.6, -0.2, 0], [1.0, -0.2, 0], color=GREY_B)
        rows = stack([(r"a billion people, \ each doing what one neuron does, \ by radio", FUNC),
                      (r"connected to a body; \ for an hour it realizes your functional organization", PHYS),
                      (r"would the nation feel pain? \ absent qualia", FEEL),
                      (r"or see red where you see green? \ inverted qualia", BAD),
                      (r"if not, \ functional role does not fix experience: \ Part 31", GOAL)], font_size=19,
                     aligned_edge=LEFT, width=4.6, buff=0.26).move_to([4.5, -0.3, 0])
        with self.voiceover(
            "Block's earlier example, from 1978, is the China brain. <bookmark mark='a'/>Suppose the whole population "
            "of China, a billion people, were each given a two-way radio and the job of doing what one neuron in "
            "your brain does: when these messages come in, send that one out. <bookmark mark='b'/>Connect the "
            "network to an artificial body. For an hour, it realizes exactly your functional organization. "
            "<bookmark mark='c'/>Would the nation, as a whole, feel pain when the body is pricked? Most people find it "
            "absurd that it would: the qualia, the felt qualities, seem absent. <bookmark mark='d'/>A related worry is "
            "inverted qualia: a system functionally just like you that sees red where you see green. "
            "<bookmark mark='e'/>If either is possible, functional role does not fix experience. That is the subject "
            "of Part 31."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in people], lag_ratio=0.005), Create(links), FadeIn(rows[0]),
                      run_time=2)
            vo.wait_until("b")
            self.play(Create(radio), FadeIn(body), FadeIn(rows[1]))
            for mk, r in zip("cde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
