from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.compute import load as load36
from videos.cs.cs37.compute import load as load37
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, mono

# US-CERT alert TA14-017A, "UDP-Based Amplification Attacks" (2014; memcached added in 2018): bandwidth
# amplification factors, as (protocol, low, high).
FACTORS = [("SNMPv2", 6.3, 6.3), ("SSDP", 30.8, 30.8), ("DNS", 28, 54), ("CharGEN", 358.8, 358.8),
           ("NTP", 556.9, 556.9), ("memcached", 10_000, 51_000)]


def cbox(text, color, w=None, h=0.5, size=18, use_mono=False, fill=0.0):
    """A labelled rounded box (Tex, or monospace with ``use_mono``)."""
    t = mono(text, size=size, color=WHITE) if use_mono else label(text, font_size=size, color=WHITE)
    w = w or t.width + 0.35
    r = RoundedRectangle(width=w, height=h, corner_radius=0.07, stroke_color=color, stroke_width=1.8,
                         fill_color=color if fill else BG, fill_opacity=fill if fill else 1)
    if t.width > w - 0.12:
        t.width = w - 0.12
    t.move_to(r)
    return VGroup(r, t)


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def say(n: int) -> str:
    """A whole number below a million, as a speaker says it."""
    n = int(round(n))
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else "-" + ONES[n % 10])
    if n < 1000:
        return ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + say(n % 100))
    return say(n // 1000) + " thousand" + ("" if n % 1000 == 0 else (" and " if n % 1000 < 100 else " ") +
                                           say(n % 1000))


def fmt_factor(v):
    return f"{v:,.0f}" if v >= 100 and v == int(v) else (f"{v:,.1f}" if v != int(v) else f"{v:,.0f}")


