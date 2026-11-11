from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.tts import REPO_ROOT
from videos.cs.cs42.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, grid_table, load, mono


def _short(s: str, n: int = 46) -> str:
    return s if len(s) <= n else s[:n - 3] + "..."


def _tt(s: str) -> str:
    """Escape a source line for \\texttt."""
    out = []
    for ch in s:
        if ch in "#$%&_{}":
            out.append("\\" + ch)
        elif ch == "\\":
            out.append(r"\textbackslash{}")
        elif ch == "^":
            out.append(r"\^{}")
        elif ch == "~":
            out.append(r"\~{}")
        elif ord(ch) > 0x2e7f:
            out.append("?")
        else:
            out.append(ch)
    return "".join(out)


class Browser(VoiceoverScene):
    def construct(self):
        self.card()
        self.stages()
        self.boxes()
        self.timing()
        self.missing()

    def card(self):
        card = chapter_card(13, r"Our toy browser", r"What does it take to turn text into a page?",
                            lit=(1990, 2004), extra=((1990, r"WorldWideWeb, \ the first browser"),
                                                     (2004, r"WHATWG founded")), part=PART)
        with self.voiceover("Chapter thirteen. Our toy browser."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def stages(self):
        p = load("pipeline")
        head = label(r"Five stages, \ one page", font_size=36).to_edge(UP, buff=0.3)

        def panel(title, lines, color, width=6.3):
            t = label(title, font_size=20, color=color)
            body = VGroup(*[mono(_short(ln), size=14, color=GREY_A) for ln in lines]).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.09)
            box = RoundedRectangle(width=width, height=body.height + 0.35, corner_radius=0.1, stroke_color=color,
                                   stroke_width=1.5, fill_color=BG, fill_opacity=1)
            body.move_to(box)
            return VGroup(t, VGroup(box, body)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        md_lines = [ln for ln in p["markdown"] if ln.strip()][:4]
        html_lines = p["html"][:4]
        out_lines = p["outline"][:8]
        a = panel(r"Markdown", md_lines, GREY_B)
        b = panel(r"HTML", html_lines, HEAD)
        c = panel(rf"tokens $\to$ the DOM \ ({p['tokens']} tokens)", out_lines, YES)
        rows = [[rf"\texttt{{{s['tag']}}}", s["style"].get("font-size", ""), s["style"].get("color", ""),
                 s["style"].get("font-weight", "")] for s in p["styles"]]
        tab = grid_table([r"element", r"size", r"colour", r"weight"], rows, widths=[1.3, 1.3, 1.7, 1.2], row_h=0.36,
                         font_size=16, mono_cols=(1, 2, 3))
        d = VGroup(label(r"the cascade", font_size=20, color=DATA), tab).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        left = VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right = VGroup(c, d).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        grid = VGroup(left, right).arrange(RIGHT, buff=0.35, aligned_edge=UP).next_to(head, DOWN, buff=0.3)
        if grid.width > 13.6:
            grid.scale_to_fit_width(13.6)
        with self.voiceover(
            "Here are the stages run on the README, one at a time. <bookmark mark='a'/> The source is Markdown, a "
            "few dozen lines of it. A converter of about fifty lines turns headings, lists, emphasis and code into "
            "HTML. <bookmark mark='b'/> The tokenizer of chapter two reads that HTML a character at a time, "
            f"producing {p['tokens']} tokens, and the tree builder turns them into a document tree: headings, "
            "paragraphs, lists, and the text inside them. <bookmark mark='c'/> Then the cascade. A user-agent "
            "stylesheet of seven rules gives headings their size and colour, paragraphs and list items their "
            "margins, and code its own colour, and inheritance carries the font size from a list item into the "
            "bold text inside it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            self.play(FadeIn(c))
            vo.wait_until("c")
            self.play(FadeIn(d))
        self.wait(0.4)
        self.clear_scene()

    def boxes(self):
        p = load("pipeline")
        b = load("browser")
        head = label(r"Layout, \ then paint", font_size=36).to_edge(UP, buff=0.3)
        outlined = ImageMobject(str(REPO_ROOT / p["png"]))
        outlined.height = 6.4
        final = ImageMobject(str(REPO_ROOT / b["png"]))
        final.height = 6.4
        pair = Group(outlined, final).arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.25)
        if pair.width > 9.0:
            pair.scale_to_fit_width(9.0)
        pair.to_edge(LEFT, buff=0.4)
        caps = VGroup(label(r"block boxes", font_size=18, color=DATA).next_to(outlined, DOWN, buff=0.08),
                      label(r"painted", font_size=18, color=KERN).next_to(final, DOWN, buff=0.08))
        notes = VGroup(
            wrapped_label(rf"{b['boxes']} block boxes stacked down the page, \ each as tall as its lines", 3.9,
                          font_size=19, color=DATA),
            wrapped_label(rf"{b['words']} words placed one at a time, \ breaking a line when the next word would "
                          r"cross the right edge", 3.9, font_size=19, color=YES),
            wrapped_label(r"a word with Chinese characters falls back to a CJK font, \ as a browser's font "
                          r"fallback does", 3.9, font_size=19, color=HEAD),
            wrapped_label(r"no space in the source, \ no space on screen: \ ``\textbf{foundations}:'' stays "
                          r"together", 3.9, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(pair, RIGHT, buff=0.4)
        with self.voiceover(
            "Layout walks down the tree. <bookmark mark='a'/> Every heading, paragraph and list item becomes a block "
            f"box, {b['boxes']} of them, stacked down the page, each as tall as the lines inside it. "
            "<bookmark mark='b'/> Inside a block, inline layout places the words one at a time, measuring each in "
            "its font, and starts a new line when the next word would cross the right edge. That is the greedy "
            "line breaker of chapter four. <bookmark mark='c'/> Two details a real browser also has to get right. "
            "A word in Chinese falls back to a font that has those characters. <bookmark mark='d'/> And spaces "
            "come from the source: where the HTML has no space between a bold word and its colon, neither does the "
            "screen. Then the painter draws every word, and the page on the right is the result."
        ) as vo:
            self.play(FadeIn(head), FadeIn(outlined), FadeIn(caps[0]))
            for mk, n in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n))
            self.play(FadeIn(final), FadeIn(caps[1]))
        self.wait(0.4)
        self.clear_scene()

    def timing(self):
        p = load("pipeline")
        ms = p["ms"]
        head = label(r"How long does a page take?", font_size=36).to_edge(UP, buff=0.3)
        names = [("markdown", r"Markdown"), ("tokenize", r"tokenize"), ("tree", r"tree"), ("cascade", r"cascade"),
                 ("layout", r"layout"), ("paint", r"paint and encode")]
        cols = [GREY_B, HEAD, HEAD, DATA, YES, KERN]
        x0, sc, y = -5.6, 11.0 / 160, 0.9
        bars = VGroup()
        t = 0.0
        for (k, nm), c in zip(names, cols):
            w = ms[k] * sc
            r = Rectangle(width=max(w, 0.03), height=0.55, stroke_width=0, fill_color=c, fill_opacity=0.9)
            r.move_to([x0 + t * sc + w / 2, y, 0])
            bars.add(r)
            t += ms[k]
        labels = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.9),
                                 label(rf"{nm}: \ {ms[k]:.1f} ms", font_size=17, color=c)).arrange(RIGHT, buff=0.12)
                          for (k, nm), c in zip(names, cols)])
        labels.arrange_in_grid(rows=2, cols=3, buff=(0.6, 0.25), flow_order="rd").next_to(bars, DOWN, buff=0.45)
        labels.set_x(0)
        budget = DashedLine([x0 + 16.7 * sc, y + 1.2, 0], [x0 + 16.7 * sc, y - 0.4, 0], color=NO)
        bl = label(r"one frame: \ 16.7 ms", font_size=17, color=NO).next_to(budget, UP, buff=0.08)
        total = sum(ms.values())
        tot = label(rf"total \ {total:.0f} ms on this machine, \ in Python", font_size=21, color=WHITE).next_to(
            labels, DOWN, buff=0.4)
        lines = VGroup(
            wrapped_label(r"a real engine is compiled code, \ restyles and relayouts only what changed \ "
                          r"(dirty bits), \ and rasterizes on the GPU in tiles, \ in parallel", 12.4, font_size=20,
                          color=YES),
            wrapped_label(r"so the first load can take a while, \ but each later frame must fit in the budget", 12.4,
                          font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How fast is it? We timed each stage on this machine, the median of five runs. <bookmark mark='a'/> "
            f"Converting the Markdown, tokenizing and building the tree take a few milliseconds together. The "
            f"cascade takes about {ms['cascade']:.0f}, and layout about {ms['layout']:.0f}. <bookmark mark='b'/> "
            f"Painting, including encoding the image file, takes about {ms['paint']:.0f}. <bookmark mark='c'/> One "
            "frame at sixty hertz is sixteen point seven milliseconds, and our browser needs about "
            f"{total:.0f} for one page. <bookmark mark='d'/> Real engines are compiled code, they restyle and lay "
            "out only what changed, and they rasterize in tiles on the GPU. So a first load may take a while, but "
            "every frame after it fits the budget."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars[:5]], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(lb) for lb in labels[:5]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[5], LEFT), FadeIn(labels[5]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(budget), FadeIn(bl), FadeIn(tot))
            vo.wait_until("d")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def missing(self):
        head = label(r"What a real browser adds", font_size=36).to_edge(UP, buff=0.3)
        rows = [
            [r"parsing", r"a dozen states, \ one repair rule", r"about 80 states, \ insertion modes, \ full recovery"],
            [r"CSS", r"tags, \ classes, \ ids, \ descendants", r"hundreds of properties, \ selectors, \ at-rules"],
            [r"layout", r"blocks and greedy lines", r"floats, \ tables, \ flex, \ grid, \ bidi text, \ hyphens"],
            [r"painting", r"one pass into a PNG", r"display lists, \ layers, \ GPU tiles"],
            [r"scripts", r"none", r"an engine with three or four compiler tiers"],
            [r"networking", r"none", r"HTTP/1.1--3, \ caches, \ TLS, \ service workers"],
            [r"security", r"none", r"origins, \ sandboxed processes, \ site isolation"],
        ]
        tab = grid_table([r"", r"ours", r"a real engine"], rows, widths=[2.2, 4.4, 6.4], row_h=0.5, font_size=18,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.35)
        foot = wrapped_label(r"Chromium is tens of millions of lines; \ the open book \textit{Web Browser "
                             r"Engineering} \ (Panchekha and Harrelson) \ builds a far fuller browser than ours, \ "
                             r"in a few thousand lines of Python", 12.4, font_size=20, color=HEAD).to_edge(DOWN,
                                                                                                    buff=0.4)
        with self.voiceover(
            "And what it leaves out. <bookmark mark='a'/> Our parser has a dozen states and one repair rule for "
            "misnested formatting; the standard's tokenizer has about eighty states, and the tree builder has "
            "insertion modes for tables, forms and scripts. Our CSS knows tags, classes, identifiers and "
            "descendants. Our layout knows blocks and greedy lines, not floats, tables, flexbox, grid, "
            "bidirectional text or hyphenation. And it runs no scripts, fetches nothing and needs no security, "
            "because it trusts its only input. <bookmark mark='b'/> A real engine is tens of millions of lines. "
            "If you want to go further, the open book Web Browser Engineering, by Pavel Panchekha and Chris "
            "Harrelson, builds a much fuller browser in a few thousand lines of Python."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, LAM, NO, YES, bar_chart, _tt)
