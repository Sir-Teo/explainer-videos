from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load

FALLACIES = [r"the network is reliable", r"latency is zero", r"bandwidth is infinite", r"the network is secure",
             r"topology doesn't change", r"there is one administrator", r"transport cost is zero",
             r"the network is homogeneous"]


class Hook(VoiceoverScene):
    def construct(self):
        self.fallacies()
        self.outages()
        self.job()
        self.plan()

    def fallacies(self):
        head = label(r"Eight things that are not true", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(*[label(rf"{i + 1}. \ {t}", font_size=26, color=WHITE) for i, t in enumerate(FALLACIES)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(head, DOWN, buff=0.45).shift(LEFT * 2.2)
        strikes = VGroup(*[Line(r.get_left() + LEFT * 0.05, r.get_right() + RIGHT * 0.05, color=NO, stroke_width=3)
                           for r in rows])
        who = wrapped_label(r"the fallacies of distributed computing: \ Bill Joy and Tom Lyon's first four, \ Peter "
                            r"Deutsch's seven \ (1994), \ James Gosling's eighth", 4.2, font_size=19, color=GREY_B)
        who.next_to(rows, RIGHT, buff=0.8)
        with self.voiceover(
            "In the nineties, engineers at Sun Microsystems wrote down the assumptions that programmers new to "
            "networks tend to make, and that are false. <bookmark mark='a'/> The network is reliable. Latency is "
            "zero. Bandwidth is infinite. The network is secure. Topology doesn't change. There is one "
            "administrator. Transport cost is zero. The network is homogeneous. <bookmark mark='b'/> Peter Deutsch "
            "set down seven of them in 1994, building on an earlier list by Bill Joy and Tom Lyon, and James "
            "Gosling added the eighth. Every one of them is tempting, because a "
            "remote call looks exactly like a local one. <bookmark mark='c'/> And every one of them has taken down "
            "real systems."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.35), run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(who))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(s) for s in strikes], lag_ratio=0.15), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def outages(self):
        head = label(r"Three outages", font_size=36).to_edge(UP, buff=0.3)
        cards = [
            (r"GitHub, \ October 2018", r"a 43-second loss of connectivity between data centres; \ databases "
             r"failed over across the country, \ and the site ran degraded for about a day", r"1. \ reliable", NO),
            (r"Dyn, \ October 2016", r"a botnet of hacked cameras and routers \ (Mirai) \ flooded a DNS provider; "
             r"\ many large sites were unreachable for hours", r"4. \ secure", KERN),
            (r"Facebook, \ October 2021", r"a routine command withdrew the backbone's routes; \ its DNS servers "
             r"took themselves offline, \ and the tools to fix it were behind the same network", r"5. \ topology",
             LAM),
        ]
        tiles = VGroup()
        for title, body, fal, col in cards:
            frame = RoundedRectangle(width=4.2, height=3.6, corner_radius=0.15, stroke_color=col, stroke_width=2,
                                     fill_color=BG, fill_opacity=1)
            t = label(title, font_size=22, color=col)
            b = wrapped_label(body, 3.8, font_size=18, color=GREY_A)
            f = label(rf"fallacy {fal}", font_size=18, color=HEAD)
            VGroup(t, b, f).arrange(DOWN, buff=0.25).move_to(frame)
            tiles.add(VGroup(frame, t, b, f))
        tiles.arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.5)
        foot = wrapped_label(r"post-incident reports: \ GitHub \ (2018), \ Dyn \ (2016), \ Facebook engineering "
                             r"\ (2021)", 12.4, font_size=17, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Three examples. <bookmark mark='a'/> In October 2018, GitHub lost connectivity between two data "
            "centres for forty-three seconds. Its databases failed over across the country, writes landed on both "
            "sides, and the site ran degraded for about a day while engineers reconciled them. The network is not "
            "reliable. <bookmark mark='b'/> In October 2016, a botnet of hacked cameras and home routers, called "
            "Mirai, flooded the DNS provider Dyn, and many of the largest sites on the web were unreachable for "
            "hours. The network is not secure. <bookmark mark='c'/> And in October 2021, a routine command "
            "withdrew the routes of Facebook's backbone. Its DNS servers, seeing no backbone, took themselves "
            "offline, and the tools engineers needed to fix it were behind the same network. Topology changes, "
            "sometimes all at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()

    def job(self):
        j = load("job")
        w, wo = j["with_keys"], j["without"]
        head = label(r"The Job, \ in three services", font_size=36).to_edge(UP, buff=0.3)
        names = [(r"tokenize", DATA), (r"count", HEAD), (r"rank", YES)]
        boxes = VGroup()
        for t, c in names:
            r = RoundedRectangle(width=2.4, height=0.9, corner_radius=0.12, stroke_color=c, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            boxes.add(VGroup(r, label(t, font_size=24, color=c).move_to(r)))
        boxes.arrange(RIGHT, buff=1.6).next_to(head, DOWN, buff=0.5)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.1, color=GREY_B,
                                stroke_width=2) for i in range(2)])
        net = label(rf"{w['chunks']} messages of counts; \ the network loses 5\% and duplicates 2\%",
                    font_size=19, color=GREY_B).next_to(boxes, DOWN, buff=0.3)
        rows = []
        for (a, b1), (_, b2) in zip(wo["top"][:5], wo["true_top"][:5]):
            rows.append([rf"\texttt{{{a}}}", f"{b2:,}", f"{b1:,}", f"{dict(w['top'])[a]:,}"])
        tab = grid_table([r"word", r"true count", r"retries, \ no keys", r"retries + keys"], rows,
                         widths=[2.0, 2.4, 2.8, 2.8], row_h=0.42, font_size=19, mono_cols=())
        tab.next_to(net, DOWN, buff=0.4)
        for r in range(1, len(rows) + 1):
            tab.cells[r][2].set_color(NO)
            tab.cells[r][3].set_color(YES)
        summ = label(rf"without keys: \ {wo['wrong_counts']:,} of {wo['distinct']:,} words miscounted, \ "
                     rf"{wo['overcount']:,} extra; \ with keys: \ {w['wrong_counts']}", font_size=20,
                     color=WHITE).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Here is this part's experiment. <bookmark mark='a'/> We split the Job into three services: one "
            "tokenizes text, one counts words, one ranks them. The tokenizer sends its counts to the counter in "
            f"{w['chunks']} messages, over a network that loses five percent of messages and duplicates two. "
            "<bookmark mark='b'/> To survive loss, the tokenizer retries until the counter acknowledges. But a "
            "retried message may have arrived after all, and a duplicated one arrives twice. "
            "<bookmark mark='c'/> Without protection, the counts drift upward: the word the is counted "
            f"{dict(wo['top'])['the']:,} times instead of {dict(wo['true_top'])['the']:,}, and "
            f"{wo['wrong_counts']:,} of the {wo['distinct']:,} distinct words are wrong. <bookmark mark='d'/> Add "
            "one idea, an idempotency key on each message, and every count is exact. Most of this part is about "
            "ideas of that size, and the mathematics that says they work."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3), Create(arrows), FadeIn(net))
            vo.wait_until("b")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*[tab.cells[r][c] for r in range(len(rows) + 1)
                                                        for c in (0, 1)])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[0][2:3], *[tab.cells[r][2] for r in range(1, len(rows) + 1)])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(tab.cells[0][3], *[tab.cells[r][3] for r in range(1, len(rows) + 1)])),
                      FadeIn(summ))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ APIs and Services", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"why a remote call is not a local one",
            r"Protocol Buffers' bytes, \ derived; \ schemas that evolve",
            r"REST, \ gRPC, \ GraphQL, \ and pagination that does not lie",
            r"exactly once $=$ at least once $+$ deduplication",
            r"queues, \ backpressure and retry storms",
            r"outboxes, \ sagas, \ meshes, \ tokens and clocks",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 43 of Computer Science, Built, the fourth part of Act Eight. <bookmark mark='a'/> We will "
            "see why a remote call can never be made to look exactly like a local one; derive the bytes Protocol "
            "Buffers puts on the wire and the rules for changing a schema safely; compare the styles of API; prove "
            "that exactly-once delivery is at-least-once delivery plus deduplication; and watch queues, retries, "
            "outboxes and sagas keep a system of services correct while its network misbehaves."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (DATA, KERN, LAM, YES)