class Networks(WatchScene):
    def construct(self):
        self.card()
        self.spoof()
        self.amplify()
        self.bgp()
        self.lesson()

    def card(self):
        self.chapter(9, r"Networks under attack", r"What does the network believe, \ and who can lie to it?", lit=(2000, 2008, 2018), extra=((2000, r"BCP 38: \ ingress filtering"),
                                                           (2008, r"Kaminsky; \ YouTube's hijack"),
                                                           (2018, r"memcached amplification")), part=PART, layers=("net", "dist"), said="Chapter nine. Networks under attack.")

    def spoof(self):
        head = label(r"Nobody checks the return address", font_size=36).to_edge(UP, buff=0.3)
        names = [r"source", r"destination", r"protocol", r"payload"]
        vals = ["203.0.113.7", "192.0.2.53", "UDP", "a small query"]
        cols = [DATA, HEAD, GREY_B, GREY_B]
        fields = VGroup(*[cbox(v, c, w=w, size=18, use_mono=k < 3)
                          for k, (v, c, w) in enumerate(zip(vals, cols, (2.9, 2.9, 1.5, 2.6)))])
        fields.arrange(RIGHT, buff=0.08).next_to(head, DOWN, buff=0.75)
        fnames = VGroup(*[label(n, font_size=17, color=GREY_A).next_to(f, UP, buff=0.1) for n, f in zip(names, fields)])
        cap = label(r"an IP packet's header \ (Part 36)", font_size=18, color=GREY_B).next_to(fields, DOWN, buff=0.15)
        cap.align_to(fields, RIGHT)
        forged = cbox("198.51.100.20", NO, w=2.9, size=18, use_mono=True).move_to(fields[0])
        xs = [-5.6, -3.0, -0.4, 2.3, 5.3]
        nm = [r"attacker", r"its edge router", r"core routers", r"reflector", r"victim"]
        nc = [NO, KERN, GREY_B, LAM, DATA]
        nodes = VGroup(*[cbox(n, c, w=2.15, h=0.62, size=18).move_to([x, -0.3, 0]) for n, x, c in zip(nm, xs, nc)])
        links = VGroup(*[Line(nodes[i].get_right(), nodes[i + 1].get_left(), color=GREY_D, stroke_width=2)
                         for i in range(3)])
        reply = CurvedArrow(nodes[3].get_bottom() + DOWN * 0.05, nodes[4].get_bottom() + DOWN * 0.05, angle=PI / 2.2,
                            color=NO, stroke_width=3)
        rl = label(r"the reply goes to the forged source", font_size=18, color=NO).next_to(reply, DOWN, buff=0.1)
        rl.set_x(3.8)
        lookup = label(r"forwards on the destination alone", font_size=18, color=GREY_A).next_to(nodes[2], UP,
                                                                                               buff=0.25)
        pk = Dot(nodes[0].get_right(), radius=0.1, color=NO)
        bcp = wrapped_label(r"\textbf{BCP 38} \ (RFC 2827, \ 2000): \ an edge network drops any packet whose source "
                            r"is not one of its own addresses", 12.4, font_size=20, color=YES).to_edge(DOWN, buff=0.4)
        stop = Cross(stroke_color=YES, stroke_width=5).scale(0.18).move_to(links[0])
        ill = label(r"documentation addresses", font_size=16, color=GREY_B).next_to(cap, LEFT, buff=0.5)
        with self.voiceover(
            "Every packet carries two addresses, and the network only cares about one of them. <bookmark mark='a'/> "
            "Routers forward by the destination, Part 36's longest-prefix match, and nothing on the way checks the "
            "source. <bookmark mark='b'/> So an attacker can write someone else's address there. <bookmark mark='c'/> "
            "The packet travels as usual, the reflector answers it, and the answer goes to the forged source, a "
            "victim who never asked. <bookmark mark='d'/> The fix has been known since 2000, as best current "
            "practice thirty-eight: each edge network drops packets whose source is not one of its own. It works "
            "only where it is deployed, which is not everywhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fields), FadeIn(fnames), FadeIn(cap), FadeIn(ill))
            self.play(FadeIn(nodes), Create(links))
            vo.wait_until("a")
            self.play(FadeIn(lookup), Indicate(fields[1], color=HEAD))
            vo.wait_until("b")
            self.play(ReplacementTransform(fields[0], forged))
            vo.wait_until("c")
            self.play(MoveAlongPath(pk, Line(nodes[0].get_right(), nodes[3].get_left())), run_time=1.6)
            self.play(FadeOut(pk), Create(reply), FadeIn(rl))
            vo.wait_until("d")
            self.play(FadeIn(bcp), nodes[1][0].animate.set_stroke(YES), Create(stop))
        self.wait(0.4)
        self.clear_scene()

    def amplify(self):
        self.ask(r"A 60-byte request draws a 3000-byte reply, \\ sent to a forged source. The attack multiplies by...",
                 [r"$1$", r"$50$"], 1,
                 say="A sixty-byte request with a forged source draws a three-thousand-byte reply to the victim. By how much does the attacker's bandwidth multiply?",
                 reveal="Fifty times. Amplification needs only spoofing and a chatty protocol.")
        head = label(r"Amplification", font_size=36).to_edge(UP, buff=0.3)
        att = cbox(r"attacker", NO, w=1.7, h=0.6).move_to([-5.7, 0.0, 0])
        refl = VGroup(*[cbox(r"reflector", LAM, w=1.7, h=0.55).move_to([-3.3, y, 0]) for y in (1.4, 0.0, -1.4)])
        vic = cbox(r"victim", DATA, w=1.5, h=0.6).move_to([-0.9, 0.0, 0])
        thin = VGroup(*[Arrow(att.get_right(), r.get_left(), buff=0.06, stroke_width=1.6, color=NO,
                              max_tip_length_to_length_ratio=0.08) for r in refl])
        thick = VGroup(*[Arrow(r.get_right(), vic.get_left(), buff=0.06, stroke_width=9, color=NO,
                               max_tip_length_to_length_ratio=0.12, max_stroke_width_to_length_ratio=12)
                         for r in refl])
        ql = label(r"requests: \ $q$ bytes each, \ with the victim's address as source", font_size=18, color=GREY_A)
        rlab = label(r"answers: \ $r$ bytes each, \ all to the victim", font_size=18, color=NO)
        VGroup(ql, rlab).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.6, -2.55, 0])
        e1 = MathTex(r"B_{\text{sent}}", r"=", r"n", r"\,q", font_size=40)
        e2 = MathTex(r"B_{\text{victim}}", r"=", r"n", r"\,r", font_size=40)
        e3 = MathTex(r"\frac{B_{\text{victim}}}{B_{\text{sent}}}", r"=", r"\frac{r}{q}", font_size=40)
        e4 = MathTex(r"B_{\text{victim}}", r"=", r"A", r"\,B_{\text{sent}}", font_size=40)
        for e in (e1, e2, e3, e4):
            e.move_to([3.7, 1.9, 0])
        e2.move_to([3.7, 0.95, 0])
        whys = [label(r"$n$ requests a second, \ $q$ bytes each", font_size=19, color=GREY_A),
                label(r"each request draws an answer of $r$ bytes", font_size=19, color=GREY_A),
                label(r"divide: \ $n$ cancels", font_size=19, color=GREY_A),
                label(r"$A = r/q$, \ the amplification factor", font_size=19, color=HEAD)]
        for w in whys:
            w.move_to([3.7, 0.2, 0])
        notes = VGroup(
            wrapped_label(r"UDP has no handshake, \ so the reflector cannot tell the source is false; \ TCP's handshake "
                          r"proves the sender can receive \ (Part 37)", 6.0, font_size=19, color=WHITE),
            wrapped_label(r"the attacker pays $q$, \ the victim receives $r$, \ and the reflectors' bandwidth is "
                          r"borrowed", 6.0, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, -1.9, 0])
        with self.voiceover(
            "Add a protocol whose answer is bigger than its question, and a forged source becomes a lever. "
            "<bookmark mark='a'/> The attacker sends n small requests a second, q bytes each, all claiming to come "
            "from the victim. <bookmark mark='b'/> Each reflector answers with r bytes, and every answer lands on the "
            "victim. <bookmark mark='c'/> Divide one rate by the other and n cancels: <bookmark mark='d'/> the victim "
            "receives A times what the attacker sent, A being the answer's size over the question's. "
            "<bookmark mark='e'/> It needs UDP, with no handshake; a TCP connection must first prove its source can "
            "receive, Part 37's handshake doing security work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(att), FadeIn(refl), FadeIn(vic))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in thin], lag_ratio=0.2), FadeIn(ql), Write(e1),
                      FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in thick], lag_ratio=0.2), FadeIn(rlab), Write(e2),
                      FadeTransform(whys[0], whys[1]))
            vo.wait_until("c")
            self.play(FadeOut(e1), TransformMatchingTex(e2, e3), FadeTransform(whys[1], whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(e3, e4), FadeTransform(whys[2], whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


    def bgp(self):
        b = load36("bgp")
        others = b["ases"] - 1                      # every AS but the attacker
        origin = b["origin_hijacked"] - 1           # the attacker counts itself; we count the others
        sub = b["sub_hijacked"] - 1
        q = next(a for a in b["adoption"] if a["frac"] == 0.25)
        rov = round(q["hijacked"] * others)
        head = label(r"Routers believe announcements \ (Part 36)", font_size=36).to_edge(UP, buff=0.3)
        dots = VGroup(*[Dot(radius=0.11, color=DATA) for _ in range(others)])
        dots.arrange_in_grid(rows=10, cols=13, buff=0.17).move_to([-3.6, -0.15, 0])
        rng = random.Random(55)
        order = list(range(others))
        rng.shuffle(order)
        order2 = order[:]
        rng.shuffle(order2)
        cap = label(rf"the {others} other networks of Part 36's simulated internet", font_size=17,
                    color=GREY_B).next_to(dots, DOWN, buff=0.25)
        sch = label(r"which dots are drawn is schematic; \ counts are simulated", font_size=16, color=GREY_B).next_to(
            cap, DOWN, buff=0.08)
        steps = VGroup(
            wrapped_label(r"the owner announces \texttt{208.65.152.0/22}: \ everyone routes to it", 5.6,
                          font_size=19, color=DATA),
            wrapped_label(rf"a stranger announces the same \texttt{{/22}}: \ {origin} of {others} follow it", 5.6,
                          font_size=19, color=KERN),
            wrapped_label(rf"a stranger announces \texttt{{208.65.153.0/24}} inside it: \ longest prefix wins, \ "
                          rf"{sub} of {others}", 5.6, font_size=19, color=NO),
            wrapped_label(rf"a quarter of networks drop routes their RPKI signatures contradict: \ {rov} of {others} still fooled",
                          5.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.4, 0.35, 0])
        foot = label(r"the prefixes of Pakistan Telecom's 2008 YouTube hijack", font_size=17,
                     color=GREY_B).next_to(steps, DOWN, buff=0.35).align_to(steps, LEFT)

        def paint(idx, n):
            return [dots[i].animate.set_color(NO if j < n else DATA) for j, i in enumerate(idx)]
        with self.voiceover(
            "Between networks, BGP believes what it is told. <bookmark mark='a'/> On Part 36's internet of a hundred "
            "and twenty-five networks, the owner of an address block announces it and everyone routes there. "
            f"<bookmark mark='b'/> If a stranger announces the same block, the {say(origin)} networks nearer to it believe "
            "the stranger. <bookmark mark='c'/> If it announces a more specific block inside, the longest prefix wins "
            "everywhere, and every network sends the traffic the wrong way: what Pakistan Telecom did to YouTube in "
            "2008, by mistake. <bookmark mark='d'/> Signed route origins, the RPKI, repair it network by network: "
            f"with a quarter of them checking, {say(rov)} are still fooled."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), FadeIn(cap), FadeIn(sch),
                      FadeIn(steps[0]), run_time=2)
            vo.wait_until("b")
            self.play(*paint(order, origin), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(*paint(order, sub), FadeIn(steps[2]), FadeIn(foot))
            vo.wait_until("d")
            self.play(*paint(order2, rov), FadeIn(steps[3]))
        self.wait(0.4)
        self.clear_scene()


    def lesson(self):
        head = label(r"Assume the path is hostile", font_size=36).to_edge(UP, buff=0.3)
        names = [r"you", r"Wi-Fi", r"your ISP", r"a resolver", r"a transit AS", r"the server"]
        cols = [DATA, NO, NO, NO, NO, YES]
        boxes = VGroup(*[cbox(n, c, w=1.85, h=0.62, size=18) for n, c in zip(names, cols)]).arrange(RIGHT, buff=0.25)
        boxes.move_to([0, 1.1, 0])
        links = VGroup(*[Line(boxes[i].get_right(), boxes[i + 1].get_left(), color=GREY_D, stroke_width=2)
                         for i in range(len(boxes) - 1)])
        tunnel = RoundedRectangle(width=boxes.width + 0.3, height=1.05, corner_radius=0.2, stroke_color=YES,
                                  stroke_width=2.5, fill_color=YES, fill_opacity=0.08).move_to(boxes)
        tl = label(r"TLS: \ keys agreed end to end \ (Part 30)", font_size=19, color=YES).next_to(tunnel, UP,
                                                                                               buff=0.12)
        mid = label(r"may read, \ drop, \ delay, \ forge", font_size=18, color=NO).next_to(boxes[1:5], DOWN,
                                                                                          buff=0.45)
        good = wrapped_label(r"\textbf{guarded:} \ what is said, \ that it arrives unaltered, \ and who answered "
                             r"\ (if the PKI holds: \ Chapter 8)", 5.9, font_size=20, color=YES)
        bad = wrapped_label(r"\textbf{not guarded:} \ whether it arrives at all, \ and who is talking to whom", 5.9,
                            font_size=20, color=NO)
        VGroup(good, bad).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([0, -1.4, 0])
        foot = label(r"the end-to-end argument \ (Saltzer, \ Reed and Clark, \ 1984), \ applied to trust",
                     font_size=19, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So what should a program believe about the network? Nothing. <bookmark mark='a'/> Between you and a "
            "server sit links, providers, resolvers and transit networks, and any of them may read, drop, delay or "
            "forge. <bookmark mark='b'/> Part 36's end-to-end argument says to do the important things at the ends, "
            "and TLS does: keys agreed between the two ends, with Part 30's mathematics, guard what is said, that it "
            "arrives unchanged, and who answered, as long as the certificates hold. <bookmark mark='c'/> What no "
            "encryption guards is whether the packets arrive at all, and who is talking to whom. Availability is "
            "bought with capacity and filtering, not with keys."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), Create(links))
            vo.wait_until("a")
            self.play(FadeIn(mid), *[Indicate(bx, color=NO, scale_factor=1.05) for bx in boxes[1:5]])
            vo.wait_until("b")
            self.play(FadeIn(tunnel), FadeIn(tl), FadeIn(foot))
            self.play(FadeIn(good))
            vo.wait_until("c")
            self.play(FadeIn(bad))
        self.wait(0.4)
        self.clear_scene()
        self.checkpoint(
            [(r"What is a confused deputy?", r"A program misusing its authority for a caller"),
             (r"Why is safety undecidable in HRU?", r"Protection commands can simulate a Turing machine")],
            narration="Checkpoint. What is a confused deputy? And why is it undecidable whether a right can leak?",
            answers_narration="A program that uses its own authority on a caller's behalf. And because protection commands can "
                              "simulate a Turing machine, so leaking is halting.")


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
