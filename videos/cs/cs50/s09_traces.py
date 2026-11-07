from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, mono


def node(text, col, w=2.4, h=0.8, size=20):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=col, stroke_width=2.2, fill_color=BG,
                         fill_opacity=1)
    return VGroup(r, label(text, font_size=size, color=col).move_to(r))


def waterfall(tr, x0=-3.0, x1=6.4, top=2.35, row_h=0.46):
    """A trace drawn as a waterfall: one row per span (depth-first), indented names on the left, bars on a time axis.
    Returns the group and helpers: ``g.xp(t)``, ``g.row_y[id]``, ``g.bars[id]``."""
    spans = tr["spans"]
    total = tr["total"]
    depth = {}
    for s in spans:
        depth[s["id"]] = 0 if s["parent"] is None else depth[s["parent"]] + 1
    t_max = 35.0

    def xp(t):
        return x0 + (x1 - x0) * t / t_max
    g = VGroup()
    names, bars = VGroup(), VGroup()
    row_y = {}
    for k, s in enumerate(spans):
        y = top - k * row_h
        row_y[s["id"]] = y
        nm = label(s["service"], font_size=19, color=GREY_A).move_to([0, y, 0])
        nm.align_to([-6.6 + 0.35 * depth[s["id"]], 0, 0], LEFT)
        col = KERN if s["parent"] is None else DATA
        b = Rectangle(width=max(0.03, xp(s["end"]) - xp(s["start"])), height=row_h * 0.62, stroke_width=0,
                      fill_color=col, fill_opacity=0.8).move_to([(xp(s["start"]) + xp(s["end"])) / 2, y, 0])
        names.add(nm)
        bars.add(b)
    base = top - len(spans) * row_h + row_h * 0.3
    axis = Line([xp(0), base, 0], [xp(t_max), base, 0], color=GREY_C, stroke_width=1.5)
    ticks = VGroup(*[VGroup(Line([xp(t), base, 0], [xp(t), base - 0.08, 0], color=GREY_C, stroke_width=1.5),
                            label(rf"{t}", font_size=15, color=GREY_B).move_to([xp(t), base - 0.25, 0]))
                     for t in range(0, 36, 5)])
    unit = label(r"ms", font_size=15, color=GREY_B).next_to(ticks[-1], RIGHT, buff=0.12)
    grid = VGroup(*[DashedLine([xp(t), base, 0], [xp(t), top + row_h / 2, 0], color=GREY_D, stroke_width=0.8,
                               dash_length=0.05) for t in range(5, 36, 5)])
    end = DashedLine([xp(total), base, 0], [xp(total), top + row_h / 2, 0], color=WHITE, stroke_width=1.5)
    g.add(grid, names, bars, axis, ticks, unit)
    g.names, g.bars, g.axis, g.ticks, g.unit, g.grid, g.end = names, bars, axis, ticks, unit, grid, end
    g.xp, g.row_y, g.base, g.row_h = xp, row_y, base, row_h
    return g


