from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, mono, module_box,
                                   tag_box)


class Rpc(VoiceoverScene):
    def construct(self):
        self.card()
        self.stubs()
        self.latency()
        self.memory()
        self.partial()
        self.generals()
        self.idl()

    def card(self):
        card = chapter_card(1, r"Calls across a network", r"Can a remote call be made to look local?",
                            lit=(1984, 1994), extra=((1984, r"Birrell \& Nelson: \ RPC"),
                                                     (1994, r"Waldo et al.: \ a note")), part=PART)
        with self.voiceover("Chapter one. Calls across a network."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def stubs(self):
        head = label(r"Remote procedure call", font_size=36).to_edge(UP, buff=0.3)
        ys = (2.0, 0.5, -1.0)
        cl = VGroup(*[module_box(n, c, w=2.6, h=0.62).move_to([-4.6, y, 0]) for n, c, y in
                      zip((r"caller", r"client stub", r"RPC runtime"), (DATA, HEAD, KERN), ys)])
        sv = VGroup(*[module_box(n, c, w=2.6, h=0.62).move_to([4.6, y, 0]) for n, c, y in
                      zip((r"procedure", r"server stub", r"RPC runtime"), (YES, HEAD, KERN), ys)])
        mach = VGroup(label(r"client machine", font_size=18, color=GREY_B).next_to(cl, UP, buff=0.18),
                      label(r"server machine", font_size=18, color=GREY_B).next_to(sv, UP, buff=0.18))
        links = VGroup(*[Line(g[i].get_bottom(), g[i + 1].get_top(), color=GREY_C, stroke_width=2)
                         for g in (cl, sv) for i in range(2)])
        net = DashedLine(cl[2].get_right(), sv[2].get_left(), color=GREY_B, stroke_width=2)
        netl = label(r"the network", font_size=18, color=GREY_B).next_to(net, DOWN, buff=0.12)
        steps = VGroup(
            label(r"marshal", font_size=19, color=HEAD).next_to(links[0], RIGHT, buff=0.25),
            label(r"send", font_size=19, color=KERN).next_to(links[1], RIGHT, buff=0.25),
            label(r"unmarshal", font_size=19, color=HEAD).next_to(links[3], LEFT, buff=0.25),
            label(r"dispatch", font_size=19, color=YES).next_to(links[2], LEFT, buff=0.25),
        )
        notes = VGroup(
            wrapped_label(r"Birrell and Nelson, \ Xerox PARC \ (1984): \ the stubs have the procedure's name and "
                          r"signature, \ so the caller writes an ordinary call; \ a program, \ Lupine, \ generated "
                          r"them from the interface", 12.4, font_size=20, color=WHITE),
            note(r"illustrative call; \ the bytes are Protocol Buffers' encoding, \ derived in the next chapter",
                 font_size=17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)

        def tok(t, c):
            return tag_box(t, color=c, size=17)
        call = tok(r"add(2, 3)", DATA).move_to(cl[0])
        with self.voiceover(
            "In 1984 Andrew Birrell and Bruce Nelson, at Xerox PARC, described how to make a call to a procedure"
            " on another machine look like an ordinary call. <bookmark mark='a'/> The caller calls a local "
            "procedure, the client stub, with the same name and arguments. <bookmark mark='b'/> The stub "
            "marshals the arguments into bytes, and the runtime sends them across the network. <bookmark "
            "mark='c'/> On the server, a matching stub unmarshals the bytes and dispatches to the real "
            "procedure. <bookmark mark='d'/> The result travels back the same way, and the caller just sees a "
            "return value. A program called Lupine wrote the stubs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cl), FadeIn(sv), FadeIn(mach), Create(links), Create(net), FadeIn(netl))
            vo.wait_until("a")
            self.play(FadeIn(call, scale=0.8))
            self.play(call.animate.move_to(cl[1]), FadeIn(steps[0]))
            vo.wait_until("b")
            wire = tok(r"08 02 10 03", KERN).move_to(cl[1])
            self.play(ReplacementTransform(call, wire))
            self.play(wire.animate.move_to(cl[2]), FadeIn(steps[1]))
            self.play(wire.animate.move_to(sv[2]), run_time=1.6)
            vo.wait_until("c")
            self.play(wire.animate.move_to(sv[1]), FadeIn(steps[2]))
            back = tok(r"add(2, 3)", DATA).move_to(sv[1])
            self.play(ReplacementTransform(wire, back))
            self.play(back.animate.move_to(sv[0]), FadeIn(steps[3]))
            vo.wait_until("d")
            res = tok(r"5", YES).move_to(sv[0])
            self.play(ReplacementTransform(back, res))
            for target in (sv[1], sv[2], cl[2], cl[1], cl[0]):
                self.play(res.animate.move_to(target), run_time=0.45 if target is not cl[2] else 1.0)
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    def latency(self):
        f = load("fanout")["single"]
        p50, p99 = f["p50"], f["p99"]
        head = label(r"Remote is not local: \ latency", font_size=36).to_edge(UP, buff=0.3)
        x0, w = -5.6, 11.2                    # 1 ns ... 1 s on a log axis
        def xs(sec):
            return x0 + (math.log10(sec) + 9) / 9 * w
        axis = Line([x0, 0.6, 0], [x0 + w, 0.6, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup()
        for e in range(-9, 1):
            x = xs(10.0 ** e)
            ticks.add(Line([x, 0.5, 0], [x, 0.7, 0], color=GREY_C, stroke_width=2 if e % 3 == 0 else 1))
        names = VGroup(*[label(t, font_size=19, color=GREY_A).move_to([xs(10.0 ** e), 0.2, 0]) for t, e in
                         ((r"1 ns", -9), (r"1 $\mu$s", -6), (r"1 ms", -3), (r"1 s", 0))])
        local = Rectangle(width=xs(1e-8) - xs(1e-9), height=0.36, stroke_width=0, fill_color=YES,
                          fill_opacity=0.8).move_to([(xs(1e-9) + xs(1e-8)) / 2, 0.6, 0])
        ll = wrapped_label(r"a local call: \ nanoseconds", 3.0, font_size=20, color=YES).next_to(
            local, UP, buff=0.3).align_to(local, LEFT)
        d50 = Dot([xs(p50 / 1000), 0.6, 0], radius=0.11, color=NO)
        d99 = Dot([xs(p99 / 1000), 0.6, 0], radius=0.09, color=KERN)
        rl = VGroup(label(rf"remote call, \ median {p50:.0f} ms", font_size=20, color=NO),
                    label(rf"99th percentile {p99:.0f} ms", font_size=19, color=KERN)).arrange(
            DOWN, aligned_edge=RIGHT, buff=0.12).next_to(d50, UP, buff=0.3).align_to(d99, RIGHT)
        lo, hi = p50 / 1000 / 1e-8, p50 / 1000 / 1e-9
        gap = DoubleArrow([xs(1e-8), -0.4, 0], [xs(p50 / 1000), -0.4, 0], color=HEAD, buff=0, stroke_width=3,
                          tip_length=0.2)
        gl = label(rf"$10^{{{round(math.log10(lo))}}}$ to $10^{{{round(math.log10(hi))}}}$ times longer", font_size=22,
                   color=HEAD).next_to(gap, DOWN, buff=0.15)
        notes = VGroup(
            wrapped_label(r"the remote figures are our latency model of one service call: \ lognormal around "
                          r"10 ms, \ with 1\% slow outliers \ (a pause, \ a retransmission); \ later chapters use "
                          r"it again", 12.4, font_size=19, color=GREY_A),
            wrapped_label(r"a loop of a thousand local calls is invisible; \ a thousand remote calls is ten "
                          r"seconds: \ interfaces must be designed for few, \ large calls", 12.4, font_size=20,
                          color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(gl, DOWN, buff=0.9).set_x(0)
        with self.voiceover(
            "In 1994 Jim Waldo, Geoff Wyant, Ann Wollrath and Sam Kendall, at Sun, wrote A Note on Distributed "
            "Computing, arguing that this illusion cannot be kept. They gave four reasons. The first is latency."
            " <bookmark mark='a'/> A local call costs nanoseconds. <bookmark mark='b'/> A remote call, in this "
            "part's latency model, takes about ten milliseconds at the median and thirty at the ninety-ninth "
            "percentile: <bookmark mark='c'/> six or seven orders of magnitude more. <bookmark mark='d'/> A "
            "thousand local calls go unnoticed; a thousand remote calls take ten seconds. Remote interfaces need"
            " few calls, each doing a lot."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(local), FadeIn(ll))
            vo.wait_until("b")
            self.play(FadeIn(d50, scale=1.5), FadeIn(d99), FadeIn(rl))
            vo.wait_until("c")
            self.play(GrowFromCenter(gap), FadeIn(gl))
            vo.wait_until("d")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    def memory(self):
        head = label(r"No shared memory, \ no single thread", font_size=36).to_edge(UP, buff=0.3)

        def space(title, x, color):
            r = RoundedRectangle(width=2.9, height=3.4, corner_radius=0.12, stroke_color=color, stroke_width=2)
            r.move_to([x, 0.5, 0])
            t = label(title, font_size=19, color=color).next_to(r, UP, buff=0.12)
            return VGroup(r, t)
        cs = space(r"client's memory", -4.9, DATA)
        ss = space(r"server's memory", -0.9, LAM)
        obj = tag_box(r"{count: 1}", color=WHITE, size=17).move_to([-4.4, 0.5, 0])
        refs = VGroup()
        for nm, dy in (("a", 0.9), ("b", -0.9)):
            d = mono(nm, size=19, color=DATA).move_to([-5.9, 0.5 + dy, 0])
            refs.add(VGroup(d, Arrow(d.get_right(), obj.get_left(), buff=0.1, color=DATA, stroke_width=2,
                                     max_tip_length_to_length_ratio=0.15)))
        addr = mono("0x7ffd5a10", size=16, color=GREY_B).next_to(obj, DOWN, buff=0.15)
        call = mono("f(a, b)", size=19, color=HEAD).next_to(cs[0], DOWN, buff=0.2)
        copies = VGroup(*[tag_box(r"{count: 1}", color=WHITE, size=17).move_to([-0.6, 0.5 + dy, 0])
                          for dy in (0.9, -0.9)])
        cnames = VGroup(*[mono(nm, size=19, color=LAM).next_to(c, LEFT, buff=0.2) for nm, c in zip("ab", copies)])
        ship = Arrow(cs[0].get_right(), ss[0].get_left(), buff=0.08, color=GREY_B, stroke_width=2)
        bumped = tag_box(r"{count: 2}", color=YES, size=17).move_to(copies[0])
        notes = VGroup(
            wrapped_label(r"a pointer is an address in one process \ (Part 32): \ meaningless anywhere else, \ so "
                          r"arguments travel as copies", 4.3, font_size=19, color=WHITE),
            wrapped_label(r"copies break sharing: \ one object passed twice arrives as two, \ and the server's "
                          r"update never reaches the caller", 4.3, font_size=19, color=NO),
            wrapped_label(r"and the server runs many clients' calls at once, \ on its own threads: \ concurrency "
                          r"the caller never wrote \ (Part 33)", 4.3, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.4, 0.4, 0])
        ill = note(r"illustrative", font_size=17).to_corner(DR, buff=0.35)
        with self.voiceover(
            "The second reason is memory. <bookmark mark='a'/> Here the caller passes one object twice, as a and"
            " as b. Locally, that is one address, passed twice. <bookmark mark='b'/> But an address means "
            "something only inside one process, Part 32's lesson, so the stub copies what it points to, and the "
            "server receives two separate objects. <bookmark mark='c'/> When it increments one, the other is "
            "unchanged, and so is the caller's original. <bookmark mark='d'/> The third reason is concurrency: a"
            " server runs many clients' calls at once, so every caller becomes part of a concurrent program, "
            "with all of Part 33's hazards."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cs), FadeIn(ss), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(obj), FadeIn(refs), FadeIn(addr), FadeIn(call))
            vo.wait_until("b")
            self.play(GrowArrow(ship), FadeIn(notes[0]))
            self.play(TransformFromCopy(obj, copies[0]), TransformFromCopy(obj, copies[1]), FadeIn(cnames))
            vo.wait_until("c")
            self.play(ReplacementTransform(copies[0], bumped), FadeIn(notes[1]))
            self.play(Indicate(obj, color=NO))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def partial(self):
        head = label(r"Partial failure: \ three ways to hear nothing", font_size=36).to_edge(UP, buff=0.3)
        x0, x1 = -5.3, 2.4
        xs, xa, xw, xr, xt = -5.0, -3.6, -2.8, -1.3, 1.6      # send, arrive, work done, reply back, timeout
        rows = VGroup()
        cases = [(r"request lost", r"the call never ran", "lost_req", NO),
                 (r"server crashed after the work", r"the call ran; \ no reply", "crash", KERN),
                 (r"reply lost", r"the call ran; \ the reply vanished", "lost_rep", LAM)]
        anims = []
        for k, (name, ran, kind, col) in enumerate(cases):
            yc = 1.85 - k * 1.6
            yc_, ys_ = yc + 0.35, yc - 0.35
            lanes = VGroup(Line([x0, yc_, 0], [x1, yc_, 0], color=GREY_C, stroke_width=1.5),
                           Line([x0, ys_, 0], [x1, ys_, 0], color=GREY_C, stroke_width=1.5))
            names = VGroup(label(r"client", font_size=16, color=DATA).next_to(lanes[0], LEFT, buff=0.12),
                           label(r"server", font_size=16, color=LAM).next_to(lanes[1], LEFT, buff=0.12))
            parts = VGroup()
            if kind == "lost_req":
                mid = [(xs + xa) / 2 + 0.3, yc, 0]
                parts.add(Line([xs, yc_, 0], mid, color=DATA, stroke_width=3),
                          Cross(scale_factor=0.14, stroke_color=NO, stroke_width=4).move_to(mid))
            else:
                parts.add(Arrow([xs, yc_, 0], [xa, ys_, 0], buff=0, color=DATA, stroke_width=3,
                                max_tip_length_to_length_ratio=0.15))
                parts.add(Rectangle(width=xw - xa, height=0.2, stroke_width=0, fill_color=YES,
                                    fill_opacity=0.85).move_to([(xa + xw) / 2, ys_, 0]))
                if kind == "crash":
                    parts.add(Cross(scale_factor=0.16, stroke_color=NO, stroke_width=4).move_to([xw + 0.35, ys_, 0]))
                else:
                    mid = [(xw + xr) / 2 + 0.2, yc + 0.05, 0]
                    parts.add(Line([xw, ys_, 0], mid, color=YES, stroke_width=3),
                              Cross(scale_factor=0.14, stroke_color=NO, stroke_width=4).move_to(mid))
            wait = DashedLine([xs, yc_ + 0.0, 0], [xt, yc_, 0], color=HEAD, stroke_width=3)
            tmo = VGroup(Line([xt, yc_ - 0.16, 0], [xt, yc_ + 0.16, 0], color=HEAD, stroke_width=4),
                         label(r"timeout", font_size=16, color=HEAD).next_to([xt, yc_ + 0.16, 0], UP, buff=0.05))
            side = VGroup(label(name, font_size=19, color=col),
                          label(ran, font_size=18, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            side.move_to([4.8, yc, 0]).align_to([3.0, 0, 0], LEFT)
            rows.add(VGroup(lanes, names, parts, wait, tmo, side))
            anims.append((parts, wait, tmo, side))
        foot = wrapped_label(r"the client sees the same thing in all three: \ silence until the timeout; \ retry, "
                             r"\ and the second and third run the call twice \ (Chapter 5)", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The fourth reason is the deepest: partial failure. A single computer works or it does not; a "
            "distributed system can be half broken. A client sends a request, no reply comes, and its timeout "
            "fires. What happened? <bookmark mark='a'/> Perhaps the request was lost, and the call never ran. "
            "<bookmark mark='b'/> Perhaps the server did the work, then crashed before replying. <bookmark "
            "mark='c'/> Perhaps it replied, and the reply was lost. <bookmark mark='d'/> From the client, all "
            "three look the same: silence. Retry, and the last two run the call twice: harmless for a read, a "
            "disaster for a payment."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(VGroup(r[0], r[1])) for r in rows])
            for mk, (parts, wait, tmo, side) in zip("abc", anims):
                vo.wait_until(mk)
                self.play(Create(parts), Create(wait), run_time=1.4)
                self.play(FadeIn(tmo), FadeIn(side))
            vo.wait_until("d")
            self.play(FadeIn(foot), *[Indicate(r[4], color=HEAD) for r in rows])
        self.wait(0.4)
        self.clear_scene()

    def generals(self):
        head = label(r"The two generals, \ again", font_size=36).to_edge(UP, buff=0.3)
        xa, xb, top, bot = -5.2, -1.6, 2.4, -2.6
        lines = VGroup(Line([xa, top, 0], [xa, bot, 0], color=DATA, stroke_width=2),
                       Line([xb, top, 0], [xb, bot, 0], color=LAM, stroke_width=2))
        who = VGroup(label(r"client", font_size=19, color=DATA).next_to(lines[0], UP, buff=0.1),
                     label(r"server", font_size=19, color=LAM).next_to(lines[1], UP, buff=0.1))
        texts = [r"do it", r"done", r"got your ``done''", r"got your ``got''"]
        msgs = VGroup()
        for k, t in enumerate(texts):
            y0, y1 = top - 0.3 - k * 1.15, top - 1.25 - k * 1.15
            a, b = ([xa, y0, 0], [xb, y1, 0]) if k % 2 == 0 else ([xb, y0, 0], [xa, y1, 0])
            arr = Arrow(a, b, buff=0, color=GREY_A, stroke_width=2.5, max_tip_length_to_length_ratio=0.08)
            tl = label(t, font_size=17, color=GREY_A).move_to(arr.get_center() + UP * 0.28)
            msgs.add(VGroup(arr, tl))
        cross = Cross(scale_factor=0.2, stroke_color=NO, stroke_width=5).move_to(msgs[-1][0].get_center())
        side = VGroup(
            wrapped_label(r"Part 38: \ over a link that can lose any message, \ no finite exchange makes both "
                          r"sides certain", 5.6, font_size=20, color=WHITE),
            wrapped_label(r"take the shortest exchange that works: \ its last message may be lost, \ so its sender "
                          r"cannot rely on it, \ and a shorter one would do; \ there is no shortest", 5.6,
                          font_size=20, color=NO),
            wrapped_label(r"so no RPC system can promise ``exactly once'' by itself: \ it runs a call at most once "
                          r"\ (never retry) \ or at least once \ (retry until answered)", 5.6, font_size=20,
                          color=HEAD),
            wrapped_label(r"the cure is in the call, \ not the network: \ make it idempotent \ (Chapter 5)", 5.6,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "Could a cleverer protocol remove the doubt? Part 38 proved it cannot. <bookmark mark='a'/> The "
            "client says do it; the server says done; but the server cannot know its done arrived, so the client"
            " acknowledges, and that acknowledgement needs one too. <bookmark mark='b'/> Take the shortest "
            "exchange that supposedly works. Its last message might be lost, so its sender cannot depend on it, "
            "and a shorter exchange would do just as well. There is no shortest. <bookmark mark='c'/> So an RPC "
            "system runs a call at most once, never retrying, or at least once, retrying until answered. "
            "<bookmark mark='d'/> Exactly once must be built into the call itself."
        ) as vo:
            self.play(FadeIn(head), Create(lines), FadeIn(who), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(m[0]) for m in msgs], lag_ratio=0.5),
                      LaggedStart(*[FadeIn(m[1]) for m in msgs], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(Create(cross), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def idl(self):
        head = label(r"Interfaces, \ described once", font_size=36).to_edge(UP, buff=0.3)
        src = code_block(["service Counter {", "  rpc Add (Counts) returns (Ack);", "}", "",
                          "message Counts {", "  string word  = 1;", "  int64  count = 2;", "}"], size=17)
        frame = SurroundingRectangle(src, buff=0.2, color=GREY_C, stroke_width=1.5, corner_radius=0.08)
        idl = VGroup(frame, src).move_to([-4.3, 1.0, 0])
        cap = label(r"an interface description \ (Protocol Buffers)", font_size=18, color=GREY_B).next_to(
            idl, UP, buff=0.12)
        gen = module_box(r"stub generator", KERN, w=2.0, h=0.62).move_to([-0.1, 1.0, 0])
        outs = VGroup(*[module_box(t, HEAD, w=3.0, h=0.5, font=17) for t in
                        (r"Go client stub", r"Java server stub", r"Python client stub")]).arrange(
            DOWN, buff=0.22).move_to([3.7, 1.0, 0])
        a1 = Arrow(idl.get_right(), gen.get_left(), buff=0.12, color=GREY_B, stroke_width=2)
        a2 = VGroup(*[Arrow(gen.get_right(), o.get_left(), buff=0.12, color=GREY_B, stroke_width=2,
                            max_tip_length_to_length_ratio=0.15) for o in outs])
        hist = [(r"Sun RPC", r"1988, \ RFC 1057", DATA), (r"CORBA", r"1991, \ OMG", LAM),
                (r"Thrift", r"2007, \ Facebook", KERN), (r"gRPC", r"2015, \ Google", YES)]
        chips = VGroup(*[VGroup(label(n, font_size=21, color=c), label(d, font_size=17, color=GREY_B)).arrange(
            DOWN, buff=0.08) for n, d, c in hist]).arrange(RIGHT, buff=1.0).move_to([0, -1.55, 0])
        rule = Line(chips.get_left() + LEFT * 0.3, chips.get_right() + RIGHT * 0.3, color=GREY_D).next_to(
            chips, UP, buff=0.12)
        foot = wrapped_label(r"gRPC's generated calls take a \textbf{deadline} and return a \textbf{status} \ "
                             r"(\texttt{DEADLINE\_EXCEEDED}, \ \texttt{UNAVAILABLE}, \ ...): \ the stub admits the "
                             r"network is there", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What survived from Birrell and Nelson is the stub generator. <bookmark mark='a'/> An interface is "
            "written once, in an interface description language: here a service with one call, and its message. "
            "<bookmark mark='b'/> A generator writes the stubs, in whatever languages each side uses. <bookmark "
            "mark='c'/> The idea runs from Sun RPC, which carried the NFS file system, through CORBA and "
            "Facebook's Thrift, to Google's gRPC. <bookmark mark='d'/> What changed is honesty. A gRPC call "
            "takes a deadline and returns a status, such as deadline exceeded or unavailable: it looks local, "
            "but admits the network is there."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(idl), FadeIn(cap))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(gen))
            self.play(LaggedStart(*[GrowArrow(a) for a in a2], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(o) for o in outs], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(Create(rule), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM)
