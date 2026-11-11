from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ The Browser and the Web", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(label(r"every input $\to$ a tree", font_size=40, color=HEAD), r"a forgiving parser", HEAD),
            tile(MathTex(r"(a,\ b,\ c)", font_size=60, color=DATA), r"specificity", DATA),
            tile(MathTex(r"\min \sum \text{badness}", font_size=48, color=YES), r"Knuth--Plass", YES),
            tile(label(r"task, \ microtasks, \ frame", font_size=36, color=KERN), r"the event loop", KERN),
            tile(label(r"shape + offset", font_size=40, color=LAM), r"inline caches", LAM),
            tile(MathTex(r"\frac{L_1+0.05}{L_2+0.05}", font_size=56, color=NO), r"contrast", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. An HTML parser that turns every input into a tree, because the web's "
            "standard says what to do with every mistake. A cascade that orders rules by origin, by specificity as "
            "a triple compared lexicographically, and by order, and matches selectors from the right. Layout as a "
            "distribution of space, and line breaking as a shortest path, better than greedy on almost every "
            "paragraph of a novel. An event loop that runs a task, drains its microtasks and renders a frame, and "
            "a long task that drops seven frames. Hidden classes and inline caches, keyed lists and signals. And "
            "caches, origins and a contrast ratio derived from the physics of light. One idea runs through it: a "
            "browser does as little work as possible, as late as possible, inside a sixteen-millisecond frame."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the APIs a web page calls, \ and their compatibility", [43]),
            (r"Core Web Vitals and A/B tests of page speed", [44]),
            (r"content delivery and caches at a planet's scale", [45, 48]),
            (r"rasterization, \ the GPU and compositing", [51]),
            (r"verified compilers and the trust in an engine", [54, 55]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 43 designs the APIs a web page calls, and keeps them compatible as they "
            "change. Part 44 measures whether a faster page changes what people do, with controlled experiments. "
            "Parts 45 and 48 put caches and content delivery at the scale of the planet. Part 51 opens the "
            "rasterizer and the GPU. And Parts 54 and 55 ask what it would take to trust a compiler, including the "
            "one inside a JavaScript engine."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"performance", r"measure in the field; \ ship less JavaScript; \ keep tasks under 50 ms"),
            (r"loading", r"defer scripts, \ preload what the first paint needs, \ size images to the screen"),
            (r"caching", r"content-hashed names cached forever; \ short lifetimes for the HTML"),
            (r"security", r"escape output, \ a strict CSP, \ SameSite cookies, \ CORS only where needed"),
            (r"access", r"real elements before ARIA, \ keyboard paths, \ contrast of at least 4.5 to 1"),
        ])
        with self.voiceover(
            "In practice. Measure performance on real users' devices, ship less JavaScript, and keep every task "
            "short enough that input never waits. Defer scripts, preload what the first paint needs, and size "
            "images to the screen. Give assets names that contain their hashes and cache them forever, and keep "
            "the HTML's lifetime short. Escape everything you insert into a page, set a strict content security "
            "policy, and mark cookies SameSite. And use real buttons and links before reaching for ARIA, make "
            "every action reachable from the keyboard, and keep text contrast at four and a half to one or more."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that specificity is a total preorder, \ and give two selectors with equal specificity whose order "
            r"in the stylesheet decides the style.",
            r"Prove that Knuth--Plass's dynamic program finds an optimal set of breaks in $O(nw)$ time for $n$ words "
            r"and at most $w$ words per line, \ and that greedy is optimal when only the number of lines counts.",
            r"Give the output order of a program mixing \texttt{setTimeout}, \ promises and \texttt{await}, \ and "
            r"justify each step from the event loop's rules.",
            r"Derive the contrast ratio's range, \ 1 to 21, \ and find the lightest grey with ratio 4.5 on white.",
            r"\textit{Build.} \ Add a flexbox container to our toy browser, \ and render a navigation bar that "
            r"shrinks as the window narrows.",
            r"$\bigstar$ \textit{Research.} \ Find a flex-layout algorithm with intrinsic sizing whose relayout cost "
            r"is bounded by the size of the change, \ with a matching lower bound.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give our toy browser flexbox, and render a navigation bar that shrinks as the window "
            "narrows. The last, marked with a star, is a research problem: incremental flex layout with intrinsic "
            "sizes, whose cost is bounded by the change, with a lower bound to match."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 43, \ APIs and Services", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"every call becomes a message that can be lost or duplicated", HEAD),
            (r"wire formats: \ JSON's numbers, \ Protocol Buffers' varints", DATA),
            (r"idempotency, \ retries and exactly-once as at-least-once plus dedup", YES),
            (r"sagas, \ backpressure and rate limits", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 43: APIs and services. When a program is split across machines, every call becomes a "
            "message that can be lost, duplicated or delayed. We derive the wire formats that carry them, make "
            "operations safe to retry, build exactly-once out of at-least-once and deduplication, and keep services "
            "from overwhelming each other."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Panchekha and Harrelson, \textit{Web Browser Engineering}; \ Grigorik, \textit{High Performance "
             r"Browser Networking}",
             r"Haverbeke, \textit{Eloquent JavaScript}; \ the WHATWG HTML standard; \ CSS specifications; \ WCAG 2.2"],
            [r"Knuth and Plass \ (1981); \ Zhang and Shasha \ (1989); \ Garsiel and Irish, \ ``How Browsers Work''",
             r"Meyerovich and Bod\'ik \ (2010); \ Panchekha and Torlak \ (2016, \ Cassius)",
             r"Akhawe et al. \ (2010); \ Fett, \ K\"usters and Schmitz \ (2016); \ Veronese et al. \ (2023)",
             r"Huang et al. \ (2012, \ LTE power); \ Kleppmann et al. \ (2019, \ local-first)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM)
