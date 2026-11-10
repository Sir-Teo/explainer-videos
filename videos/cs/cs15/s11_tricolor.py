from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, BLACK_OBJ, CODE, COST, CTRL, DATA, FUNC, GRAY_OBJ, HEAD, LAM, NO, PART,
                                   WHITE_OBJ, YES, grid_table, load, mono, words)

from .measurements import barrier_color_witness

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
            label('a full marking pause grows with the work in the chosen model',
                  font_size=21, color=NO),
            label(r"so do it in small steps, \ between the program's own \ (\textbf{incremental}), \ or beside it \ "
                  r"(\textbf{concurrent})", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover("Every collector so far stops the program while it works. For a large heap the pause can be a tenth of a second or more: too long for a game, a trading system, or a web server's tail latency. To collect a little at a time, we need to describe a collection half done. <bookmark mark='a'/> Dijkstra and his colleagues did it in 1978 with three colours. White: not reached yet. Gray: reached, but its fields not yet scanned. Black: reached and scanned. <bookmark mark='b'/> Marking shades the roots gray, then repeatedly takes a gray object, shades everything it points at, and makes it black. When nothing is gray, the white objects are garbage. <bookmark mark='c'/> Those steps can be interleaved with the program's own, or run on another core beside it. But then the program is changing pointers while the collector is following them.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(k, shift=RIGHT * 0.1) for k in keys], lag_ratio=0.4), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[:2]))
            vo.wait_until('c')
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
        with self.voiceover("Here is how it goes wrong. <bookmark mark='a'/> Marking is under way. The root and A are black, B is gray, C, which only B points at, is still white. <bookmark mark='b'/> Now the program runs. It copies B's pointer to C into A, which is already black. <bookmark mark='c'/> Then it deletes B's pointer to C. <bookmark mark='d'/> The collector resumes and scans B: nothing there. Marking ends with C white, so C is freed. But A, a live object, still points at it. The program will now read memory that belongs to someone else.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(g), FadeIn(rl), FadeIn(cap), run_time=0.6)
            vo.wait_until('a')
            for mk, (desc, col, edges) in zip(['b', 'c', 'd'], frames[1:]):
                vo.wait_until(mk)
                g2, nodes2 = self._draw(col, edges)
                cap2 = label(desc, font_size=22, color=NO if mk == 'd' else GREY_A).move_to(cap)
                if cap2.width > 13:
                    cap2.scale_to_fit_width(13)
                self.play(Transform(g, g2), Transform(cap, cap2))
            self.play(Indicate(nodes['C'], color=NO))
        self.wait(0.3)
        self.clear_scene()

    def barriers(self):
        d=load('tricolor')['experiment']
        head=label('Two invariants, two barriers',font_size=34).to_edge(UP,buff=.3)
        inv=VGroup(
            label('loss: a black-to-white edge, then the last gray path is cut',font_size=21,color=GREY_A),
            label('strong: no black object points to a white object',font_size=22,color=YES),
            label('weak: each such white target has a white path from gray',font_size=21,color=YES),
        ).arrange(DOWN,buff=.35).move_to(UP*.5)
        bars=VGroup()
        columns=[-3.2,-.5,2.2,4.9]
        for x,txt in zip(columns,['start','copy C pointer into A','delete B to C','finish marking']):
            bars.add(label(txt,font_size=17,color=GREY_A).move_to([x,1.6,0]))
        for y,row,name in zip([.65,-.3,-1.25],barrier_color_witness(),
                             ['no barrier','insertion','deletion']):
            bars.add(label(name,font_size=20,color=GREY_A).move_to([-5.5,y,0]))
            for x,color in zip(columns,row['colors']):
                bars.add(obj('C',color).scale(.65).move_to([x,y,0]))
            for x1,x2 in zip(columns,columns[1:]):
                bars.add(Arrow([x1+.4,y,0],[x2-.4,y,0],buff=0,color=GREY_D,stroke_width=2,tip_length=.1))
        bars.add(label('C remains reachable in all three rows',font_size=20,color=HEAD).move_to(DOWN*2.2))
        names=[('none','no barrier'),('dijkstra','insertion'),('yuasa','deletion')]
        rows=[[name,f"{d[k]['cycles_losing']} / {d[k]['trials']}",f"{d[k]['floating']:.1f}"] for k,name in names]
        tab=grid_table(['model; 2,000 randomized cycles','cycles losing live objects','floating garbage per cycle'],
                       rows,widths=[4.2,4.1,3.8],row_h=.55,font_size=20,mono_cols=()).move_to(UP*.6)
        policy=VGroup(
            label('insertion: rescan registers before finishing',font_size=20,color=DATA),
            label('barrier modes allocate new objects black; root rules matter',font_size=20,color=LAM),
        ).arrange(DOWN,buff=.2).move_to(DOWN*1.6)
        note=label('finite checks support this model; they are not a concurrency proof',font_size=20,color=HEAD).to_edge(DOWN,buff=.4)
        with self.voiceover(
            (
            "The loss needs two changes: a black object gains a white target, and the last gray-to-white path is "
            "cut. <bookmark mark='a'/> The strong invariant forbids black-to-white edges. The weak invariant "
            "permits them only when the white target is protected by a path of white objects from a gray object. "
            "<bookmark mark='b'/> In our insertion barrier, a black-source store shades a white target. Our "
            "deletion barrier shades the old white target before overwriting it. The three timelines apply these "
            "rules to the same pointer moves. <bookmark mark='c'/> The table summarizes two thousand randomized "
            "cycles, not a general concurrency proof. Our model also specifies root handling and allocates new "
            "objects black with a barrier; insertion mode rescans registers before finishing. <bookmark "
            "mark='d'/> Barriers add work and can retain floating garbage. The complete invariant includes these "
            "root and allocation rules, not just the field-store instruction."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(inv[0]))
            vo.wait_until("a")
            self.play(FadeIn(inv[1:]))
            vo.wait_until("b")
            self.play(FadeOut(inv),FadeIn(bars))
            vo.wait_until("c")
            self.play(FadeOut(bars),FadeIn(tab),FadeIn(policy))
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
                         row_h=0.5, font_size=20, colors=cols, mono_cols=()).next_to(head, DOWN, buff=0.45)
        cap=VGroup(
            label('60 million allocations; 200,000 list heads; JVM fixed 1 GiB; Go GOGC=100, soft limit 1 GiB',
                  font_size=17,color=GREY_B),
            mono("JDK "+d['java'].split('"')[1]+"; "+d['go'].replace('go version ',''),15,GREY_B),
        ).arrange(DOWN,buff=.1).next_to(tab,DOWN,buff=.25)
        if cap.width>13:cap.scale_to_fit_width(13)
        pts = VGroup(
            label('Serial and Parallel pause; G1 also marks concurrently', font_size=21,
                  color=NO),
            label('ZGC: concurrent relocation; Go: concurrent, nonmoving, non-generational', font_size=21, color=YES),
            label('single-host runs; heap policies differ; pauses exclude assists and concurrent work', font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "Real runtimes expose different throughput and latency choices. Our allocation-heavy program uses "
            "sixty million allocations and two hundred thousand list heads. These are single runs on this host. "
            "<bookmark mark='a'/> The JVM runs use a fixed one-gibibyte heap. Serial and Parallel collect during "
            "pauses; G1 combines concurrent marking with stop-the-world phases. Read the measured pause counts "
            "and maxima here. <bookmark mark='b'/> ZGC performs much of its marking and relocation concurrently. "
            "Go marks concurrently but does not move objects, and its collector is non-generational. Go uses a "
            "growth target and a soft memory limit, so its heap policy differs from the JVM's. <bookmark "
            "mark='c'/> Short recorded pauses do not include all barrier, concurrent-worker or allocation-assist "
            "costs. The whole-run time is a second observation, not a universal ranking or a worst-case latency "
            "guarantee."
        )
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
