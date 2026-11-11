from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load)

TANNER = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (2, 5), (2, 6), (2, 7),
          (3, 6), (3, 7), (3, 0), (3, 1)]


class Ldpc(VoiceoverScene):
    def construct(self):
        self.card()
        self.tanner()
        self.rounds()
        self.waterfall()
        self.history()

    def card(self):
        card = chapter_card(11, r"LDPC codes and belief propagation", r"How did codes finally reach Shannon's limit?",
                            lit=(1962, 2001), extra=((1962, r"Gallager"), (1993, r"turbo codes"),
                                                     (1996, r"MacKay--Neal")), part=PART)
        with self.voiceover("Chapter eleven. LDPC codes and belief propagation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tanner(self):
        head = label(r"A sparse code on a graph", font_size=34).to_edge(UP, buff=0.3)
        var = VGroup(*[Circle(radius=0.22, color=DATA, stroke_width=3).set_fill(BG, 1).move_to([-5.8 + 0.8 * i, -1.6, 0])
                       for i in range(8)])
        chk = VGroup(*[Square(side_length=0.42, color=HEAD, stroke_width=3).set_fill(BG, 1).move_to(
            [-5.0 + 1.6 * j, 1.0, 0]) for j in range(4)])
        edges = VGroup(*[Line(chk[c].get_bottom(), var[v].get_top(), color=GREY_C, stroke_width=1.8) for c, v in TANNER])
        vl = label(r"bits \ (a small example: \ each bit in 2 checks)", font_size=18, color=DATA).next_to(var, DOWN, buff=0.2)
        cl = label(r"parity checks", font_size=18, color=HEAD).next_to(chk, UP, buff=0.2)
        up = [Dot(e.get_end(), radius=0.06, color=YES) for e in edges]
        down = [Dot(e.get_start(), radius=0.06, color=LAM) for e in edges]
        lines = VGroup(
            label(r"\textbf{Gallager} \ (1962): \ a parity-check matrix that is almost all zeros: \\ each bit in 3 "
                  r"checks, \ each check on 6 bits", font_size=21, color=WHITE),
            label(r"the \textbf{Tanner graph} \ (1981): \ bits on one side, \ checks on the other", font_size=21,
                  color=GREY_A),
            label(r"\textbf{belief propagation}: \ each bit tells its checks how sure it is; \\ each check replies "
                  r"what it believes the bit must be, \ from the others", font_size=21, color=YES),
            label(r"repeat: \ local messages, \ like the inference of \textit{AI, Built} 7, \\ until every check is "
                  r"satisfied", font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(VGroup(var, chk), RIGHT, buff=0.6).align_to(chk, UP)
        fit_right(lines)
        with self.voiceover(
            "In his 1960 thesis Robert Gallager proposed codes defined by sparse parity checks: each bit takes part "
            "in only three checks, and each check involves only six bits. <bookmark mark='a'/> Draw the bits on one "
            "side and the checks on the other, joined where a bit is in a check, as Michael Tanner did in 1981. "
            "<bookmark mark='b'/> Decoding passes messages along these edges. Each bit tells its checks how likely "
            "it is to be a one, from the channel and from the other checks. <bookmark mark='c'/> Each check replies "
            "with what the bit must be, judging from the other bits it sees. <bookmark mark='d'/> Repeat until every "
            "check is satisfied. This is belief propagation, the message passing of AI, Built's seventh part, and on "
            "a sparse graph each round costs time proportional to the length."
        ) as vo:
            self.play(FadeIn(head), FadeIn(var), FadeIn(chk), FadeIn(vl), FadeIn(cl), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(Create(edges), FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(*[MoveAlongPath(d, Line(e.get_end(), e.get_start())) for d, e in zip(up, edges)],
                      FadeIn(lines[2]), run_time=1.6)
            self.remove(*up)
            vo.wait_until("c")
            self.play(*[MoveAlongPath(d, Line(e.get_start(), e.get_end())) for d, e in zip(down, edges)],
                      run_time=1.6)
            self.remove(*down)
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
            for _ in range(2):
                ups = [Dot(e.get_end(), radius=0.05, color=YES) for e in edges]
                self.play(*[MoveAlongPath(d, Line(e.get_end(), e.get_start())) for d, e in zip(ups, edges)],
                          run_time=0.8)
                self.remove(*ups)
                downs = [Dot(e.get_start(), radius=0.05, color=LAM) for e in edges]
                self.play(*[MoveAlongPath(d, Line(e.get_start(), e.get_end())) for d, e in zip(downs, edges)],
                          run_time=0.8)
                self.remove(*downs)
        self.wait(0.3)
        self.clear_scene()

    def rounds(self):
        t = load("bptrace")
        head = label(r"Belief propagation, \ round by round", font_size=34).to_edge(UP, buff=0.3)
        top = max(max(t["good"]), max(t["bad"]))
        ax = Axes(x_range=[0, 31, 5], y_range=[0, top * 1.08, 100], x_length=6.2, y_length=4.2,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.55).to_edge(
            LEFT, buff=1.0)
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (0, 5, 10, 15, 20, 25, 30)])
        yt = VGroup(*[label(str(y), font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (100, 200, 300, 400)])
        xl = label(r"round", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        yl = label(r"wrong bits in the block", font_size=17, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT, buff=0.45)
        g = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(i, v) for i, v in enumerate(t["good"])])
        b = VMobject(color=NO, stroke_width=3).set_points_as_corners([ax.c2p(i, v) for i, v in enumerate(t["bad"])])
        gl = label(rf"$p$ = {t['p_good']}", font_size=18, color=YES).next_to(ax.c2p(4, t["good"][4]), DL, buff=0.1)
        bl = label(rf"$p$ = {t['p_bad']}", font_size=18, color=NO).next_to(ax.c2p(20, t["bad"][20]), UP, buff=0.12)
        notes = VGroup(
            label(rf"one block of {t['n']:,} bits".replace(",", "{,}"), font_size=20, color=WHITE),
            label(rf"$p$ = {t['p_good']}: \ {t['good'][0]} bits arrive flipped; \\ round by round the errors melt "
                  rf"away: \ zero after {len(t['good']) - 1} rounds", font_size=20, color=YES),
            label(rf"$p$ = {t['p_bad']}: \ {t['bad'][0]} flipped; \\ the decoder gets stuck near {t['bad'][-1]} "
                  r"\\ and stops after 30 rounds", font_size=20, color=NO),
            label(r"the decoder knows when it has failed: \\ some parity checks stay unsatisfied", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Here is the decoder at work on one block of our code. <bookmark mark='a'/> At seven percent noise, "
            "three hundred and forty-two bits arrive flipped. Round by round, the beliefs sharpen and the errors "
            "melt away: none are left after fourteen rounds. <bookmark mark='b'/> At nine percent, four hundred and "
            "thirty-two bits are flipped, and the decoder gets stuck at around three hundred, no matter how long it "
            "runs. <bookmark mark='c'/> But it knows: some parity checks are still unsatisfied, so a failed block is "
            "reported, not silently passed on."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(g), FadeIn(gl), FadeIn(notes[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(b), FadeIn(bl), FadeIn(notes[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def waterfall(self):
        d = load("ldpc")
        head = label(r"The waterfall", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0.035, 0.115, 0.01], y_range=[0, 1.02, 0.25], x_length=6.2, y_length=4.2,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.55).to_edge(
            LEFT, buff=1.0)
        xt = VGroup(*[label(f"{x:g}", font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (0.04, 0.06, 0.08, 0.1)])
        yt = VGroup(*[label(f"{int(y * 100)}\\%", font_size=15, color=GREY_A).next_to(ax.c2p(0.035, y), LEFT,
                                                                                    buff=0.08)
                      for y in (0.25, 0.5, 0.75, 1.0)])
        xl = label(r"channel flip probability $p$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        yl = label(r"blocks not decoded", font_size=17, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT, buff=0.45)
        pts = [ax.c2p(r["p"], r["fer"]) for r in d["rows"]]
        curve = VMobject(color=YES, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(q, radius=0.06, color=YES) for q in pts])
        bp = DashedLine(ax.c2p(0.084, 0), ax.c2p(0.084, 1.02), color=HEAD, stroke_width=2)
        sh = DashedLine(ax.c2p(0.11, 0), ax.c2p(0.11, 1.02), color=NO, stroke_width=2)
        bpl = label(r"BP reference \\ $\approx 0.084$", font_size=15, color=HEAD).next_to(bp, UP, buff=0.05).shift(LEFT * 0.35)
        shl = label(r"Shannon \\ 0.11", font_size=15, color=NO).next_to(sh, UP, buff=0.05)
        last_ok = max(r["p"] for r in d["rows"] if r["fer"] == 0)
        notes = VGroup(
            label(rf"a (3,6) code of length {d['n']:,}: \ design rate $\tfrac12$, \\ 100 blocks per point, \ 50 rounds of "
                  r"BP".replace(",", "{,}"), font_size=20, color=WHITE),
            label(rf"0 failures in 100 trials up to $p$ = {last_ok:g}; \\ parity checks decide when BP stops", font_size=20, color=YES),
            label(r"density evolution predicts the cliff \\ for long codes: \ 0.084 \ (Richardson and Urbanke)",
                  font_size=20, color=HEAD),
            label(rf"BEC density evolution, \ numerical threshold: \\ {d['bec_threshold']:.4f}, \ against "
                  r"capacity's 0.5", font_size=20, color=DATA),
            label(r"irregular degrees close the gap: \\ within 0.0045 dB of capacity \ (Chung et al., 2001)",
                  font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "We built a design-rate-one-half code of length four thousand eight hundred, using bounded swaps to "
            "remove four-cycles, and decoded a hundred noisy blocks at each noise level. The decoder stops when "
            "all parity checks pass or its iteration budget runs out; a wrong codeword still counts as a failure. "
            "<bookmark mark='a'/> At the lower sampled noise levels all hundred blocks came back perfectly. "
            "At higher noise levels almost none do: the "
            "waterfall. <bookmark mark='b'/> Tom Richardson and Rüdiger Urbanke's density evolution predicts where "
            "the cliff falls for very long codes of this kind: about eight point four percent. Our small finite "
            "experiment does not prove that threshold. Shannon's limit for this "
            "rate is eleven. <bookmark mark='c'/> On the erasure channel the prediction is a one-line recursion, "
            "and numerical iteration gives about point four two nine four, against a capacity of one half. <bookmark "
            "mark='d'/> Giving different bits different numbers of checks closes most of the remaining gap. In 2001 "
            "Sae-Young Chung, Forney, Richardson and Urbanke designed such a code within four thousandths of a "
            "decibel of the Shannon limit."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(dots), FadeIn(notes[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(bp), FadeIn(bpl), Create(sh), FadeIn(shl), FadeIn(notes[2]))
            for mk, n_ in zip("cd", notes[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def history(self):
        head = label(r"Forgotten, \ then everywhere", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"1962: \ Gallager's codes are too costly for the hardware of the day, \ and are forgotten",
                  font_size=22, color=GREY_A),
            label(r"1993: \ Berrou, \ Glavieux and Thitimajshima's \textbf{turbo codes}: \ two convolutional codes and "
                  r"an interleaver, \ within 0.7 dB of capacity", font_size=22, color=HEAD),
            label(r"the audience doubted the numbers; \ they were right, \ and decoding was belief propagation in "
                  r"disguise", font_size=22, color=WHITE),
            label(r"1996: \ MacKay and Neal rediscover Gallager's codes; \ they match turbo codes", font_size=22,
                  color=DATA),
            label(r"today: \ LDPC in Wi-Fi \ (802.11n onward), \ DVB-S2 satellite TV, \ 10-gigabit Ethernet, \ 5G "
                  r"data, \ SSDs", font_size=22, color=YES),
            label(r"turbo codes carried 3G and 4G data, \ and spacecraft since 2000", font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The history is strange. <bookmark mark='a'/> Gallager's codes needed more computation than the hardware "
            "of the 1960s could give, and they were forgotten for thirty years. <bookmark mark='b'/> In 1993 Claude "
            "Berrou, Alain Glavieux and Punya Thitimajshima presented turbo codes: two convolutional codes, one fed "
            "a shuffled copy of the data, decoded by trading beliefs back and forth. <bookmark mark='c'/> They "
            "claimed performance within a fraction of a decibel of Shannon's limit, and many listeners assumed a "
            "mistake. There was none, and the decoder turned out to be belief propagation. <bookmark mark='d'/> In "
            "1996 David MacKay and Radford Neal rediscovered Gallager's codes and found them just as good. "
            "<bookmark mark='e'/> Today LDPC codes run Wi-Fi, satellite television, ten-gigabit Ethernet, 5G data "
            "channels and the flash in solid-state drives. <bookmark mark='f'/> Turbo codes carried 3G and 4G, and "
            "spacecraft data since 2000."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
