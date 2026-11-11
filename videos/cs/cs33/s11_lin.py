from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (HEAD, NO, PART, T0C, T1C, T2C, YES, grid_table, load, num)

TCOL = (T0C, T1C, T2C)


def timeline(ops, lin, y0=1.2, x0=-5.6, sx=1.45, dy=0.95):
    """Each operation as an interval on its thread's line; ``lin``: the chosen linearization, drawn as points."""
    g = VGroup()
    names = VGroup()
    for t in range(3):
        y = y0 - dy * t
        names.add(label(rf"thread {t}", font_size=19, color=TCOL[t]).move_to([x0 - 0.9, y, 0]))
        g.add(DashedLine([x0, y, 0], [x0 + sx * 6.5, y, 0], color=GREY_D, stroke_width=1))
    ivs = VGroup()
    for k, o in enumerate(ops):
        y = y0 - dy * o["thread"]
        a, b = x0 + sx * o["start"], x0 + sx * o["end"]
        c = TCOL[o["thread"]]
        r = RoundedRectangle(width=b - a, height=0.5, corner_radius=0.08, stroke_color=c, stroke_width=1.8,
                             fill_color=c, fill_opacity=0.18).move_to([(a + b) / 2, y, 0])
        txt = (rf"enq({o['arg']})" if o["kind"] == "enq" else rf"deq() $\rightarrow$ {o['ret']}")
        ivs.add(VGroup(r, label(txt, font_size=19, color=WHITE).move_to(r)))
    pts = VGroup()
    if lin:
        for rank, k in enumerate(lin):
            o = ops[k]
            r = ivs[k][0]
            frac = (rank + 1) / (len(lin) + 1)
            x = r.get_left()[0] + 0.25 + (r.width - 0.5) * 0.5
            pts.add(Dot([x, r.get_center()[1] + 0.32, 0], radius=0.07, color=YES))
            del frac, o
    return VGroup(g, names), ivs, pts


