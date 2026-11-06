from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.compute import load as load39
from videos.cs.cs42.compute import load as load42
from videos.cs.cs43.compute import load as load43
from videos.cs.cs47.compute import load as load47
from videos.cs.cs48.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, code_block, mono, module_box,
                                   tag_box)


def arrow(a, b, color=GREY_B, buff=0.08, width=2.0):
    return Arrow(a, b, buff=buff, stroke_width=width, color=color, max_tip_length_to_length_ratio=0.15)


class Realtime(VoiceoverScene):
    def construct(self):
        self.card()
        self.transports()
        self.connections()
        self.notifications()
        self.presence()
        self.search()

    def card(self):
        card = chapter_card(13, r"Real-time blocks", r"How does the server speak first?",
                            lit=(2006, 2011), extra=((2006, r"``Comet'': \ long polling named"),
                                                     (2011, r"RFC 6455: \ WebSocket")), part=PART)
        with self.voiceover("Chapter thirteen. Real-time blocks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ polling, long polling, a socket
    def transports(self):
        head = label(r"Polling, \ long polling, \ a socket", font_size=36).to_edge(UP, buff=0.3)
        T, x0, x1 = 60.0, -3.6, 6.4                                       # an illustrative minute

        def X(t):
            return x0 + (x1 - x0) * t / T
        ys = {"ev": 2.25, "poll": 1.35, "long": 0.45, "ws": -0.45}
        names = VGroup(
            label(r"news at the server", font_size=19, color=HEAD).move_to([-5.2, ys["ev"], 0]),
            label(r"poll every 10 s", font_size=19, color=NO).move_to([-5.2, ys["poll"], 0]),
            label(r"long polling", font_size=19, color=DATA).move_to([-5.2, ys["long"], 0]),
            label(r"WebSocket", font_size=19, color=YES).move_to([-5.2, ys["ws"], 0]),
        )
        rails = VGroup(*[Line([X(0), y, 0], [X(T), y, 0], color=GREY_D, stroke_width=1.5) for y in ys.values()])
        ticks = VGroup(*[label(rf"{t} s", font_size=16, color=GREY_B).move_to([X(t), ys["ws"] - 0.45, 0])
                         for t in (0, 20, 40, 60)])
        events = [13.0, 31.0, 34.0, 52.0]
        ev = VGroup(*[Triangle(color=HEAD, fill_opacity=1).scale(0.1).rotate(PI).move_to([X(t), ys["ev"], 0])
                      for t in events])
        # polling: a request every 10 s; news waits for the next poll
        polls = VGroup(*[Line([X(t), ys["poll"] - 0.18, 0], [X(t), ys["poll"] + 0.18, 0], color=GREY_B,
                              stroke_width=2) for t in range(0, 61, 10)])
        waits = VGroup(*[Rectangle(width=X(10 * (int(t // 10) + 1)) - X(t), height=0.2, stroke_width=0,
                                   fill_color=NO, fill_opacity=0.7).move_to(
            [(X(t) + X(10 * (int(t // 10) + 1))) / 2, ys["poll"], 0]) for t in events])
        # long polling: a request held open until there is news, then at once another
        starts = [0.0] + events
        held = VGroup(*[VGroup(Rectangle(width=max(0.03, X(b) - X(a) - 0.12), height=0.2, stroke_width=0,
                                         fill_color=DATA, fill_opacity=0.55).move_to([(X(a) + X(b)) / 2,
                                                                                      ys["long"], 0]),
                               Line([X(a) + 0.03, ys["long"] - 0.18, 0], [X(a) + 0.03, ys["long"] + 0.18, 0],
                                    color=GREY_B, stroke_width=2))
                        for a, b in zip(starts, events + [T])])
        # a socket: one connection, a frame per message
        sock = Rectangle(width=X(T) - X(0), height=0.2, stroke_width=0, fill_color=YES, fill_opacity=0.3).move_to(
            [(X(0) + X(T)) / 2, ys["ws"], 0])
        frames = VGroup(*[Dot([X(t), ys["ws"], 0], radius=0.07, color=YES) for t in events])
        drops = VGroup(*[DashedLine([X(t), ys["ev"] - 0.12, 0], [X(t), ys["ws"], 0], color=HEAD, stroke_width=1.2,
                                    dash_length=0.06) for t in events])
        notes = VGroup(
            wrapped_label(r"polling: \ news waits for the next poll, \ and most answers are empty", 6.0,
                          font_size=19, color=NO),
            wrapped_label(r"long polling: \ the server holds the request until there is news; \ plain HTTP, \ "
                          r"one round trip per message", 6.0, font_size=19, color=DATA),
            wrapped_label(r"WebSocket \ (RFC 6455, \ 2011): \ one HTTP request upgraded to a two-way connection; \ "
                          r"each message a frame with a few bytes of header", 6.0, font_size=19, color=YES),
            wrapped_label(r"Server-Sent Events: \ a one-way stream of messages over an ordinary HTTP response", 6.0,
                          font_size=19, color=LAM),
        )
        notes.arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.25), col_alignments="ll").move_to([0, -2.45, 0])
        foot = note(r"illustrative", font_size=16).to_corner(DR, buff=0.12)
        with self.voiceover(
            "Most of the web is a client asking and a server answering; real-time features need the server to speak "
            "first. <bookmark mark='a'/> The simplest trick is polling: ask every ten seconds. News waits for the "
            "next poll, and most answers are empty. <bookmark mark='b'/> Long polling, named Comet in 2006, sends a "
            "request the server holds until there is news, then asks again at once: plain HTTP, one round trip per "
            "message. <bookmark mark='c'/> A WebSocket, standardised in RFC 6455 in 2011, starts as an HTTP request "
            "and is upgraded into a two-way connection that stays open; each message is a frame with a few bytes of "
            "header. <bookmark mark='d'/> For one-way streams, Server-Sent Events keep one HTTP response open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names), Create(rails), FadeIn(ticks), FadeIn(foot))
            self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.1) for e in ev], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Create(polls), Create(drops))
            self.play(LaggedStart(*[GrowFromEdge(w, LEFT) for w in waits], lag_ratio=0.3), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(h, shift=RIGHT * 0.1) for h in held], lag_ratio=0.3), FadeIn(notes[1]),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(GrowFromEdge(sock, LEFT), FadeIn(frames), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ connection servers
    def connections(self):
        st = load43("storm")
        imm, bo = st["immediate"], st["backoff"]
        cap = 100
        head = label(r"Connections are state", font_size=36).to_edge(UP, buff=0.3)
        reg = module_box(r"registry: \ user $\to$ server", KERN, w=3.2, h=0.6, font=18).move_to([-3.4, 2.15, 0])
        servers = VGroup(*[module_box(rf"connections {i + 1}", DATA, w=1.85, h=0.6, font=17) for i in range(3)])
        servers.arrange(RIGHT, buff=0.35).move_to([-3.4, 0.75, 0])
        links = VGroup(*[Line(reg.get_bottom(), s.get_top(), color=GREY_C, stroke_width=1.5) for s in servers])
        rng = np.random.default_rng(7)
        clusters = []
        for s in servers:
            pts = VGroup(*[Dot(s.get_bottom() + np.array([rng.uniform(-0.8, 0.8), -0.45 - rng.uniform(0, 0.9), 0]),
                               radius=0.05, color=GREY_A) for _ in range(12)])
            clusters.append(pts)
        cl_lines = VGroup(*[Line(d.get_center(), s.get_bottom(), color=GREY_D, stroke_width=0.8)
                            for s, pts in zip(servers, clusters) for d in pts])
        cross = Cross(servers[2], stroke_color=NO, stroke_width=4, scale_factor=0.7)
        # the right: Part 43's ten-second outage, peak offered load
        base_y, hmax, vmax = -2.25, 3.6, 1000.0
        bars, vals, nms = VGroup(), VGroup(), VGroup()
        for k, (r, c, nm) in enumerate(((imm, NO, r"all at once"), (bo, YES, r"backoff with jitter"))):
            h = hmax * r["peak_offered"] / vmax
            b = Rectangle(width=0.9, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(
                [2.6 + 2.1 * k, base_y + h / 2, 0])
            bars.add(b)
            vals.add(label(rf"peak {r['peak_offered']}/s; \ below capacity at {r['recovered_at']} s", font_size=17,
                           color=c).next_to(b, UP, buff=0.1))
            nms.add(label(nm, font_size=17, color=GREY_A).next_to(b, DOWN, buff=0.12))
        axis = Line([1.6, base_y, 0], [6.6, base_y, 0], color=GREY_C, stroke_width=1.5)
        capl = DashedLine([1.6, base_y + hmax * cap / vmax, 0], [6.6, base_y + hmax * cap / vmax, 0], color=HEAD,
                          stroke_width=2)
        capt = label(rf"capacity {cap}/s", font_size=16, color=HEAD).next_to(capl, UP, buff=0.05).align_to(
            capl, RIGHT)
        ttl = wrapped_label(r"Part 43: \ a service down for ten seconds, \ its clients retrying", 4.8,
                            font_size=18, color=WHITE).move_to([4.1, 2.3, 0])
        notes = VGroup(
            wrapped_label(r"each server holds thousands of open sockets: \ to reach a user, \ look up their server, "
                          r"\ then forward", 6.0, font_size=19, color=WHITE),
            wrapped_label(r"a server dies: \ all its clients reconnect at once, \ to the others", 6.0, font_size=19,
                          color=NO),
            wrapped_label(r"reconnect with jittered backoff; \ drain a server before stopping it", 6.0, font_size=19,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.2, -2.55, 0])
        with self.voiceover(
            "Open connections are state. <bookmark mark='a'/> Connection servers each hold many thousands of sockets."
            " To reach a user, look up their server in a registry, and forward the message there. <bookmark "
            "mark='b'/> When a server dies, all its clients reconnect at once, to the others. <bookmark mark='c'/> "
            "Part 43 measured that shape: a service down for ten seconds, with clients retrying every second, was "
            "offered nine hundred and ninety requests a second against a capacity of a hundred, and recovered only at"
            " second a hundred and nineteen. With exponential backoff and jitter, the peak was three hundred and "
            "eighty-one, and recovery came at sixty-nine. <bookmark mark='d'/> So clients reconnect with jitter, and "
            "servers are drained before they stop."
        ) as vo:
            self.play(FadeIn(head), FadeIn(reg), FadeIn(servers), Create(links))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in clusters], Create(cl_lines), FadeIn(notes[0]))
            vo.wait_until("b")
            moved = clusters[2]
            self.play(Create(cross), FadeOut(VGroup(*cl_lines[24:])), moved.animate.set_color(NO))
            self.play(*[d.animate.move_to(servers[k % 2].get_bottom() + np.array([rng.uniform(-0.8, 0.8),
                                                                                    -0.45 - rng.uniform(0, 0.9), 0]))
                        for k, d in enumerate(moved)], FadeIn(notes[1]), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(ttl), Create(axis), Create(capl), FadeIn(capt))
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(vals[0]), FadeIn(nms[0]))
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(vals[1]), FadeIn(nms[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ notifications
    def notifications(self):
        r = load42("radio")
        head = label(r"Notifications", font_size=36).to_edge(UP, buff=0.3)
        y = 1.55
        ev = module_box(r"an event", DATA, w=1.5, h=0.6, font=18).move_to([-5.9, y, 0])
        svc = module_box(r"notification service", KERN, w=2.8, h=0.6, font=18).move_to([-3.2, y, 0])
        q = module_box(r"queue", GREY_B, w=1.3, h=0.6, font=18).move_to([-0.85, y, 0])
        chans = VGroup(*[module_box(t, LAM, w=1.5, h=0.5, font=17) for t in (r"push", r"email", r"SMS")]).arrange(
            DOWN, buff=0.18).move_to([1.3, y, 0])
        plat = module_box(r"APNs, \ FCM", YES, w=1.7, h=0.6, font=18).move_to([3.75, chans[0].get_y(), 0])
        phone = RoundedRectangle(width=0.5, height=0.85, corner_radius=0.08, stroke_color=GREY_A,
                                 stroke_width=2).move_to([5.9, chans[0].get_y(), 0])
        arrows = VGroup(arrow(ev.get_right(), svc.get_left()), arrow(svc.get_right(), q.get_left()),
                        *[arrow(q.get_right(), c.get_left(), buff=0.05) for c in chans],
                        arrow(chans[0].get_right(), plat.get_left()), arrow(plat.get_right(), phone.get_left()))
        checks = VGroup(*[tag_box(t, KERN, size=15) for t in ("preferences", "rate limit", "idempotency key")])
        checks.arrange(DOWN, buff=0.1).next_to(svc, DOWN, buff=0.2)
        conn = label(r"one connection per phone, \ kept by the operating system", font_size=17,
                     color=YES).next_to(VGroup(plat, phone), UP, buff=0.18)
        # Part 42's radio: ten requests spread out against batched
        scale = 6.2 / r["spread_J"]
        e1 = Rectangle(width=scale * r["spread_J"], height=0.36, stroke_width=0, fill_color=NO, fill_opacity=0.85)
        e2 = Rectangle(width=scale * r["batched_J"], height=0.36, stroke_width=0, fill_color=YES, fill_opacity=0.85)
        VGroup(e1, e2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-0.8, -1.6, 0], aligned_edge=LEFT)
        e1l = label(r"ten requests, \ 20 s apart", font_size=18, color=NO).next_to(e1, LEFT, buff=0.2)
        e2l = label(r"the same ten, \ together", font_size=18, color=YES).next_to(e2, LEFT, buff=0.2)
        e1v = label(rf"{r['spread_J']:.0f} J", font_size=18, color=NO).next_to(e1, RIGHT, buff=0.12)
        e2v = label(rf"{r['batched_J']:.1f} J: \ {r['ratio']:.1f}$\times$ less", font_size=18, color=YES).next_to(
            e2, RIGHT, buff=0.12)
        el = label(rf"Part 42: \ a phone's radio stays awake about {r['params']['tail_s']:.1f} s after each burst \ "
                   r"(Huang et al., \ 2012)",
                   font_size=18, color=GREY_A).next_to(VGroup(e1l, e2), UP, buff=0.25).align_to(e1l, LEFT)
        nt = wrapped_label(r"delivery is at least once: \ the idempotency key \ (Part 43) \ lets the phone drop "
                           r"a repeat", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Notifications reach people who are not looking. <bookmark mark='a'/> An event enters a notification "
            "service, which checks the user's preferences, applies chapter five's rate limits, and stamps an "
            "idempotency key. A queue feeds a worker per channel: push, email, text. <bookmark mark='b'/> Push goes "
            "through Apple's or Google's service, because a phone keeps one connection for all its apps. <bookmark "
            "mark='c'/> Apps that poll on their own keep waking the radio. In Part 42's model, ten requests twenty "
            "seconds apart cost about a hundred and thirty joules; the same ten together, sixteen and a half, nearly "
            "eight times less. <bookmark mark='d'/> Delivery is at least once, so the idempotency key lets the phone "
            "drop a repeat."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ev))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), FadeIn(svc))
            self.play(LaggedStart(*[FadeIn(c) for c in checks], lag_ratio=0.3))
            self.play(GrowArrow(arrows[1]), FadeIn(q), *[GrowArrow(a) for a in arrows[2:5]], FadeIn(chans))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[5]), FadeIn(plat), GrowArrow(arrows[6]), FadeIn(phone), FadeIn(conn))
            vo.wait_until("c")
            self.play(FadeIn(el), FadeIn(e1l), FadeIn(e2l))
            self.play(GrowFromEdge(e1, LEFT), FadeIn(e1v))
            self.play(GrowFromEdge(e2, LEFT), FadeIn(e2v))
            vo.wait_until("d")
            self.play(FadeIn(nt), Circumscribe(checks[2], color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ presence
    def presence(self):
        d = load39("detect")
        fx, ac = d["fixed"], d["accrual"]
        head = label(r"Presence: \ who is online?", font_size=36).to_edge(UP, buff=0.3)
        x0, step, yb = -6.3, 0.42, 1.75
        beats = VGroup(*[Line([x0 + k * step, yb - 0.18, 0], [x0 + k * step, yb + 0.18, 0], color=YES,
                              stroke_width=3) for k in range(7)])
        rail = Line([x0, yb, 0], [-0.6, yb, 0], color=GREY_D, stroke_width=1.5)
        crash = x0 + 6.5 * step
        cx = Cross(Dot([crash, yb, 0]), stroke_color=NO, stroke_width=4, scale_factor=1.6)
        tout = x0 + 6 * step + 2.6 * step * 1.5
        brace = BraceBetweenPoints([x0 + 6 * step, yb - 0.3, 0], [tout, yb - 0.3, 0], DOWN, color=HEAD)
        bl = label(r"timeout", font_size=17, color=HEAD).next_to(brace, DOWN, buff=0.08)
        off = label(r"offline", font_size=18, color=NO).next_to(Dot([tout, yb, 0]), UP, buff=0.2)
        tick_off = Line([tout, yb - 0.25, 0], [tout, yb + 0.25, 0], color=NO, stroke_width=3)
        hl = label(r"heartbeats", font_size=17, color=YES).next_to(beats, UP, buff=0.12).align_to(beats, LEFT)
        store = code_block(["SET presence:ada  conn-2  EX 30", "# refreshed by every heartbeat"], size=16)
        store.move_to([-3.5, 0.0, 0]).align_to(rail, LEFT)
        lg = math.log10
        g = axes([1.7, 3.7, 2.0], [0, 1250, 250], x_length=5.0, y_length=3.6,
                 x_label=r"time to notice a crash, \ ms \ (log scale)", y_label=r"false alarms per hour",
                 xticks=[2, 3, lg(3000)], yticks=[0, 500, 1000], fx=lambda v: f"{10 ** v:,.0f}", font=16)
        g.move_to([3.6, -0.2, 0])
        ax = g.ax
        pf = VGroup(*[Dot(ax.c2p(lg(r["detect_ms"]), r["false_per_hour"]), radius=0.06, color=DATA) for r in fx])
        lf = VMobject(stroke_color=DATA, stroke_width=2.5).set_points_as_corners(
            [ax.c2p(lg(r["detect_ms"]), r["false_per_hour"]) for r in fx])
        pa = VGroup(*[Dot(ax.c2p(lg(r["detect_ms"]), r["false_per_hour"]), radius=0.06, color=LAM) for r in ac])
        la = VMobject(stroke_color=LAM, stroke_width=2.5).set_points_as_corners(
            [ax.c2p(lg(r["detect_ms"]), r["false_per_hour"]) for r in ac])
        leg = VGroup(label(r"fixed timeouts", font_size=17, color=DATA),
                     label(r"$\phi$ accrual", font_size=17, color=LAM)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        leg.next_to(ax.c2p(2.6, 1100), RIGHT, buff=0.1)
        notes = VGroup(
            wrapped_label(r"a user is online while their heartbeats arrive: \ a key that expires unless renewed", 5.8,
                          font_size=19, color=WHITE),
            wrapped_label(rf"Part 39's detector, \ heartbeats every {d['interval_ms']:.0f} ms: \ notice a crash "
                          r"sooner and you suspect the living more often", 5.8, font_size=19, color=HEAD),
            wrapped_label(r"each change is news for every friend: \ fan-out \ (Part 49); \ many apps fetch "
                          r"presence only for the people on screen", 5.8, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(store, DOWN, buff=0.35).align_to(rail, LEFT)
        foot = note(r"the heartbeat timeline and key are illustrative", font_size=16).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Presence, the green dot beside a name, is a failure detector. <bookmark mark='a'/> Each heartbeat renews"
            " a key that otherwise expires; when the heartbeats stop, the key expires, and the user is offline. "
            "<bookmark mark='b'/> The timeout is Part 39's trade-off. With heartbeats every tenth of a second, "
            "delayed at random, a timeout that notices a crash in about a hundred milliseconds raises hundreds of "
            "false alarms an hour; one that raises none takes three seconds. Phi accrual adapts to the delays it has "
            "seen. <bookmark mark='c'/> And every change is news for every friend, a fan-out like Part 49's feeds, so"
            " many apps fetch presence only for the people on screen."
        ) as vo:
            self.play(FadeIn(head), Create(rail), FadeIn(foot))
            self.play(LaggedStart(*[FadeIn(b) for b in beats], lag_ratio=0.2), FadeIn(hl), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(store), FadeIn(notes[0]))
            self.play(Create(cx))
            self.play(GrowFromCenter(brace), FadeIn(bl), Create(tick_off), FadeIn(off))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(notes[1]))
            self.play(Create(lf), LaggedStart(*[FadeIn(p) for p in pf], lag_ratio=0.1), FadeIn(leg[0]), run_time=2.0)
            self.play(Create(la), LaggedStart(*[FadeIn(p) for p in pa], lag_ratio=0.1), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ search as a block
    def search(self):
        comp = load47("spell")["complete"]
        head = label(r"Search as a block", font_size=36).to_edge(UP, buff=0.3)
        box = RoundedRectangle(width=3.6, height=0.6, corner_radius=0.1, stroke_color=GREY_A,
                               stroke_width=2).move_to([-4.5, 2.0, 0])
        typed = ["e", "el", "eli", "eliz"]
        texts = [mono(t, size=22, color=WHITE).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.2) for t in typed]
        sugg = VGroup(*[mono(w, size=19, color=YES) for w in comp["eliz"]]).arrange(DOWN, buff=0.14,
                                                                                    aligned_edge=LEFT)
        drop = SurroundingRectangle(sugg, buff=0.15, color=GREY_C, stroke_width=1.2, corner_radius=0.06)
        VGroup(drop, sugg).next_to(box, DOWN, buff=0.1).align_to(box, LEFT)
        sl = wrapped_label(r"the five commonest words beginning \texttt{eliz} in the thirty novels \ (Part 47)",
                           3.6, font_size=17, color=GREY_A).next_to(drop, DOWN, buff=0.15).align_to(box, LEFT)
        db = module_box(r"database", LAM, w=1.8, h=0.6, font=18).move_to([0.6, 2.0, 0])
        log = module_box(r"change log", GREY_B, w=1.9, h=0.6, font=18).move_to([3.1, 2.0, 0])
        idxr = module_box(r"indexer", KERN, w=1.5, h=0.6, font=18).move_to([5.5, 2.0, 0])
        index = module_box(r"search index", YES, w=2.2, h=0.6, font=18).move_to([5.3, 0.3, 0])
        app = module_box(r"application", DATA, w=2.0, h=0.6, font=18).move_to([0.6, 0.3, 0])
        flow = VGroup(arrow(db.get_right(), log.get_left()), arrow(log.get_right(), idxr.get_left()),
                      arrow(idxr.get_bottom(), index.get_top() + RIGHT * 0.2))
        ask = arrow(app.get_right() + UP * 0.1, index.get_left() + UP * 0.1, color=DATA)
        ids = arrow(index.get_left() + DOWN * 0.1, app.get_right() + DOWN * 0.1, color=YES)
        fetch = arrow(app.get_top(), db.get_bottom(), color=LAM)
        al = label(r"query $\to$ ids", font_size=16, color=DATA).next_to(ask, UP, buff=0.06)
        fl = label(r"records by id", font_size=16, color=LAM).next_to(fetch, LEFT, buff=0.08)
        tl = label(r"Part 46", font_size=16, color=GREY_B).next_to(log, UP, buff=0.08)
        notes = VGroup(
            wrapped_label(r"the database stays the truth; \ the index is a view of it, \ fed by its change log", 6.2,
                          font_size=19, color=WHITE),
            wrapped_label(r"so search is eventually consistent: \ a new item appears after the pipeline's lag; \ "
                          r"read your own writes from the database", 6.2, font_size=19, color=NO),
            wrapped_label(r"type-ahead sends a query per keystroke: \ wait for a pause, \ and cache popular "
                          r"prefixes \ (chapter 3)", 6.2, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.5, -1.85, 0])
        with self.voiceover(
            "The last block is Part 47's search. <bookmark mark='a'/> The database stays the truth. Its change log, "
            "from Part 46, feeds an indexer that keeps a search index current. The application sends the query to the"
            " index, gets back ids, and fetches the records from the database. <bookmark mark='b'/> So search is "
            "eventually consistent: a new item appears after the pipeline's lag, and a user who has just written "
            "something should read it from the database. <bookmark mark='c'/> Type-ahead searches at every keystroke:"
            " typing e l i z returns the five commonest such words in our thirty novels, Elizabeth first. Wait for a "
            "pause in the typing, and cache popular prefixes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(box), FadeIn(db), FadeIn(app))
            vo.wait_until("a")
            self.play(GrowArrow(flow[0]), FadeIn(log), FadeIn(tl))
            self.play(GrowArrow(flow[1]), FadeIn(idxr), GrowArrow(flow[2]), FadeIn(index))
            self.play(GrowArrow(ask), FadeIn(al), FadeIn(notes[0]))
            self.play(GrowArrow(ids), GrowArrow(fetch), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), Indicate(flow[1], color=NO))
            vo.wait_until("c")
            cur = texts[0]
            self.play(FadeIn(cur), run_time=0.4)
            for t in texts[1:]:
                self.play(ReplacementTransform(cur, t), run_time=0.4)
                cur = t
            self.play(FadeIn(drop), LaggedStart(*[FadeIn(s, shift=DOWN * 0.08) for s in sugg], lag_ratio=0.2),
                      FadeIn(sl), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, HEAD)
