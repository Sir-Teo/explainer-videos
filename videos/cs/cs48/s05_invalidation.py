from __future__ import annotations

import inspect
import math

from explainer.cs import *  # noqa: F403
from explainer.cs.design import blocks as B
from videos.cs.cs48.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, module_box,
                                   timeline_bar)

# the parameters of the stampede experiment (blocks.stampede's defaults, which compute.py uses unchanged)
SP = {k: v.default for k, v in inspect.signature(B.stampede).parameters.items()}


class Invalidation(VoiceoverScene):
    def construct(self):
        self.card()
        self.race()
        self.ttl()
        self.herd()
        self.leases()
        self.xfetch()

    def card(self):
        card = chapter_card(4, r"Caching: \ staleness and stampedes", r"How does a copy stay honest, \ and survive "
                            r"its own expiry?", lit=(2013, 2015),
                            extra=((2013, r"Nishtala et al.: \ memcache leases"),
                                   (2015, r"Vattani et al.: \ XFetch")), part=PART)
        with self.voiceover("Chapter four. Caching: staleness and stampedes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def race(self):
        head = label(r"The race that keeps a stale value", font_size=36).to_edge(UP, buff=0.3)
        xs = {"A": -6.0, "B": -4.1, "C": -2.2, "D": -0.3}
        names = {"A": (r"reader", DATA), "B": (r"writer", LAM), "C": (r"cache", KERN), "D": (r"database", GREY_A)}
        top, bot = 2.35, -2.45
        lanes = VGroup()
        for k, x in xs.items():
            t, c = names[k]
            lanes.add(VGroup(label(t, font_size=19, color=c).move_to([x, top + 0.3, 0]),
                             DashedLine([x, top, 0], [x, bot, 0], color=GREY_D, stroke_width=1.5)))
        steps = [("A", "C", r"get k: \ miss", DATA), ("A", "D", r"read k: \ v1", DATA),
                 ("B", "D", r"write v2", LAM), ("B", "C", r"delete k", LAM), ("A", "C", r"set k = v1", NO)]
        arrows = VGroup()
        for i, (a, b, t, c) in enumerate(steps):
            y = 1.75 - i * 0.85
            ar = Arrow([xs[a], y, 0], [xs[b], y, 0], buff=0.05, stroke_width=2.5, color=c,
                       max_tip_length_to_length_ratio=0.08)
            arrows.add(VGroup(ar, label(t, font_size=16, color=c).next_to(ar, UP, buff=0.04)))
        cache_end = module_box(r"v1: \ stale", NO, w=1.6, h=0.5, font=17).move_to([xs["C"], -2.85, 0])
        db_end = module_box(r"v2", YES, w=1.2, h=0.5, font=17).move_to([xs["D"], -2.85, 0])
        notes = VGroup(
            wrapped_label(r"on a write: \ update the database, \ then \textbf{delete} the cached copy \ (an update "
                          r"to the cache could arrive out of order)", 5.6, font_size=19, color=WHITE),
            wrapped_label(r"a reader that missed still holds the old value it read \dots", 5.6, font_size=19,
                          color=DATA),
            wrapped_label(r"\dots and its set lands \textit{after} the delete: \ the cache now disagrees with the "
                          r"database, \ and nothing will remove it", 5.6, font_size=19, color=NO),
            wrapped_label(r"nothing but its time to live", 5.6, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.95, 0.2, 0])
        foot = note(r"an illustrative interleaving", font_size=16).to_edge(DOWN, buff=0.2).set_x(3.95)
        with self.voiceover(
            "A line usually credited to Phil Karlton says there are only two hard things in computer science: cache "
            "invalidation, and naming things. <bookmark mark='a'/> The usual rule on a write is: update the "
            "database, then delete the cached copy, rather than updating it, because two updates can reach the "
            "cache in the wrong order. <bookmark mark='b'/> Even deletion has a race. A reader misses, and reads "
            "the old value from the database. <bookmark mark='c'/> Before it stores that value, a writer commits a "
            "new one and deletes the key. <bookmark mark='d'/> Then the reader's set lands. The cache holds the old "
            "value, the database the new one, and nothing is left to remove it, <bookmark mark='e'/> except its time "
            "to live."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lanes), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0][0]), FadeIn(arrows[0][1]))
            self.play(GrowArrow(arrows[1][0]), FadeIn(arrows[1][1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[2][0]), FadeIn(arrows[2][1]))
            self.play(GrowArrow(arrows[3][0]), FadeIn(arrows[3][1]))
            vo.wait_until("d")
            self.play(GrowArrow(arrows[4][0]), FadeIn(arrows[4][1]), FadeIn(notes[2]))
            self.play(FadeIn(cache_end), FadeIn(db_end))
            vo.wait_until("e")
            self.play(FadeIn(notes[3]), Indicate(cache_end, color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    def ttl(self):
        head = label(r"A time to live bounds the damage", font_size=36).to_edge(UP, buff=0.3)
        s = 1.0
        x0, xw, xe, x1 = -4.6, -1.4, 2.2, 6.4          # fill, write, expiry, end (scene units)
        rows = VGroup(label(r"database", font_size=19, color=GREY_A).move_to([-5.8, 1.9, 0]),
                      label(r"cache", font_size=19, color=KERN).move_to([-5.8, 1.1, 0]))
        db = VGroup(timeline_bar(x0, xw, 1.9, DATA, h=0.42, scale=s, label_text=r"v1", size=17),
                    timeline_bar(xw, x1, 1.9, YES, h=0.42, scale=s, label_text=r"v2", size=17))
        ca = VGroup(timeline_bar(x0, xe, 1.1, DATA, h=0.42, scale=s, label_text=r"v1", size=17),
                    timeline_bar(xe, x1, 1.1, YES, h=0.42, scale=s, label_text=r"v2", size=17))
        stale = Rectangle(width=xe - xw, height=1.35, stroke_color=NO, stroke_width=2, fill_color=NO,
                          fill_opacity=0.12).move_to([(xw + xe) / 2, 1.5, 0])
        stale_l = label(r"served stale", font_size=17, color=NO).next_to(stale, UP, buff=0.06)
        ttl_b = BraceBetweenPoints([x0, 0.75, 0], [xe, 0.75, 0], direction=DOWN, color=GREY_B)
        ttl_l = label(r"TTL", font_size=18, color=GREY_B).next_to(ttl_b, DOWN, buff=0.06)
        wr = label(r"write", font_size=16, color=YES).move_to([xw, 2.35, 0])
        ex = label(r"expiry", font_size=16, color=HEAD).move_to([xe, 2.35, 0])
        bound = label(r"staleness $\le$ TTL, \ whatever invalidation misses", font_size=21,
                      color=HEAD).move_to([0.9, -0.35, 0])
        # jitter: twelve keys filled together, with and without a random addition to their TTL
        lab_j = VGroup(label(r"filled together", font_size=18, color=NO),
                       label(r"with jitter", font_size=18, color=YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        lab_j.move_to([-5.2, -1.85, 0])
        base = lab_j.get_right()[0] + 0.4
        same = VGroup(*[Line([base + 4.6, -1.62 - 0.0, 0], [base + 4.6, -2.02, 0], color=NO, stroke_width=3)
                        for _ in range(12)])
        offs = [0.3, 2.1, 1.2, 3.6, 0.8, 2.9, 4.4, 1.7, 3.1, 5.2, 2.5, 4.0]   # illustrative jitter
        spread = VGroup(*[Line([base + 2.4 + o, -2.32, 0], [base + 2.4 + o, -2.72, 0], color=YES, stroke_width=3)
                          for o in offs])
        axis_j = VGroup(*[Line([base, y, 0], [6.6, y, 0], color=GREY_D, stroke_width=1.2) for y in (-2.02, -2.72)])
        herd_l = label(r"all miss at once", font_size=16, color=NO).next_to(same, RIGHT, buff=0.15)
        foot = note(r"illustrative timelines", font_size=16).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "A time to live puts a bound on how wrong a cache can be. <bookmark mark='a'/> The database changes at "
            "the moment of the write. The cached copy carries on serving the old value until it expires. "
            "<bookmark mark='b'/> So with no invalidation at all, a value is stale for at most the TTL, and with "
            "invalidation, the TTL still catches whatever the races let through. <bookmark mark='c'/> One trap. Keys "
            "filled together, "
            "after a restart or a deploy, also expire together, and all miss at once. Adding a small random jitter "
            "to each TTL spreads the expiries out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows), FadeIn(db[0]), FadeIn(ca[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(wr), FadeIn(db[1]))
            self.play(FadeIn(stale), FadeIn(stale_l))
            vo.wait_until("b")
            self.play(GrowFromCenter(ttl_b), FadeIn(ttl_l), FadeIn(ex), FadeIn(ca[1]), FadeIn(bound))
            vo.wait_until("c")
            self.play(FadeIn(lab_j), Create(axis_j), FadeIn(same), FadeIn(herd_l))
            self.play(LaggedStart(*[FadeIn(m) for m in spread], lag_ratio=0.15), run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def herd(self):
        st = load("stampede")["plain"]
        head = label(r"A stampede at expiry", font_size=36).to_edge(UP, buff=0.3)
        rate, ttl, rec, hz = SP["rate"], SP["ttl"], SP["recompute"], SP["horizon"]
        g = axes([0, hz, 60], [0, 250, 50], x_length=8.2, y_length=4.0, x_label=r"seconds",
                 y_label=r"rebuilds started per second", xticks=[0, 60, 120, 180, 240, 300],
                 yticks=[0, 100, 200], font=16)
        g.to_edge(LEFT, buff=0.75).shift(DOWN * 0.35)
        ax = g.ax
        spikes = VGroup()
        for k in range(st["expiries"]):
            te = ttl + k * (ttl + rec)
            r = Rectangle(width=ax.c2p(te + rec, 0)[0] - ax.c2p(te, 0)[0], height=ax.c2p(0, rate)[1] - ax.c2p(0, 0)[1],
                          stroke_width=0, fill_color=NO, fill_opacity=0.9)
            r.move_to(ax.c2p(te + rec / 2, rate / 2))
            spikes.add(r)
        flat = Line(ax.c2p(0, 1), ax.c2p(hz, 1), color=YES, stroke_width=2)
        per = st["recomputations"] / st["expiries"]
        notes = VGroup(
            wrapped_label(rf"one hot key: \ {rate:.0f} requests a second, \ a {ttl:.0f}-second TTL, \ "
                          rf"{rec:.0f} seconds to rebuild", 4.2, font_size=19, color=WHITE),
            wrapped_label(rf"every request that misses during the rebuild starts one too: \ about {per:.0f} per "
                          r"expiry", 4.2, font_size=19, color=NO),
            wrapped_label(rf"in {hz:.0f} seconds: \ {st['expiries']} expiries, \ {st['recomputations']:,} rebuilds; "
                          rf"\ at worst {st['peak_per_second']} in one second, \ all on the database", 4.2,
                          font_size=19, color=NO),
            wrapped_label(r"the thundering herd: \ the cache's own expiry aims its full load at the store it "
                          r"protects", 4.2, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.45).shift(UP * 0.3)
        foot = note(r"simulated \ (blocks.stampede); \ spike shapes drawn at the request rate", font_size=16).to_edge(
            DOWN, buff=0.2)
        with self.voiceover(
            "Expiry has a second danger, for a key that is hot. <bookmark mark='a'/> In our experiment, one key is "
            "requested two hundred times a second, lives for sixty seconds, and takes two seconds to rebuild. "
            "<bookmark mark='b'/> When it expires, every request in those two seconds misses, and each one rebuilds "
            "the same value. <bookmark mark='c'/> Over five minutes, four expiries caused one "
            "thousand six hundred and three rebuilds, at worst two hundred and twenty-three in a single second, all "
            "on the database. <bookmark mark='d'/> This is the thundering herd, or cache stampede: the "
            "cache's own expiry aims the full load at the store it was there to protect."
        ) as vo:
            self.play(FadeIn(head), Create(g), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), Create(flat))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(s_, DOWN) for s_ in spikes], lag_ratio=0.4), FadeIn(notes[1]),
                      run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def leases(self):
        head = label(r"Rebuild once: \ coalescing and leases", font_size=36).to_edge(UP, buff=0.3)

        def panel(title, color, one):
            reqs = VGroup(*[Dot(radius=0.07, color=DATA) for _ in range(7)]).arrange(DOWN, buff=0.22)
            cache = module_box(r"cache: \ miss", KERN, w=1.7, h=0.6, font=17)
            db = module_box(r"database", GREY_A, w=1.6, h=0.6, font=17)
            row = VGroup(reqs, cache, db).arrange(RIGHT, buff=1.0)
            ins = VGroup(*[Arrow(d.get_center(), cache.get_left(), buff=0.1, stroke_width=1.6, color=DATA,
                                 max_tip_length_to_length_ratio=0.1) for d in reqs])
            if one:
                outs = VGroup(Arrow(cache.get_right(), db.get_left(), buff=0.08, stroke_width=3, color=YES))
                extra = label(r"6 wait for it", font_size=16, color=GREY_B).next_to(cache, DOWN, buff=0.15)
            else:
                dy = [UP * (0.24 - 0.08 * i) for i in range(7)]
                outs = VGroup(*[Arrow(cache.get_right() + dy[i], db.get_left() + dy[i], buff=0.08,
                                      stroke_width=1.6, color=NO, max_tip_length_to_length_ratio=0.1)
                                for i in range(7)])
                extra = label(r"7 queries", font_size=16, color=NO).next_to(cache, DOWN, buff=0.15)
            t = label(title, font_size=20, color=color).next_to(row, UP, buff=0.25)
            return VGroup(t, row, ins, outs, extra)
        left = panel(r"without", NO, False)
        right = panel(r"single flight", YES, True)
        panels = VGroup(left, right).arrange(RIGHT, buff=0.9).next_to(head, DOWN, buff=0.45)
        lines = VGroup(
            wrapped_label(r"\textbf{request coalescing}: \ the first miss rebuilds; \ every other request for the key "
                          r"waits for that result", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"\textbf{leases} \ (memcache at Facebook, \ Nishtala et al.\ 2013): \ a miss gets a token, "
                          r"\ at most one per key every 10 seconds; \ others wait briefly and retry", 12.4,
                          font_size=20, color=YES),
            wrapped_label(r"only the token's holder may set the value, \ and a delete voids the token: \ the stale "
                          r"set of the first race is refused", 12.4, font_size=20, color=HEAD),
            wrapped_label(r"reported: \ peak database query rate cut from 17{,}000 to 1{,}300 a second", 12.4,
                          font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(panels, DOWN, buff=0.7)
        with self.voiceover(
            "The first remedy is to rebuild once. <bookmark mark='a'/> Request coalescing, sometimes called single "
            "flight, lets the first miss start the rebuild and makes every other request for that key wait for its "
            "result: one query instead of hundreds. <bookmark mark='b'/> Facebook's memcache, described by Rajesh "
            "Nishtala and colleagues in 2013, does this with leases. On a miss, the cache hands out a token, at most "
            "once every ten seconds for each key, and other clients wait briefly and try again. "
            "<bookmark mark='c'/> Only the holder of the token may set the value, and a delete in the meantime voids "
            "it, which closes the race we began with. <bookmark mark='d'/> They reported that leases cut the peak "
            "rate of database queries from seventeen thousand a second to thirteen hundred."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left[0]), FadeIn(left[1]), FadeIn(right[0]), FadeIn(right[1]))
            self.play(LaggedStart(*[GrowArrow(a) for a in left[2]], lag_ratio=0.1),
                      LaggedStart(*[GrowArrow(a) for a in left[3]], lag_ratio=0.1), FadeIn(left[4]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in right[2]], lag_ratio=0.1), GrowArrow(right[3][0]),
                      FadeIn(right[4]), FadeIn(lines[0]))
            for mk, ln in zip("bcd", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    def xfetch(self):
        st = load("stampede")
        p, e = st["plain"], st["early"]
        head = label(r"Expire early, \ at random", font_size=36).to_edge(UP, buff=0.3)
        rate, rec, beta = SP["rate"], SP["recompute"], SP["beta"]
        lead = beta * rec * math.log(rate * beta * rec)       # where the expected count of early triggers is one
        steps = VGroup(
            MathTex(r"\text{refresh if }\; t - \Delta\beta\ln U \;\ge\; \text{expiry}", font_size=32),
            MathTex(r"-\ln U \sim \text{Exp}(1)", font_size=28, color=DATA),
            MathTex(r"P(\text{a request } r \text{ s before expiry triggers}) = e^{-r/\beta\Delta}", font_size=28,
                    color=DATA),
            MathTex(r"\text{expected triggers by then} = \lambda\beta\Delta\, e^{-r/\beta\Delta} = 1", font_size=28,
                    color=YES),
            MathTex(r"r^\ast = \beta\Delta \ln(\lambda\beta\Delta) \approx " + f"{lead:.0f}" + r"\text{ s}",
                    font_size=30, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        legend = label(rf"$U$ uniform on $(0,1)$; \ $\Delta = {rec:.0f}$ s to rebuild, \ $\beta = {beta:g}$, \ "
                       rf"$\lambda = {rate:.0f}$ requests a second", font_size=18, color=GREY_B)
        left = VGroup(steps, legend).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.4)
        left.shift(UP * 0.75)
        g = axes([0, 20, 5], [0, 4, 1], x_length=5.4, y_length=3.0, x_label=r"seconds to expiry",
                 y_label=r"expected early refreshes", xticks=[0, 5, 10, 15, 20], yticks=[0, 1, 2, 3, 4],
                 fx=lambda v: f"{20 - v:g}", font=16)
        g.to_edge(RIGHT, buff=0.45).align_to(left, UP).shift(DOWN * 0.1)
        g[-1].shift(UP * 0.12)                                  # the y label, clear of the top tick
        ax = g.ax
        # x is time since 20 s before expiry; r = 20 - x seconds remain
        pts = [(x, rate * beta * rec * math.exp(-(20 - x) / (beta * rec))) for x in [0.1 * i for i in range(201)]]
        curve = VMobject(color=YES, stroke_width=3).set_points_as_corners(
            [ax.c2p(x, n) for x, n in pts if n <= 4.0])
        mark = DashedLine(ax.c2p(20 - lead, 0), ax.c2p(20 - lead, 1), color=HEAD, stroke_width=2)
        dot = Dot(ax.c2p(20 - lead, 1), radius=0.07, color=HEAD)
        rows = [[r"rebuilds", f"{p['recomputations']:,}", f"{e['recomputations']}"],
                [r"misses", f"{p['misses']:,}", f"{e['misses']}"],
                [r"most in one second", f"{p['peak_per_second']}", f"{e['peak_per_second']}"]]
        tab = grid_table([r"in 300 s", r"expire at TTL", r"early, \ at random"], rows, widths=[3.0, 2.1, 2.4],
                         row_h=0.42, font_size=19, mono_cols=())
        for i in range(1, 4):
            tab.cells[i][1].set_color(NO)
            tab.cells[i][2].set_color(YES)
        tab.next_to(left, DOWN, buff=0.45).align_to(left, LEFT)
        foot = wrapped_label(r"Vattani, \ Chierichetti and Lowenstein \ (2015), \ ``XFetch''; \ one request refreshes "
                             r"while the rest still hit the old value; \ the price: \ refreshing a little more often",
                             12.4, font_size=18, color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The second remedy avoids the miss altogether: refresh a little before expiry, at random. "
            "<bookmark mark='a'/> In the rule of Andrea Vattani, Flavio Chierichetti and Keegan Lowenstein, each "
            "request draws a uniform random number, and recomputes early if the time now, minus the rebuild time "
            "times beta times the log of that number, has passed the expiry. <bookmark mark='b'/> Minus the log of "
            "a uniform number is exponential, so a request r seconds before expiry triggers with a probability that "
            "rises steeply as expiry nears. <bookmark mark='c'/> With two hundred requests a second, the expected "
            "number of triggers reaches one about twelve seconds before expiry. <bookmark mark='d'/> One request "
            "refreshes while everyone else keeps hitting the old value. In the same experiment: six rebuilds instead "
            "of sixteen hundred, no misses, and never more than one in a second."
        ) as vo:
            self.play(FadeIn(head), Create(g))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(legend))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(FadeIn(steps[3]), Create(curve), run_time=1.5)
            self.play(FadeIn(steps[4]), Create(mark), FadeIn(dot))
            vo.wait_until("d")
            self.play(FadeIn(tab), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, HEAD, YES, LAM)