class Traces(VoiceoverScene):
    def construct(self):
        self.card()
        self.logs()
        self.spans()
        self.waterfall()
        self.critical()
        self.sampling()

    def card(self):
        card = chapter_card(8, r"Logs and traces", r"Where did this request spend its time?", lit=(2010, 2019),
                            extra=((2010, r"Sigelman et al.: \ Dapper"), (2019, r"OpenTelemetry")), part=PART)
        with self.voiceover("Chapter eight. Logs and traces: following one request through many services."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def logs(self):
        head = label(r"Structured logs", font_size=36).to_edge(UP, buff=0.3)
        t1 = label(r"a line of prose", font_size=20, color=GREY_A)
        prose = mono("2026-11-07 14:03:12 ERROR book 4711 failed after 2310ms (db timeout)", size=17,
                     color=GREY_A)
        top = VGroup(t1, prose).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, 2.15, 0])
        regex = mono(r"grep -E 'failed after [0-9]+ms'", size=16, color=NO)
        regex_l = label(r"breaks when someone rewords the message", font_size=18, color=NO)
        rx = VGroup(regex, regex_l).arrange(RIGHT, buff=0.35).next_to(top, DOWN, buff=0.3).align_to(top, LEFT)
        t2 = label(r"the same event as named fields", font_size=20, color=YES)
        js = code_block(['{"ts": "2026-11-07T14:03:12.481Z",',
                         ' "level": "error",',
                         ' "service": "catalog",',
                         ' "route": "/book/:id",',
                         ' "book": 4711,',
                         ' "duration_ms": 2310,',
                         ' "error": "db timeout",',
                         ' "trace_id": "4bf92f3577b34da6"}'], size=16)
        bottom = VGroup(t2, js).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-3.4, -1.35, 0])
        hl = SurroundingRectangle(js[-1], color=HEAD, buff=0.05, stroke_width=2)
        q_t = label(r"questions become queries", font_size=20, color=WHITE)
        q = code_block(['level = "error"', '| group by route, region', '| count, p99(duration_ms)'], size=16,
                       color=DATA)
        qq = VGroup(q_t, q).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        qq.move_to([1.5, 0, 0], aligned_edge=LEFT).align_to(bottom, UP)
        tid = wrapped_label(r"the \textbf{trace id} joins every line one request wrote, \ in every service it "
                            r"touched", 5.0, font_size=19, color=HEAD).next_to(qq, DOWN, buff=0.45).align_to(qq, LEFT)
        ill = note(r"illustrative", font_size=16).to_edge(DOWN, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Logs come first. <bookmark mark='a'/> A line of prose is easy to write and hard to use. To count "
            "failures by route, someone writes a regular expression, and it breaks the day the message is reworded. "
            "<bookmark mark='b'/> A structured log writes the same event as named fields. <bookmark mark='c'/> Then "
            "questions become queries over Part 46's append-only streams: errors by route and region, counted, "
            "with their ninety-ninth percentile. <bookmark mark='d'/> One field matters most: the trace identifier. "
            "It joins every line that one request wrote, in every service it touched."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(top))
            self.play(FadeIn(rx))
            vo.wait_until("b")
            self.play(FadeIn(t2), LaggedStart(*[FadeIn(x) for x in js], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(qq))
            vo.wait_until("d")
            self.play(Create(hl), FadeIn(tid))
        self.wait(0.4)
        self.clear_scene()

    def spans(self):
        head = label(r"Spans, \ and the context that links them", font_size=36).to_edge(UP, buff=0.3)
        names = (r"frontend", r"catalog", r"db")
        svcs = VGroup(*[node(n, c, w=2.1) for n, c in zip(names, (KERN, DATA, DATA))]).arrange(RIGHT, buff=2.9)
        svcs.move_to([0, 1.7, 0])
        hdrs = ("00-4bf9...-a3ce...-01", "00-4bf9...-53f1...-01")
        arrows = VGroup(*[Arrow(svcs[k].get_right(), svcs[k + 1].get_left(), buff=0.1, color=GREY_B,
                                stroke_width=2.5) for k in range(2)])
        hlab = VGroup(*[VGroup(mono("traceparent:", size=14, color=HEAD), mono(h, size=14, color=HEAD)).arrange(
            DOWN, buff=0.06).next_to(arrows[k], UP, buff=0.12) for k, h in enumerate(hdrs)])
        ids = (("a3ce929d", "-", "GET /book/4711"), ("53f1e0b2", "a3ce929d", "lookup"),
               ("9e0277c4", "53f1e0b2", "SELECT ..."))
        cards = VGroup()
        for (sid, par, nm), sv in zip(ids, svcs):
            body = code_block(["trace  4bf92f35...", f"span   {sid}", f"parent {par}", f"name   {nm}",
                               "start, end"], size=16)
            body[0].set_color(HEAD)
            body[2].set_color(YES)
            fr = SurroundingRectangle(body, color=GREY_C, buff=0.15, corner_radius=0.08, stroke_width=1.5)
            cards.add(VGroup(fr, body).next_to(sv, DOWN, buff=0.55))
        links = VGroup(*[CurvedArrow(cards[k + 1][1][2].get_left() + LEFT * 0.12,
                                     cards[k][1][1].get_right() + RIGHT * 0.12, angle=-PI / 6, color=YES,
                                     stroke_width=2) for k in range(2)])
        notes = VGroup(
            wrapped_label(r"\textbf{trace id}: \ shared by every span of the request", 4.0, font_size=19, color=HEAD),
            wrapped_label(r"\textbf{parent id}: \ the span that caused this one; \ the spans form a tree", 4.0,
                          font_size=19, color=YES),
            wrapped_label(r"the context travels in a header \ (W3C Trace Context); \ each service starts a child span "
                          r"and passes it on", 4.0, font_size=19, color=WHITE),
        ).arrange(RIGHT, buff=0.4, aligned_edge=UP).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 2010 Benjamin Sigelman and colleagues described Dapper, Google's tracing system. "
            "<bookmark mark='a'/> One user request crosses many services, and each unit of work becomes a span: a "
            "name, a start and an end, and three identifiers. <bookmark mark='b'/> The trace identifier is shared by "
            "every span of the request. The span identifier is the span's own. The parent identifier names the span "
            "that caused it, so the spans form a tree. <bookmark mark='c'/> The identifiers travel with the request "
            "in a header, which the W3C's Trace Context standard calls traceparent. Each service reads it, starts a "
            "child span, and passes the header on. <bookmark mark='d'/> Spans are reported separately and joined "
            "later by trace identifier. OpenTelemetry, formed in 2019, is today's common toolkit for all of this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(svcs))
            vo.wait_until("a")
            self.play(FadeIn(cards[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), Indicate(cards[0][1][0], color=HEAD))
            self.play(FadeIn(notes[1]), Indicate(cards[0][1][2], color=YES))
            vo.wait_until("c")
            for k in range(2):
                self.play(GrowArrow(arrows[k]), FadeIn(hlab[k]))
                self.play(FadeIn(cards[k + 1]), Create(links[k]))
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(*[Indicate(c[1][0], color=HEAD) for c in cards])
        self.wait(0.4)
        self.clear_scene()

    def waterfall(self):
        tr = load("trace")
        head = label(r"A trace as a waterfall", font_size=36).to_edge(UP, buff=0.3)
        wf = waterfall(tr)
        sp = {s["service"]: s for s in tr["spans"]}
        ids = [s["id"] for s in tr["spans"]]
        tot = label(rf"{tr['total']:.1f} ms", font_size=19, color=WHITE).next_to(wf.end, UP, buff=0.05)
        par = Brace(VGroup(wf.bars[ids.index(sp["catalog"]["id"])], wf.bars[ids.index(sp["recommend"]["id"])]),
                    RIGHT, buff=0.1, color=GREY_B)
        par.next_to([wf.xp(sp["recommend"]["end"]), 0, 0], RIGHT, buff=0.1).set_y(
            (wf.row_y[sp["catalog"]["id"]] + wf.row_y[sp["recommend"]["id"]]) / 2)
        par_l = label(r"in parallel", font_size=17, color=GREY_A).next_to(par, RIGHT, buff=0.08)
        foot = label(r"one trace from our simulator: \ nine spans, \ each indented under its parent", font_size=19,
                     color=GREY_A).to_edge(DOWN, buff=0.3)

        def show(*names):
            return [GrowFromEdge(wf.bars[ids.index(sp[n]["id"])], LEFT) for n in names] + \
                   [FadeIn(wf.names[ids.index(sp[n]["id"])]) for n in names]
        with self.voiceover(
            "Here is one trace from our simulator, drawn as a waterfall: time runs to the right, and each span is "
            "indented under its parent. <bookmark mark='a'/> The front end starts, and checks authentication first. "
            "<bookmark mark='b'/> Then it calls the catalog and the recommender at the same time, and each calls its "
            "own dependencies in turn: a cache and then a database; features, and then a model. "
            "<bookmark mark='c'/> When both have answered, it renders the page. The whole request took thirty-two "
            "point six milliseconds. <bookmark mark='d'/> If it has to be faster, where should the effort go?"
        ) as vo:
            self.play(FadeIn(head), Create(wf.axis), FadeIn(wf.ticks), FadeIn(wf.unit), FadeIn(wf.grid),
                      FadeIn(foot))
            vo.wait_until("a")
            self.play(*show("frontend"))
            self.play(*show("auth"))
            vo.wait_until("b")
            self.play(*show("catalog", "recommend"))
            self.play(*show("cache", "features"))
            self.play(*show("db", "model"))
            self.play(GrowFromCenter(par), FadeIn(par_l))
            vo.wait_until("c")
            self.play(*show("render"))
            self.play(Create(wf.end), FadeIn(tot))
            vo.wait_until("d")
            self.play(Indicate(tot, color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    def critical(self):
        tr = load("trace")
        spans = tr["spans"]
        sp = {s["service"]: s for s in spans}
        ids = [s["id"] for s in spans]
        head = label(r"The critical path", font_size=36).to_edge(UP, buff=0.3)
        wf = waterfall(tr)
        tot = label(rf"{tr['total']:.1f} ms", font_size=19, color=WHITE).next_to(wf.end, UP, buff=0.05)
        segs = VGroup()
        path_pts = []
        for sid, a, b in tr["critical"]:
            y = wf.row_y[sid]
            segs.add(Rectangle(width=max(0.03, wf.xp(b) - wf.xp(a)), height=wf.row_h * 0.62, stroke_color=HEAD,
                               stroke_width=2, fill_color=HEAD, fill_opacity=0.9).move_to(
                [(wf.xp(a) + wf.xp(b)) / 2, y, 0]))
            path_pts += [[wf.xp(a), y, 0], [wf.xp(b), y, 0]]
        path = VMobject(color=HEAD, stroke_width=2.5).set_points_as_corners(path_pts)
        path.set_z_index(2)
        segs.set_z_index(1)
        on_path = {sid for sid, _, _ in tr["critical"]}
        off = [wf.bars[ids.index(s["id"])] for s in spans if s["id"] not in on_path]
        share = sorted(tr["share"].items(), key=lambda kv: -kv[1])
        slack = sp["recommend"]["end"] - sp["catalog"]["end"]
        db_ms = sp["db"]["end"] - sp["db"]["start"]
        sh_txt = r", \ ".join(rf"{n} {v:.1f}" for n, v in share)
        notes = VGroup(
            wrapped_label(rf"on the critical path, \ in ms: \ {sh_txt}", 12.6, font_size=19, color=HEAD),
            wrapped_label(rf"off it: \ the catalog, \ and its database \ ({db_ms:.1f} ms); \ speeding them up saves "
                          rf"nothing; \ the catalog has {slack:.1f} ms of slack", 12.6, font_size=19, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.22)
        part = label(r"the longest path through the DAG of work \ (Part 19)", font_size=18, color=GREY_A)
        part.next_to(head, DOWN, buff=0.12)
        with self.voiceover(
            "The answer is the critical path: the chain of work the end was waiting for. <bookmark mark='a'/> "
            "Walk back from the end: the front end waited for render, render for the recommender, the recommender "
            "for its model, the model for the features, and so back to authentication. <bookmark mark='b'/> It is "
            "the longest path through the DAG of the trace's work, as in Part 19. Along it the model accounts for "
            "twelve point six milliseconds, render for six, the features for five point eight. <bookmark "
            "mark='c'/> The catalog and its database are not on it. The database takes twelve and a half "
            "milliseconds, yet making it faster would save nothing. The catalog has seven point three "
            "milliseconds of slack: shave more than that off the model, and the catalog becomes critical instead."
        ) as vo:
            self.play(FadeIn(head), FadeIn(wf), FadeIn(wf.end), FadeIn(tot))
            vo.wait_until("a")
            self.play(*[b.animate.set_fill(opacity=0.3) for b in wf.bars])
            for seg in reversed(segs):
                self.play(FadeIn(seg), run_time=0.45)
            self.play(Create(path), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(part), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(*[b.animate.set_fill(DATA, 0.85) for b in off], FadeIn(notes[1]))
            self.play(*[Indicate(b, color=DATA) for b in off])
        self.wait(0.4)
        self.clear_scene()

    def sampling(self):
        s = load("sampling")
        n, tot, hd, tl = s["n"], s["total"], s["head"], s["tail"]
        rate = s["head_rate"]
        head = label(r"Which traces to keep?", font_size=36).to_edge(UP, buff=0.3)
        X0, W = -3.4, 6.0
        groups = VGroup()
        specs = (("errors", rf"traces with an error: \ {tot['errors']:,}"),
                 ("slow", rf"traces slower than 100 ms: \ {tot['slow']:,}"))
        rows_by = {}
        for gi, (key, title) in enumerate(specs):
            y0 = 2.0 - gi * 2.15
            t = label(title, font_size=21, color=WHITE).move_to([X0, y0, 0], aligned_edge=LEFT)
            rows = VGroup()
            for ri, (name, kept, col) in enumerate(((rf"head, \ {100 * rate:.0f}\%", hd[key], DATA),
                                                    (r"tail", tl[key], YES))):
                y = y0 - 0.6 - ri * 0.55
                frame = Rectangle(width=W, height=0.36, stroke_color=GREY_C, stroke_width=1.2).move_to(
                    [X0 + W / 2, y, 0])
                fill = Rectangle(width=max(0.03, W * kept / tot[key]), height=0.36, stroke_width=0, fill_color=col,
                                 fill_opacity=0.85).move_to([X0, y, 0], aligned_edge=LEFT)
                nm = label(name, font_size=19, color=col).next_to(frame, LEFT, buff=0.25)
                val = label(rf"{kept:,} kept", font_size=19, color=col).next_to(frame, RIGHT, buff=0.2)
                rows.add(VGroup(frame, fill, nm, val))
            rows_by[key] = rows
            groups.add(VGroup(t, rows))
        kept = VGroup(
            label(rf"of {n:,} simulated traces, \ head sampling kept {hd['kept']:,}; \ tail sampling kept "
                  rf"{tl['kept']:,}", font_size=19, color=GREY_A),
        ).next_to(groups, DOWN, buff=0.35)
        notes = VGroup(
            wrapped_label(r"\textbf{head}: \ a coin at the first span; \ the decision travels in the context, \ so "
                          r"all services agree", 6.0, font_size=19, color=DATA),
            wrapped_label(r"\textbf{tail}: \ decided when the trace ends; \ every span buffered at one collector, \ "
                          r"chosen by hashing the trace id \ (Part 39)", 6.0, font_size=19, color=YES),
        ).arrange(RIGHT, buff=0.4, aligned_edge=UP).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Tracing every request costs too much, so traces are sampled. <bookmark mark='a'/> Head sampling "
            "decides at the first span, with a coin that keeps one trace in a hundred, and the decision travels "
            "in the context, so every service keeps the same traces. Of fifty thousand simulated requests it kept "
            "five hundred and thirty-three, <bookmark mark='b'/> but only four of the eight hundred and "
            "seventy-six that failed, and fifty-four of the four thousand three hundred slow ones. <bookmark "
            "mark='c'/> Tail sampling decides when the trace has finished: keep every error, every trace over a "
            "hundred milliseconds, and one in a hundred of the rest. That kept all of them, in five thousand five "
            "hundred and eighty-four traces. <bookmark mark='d'/> The price: every span is buffered until its "
            "trace ends, at one collector chosen by hashing the trace identifier, Part 39 again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(groups[0][0]), FadeIn(groups[1][0]),
                      *[FadeIn(r[0]) for g in groups for r in g[1]], *[FadeIn(r[2]) for g in groups for r in g[1]])
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(kept))
            vo.wait_until("b")
            for key in ("errors", "slow"):
                r = rows_by[key][0]
                self.play(GrowFromEdge(r[1], LEFT), FadeIn(r[3]))
            vo.wait_until("c")
            for key in ("errors", "slow"):
                r = rows_by[key][1]
                self.play(GrowFromEdge(r[1], LEFT), FadeIn(r[3]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, NO)
