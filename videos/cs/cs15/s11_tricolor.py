from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, BLACK_OBJ, CODE, COST, CTRL, DATA, FUNC, GRAY_OBJ, HEAD, LAM, NO, PART,
                                   WHITE_OBJ, YES, grid_table, load, mono, words)

POS = {"R": (-4.5, 0.6), "A": (-2.0, 0.6), "B": (0.5, 1.6), "C": (3.0, 0.6)}
FILL = {0: WHITE_OBJ, 1: GRAY_OBJ, 2: BLACK_OBJ}


def obj(name, color):
    c = Circle(radius=0.42, stroke_color=GREY_A, stroke_width=2.5).set_fill(FILL[color], 1)
    t = mono(name, 20, BLACK if color == 0 else WHITE).move_to(c)
    return VGroup(c, t)


class Concurrent(VoiceoverScene):
    def construct(self):
        self.card()
        self.colors()
        self.loss()
        self.barriers()
        self.pauses()

    def card(self):
        card = chapter_card(10, r"Collecting while the program runs", r"Can the collector and the program share the "
                            r"heap?", lit=(1978,), extra=((1978, r"Dijkstra et al.: \ on-the-fly collection"),),
                            part=PART)
        with self.voiceover("Chapter ten. Collecting while the program runs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def colors(self):
        head = label(r"Three colours", font_size=34).to_edge(UP, buff=0.3)
        keys = VGroup(*[VGroup(obj(n, c), label(t, font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.35)
                        for n, c, t in (("w", 0, r"\textbf{white}: \ not reached \ (yet)"),
                                        ("g", 1, r"\textbf{gray}: \ reached, \ fields not yet scanned"),
                                        ("b", 2, r"\textbf{black}: \ reached, \ and every field scanned"))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"marking: \ shade the roots gray; \ then take a gray object, \ shade its targets, \ make it "
                  r"black", font_size=21, color=GREY_A),
            label(r"done when nothing is gray: \ white is garbage", font_size=21, color=GREY_A),
            label(r"a pause that marks everything at once is as long as the live data: \ 100 ms for a large heap",
                  font_size=21, color=NO),
            label(r"so do it in small steps, \ between the program's own \ (\textbf{incremental}), \ or beside it \ "
                  r"(\textbf{concurrent})", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Every collector so far stops the program while it works. For a large heap the pause can be a tenth "
            "of a second or more: too long for a game, a trading system, or a web server's tail latency. To "
            "collect a little at a time, we need to describe a collection half done. <bookmark mark='a'/> Dijkstra "
            "and his colleagues did it in 1978 with three colours. White: not reached yet. Gray: reached, but its "
            "fields not yet scanned. Black: reached and scanned. <bookmark mark='b'/> Marking shades the roots "
            "gray, then repeatedly takes a gray object, shades everything it points at, and makes it black. When "
            "nothing is gray, the white objects are garbage. <bookmark mark='c'/> Those steps can be interleaved "
            "with the program's own, or run on another core beside it. But then the program is changing pointers "
            "while the collector is following them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(k, shift=RIGHT * 0.1) for k in keys], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2:]))
        self.wait(0.3)
        self.clear_scene()

    def _draw(self, colors, edges):
        nodes = {n: obj(n, colors[n]).move_to([x, y, 0]) for n, (x, y) in POS.items()}
        ar = VGroup()
        for a, b in edges:
            ar.add(Arrow(nodes[a][0].get_center(), nodes[b][0].get_center(), buff=0.45, color=GREY_B,
                         stroke_width=2.5, tip_length=0.15))
        return VGroup(*nodes.values(), ar), nodes

    def loss(self):
        d = load("tricolor")
        head = label(r"How a live object gets lost", font_size=34).to_edge(UP, buff=0.3)
        frames = d["frames"]
        g, nodes = self._draw(frames[0][1], frames[0][2])
        rl = label(r"root", font_size=18, color=CTRL).next_to(nodes["R"], DOWN, buff=0.15)
        cap = label(frames[0][0], font_size=22, color=GREY_A).to_edge(DOWN, buff=1.4)
        marks = ["a", "b", "c"]
        with self.voiceover(
            "Here is how it goes wrong. <bookmark mark='a'/> Marking is under way. The root and A are black, B is "
            "gray, C, which only B points at, is still white. <bookmark mark='b'/> Now the program runs. It copies "
            "B's pointer to C into A, which is already black. <bookmark mark='c'/> Then it deletes B's pointer to "
            "C. <bookmark mark='d'/> The collector resumes and scans B: nothing there. Marking ends with C white, "
            "so C is freed. But A, a live object, still points at it. The program will now read memory that "
            "belongs to someone else."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(rl), FadeIn(cap))
            for mk, (desc, col, edges) in zip(["b", "c", "d"], frames[1:]):
                vo.wait_until(mk)
                g2, nodes2 = self._draw(col, edges)
                cap2 = label(desc, font_size=22, color=NO if mk == "d" else GREY_A).move_to(cap)
                if cap2.width > 13:
                    cap2.scale_to_fit_width(13)
                self.play(Transform(g, g2), Transform(cap, cap2))
            self.play(Indicate(nodes["C"], color=NO))
        self.wait(0.3)
        self.clear_scene()

    def barriers(self):
        d = load("tricolor")["experiment"]
        head = label(r"Two invariants, \ two barriers", font_size=34).to_edge(UP, buff=0.3)
        inv = VGroup(
            label(r"the loss needs both: \ a black object gets a pointer to a white one, \textit{and} \ the last "
                  r"gray path to it is cut", font_size=21, color=GREY_A),
            label(r"\textbf{strong} invariant: \ no black object points at a white one", font_size=22, color=YES),
            label(r"\textbf{weak} invariant: \ every white object a black one points at is still reachable from a "
                  r"gray one", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).next_to(head, DOWN, buff=0.4)
        bars = VGroup(
            label(r"\textbf{Dijkstra}'s insertion barrier \ (incremental update): \ storing a pointer to a white "
                  r"object shades it gray", font_size=20, color=DATA),
            label(r"\textbf{Yuasa}'s deletion barrier \ (snapshot at the beginning): \ overwriting a pointer "
                  r"shades its old target gray", font_size=20, color=LAM),
        ).arrange(DOWN, buff=0.15).next_to(inv, DOWN, buff=0.35)
        rows = []
        for k, name in (("none", r"no barrier"), ("dijkstra", r"Dijkstra (insertion)"), ("yuasa", r"Yuasa (deletion)")):
            r = d[k]
            rows.append([name, f"{words(r['cycles_losing'])} of {words(r['trials'])}", f"{r['floating']:.1f}"])
        tab = grid_table([r"2,000 random collection cycles, \ a hostile mutator", r"cycles that lose a live object",
                          r"garbage kept, \ per cycle"], rows, widths=[5.6, 4.0, 3.2], row_h=0.5, font_size=20,
                         colors=[[WHITE, NO, WHITE], [DATA, YES, WHITE], [LAM, YES, WHITE]]).next_to(bars, DOWN,
                                                                                               buff=0.35)
        note = label(r"the price of safety: \ a barrier on every pointer write, \ and some garbage survives until "
                     r"the next cycle", font_size=19, color=HEAD).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The loss needed two things: a black object was given a pointer to a white one, and the last path to "
            "that white object through a gray one was cut. Prevent either and nothing is lost. <bookmark "
            "mark='a'/> The strong invariant forbids the first: no black object may point at a white one. The "
            "weak invariant allows it, provided some gray object can still reach the white one. <bookmark "
            "mark='b'/> Dijkstra's barrier enforces the strong invariant: whenever the program stores a pointer to "
            "a white object, shade that object gray. Yuasa's barrier, from 1990, protects the weak one: whenever "
            "the program overwrites a pointer, shade the old target, so everything reachable when marking began "
            "will be marked. <bookmark mark='c'/> We tested all three on two thousand random collection cycles, "
            "with a mutator moving and deleting pointers between marking steps. Without a barrier, more than a "
            "third of the cycles freed a live object. With either barrier, none did. <bookmark mark='d'/> The "
            "cost is a few instructions on every pointer write, and some garbage, floating garbage, that survives "
            "until the next cycle; Yuasa's barrier, the more conservative, keeps the most."
        ) as vo:
            self.play(FadeIn(head), FadeIn(inv[0]))
            vo.wait_until("a")
            self.play(FadeIn(inv[1:]))
            vo.wait_until("b")
            self.play(FadeIn(bars))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def pauses(self):
        d = load("pauses")
        head = label(r"Pauses, \ measured on this machine", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        cols = []
        for r in d["rows"]:
            mx = r["max_ms"]
            rows.append([r["collector"], str(r["pauses"]), f"{mx:.3f} ms" if mx < 1 else f"{mx:.0f} ms",
                         f"{r['seconds']:.1f} s" if r["seconds"] else "?"])
            cols.append([WHITE, WHITE, YES if mx < 1 else NO, WHITE])
        tab = grid_table([r"collector", r"pauses", r"longest", r"whole run"], rows, widths=[4.8, 1.8, 2.6, 2.4],
                         row_h=0.5, font_size=20, colors=cols).next_to(head, DOWN, buff=0.45)
        cap = label(rf"{d['workload']}; \ {d['java'].split('(')[0].strip()}, \ {d['go'].replace('go version ', '')}"
                    .replace("_", r"\_"), font_size=17, color=GREY_B).next_to(tab, DOWN, buff=0.25)
        pts = VGroup(
            label(r"stop-the-world collectors: \ pauses of tens to hundreds of milliseconds", font_size=21,
                  color=NO),
            label(r"ZGC and Go: \ tens of \textit{micro}seconds, \ because marking and moving happen while the program "
                  r"runs", font_size=21, color=YES),
            label(r"the price: \ barriers in the program's own code, \ and often a longer run overall", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Real runtimes make these trades every day, and we can measure them. We wrote one allocation-heavy "
            "program, sixty million allocations with a live set of two hundred thousand lists, and ran it on the "
            "Java virtual machine with four different collectors, and in Go. <bookmark mark='a'/> The serial, "
            "parallel and G1 collectors stop the program: their longest pauses are tens to hundreds of "
            "milliseconds. <bookmark mark='b'/> ZGC and Go's collector do their marking, and ZGC even its moving, "
            "while the program runs, using barriers like the ones we just tested. Their longest pauses are "
            "measured in microseconds. <bookmark mark='c'/> They are not free. The barriers run in the program's "
            "own code, and the whole run is not faster: the parallel collector, with the longest pauses but no "
            "barriers, finishes first. Throughput or latency: a collector chooses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
