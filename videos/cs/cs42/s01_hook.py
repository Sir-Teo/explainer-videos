from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.tts import REPO_ROOT
from videos.cs.cs42.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

# a typical first visit, in milliseconds (illustrative): (layer, start, end, colour, part it comes from)
STEPS = [
    (r"DNS lookup", 0, 40, LAM, 36),
    (r"TCP handshake", 40, 80, DATA, 37),
    (r"TLS handshake", 80, 120, NO, 30),
    (r"request, \ first byte", 120, 200, DATA, 37),
    (r"parse HTML", 200, 240, HEAD, 42),
    (r"fetch CSS and scripts", 215, 330, DATA, 37),
    (r"style and layout", 330, 365, YES, 42),
    (r"paint and composite", 365, 385, KERN, 42),
]


class Hook(VoiceoverScene):
    def construct(self):
        self.url()
        self.machines()
        self.toy()
        self.plan()

    def url(self):
        head = label(r"What happens when you type a URL?", font_size=36).to_edge(UP, buff=0.3)
        bar = RoundedRectangle(width=7.2, height=0.6, corner_radius=0.25, stroke_color=GREY_B, stroke_width=1.5,
                               fill_color=BG, fill_opacity=1).next_to(head, DOWN, buff=0.35)
        url = label(r"\texttt{https://example.org/}", font_size=24, color=WHITE).move_to(bar).align_to(bar, LEFT).shift(
            RIGHT * 0.3)
        x0, scale, y0 = -3.4, 9.6 / 400, 1.1
        axis = Line([x0, -2.55, 0], [x0 + 400 * scale, -2.55, 0], color=GREY_C, stroke_width=1.5)
        ticks = VGroup()
        for ms in range(0, 401, 100):
            x = x0 + ms * scale
            ticks.add(Line([x, -2.6, 0], [x, -2.5, 0], color=GREY_C, stroke_width=1.5),
                      label(f"{ms} ms", font_size=16, color=GREY_B).move_to([x, -2.82, 0]))
        rows = VGroup()
        for k, (name, a, b, col, part) in enumerate(STEPS):
            y = y0 - k * 0.45
            r = Rectangle(width=(b - a) * scale, height=0.3, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to([x0 + (a + b) / 2 * scale, y, 0])
            n = label(name, font_size=18, color=col).move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT)
            p = label(rf"Part {part}", font_size=15, color=GREY_B).next_to(r, RIGHT, buff=0.12)
            rows.add(VGroup(n, r, p))
        illus = note(r"illustrative timings for a first visit to a nearby server", font_size=16).to_edge(DOWN,
                                                                                                     buff=0.15)
        with self.voiceover(
            "Type an address into a browser and press enter. In a few hundred milliseconds, a page appears. "
            "<bookmark mark='a'/> Between the key press and the pixels, almost everything this series has built "
            "takes a turn. The name is resolved by the domain name system of Part 36. A TCP connection is opened, "
            "and a TLS handshake agrees keys with the public-key cryptography of Part 30. <bookmark mark='b'/> The "
            "request goes out, and the first bytes of HTML come back over the transport protocols of Part 37. "
            "<bookmark mark='c'/> Then the browser's own work begins. It parses the HTML while it is still "
            "arriving, discovers stylesheets and scripts and fetches them in parallel, computes the style of every "
            "element, lays out the page, and paints it. <bookmark mark='d'/> That last stretch, from bytes to "
            "pixels, is this part's subject: what a browser does with a page once it has one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), Write(url))
            vo.wait_until("a")
            self.play(Create(axis), FadeIn(ticks), FadeIn(illus))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[:3]], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[4:]], lag_ratio=0.5), run_time=3)
            vo.wait_until("d")
            self.play(*[Indicate(r[1], color=WHITE, scale_factor=1.05) for r in rows[4:]])
        self.wait(0.4)
        self.clear_scene()

    def machines(self):
        head = label(r"Five machines in one program", font_size=36).to_edge(UP, buff=0.3)
        specs = [
            (r"a parser that never rejects", r"every byte sequence becomes a tree", HEAD),
            (r"a constraint solver", r"boxes, \ lines and space, \ every frame", YES),
            (r"a GPU compositor", r"layers moved and blended at 60 to 120 Hz", KERN),
            (r"a JIT compiler", r"untrusted JavaScript made fast", DATA),
            (r"an operating system", r"processes, \ sandboxes, \ permissions, \ storage", NO),
        ]
        tiles = VGroup()
        for t, sub, col in specs:
            frame = RoundedRectangle(width=4.0, height=1.45, corner_radius=0.15, stroke_color=col, stroke_width=2,
                                     fill_color=BG, fill_opacity=1)
            a = label(t, font_size=22, color=col)
            b = wrapped_label(sub, 3.6, font_size=17, color=GREY_A)
            VGroup(a, b).arrange(DOWN, buff=0.15).move_to(frame)
            tiles.add(VGroup(frame, a, b))
        tiles[:3].arrange(RIGHT, buff=0.3)
        tiles[3:].arrange(RIGHT, buff=0.3)
        VGroup(tiles[:3], tiles[3:]).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.45)
        loop = Circle(radius=0.55, color=HEAD, stroke_width=4, fill_opacity=0)
        clock = VGroup(loop, label(r"16.7 ms", font_size=20, color=HEAD).move_to(loop))
        cap = wrapped_label(r"one event loop holds it together: \ at 60 frames a second, \ everything for a frame "
                            r"must fit in 16.7 milliseconds", 8.6, font_size=21, color=WHITE)
        VGroup(clock, cap).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A browser is several machines in one program. <bookmark mark='a'/> It is a parser that never rejects "
            "its input: every sequence of bytes, however broken, becomes a document tree. <bookmark mark='b'/> It is "
            "a constraint solver, fitting boxes, lines of text and free space together. It is a graphics "
            "compositor, moving and blending layers on the GPU sixty or a hundred and twenty times a second. "
            "<bookmark mark='c'/> It is a just-in-time compiler that makes untrusted code fast, and an operating "
            "system that keeps that code in a sandbox. <bookmark mark='d'/> And one event loop holds it all "
            "together, with a deadline: at sixty frames a second, everything for the next frame has to fit in "
            "sixteen point seven milliseconds."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tiles[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(tiles[1], shift=UP * 0.15), FadeIn(tiles[2], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(tiles[3], shift=UP * 0.15), FadeIn(tiles[4], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(Create(loop), FadeIn(clock[1]), FadeIn(cap))
            self.play(Rotate(loop, angle=-TAU, about_point=loop.get_center()), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def toy(self):
        b = load("browser")
        head = label(r"A browser of our own", font_size=36).to_edge(UP, buff=0.3)
        img = ImageMobject(str(REPO_ROOT / b["png"]))
        img.height = 6.6
        img.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        stages = VGroup(*[label(t, font_size=21, color=c) for t, c in (
            (r"Markdown $\to$ HTML", GREY_A),
            (r"HTML $\to$ tokens $\to$ a DOM of " + f"{b['nodes']}" + r" nodes", HEAD),
            (r"the cascade: \ a style for every element", YES),
            (rf"layout: \ {b['boxes']} blocks, \ {b['words']} words in lines", DATA),
            (r"paint: \ real fonts, \ real pixels", KERN))]).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        stages.next_to(img, RIGHT, buff=0.6).shift(UP * 0.3)
        cap = wrapped_label(r"this series' own README, \ rendered by about 700 lines of our Python", 5.6,
                            font_size=19, color=GREY_B).next_to(stages, DOWN, buff=0.5).align_to(stages, LEFT)
        with self.voiceover(
            "We will build each stage, small enough to read, and at the end run them together as a toy browser. "
            "<bookmark mark='a'/> Here is its output: the top of this series' own README. <bookmark mark='b'/> The "
            f"Markdown becomes HTML; a tokenizer and a tree builder turn the HTML into a tree of {b['nodes']} nodes; "
            "the cascade gives every element a style; layout breaks the text into lines and stacks the blocks; and "
            "a painter draws the words with real fonts into real pixels. <bookmark mark='c'/> It is missing almost "
            "everything a real browser has. But each piece does what the real piece does, and it shows the shape "
            "of the problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(img, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.1) for s in stages], lag_ratio=0.5), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ The Browser and the Web", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"why HTML is parsed by a state machine, \ not a grammar",
            r"the cascade, \ specificity and selector matching",
            r"layout: \ flexbox and Knuth--Plass line breaking",
            r"the event loop and the 16.7 ms frame",
            r"inside a JavaScript engine; \ virtual DOMs and signals",
            r"caching, \ performance, \ security and accessibility",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 42 of Computer Science, Built, the third part of Act Eight. <bookmark mark='a'/> We will "
            "see why HTML is parsed by a state machine rather than a grammar; how the cascade decides which style "
            "wins; how a page is laid out, down to the dynamic program that breaks a paragraph into lines; how the "
            "event loop schedules everything into frames; what a JavaScript engine does to make dynamic code fast; "
            "and how frameworks, caches, the security model and accessibility rest on all of it."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (LAM, NO, YES)