class Lin(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.bad()
        self.vs_sc()
        self.checker()

    def card(self):
        card = chapter_card(10, r"Linearizability", r"What does it mean for a concurrent queue to be correct?",
                            lit=(1990,), extra=((1990, r"Herlihy and Wing"),), part=PART)
        with self.voiceover("Chapter ten. Linearizability."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def idea(self):
        d = load("lin")
        h = d["hand"][0]
        head = label(r"Each operation takes effect at one instant", font_size=34).to_edge(UP, buff=0.3)
        lanes, ivs, _ = timeline(h["ops"], h["lin"])
        order = h["lin"]
        pts = VGroup()
        xs = {1: 1.2, 0: 1.7, 2: 3.0, 3: 5.0}       # instants inside each interval, in time units
        for k in order:
            o = h["ops"][k]
            x = -5.6 + 1.45 * xs[k]
            y = 1.2 - 0.95 * o["thread"]
            pts.add(VGroup(Line([x, y - 0.34, 0], [x, y + 0.34, 0], color=YES, stroke_width=4)))
        seq = label(r"in instant order: \ enq(y), \ enq(x), \ deq() $\rightarrow$ y, \ deq() $\rightarrow$ x: \ a "
                    r"legal run of a queue", font_size=21, color=YES).next_to(lanes, DOWN, buff=0.5)
        lines = VGroup(
            label(r"an operation is an interval: \ from its call to its return", font_size=21, color=WHITE),
            label(r"\textbf{linearizable} \ (Herlihy and Wing, 1990): \ every operation can be given an instant inside "
                  r"its interval, \ so that in instant order they make sense for the sequential object", font_size=20,
                  color=HEAD),
            label(r"overlapping operations may go either way; \ non-overlapping ones keep their real-time order",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A lock makes a queue correct by making every operation happen one at a time. But what does correct mean "
            "for a queue with no lock, where operations overlap? <bookmark mark='a'/> Draw each operation as an "
            "interval, from the moment it is called to the moment it returns. Here thread zero enqueues x while thread "
            "one enqueues y, and thread two's dequeue overlaps them and returns y. <bookmark mark='b'/> Herlihy and "
            "Wing's answer, in 1990: the history is linearizable if each operation can be given a single instant "
            "inside its own interval, such that, in the order of those instants, the operations make sense for an "
            "ordinary sequential queue. <bookmark mark='c'/> Here they can. Put enqueue y first, then enqueue x, then "
            "the dequeue of y, then the dequeue of x. <bookmark mark='d'/> Operations that overlap may be ordered "
            "either way; operations that do not overlap must keep the order in which they really happened."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lanes))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(i) for i in ivs], lag_ratio=0.3), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(p) for p in pts], lag_ratio=0.4), FadeIn(seq))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def bad(self):
        d = load("lin")
        h = d["hand"][1]
        head = label(r"A history that no instant can explain", font_size=34).to_edge(UP, buff=0.3)
        lanes, ivs, _ = timeline(h["ops"], None)
        lines = VGroup(
            label(r"enq(x) finished before enq(y) began: \ x must come first", font_size=21, color=WHITE),
            label(r"so the first dequeue must return x; \ it returned y", font_size=21, color=NO),
            label(r"the checker: \ no linearization \ (it tries every order consistent with the intervals)",
                  font_size=21, color=NO),
            label(r"linearizability is \textbf{local}: \ a system of linearizable objects is linearizable; \ "
                  r"you can check each object alone", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now a history that is wrong. <bookmark mark='a'/> Here enqueue x finishes before enqueue y even starts, so "
            "any explanation must put x first. <bookmark mark='b'/> Then the first dequeue must return x. It returned "
            "y. <bookmark mark='c'/> No choice of instants can explain this, and our checker, which tries every order "
            "the intervals allow, reports that there is none. <bookmark mark='d'/> Linearizability has a property "
            "that makes it the standard: it is local. If each object in a system is linearizable, the whole system is, "
            "so each object can be built and checked on its own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lanes), LaggedStart(*[FadeIn(i) for i in ivs], lag_ratio=0.3))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def vs_sc(self):
        head = label(r"Linearizable, \ or only sequentially consistent?", font_size=34).to_edge(UP, buff=0.3)
        ops = [{"thread": 0, "kind": "enq", "arg": "x", "ret": None, "start": 0.3, "end": 1.8},
               {"thread": 1, "kind": "deq", "arg": None, "ret": r"empty", "start": 2.6, "end": 4.0}]
        lanes, ivs, _ = timeline(ops, None)
        ivs[1][1].become(label(r"deq() $\rightarrow$ empty", font_size=19, color=WHITE).move_to(ivs[1][0]))
        arrow = Arrow([-5.6 + 1.45 * 1.8, -1.45, 0], [-5.6 + 1.45 * 2.6, -1.45, 0], buff=0, color=GREY_B,
                      stroke_width=2)
        al = label(r"real time", font_size=16, color=GREY_B).next_to(arrow, DOWN, buff=0.05)
        lines = VGroup(
            label(r"\textbf{sequential consistency} of an object: \ some order that keeps each thread's own order",
                  font_size=20, color=WHITE),
            label(r"here: \ put the dequeue first: \ legal; \ so this history is sequentially consistent", font_size=20,
                  color=HEAD),
            label(r"\textbf{linearizability} also keeps real time: \ the enqueue had \textit{finished} \ $\Rightarrow$ "
                  r"\ not linearizable", font_size=20, color=NO),
            label(r"and only linearizability is local: \ two sequentially consistent queues can make a system that "
                  r"is not", font_size=20, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Linearizability is stronger than the sequential consistency of chapter four. <bookmark mark='a'/> For an "
            "object, sequential consistency asks only for some order of all the operations that respects each "
            "thread's own order. <bookmark mark='b'/> Here thread zero's enqueue finishes before thread one's dequeue "
            "begins, yet the dequeue reports an empty queue. Put the dequeue first and the order is legal, so the "
            "history is sequentially consistent. <bookmark mark='c'/> But linearizability also respects real time: "
            "the enqueue had finished, so the dequeue must see it. Not linearizable. <bookmark mark='d'/> The "
            "difference matters. Herlihy and Wing showed that sequential consistency is not local: two queues, each "
            "sequentially consistent on its own, can together produce a history that no order explains."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lanes), LaggedStart(*[FadeIn(i) for i in ivs], lag_ratio=0.3),
                      GrowArrow(arrow), FadeIn(al))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def checker(self):
        d = load("lin")
        fr = load("frontier")
        head = label(r"Checking histories", font_size=36).to_edge(UP, buff=0.3)
        rows = []
        for spec, nm in (("queue", r"queue"), ("stack", r"stack"), ("register", r"register"), ("counter", r"counter")):
            g, b = d["random"][f"{spec}_0.0"], d["random"][f"{spec}_0.3"]
            rows.append([nm, f"{g['linearizable']} / {g['of']}", f"{b['linearizable']} / {b['of']}"])
        tab = grid_table([r"object", r"correct: \ linearizable", r"30\% stale answers: \ linearizable"], rows,
                         widths=[2.4, 3.6, 4.6], row_h=0.5, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.4)
        sub = label(r"random histories, \ 3 threads, \ 12 operations", font_size=18, color=GREY_A).next_to(tab, UP,
                                                                                                         buff=0.1)
        lin = fr["lin"]
        l60 = next(r for r in lin if r["ops"] == 60)
        l80 = next(r for r in lin if r["ops"] == 80)
        lines = VGroup(
            label(r"Wing and Gong's search \ (1993), \ with Lowe's memo \ (2017): \ pick an operation that may go "
                  r"next, \ apply it, \ backtrack", font_size=20, color=WHITE),
            label(r"a stale answer is not always caught: \ another order may explain it, \ or the history has none",
                  font_size=20, color=HEAD),
            label(rf"cost: \ for 80 operations, \ median {num(l80['median'])} steps, \ but {l80['gave_up']} of 20 "
                  rf"histories pass {num(fr['cap'])} \ (chapter 16)", font_size=20, color=NO),
        ).arrange(DOWN, buff=0.15).next_to(tab, DOWN, buff=0.45)
        del l60
        with self.voiceover(
            "Our checker does this for any history. <bookmark mark='a'/> It is Wing and Gong's search from 1993: pick "
            "an operation that could go next, apply it to the sequential object, and backtrack if its result "
            "disagrees, remembering combinations already ruled out. <bookmark mark='b'/> On histories from a correct "
            "queue, stack, register or counter, every one is linearizable. When three answers in ten may be stale, the "
            "checker rejects about a third of the queue histories and nearly every counter history. The rest either "
            "contain no stale answer, or have one that another order happens to explain. <bookmark "
            "mark='c'/> And the cost is the catch. For eighty operations the median search is ten thousand steps, but "
            "a quarter of the histories run past three hundred thousand, where we gave up. Chapter sixteen explains "
            "why that is not our fault."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()
