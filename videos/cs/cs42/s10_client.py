from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, module_box,
                                   mono, tag_box)

# the input compute.py gives cache_sim: the resource changes at 300 s
CHANGE_AT = 300
OUTCOME = {"miss": (r"miss: \ full body", DATA), "fresh": (r"fresh: \ no request", YES),
           "revalidate: 304": (r"304: \ headers only", HEAD), "revalidate: 200": (r"200: \ changed body", KERN),
           "stale": (r"stale: \ served, \ checked in background", LAM)}


def _kind(text: str) -> str:
    for k in OUTCOME:
        if text.startswith(k):
            return k
    raise ValueError(text)


def _item(text, done=False, color=WHITE, w=2.6):
    r = Rectangle(width=w, height=0.42, stroke_color=GREY_C, stroke_width=1.2)
    box = Square(0.24, stroke_color=GREY_A, stroke_width=1.5).move_to(r.get_left() + RIGHT * 0.3)
    tick = Square(0.14, stroke_width=0, fill_color=YES, fill_opacity=1 if done else 0).move_to(box)
    t = label(text, font_size=19, color=color).next_to(box, RIGHT, buff=0.25)
    return VGroup(r, box, tick, t)


class Client(VoiceoverScene):
    def construct(self):
        self.card()
        self.revalidate()
        self.afternoon()
        self.assets()
        self.worker()
        self.storage()
        self.localfirst()

    def card(self):
        card = chapter_card(9, r"Caches, \ offline and local-first", r"What should the browser keep, \ and for how "
                            r"long?", lit=(1997, 2019), extra=((1997, r"HTTP/1.1: \ Cache-Control"),
                                                               (2019, r"Kleppmann et al.: \ local-first")), part=PART)
        with self.voiceover("Chapter nine. Caches, offline, and local-first software."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def revalidate(self):
        head = label(r"Fresh, \ stale, \ revalidated", font_size=36).to_edge(UP, buff=0.3)
        xl, xr, top, bot = -4.2, 4.2, 2.4, -2.9
        lines = VGroup(Line([xl, top, 0], [xl, bot, 0], color=GREY_C), Line([xr, top, 0], [xr, bot, 0],
                                                                             color=GREY_C))
        names = VGroup(label(r"browser cache", font_size=20, color=GREY_A).next_to(lines[0], UP, buff=0.1),
                       label(r"server", font_size=20, color=GREY_A).next_to(lines[1], UP, buff=0.1))

        def exchange(y, req, resp, col):
            a = Arrow([xl, y, 0], [xr, y - 0.25, 0], buff=0, stroke_width=2, color=GREY_B,
                      max_tip_length_to_length_ratio=0.03)
            b = Arrow([xr, y - 0.55, 0], [xl, y - 0.8, 0], buff=0, stroke_width=2.5, color=col,
                      max_tip_length_to_length_ratio=0.03)
            rq = code_block(req, size=16, color=GREY_A).next_to(a, UP, buff=0.04)
            rs = code_block(resp, size=16, color=col).next_to(b, DOWN, buff=0.04)
            return VGroup(a, rq), VGroup(b, rs)
        e1 = exchange(1.85, ["GET /app.css"], ['200 OK   Cache-Control: max-age=60   ETag: "v1"'], DATA)
        t1 = label(r"0 s", font_size=17, color=GREY_B).next_to([xl, 1.85, 0], LEFT, buff=0.15)
        fresh = VGroup(label(r"20 s", font_size=17, color=GREY_B).next_to([xl, 0.25, 0], LEFT, buff=0.15),
                       label(r"younger than 60 s: \ fresh, \ served from the cache with no request at all",
                             font_size=19, color=YES).move_to([0, 0.25, 0]))
        e2 = exchange(-0.65, ['GET /app.css   If-None-Match: "v1"'], ['304 Not Modified   (no body)'], HEAD)
        t2 = label(r"70 s", font_size=17, color=GREY_B).next_to([xl, -0.65, 0], LEFT, buff=0.15)
        ill = note(r"illustrative headers", font_size=17).to_corner(DR, buff=0.35)
        side = wrapped_label(r"the \textbf{ETag} names a version of the resource; \ if it still matches, \ the "
                             r"answer is a few hundred bytes of headers", 7.4, font_size=19, color=WHITE).move_to(
            [0, -2.35, 0])
        with self.voiceover(
            "The fastest request is the one never sent. <bookmark mark='a'/> With its answer, a server "
            "can say how long the answer stays good: max age sixty, fresh for a minute. It also sends an "
            "ETag, a name for this version. <bookmark mark='b'/> Twenty seconds later, the browser uses "
            "its copy without asking anyone. <bookmark mark='c'/> After a minute the copy is stale, but "
            "not useless. The browser asks again, sending the ETag. Nothing has changed, so the server "
            "answers three hundred and four, not modified: headers only, a round trip but no body."
        ) as vo:
            self.play(FadeIn(head), Create(lines), FadeIn(names), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(t1), GrowArrow(e1[0][0]), FadeIn(e1[0][1]))
            self.play(GrowArrow(e1[1][0]), FadeIn(e1[1][1]))
            vo.wait_until("b")
            self.play(FadeIn(fresh))
            vo.wait_until("c")
            self.play(FadeIn(t2), GrowArrow(e2[0][0]), FadeIn(e2[0][1]))
            self.play(GrowArrow(e2[1][0]), FadeIn(e2[1][1]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def afternoon(self):
        c = load("cache")
        head = label(r"Nine requests, \ two policies", font_size=36).to_edge(UP, buff=0.3)
        x0, sc = -5.2, 11.0 / 420

        def X(t):
            return x0 + t * sc

        def row(outcomes, y, swr):
            base = Line([X(0), y, 0], [X(420), y, 0], color=GREY_C, stroke_width=1.5)
            bars, dots = VGroup(), VGroup()
            for t, text in outcomes:
                k = _kind(text)
                if k != "fresh":            # the copy is stored, or re-validated, at this moment
                    w = min(60, 420 - t)
                    bars.add(Rectangle(width=w * sc - 0.05, height=0.14, stroke_width=0, fill_color=YES,
                                       fill_opacity=0.6).move_to([X(t) + w * sc / 2, y + 0.3, 0]))
                    if swr and t + 60 < 420:
                        e = min(420, t + 180)
                        bars.add(Rectangle(width=(e - t - 60) * sc - 0.05, height=0.14, stroke_width=0, fill_color=LAM,
                                           fill_opacity=0.35).move_to([X(t + 60) + (e - t - 60) * sc / 2, y + 0.3,
                                                                       0]))
                dots.add(Dot([X(t), y, 0], radius=0.13, color=OUTCOME[k][1]))
            return base, bars, dots
        y1, y2 = 1.15, -0.85
        p_base, p_bars, p_dots = row(c["plain"], y1, False)
        s_base, s_bars, s_dots = row(c["swr"], y2, True)
        ticks = VGroup(*[label(f"{t}", font_size=16, color=GREY_B).move_to([X(t), y2 - 0.4, 0]) for t in c["times"]])
        unit = label(r"seconds", font_size=16, color=GREY_B).next_to(ticks, RIGHT, buff=0.3)
        names = VGroup(label(r"\texttt{max-age=60}", font_size=19, color=WHITE).next_to([X(0), y1 + 0.75, 0], RIGHT,
                                                                                       buff=0),
                       label(r"\texttt{max-age=60, stale-while-revalidate=120}", font_size=19, color=WHITE).next_to(
                           [X(0), y2 + 0.75, 0], RIGHT, buff=0))
        chg = VGroup(DashedLine([X(CHANGE_AT), y1 + 0.55, 0], [X(CHANGE_AT), y2 - 0.2, 0], color=NO,
                                stroke_width=2),
                     label(r"the file changes", font_size=16, color=NO).next_to([X(CHANGE_AT), y1 + 0.55, 0], UP,
                                                                                 buff=0.05))
        legend = VGroup(*[VGroup(Dot(radius=0.09, color=col), label(t, font_size=17, color=col)).arrange(
            RIGHT, buff=0.1) for t, col in OUTCOME.values()]).arrange(RIGHT, buff=0.35).next_to(ticks, DOWN,
                                                                                               buff=0.4)
        if legend.width > 13.2:
            legend.width = 13.2
        legend.set_x(0)
        waits_p = sum(_kind(t) != "fresh" for _, t in c["plain"])
        waits_s = sum(_kind(t) not in ("fresh", "stale") for _, t in c["swr"])
        old = [t for t, text in c["swr"] if _kind(text) == "stale" and t >= CHANGE_AT and
               max(s for s, x in c["swr"] if s < t and _kind(x) != "fresh") < CHANGE_AT]
        res = VGroup(
            label(rf"waited on the network: \ {waits_p} of {len(c['times'])} requests", font_size=19,
                  color=HEAD).next_to([X(420), y1 - 0.4, 0], LEFT, buff=0).align_to(p_base, RIGHT),
            label(rf"waited: \ {waits_s} of {len(c['times'])}; \ but at {old[0]} s the old version, \ once",
                  font_size=19, color=HEAD).next_to([X(420), y2 - 0.4, 0], LEFT, buff=0),
        )
        res[0].move_to([X(210), y1 - 0.45, 0])
        res[1].move_to([X(210), y2 - 0.95, 0]).shift(UP * 0)
        legend.next_to(res[1], DOWN, buff=0.35).set_x(0)
        with self.voiceover(
            "Here one file is requested nine times in seven minutes, and changes at three hundred "
            "seconds. <bookmark mark='a'/> With max age sixty: a miss, then two fresh hits, then "
            "revalidations answered with three hundred and four, until three hundred and twenty, when the"
            " ETag no longer matches and the new body comes back. Seven of the nine requests waited on "
            "the network. <bookmark mark='b'/> Add stale while revalidate, a hundred and twenty seconds: "
            "a stale copy is served at once, and checked in the background. Only the first request waits."
            " <bookmark mark='c'/> The price: at three hundred and twenty, the user sees the old version,"
            " once."
        ) as vo:
            self.play(FadeIn(head), Create(p_base), Create(s_base), FadeIn(ticks), FadeIn(unit), FadeIn(names),
                      FadeIn(chg), FadeIn(legend))
            vo.wait_until("a")
            for k in range(len(p_dots)):
                bar = [b for b in p_bars if abs(b.get_left()[0] - p_dots[k].get_x()) < 0.05]
                self.play(FadeIn(p_dots[k], scale=0.5), *[FadeIn(b) for b in bar], run_time=0.5)
            self.play(FadeIn(res[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in s_dots], lag_ratio=0.2), FadeIn(s_bars),
                      run_time=2.5)
            vo.wait_until("c")
            i = c["times"].index(old[0])
            self.play(Indicate(s_dots[i], color=NO, scale_factor=1.8), FadeIn(res[1]))
        self.wait(0.4)
        self.clear_scene()

    def assets(self):
        head = label(r"Names that never go stale", font_size=36).to_edge(UP, buff=0.3)
        html = VGroup(mono("index.html", size=19, color=WHITE),
                      mono("Cache-Control: no-cache", size=16, color=HEAD)).arrange(DOWN, buff=0.12)
        hbox = SurroundingRectangle(html, color=HEAD, buff=0.2, corner_radius=0.08)
        page = VGroup(hbox, html).move_to([-4.0, 0.9, 0])
        refs = code_block(['<script src="/app.3f9a2c.js">', '<link href="/style.8be1d0.css">'], size=16,
                          color=GREY_A).next_to(page, DOWN, buff=0.3)

        def asset(name, col):
            t = VGroup(mono(name, size=18, color=col),
                       mono("max-age=31536000, immutable", size=16, color=YES)).arrange(DOWN, buff=0.1)
            return VGroup(SurroundingRectangle(t, color=col, buff=0.16, corner_radius=0.08), t)
        a1 = asset("app.3f9a2c.js", DATA)
        a2 = asset("style.8be1d0.css", DATA)
        VGroup(a1, a2).arrange(DOWN, buff=0.35).move_to([2.6, 1.0, 0])
        ar = VGroup(Arrow(refs[0].get_right(), a1.get_left(), buff=0.1, stroke_width=2, color=GREY_B,
                          max_tip_length_to_length_ratio=0.08),
                    Arrow(refs[1].get_right(), a2.get_left(), buff=0.1, stroke_width=2, color=GREY_B,
                          max_tip_length_to_length_ratio=0.08))
        a3 = asset("app.b71e04.js", YES).next_to(a2, DOWN, buff=0.35)
        new_ref = mono('<script src="/app.b71e04.js">', size=16, color=YES).move_to(refs[0], aligned_edge=LEFT)
        ar3 = Arrow(refs[0].get_right() + DOWN * 0.05, a3.get_left(), buff=0.1, stroke_width=2, color=YES,
                    max_tip_length_to_length_ratio=0.08)
        ill = note(r"illustrative hashes", font_size=17).next_to(a3, DOWN, buff=0.2).align_to(a3, RIGHT)
        lines = VGroup(
            wrapped_label(r"the file's name contains a hash of its content \ (Part 41): \ the same name always means "
                          r"the same bytes, \ so the copy may be kept for a year and never checked", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"a new release is new names; \ only the small page that lists them is revalidated", 12.4,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Build tools avoid that bet altogether. <bookmark mark='a'/> The page is revalidated every "
            "time, but the scripts and styles it names carry a hash of their content in the file name: "
            "Part 41's content addressing. <bookmark mark='b'/> One name means one set of bytes, so those"
            " files are cached for a year and marked immutable, never checked. <bookmark mark='c'/> "
            "Change a line, and the build emits a new name. The page points at it, the browser fetches "
            "that one file, and the old copy is simply never used again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(page), FadeIn(refs))
            vo.wait_until("a")
            self.play(FadeIn(a1), FadeIn(a2), Create(ar))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]), Indicate(a1[1][1], color=YES), Indicate(a2[1][1], color=YES))
            vo.wait_until("c")
            self.play(Transform(refs[0], new_ref), FadeOut(ar[0]), a1.animate.set_opacity(0.35))
            self.play(FadeIn(a3), Create(ar3), FadeIn(ill), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def worker(self):
        head = label(r"Service workers: \ a proxy inside the browser", font_size=36).to_edge(UP, buff=0.3)
        pagebox = module_box(r"the page", DATA, w=1.9, h=0.7, font=20).move_to([-5.2, 1.2, 0])
        sw = module_box(r"service worker", KERN, w=2.4, h=0.7, font=20).move_to([-1.4, 1.2, 0])
        cache = module_box(r"cache storage", YES, w=2.4, h=0.7, font=20).move_to([-1.4, -0.6, 0])
        net = module_box(r"network", LAM, w=1.9, h=0.7, font=20).move_to([2.4, 1.2, 0])
        wires = VGroup(Line(pagebox.get_right(), sw.get_left(), color=GREY_C),
                       Line(sw.get_bottom(), cache.get_top(), color=GREY_C),
                       Line(sw.get_right(), net.get_left(), color=GREY_C))
        code = code_block(['self.onfetch = e => e.respondWith(', '  caches.match(e.request)',
                           '    .then(hit => hit || fetch(e.request)));'], size=16).move_to([4.6, -0.6, 0])
        code.to_edge(RIGHT, buff=0.35)
        codel = label(r"cache-first, \ in three lines", font_size=17, color=GREY_A).next_to(code, UP, buff=0.15
                                                                                          ).align_to(code, LEFT)
        mode = label(r"", font_size=20).move_to([-3.3, 2.3, 0])
        cross = Cross(net, stroke_color=NO, stroke_width=5).scale(0.6)
        lines = VGroup(
            wrapped_label(r"\textbf{cache-first}: \ answer from the cache, \ go to the network only on a miss \ --- \ "
                          r"for the app's own files", 12.4, font_size=19, color=YES),
            wrapped_label(r"\textbf{network-first}: \ try the network, \ fall back to the cache when offline \ --- \ "
                          r"for data that should be current", 12.4, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)

        def go(points, color, rt=0.45):
            d = Dot(points[0], radius=0.11, color=color)
            anims = [FadeIn(d, run_time=0.2)]
            for p in points[1:]:
                anims.append(d.animate(run_time=rt).move_to(p))
            anims.append(FadeOut(d, run_time=0.2))
            return Succession(*anims)
        P, S, C, N = pagebox.get_center(), sw.get_center(), cache.get_center(), net.get_center()

        def set_mode(text, col):
            return Transform(mode, label(text, font_size=20, color=col).move_to([-3.3, 2.3, 0]))
        with self.voiceover(
            "A service worker is a script the page installs between itself and the network. <bookmark "
            "mark='a'/> Every request the page makes, the worker sees first, and answers in ordinary "
            "JavaScript. <bookmark mark='b'/> Cache first: answer from the cache, and only on a miss go "
            "to the network, keeping a copy. That suits the app's own files, and lets it open with no "
            "connection at all. <bookmark mark='c'/> Network first: try the network, so the data is "
            "current, and when it is gone, fall back to the last copy. The page just keeps working."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pagebox), FadeIn(net))
            vo.wait_until("a")
            self.play(FadeIn(sw), FadeIn(cache), Create(wires), FadeIn(code), FadeIn(codel))
            vo.wait_until("b")
            self.play(set_mode(r"cache-first", YES), FadeIn(lines[0]))
            self.play(go([P, S, C, S, P], YES))
            self.play(go([P, S, C, S, N, S, C, S, P], HEAD, rt=0.35))
            vo.wait_until("c")
            self.play(set_mode(r"network-first", LAM), FadeIn(lines[1]))
            self.play(go([P, S, N, S, P], LAM))
            self.play(Create(cross))
            self.play(go([P, S, N + LEFT * 0.9, S, C, S, P], NO, rt=0.35))
        self.wait(0.4)
        self.clear_scene()

    def storage(self):
        head = label(r"Where the copies live", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"Cache Storage", r"requests and responses", r"asynchronous", r"the service worker's files"],
                [r"IndexedDB", r"objects, \ indexes, \ transactions", r"asynchronous", r"the app's data"],
                [r"localStorage", r"strings by key", r"synchronous", r"a few small settings"]]
        tab = grid_table([r"store", r"holds", r"access", r"good for"], rows, widths=[2.6, 3.9, 2.4, 3.6],
                         row_h=0.62, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.7).set_x(0)
        tab.cells[3][2].set_color(NO)
        for r in (1, 2):
            tab.cells[r][2].set_color(YES)
        lines = VGroup(
            wrapped_label(r"each is per origin \ (Chapter 11); \ a synchronous read blocks the main thread, \ "
                          r"Chapter 5's one long task", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"browsers may evict an origin's storage when the disk fills, \ unless the page asks for "
                          r"persistent storage", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.6)
        with self.voiceover(
            "Those copies need somewhere to live. <bookmark mark='a'/> Cache storage holds responses, for"
            " the worker. IndexedDB is a small transactional database of objects with indexes, for the "
            "app's data. localStorage holds strings by key, synchronously, so a large read blocks the "
            "main thread. <bookmark mark='b'/> All of it belongs to one origin, and may be evicted under "
            "pressure, unless the page asks for persistent storage."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def localfirst(self):
        head = label(r"Local-first software", font_size=36).to_edge(UP, buff=0.3)
        start = [("eggs", False), ("tea", False)]

        def device(name, x):
            items = VGroup(*[_item(t, d) for t, d in start]).arrange(DOWN, buff=0.08)
            frame = RoundedRectangle(width=3.1, height=2.6, corner_radius=0.15, stroke_color=GREY_B)
            title = label(name, font_size=20, color=GREY_A).next_to(frame, UP, buff=0.1)
            g = VGroup(frame, title).move_to([x, 0.7, 0])
            items.move_to(frame).align_to(frame, UP).shift(DOWN * 0.25)
            return g, items
        phone, p_items = device(r"phone", -4.6)
        laptop, l_items = device(r"laptop", 4.6)
        link = DashedLine(phone[0].get_right(), laptop[0].get_left(), color=NO, dash_length=0.15)
        off = label(r"offline", font_size=19, color=NO).next_to(link, UP, buff=0.1)
        on = label(r"back online: \ exchange operations", font_size=19, color=YES).next_to(link, UP, buff=0.1)
        ops_p = tag_box("insert milk", color=DATA, size=16)
        ops_l = VGroup(tag_box("insert bread", color=LAM, size=16), tag_box("tick eggs", color=LAM, size=16))
        ill = note(r"illustrative", font_size=17).next_to(laptop, DOWN, buff=0.12).align_to(laptop, RIGHT)
        same = label(r"the same list on both, \ whatever order the operations arrive in", font_size=20,
                     color=YES).next_to(VGroup(phone, laptop), DOWN, buff=0.3)
        lines = VGroup(
            wrapped_label(r"Kleppmann, \ Wiggins, \ van Hardenberg and McGranaghan \ (2019): \ the data lives on your "
                          r"devices, \ works offline and instantly; \ servers only help devices sync", 12.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"the merge is a \textbf{CRDT} \ (Part 39): \ commutative, \ associative and idempotent, \ "
                          r"so replicas converge with no server deciding; \ Automerge and Yjs are such libraries",
                          12.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Push this further, and the server stops being the home of the data. <bookmark mark='a'/> In "
            "2019 Martin Kleppmann and his co-authors, with the research lab Ink and Switch, called it "
            "local-first software: your data lives on your own devices, opens instantly, works offline, "
            "and servers only help the devices sync. <bookmark mark='b'/> A shopping list on two devices,"
            " both offline. The phone adds milk; the laptop adds bread and ticks off eggs. <bookmark "
            "mark='c'/> Reconnected, each sends the other its operations. <bookmark mark='d'/> A CRDT "
            "from Part 39 merges them: its merge is commutative, associative and idempotent, so both "
            "reach the same list, whatever order the messages arrive in. Automerge and Yjs are libraries "
            "built for exactly this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(phone), FadeIn(laptop), FadeIn(p_items), FadeIn(l_items))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(link), FadeIn(off), FadeIn(ill))
            pm = _item("milk", color=DATA).next_to(p_items, DOWN, buff=0.08)
            lb = _item("bread", color=LAM).next_to(l_items, DOWN, buff=0.08)
            self.play(FadeIn(pm, shift=DOWN * 0.2))
            self.play(FadeIn(lb, shift=DOWN * 0.2), l_items[0][2].animate.set_fill(YES, 1))
            vo.wait_until("c")
            self.play(Transform(off, on), link.animate.set_color(YES))
            ops_p.move_to([phone[0].get_right()[0] + 1.0, 0.0, 0])
            ops_l.arrange(DOWN, buff=0.1).move_to([laptop[0].get_left()[0] - 1.0, -0.85, 0])
            self.play(FadeIn(ops_p), FadeIn(ops_l))
            self.play(ops_p.animate.move_to([laptop[0].get_left()[0] - 1.0, 0.0, 0]),
                      ops_l.animate.move_to([phone[0].get_right()[0] + 1.0, -0.85, 0]), run_time=1.8)
            vo.wait_until("d")
            pb = _item("bread", color=LAM).next_to(pm, DOWN, buff=0.08)
            lm = _item("milk", color=DATA).move_to(lb)
            self.play(FadeOut(ops_p), FadeOut(ops_l), FadeIn(pb), p_items[0][2].animate.set_fill(YES, 1),
                      lb.animate.next_to(lm, DOWN, buff=0.08), FadeIn(lm))
            self.play(FadeOut(ill), FadeIn(same), FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, HEAD)
