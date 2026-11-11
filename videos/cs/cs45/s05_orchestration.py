from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, code_block, grid_table, load,
                                   module_box, trace)


class Orchestration(VoiceoverScene):
    def construct(self):
        self.card()
        self.borg()
        self.declarative()
        self.loop()
        self.levels()
        self.etcd()

    def card(self):
        card = chapter_card(4, r"Orchestration and reconciliation",
                            r"How do ten thousand machines keep doing what they were told?", lit=(2014, 2016),
                            extra=((2014, r"Kubernetes open-sourced"), (2015, r"Verma et al.: \ Borg"),
                                   (2016, r"Burns et al.: \ Borg, \ Omega, \ Kubernetes")), part=PART)
        with self.voiceover("Chapter four. Orchestration and reconciliation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def borg(self):
        head = label(r"From Borg to Kubernetes", font_size=36).to_edge(UP, buff=0.3)
        master = RoundedRectangle(width=4.2, height=1.1, corner_radius=0.12, stroke_color=KERN, stroke_width=2,
                                  fill_color=KERN, fill_opacity=0.12).move_to([-3.4, 1.85, 0])
        mname = label(r"Borgmaster", font_size=20, color=WHITE).next_to(master.get_top(), DOWN, buff=0.12)
        reps = VGroup(*[Dot(radius=0.11, color=HEAD if i == 0 else KERN) for i in range(5)]).arrange(RIGHT, buff=0.3)
        reps.next_to(mname, DOWN, buff=0.14)
        rl = label(r"five replicas, \ kept consistent by Paxos", font_size=16, color=GREY_A).next_to(master, UP,
                                                                                                    buff=0.08)
        machines = VGroup()
        cols = [DATA, LAM, YES, HEAD]
        for i in range(6):
            box = RoundedRectangle(width=0.95, height=1.35, corner_radius=0.06, stroke_color=GREY_B, stroke_width=1.5)
            tasks = VGroup(*[Square(0.26, stroke_width=0, fill_color=cols[(i + k) % 4], fill_opacity=0.85)
                             for k in range(2 + i % 3)]).arrange_in_grid(cols=2, buff=0.08)
            agent = label(r"Borglet", font_size=16, color=GREY_A)
            inner = VGroup(tasks, agent).arrange(DOWN, buff=0.12).move_to(box)
            machines.add(VGroup(box, inner))
        machines.arrange(RIGHT, buff=0.18).move_to([-3.4, -0.55, 0])
        links = VGroup(*[Line(master.get_bottom(), m[0].get_top(), color=GREY_D, stroke_width=1.5) for m in machines])
        cell = label(r"one \textbf{cell}: \ about ten thousand machines in the median cell", font_size=18,
                     color=GREY_A).next_to(machines, DOWN, buff=0.2)
        rows = [[r"cell", r"cluster"], [r"Borgmaster", r"API server, \ controllers"], [r"scheduler",
                r"kube-scheduler"], [r"Borglet", r"kubelet"], [r"task", r"pod"], [r"job", r"Deployment"],
                [r"Paxos store", r"etcd \ (Raft)"]]
        tab = grid_table([r"Borg", r"Kubernetes"], rows, widths=[2.4, 3.4], row_h=0.44, font_size=19, mono_cols=())
        tab.move_to([3.85, 0.55, 0])
        for r in range(1, len(rows) + 1):
            tab.cells[r][1].set_color(YES)
        src = wrapped_label(r"Verma et al. \ (2015) \ describe Borg; \ Burns et al. \ (2016) \ trace Kubernetes back "
                            r"through Borg and Omega", 12.4, font_size=19, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Google ran its services on a cluster manager called Borg for more than a decade before Abhishek "
            "Verma and his colleagues described it in 2015. <bookmark mark='a'/> A Borg cell is a set of "
            "machines managed as one, about ten thousand in the median cell. A Borgmaster, replicated five "
            "times and kept consistent with Paxos, decides where tasks run, and an agent on every machine, the "
            "Borglet, starts them and reports back. <bookmark mark='b'/> Kubernetes, open-sourced by Google in "
            "2014, was built by people who had worked on Borg, and its pieces map onto Borg's almost one for "
            "one: a pod is a task, and a kubelet is a Borglet."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(master), FadeIn(mname), FadeIn(reps), FadeIn(rl), Create(links), FadeIn(machines),
                      FadeIn(cell))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def declarative(self):
        head = label(r"Say what, \ not how", font_size=36).to_edge(UP, buff=0.3)
        imp = code_block(["start job-web on m3", "start job-web on m7", "start job-web on m2",
                          "# m7 dies: what now?"], size=17)
        imp[3].set_color(NO)
        dec = code_block(["kind: Deployment", "name: job-web", "replicas: 5", "image: job:1.4"], size=17)
        dec[2].set_color(HEAD)
        it = label(r"imperative: \ a script of commands", font_size=20, color=NO)
        dt = label(r"declarative: \ the state you want", font_size=20, color=YES)
        left = VGroup(it, imp).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        right = VGroup(dt, dec).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=1.6, aligned_edge=UP).next_to(head, DOWN, buff=0.5)
        ill = note(r"illustrative", font_size=16).next_to(right, RIGHT, buff=0.3).align_to(right, UP)
        want = module_box(r"desired: \ 5 replicas", YES, w=3.0, h=0.65, font=19)
        have = module_box(r"observed: \ 3 running", DATA, w=3.0, h=0.65, font=19)
        diff = module_box(r"difference: \ start 2", HEAD, w=3.0, h=0.65, font=19)
        flow = VGroup(want, have, diff).arrange(RIGHT, buff=0.9).next_to(VGroup(left, right), DOWN, buff=0.7)
        a1 = Arrow(want.get_right(), have.get_left(), buff=0.08, stroke_width=2, color=GREY_B)
        a2 = Arrow(have.get_right(), diff.get_left(), buff=0.08, stroke_width=2, color=GREY_B)
        lines = wrapped_label(r"the goal is stored, \ not the steps: \ after any crash, \ any controller can compare "
                              r"it with what it sees and recompute what to do", 12.4, font_size=21,
                              color=WHITE).next_to(flow, DOWN, buff=0.5)
        with self.voiceover(
            "The idea that makes this work is to say what you want, not how to get it. <bookmark mark='a'/> An "
            "imperative script says: start the web server on machine three, then seven, then two. If machine "
            "seven dies halfway, the script cannot tell what state the world is in. <bookmark mark='b'/> A "
            "declarative specification says only: there should be five replicas of this image. <bookmark "
            "mark='c'/> The system stores that goal, observes what is running, and acts on the difference. "
            "Because the goal is written down, and not the steps, any controller, after any crash, can look "
            "again and work out what remains."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(ill))
            vo.wait_until("c")
            self.play(FadeIn(want), GrowArrow(a1), FadeIn(have))
            self.play(GrowArrow(a2), FadeIn(diff), FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def loop(self):
        head = label(r"The reconciliation loop", font_size=36).to_edge(UP, buff=0.3)
        code = code_block(["while True:", "    want = spec.replicas", "    have = observe_pods()",
                           "    if len(have) < want:", "        start_pod()", "    elif len(have) > want:",
                           "        stop_pod(have[-1])", "    sleep(period)"], size=17)
        code.move_to([-3.7, 0.6, 0])
        stages = VGroup(*[module_box(t, c, w=1.9, h=0.6, font=19) for t, c in
                          ((r"observe", DATA), (r"compare", HEAD), (r"act", YES))])
        stages[0].move_to([1.2, 2.0, 0])
        stages[1].move_to([5.2, 2.0, 0])
        stages[2].move_to([3.2, 0.6, 0])
        arcs = VGroup(Arrow(stages[0].get_right(), stages[1].get_left(), buff=0.1, stroke_width=2, color=GREY_B),
                      Arrow(stages[1].get_bottom(), stages[2].get_right(), buff=0.1, stroke_width=2, color=GREY_B),
                      Arrow(stages[2].get_left(), stages[0].get_bottom(), buff=0.1, stroke_width=2, color=GREY_B))
        slots = VGroup(*[Circle(radius=0.28, color=GREY_C, stroke_width=1.5) for _ in range(5)]).arrange(
            RIGHT, buff=0.3).move_to([3.2, -0.85, 0])
        pods = VGroup(*[Dot(radius=0.22, color=YES).move_to(s) for s in slots])
        sl = label(r"five slots wanted", font_size=18, color=GREY_A).next_to(slots, DOWN, buff=0.15)
        crosses = VGroup(*[Cross(pods[i], stroke_color=NO, stroke_width=4, scale_factor=0.9) for i in (1, 3)])
        status = label(r"observed 3, \ wanted 5: \ start one pod per pass", font_size=19,
                       color=HEAD).next_to(sl, DOWN, buff=0.2)
        lines = wrapped_label(r"the loop never asks \textit{what happened?}, \ only \textit{what is different?}: \ "
                              r"it is idempotent, \ so running it twice, \ or after a crash, \ is harmless", 12.4,
                              font_size=21, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Each kind of object has a controller, and each controller is the same small loop. <bookmark "
            "mark='a'/> Read what is wanted. Observe what is there. Too few pods: start one. Too many: stop "
            "one. Sleep, and repeat. <bookmark mark='b'/> Here five replicas are running, and two crash. "
            "<bookmark mark='c'/> On its next pass the loop sees three where five are wanted, and starts "
            "replacements until the counts agree. <bookmark mark='d'/> The loop never asks what happened, only "
            "what is different now. That makes it idempotent: running it twice, or restarting it after a crash,"
            " does no harm."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code), FadeIn(stages), Create(arcs), FadeIn(slots), FadeIn(sl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pods], lag_ratio=0.15))
            self.play(Create(crosses))
            self.play(FadeOut(crosses), pods[1].animate.set_opacity(0), pods[3].animate.set_opacity(0))
            vo.wait_until("c")
            self.play(FadeIn(status), Indicate(stages[1], color=HEAD))
            for i in (1, 3):
                self.play(Indicate(stages[2], color=YES), pods[i].animate.set_opacity(1), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def levels(self):
        r = load("reconcile")
        ser, want, crash = r["series"], r["desired"], r["crash_at"]
        n = len(ser["edge"])
        head = label(r"Level-triggered against edge-triggered", font_size=36).to_edge(UP, buff=0.3)

        def plot(series, title, color, y):
            g = axes([0, n, 10], [0, want + 1.5, 1], x_length=6.8, y_length=1.75, y_label=title,
                     xticks=range(0, n + 1, 10), yticks=(0, want)).move_to([-2.6, y, 0])
            ax = g.ax
            goal = DashedLine(ax.c2p(0, want), ax.c2p(n, want), color=GREY_B, stroke_width=1.5)
            marks = VGroup(*[DashedLine(ax.c2p(t, 0), ax.c2p(t, want + 1.3), color=NO, stroke_width=1.5)
                             for t in crash])
            pts = []
            for t, v in enumerate(series):                  # a step plot: the count holds until the next step
                pts += [(t, v), (t + 1, v)]
            return g, goal, marks, trace(ax, pts, color, width=3.5)
        top = plot(ser["edge"], r"edge-triggered: \ replicas, \ reacting to `pod died' events", NO, 1.35)
        bot = plot(ser["level"], r"level-triggered: \ replicas, \ comparing with the goal every step", YES, -1.25)
        xl = label(r"step", font_size=17, color=GREY_A).next_to(bot[0].ax, DOWN, buff=0.4)
        crash_l = label(rf"two pods crash at steps {crash[0]} and {crash[1]}", font_size=17, color=NO).next_to(
            top[0].ax.c2p(crash[1], want + 1.3), RIGHT, buff=0.1)
        short = max(sum(1 for t in range(c, n) if ser["level"][t] < want and all(ser["level"][u] < want
                                                                                for u in range(c, t + 1)))
                    for c in crash)
        notes = VGroup(
            wrapped_label(rf"edge: \ one of the two `died' events at step {crash[1]} is lost, \ and nothing ever "
                          rf"looks again: \ {ser['edge'][-1]} replicas, \ for good", 4.6, font_size=19, color=NO),
            wrapped_label(rf"level: \ starts one pod per step, \ so it climbs to the goal at first; \ after each "
                          rf"crash it is short for {short} step, \ whatever was lost", 4.6, font_size=19, color=YES),
            wrapped_label(r"Kubernetes' controllers are written to be level-triggered: \ an event is only a hint to "
                          r"look sooner, \ and a periodic resync compares everything again", 4.6, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.5, 0.0, 0])
        with self.voiceover(
            "There are two ways to write a controller, and the difference shows when messages go astray. "
            "<bookmark mark='a'/> We simulated five replicas whose pods crash two at a time, at steps twelve "
            "and twenty-five. An edge-triggered controller reacts to events: each pod died message starts a "
            "replacement. But some messages are dropped. At the second crash one is lost, and the controller "
            "stays at four replicas forever, because nothing makes it look again. <bookmark mark='b'/> A level-"
            "triggered controller compares the goal with the world on every pass. It starts slowly, one pod per"
            " step, but after each crash it is short for a single step, whatever was lost. <bookmark mark='c'/>"
            " Kubernetes' controllers work this way: an event is only a hint to look sooner."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top[0]), FadeIn(bot[0]), FadeIn(xl), Create(top[1]), Create(bot[1]),
                      Create(top[2]), Create(bot[2]), FadeIn(crash_l))
            vo.wait_until("a")
            self.play(Create(top[3]), run_time=2.5)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(bot[3]), run_time=2.5)
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def etcd(self):
        head = label(r"Where the desired state lives", font_size=36).to_edge(UP, buff=0.3)
        api = module_box(r"API server", KERN, w=2.6, h=0.75, font=21).move_to([-0.6, 1.25, 0])
        user = module_box(r"\texttt{kubectl apply}", DATA, w=2.4, h=0.6, font=18).move_to([-4.6, 1.25, 0])
        ua = Arrow(user.get_right(), api.get_left(), buff=0.08, stroke_width=2, color=GREY_B)
        ul = label(r"write the goal", font_size=16, color=GREY_A).next_to(ua, UP, buff=0.06)
        members = VGroup(*[module_box(t, HEAD if i == 1 else LAM, w=1.45, h=0.55, font=17)
                           for i, t in enumerate((r"follower", r"leader", r"follower"))]).arrange(RIGHT, buff=0.65)
        members.move_to([-0.6, -0.55, 0])
        et = label(r"etcd: \ a key--value store replicated by Raft", font_size=18, color=LAM).next_to(members, DOWN,
                                                                                                      buff=0.15)
        ea = Arrow(api.get_bottom(), members[1].get_top(), buff=0.08, stroke_width=2, color=GREY_B)
        repl = VGroup(Arrow(members[1].get_left(), members[0].get_right(), buff=0.05, stroke_width=2, color=HEAD),
                      Arrow(members[1].get_right(), members[2].get_left(), buff=0.05, stroke_width=2, color=HEAD))
        kinds = ((r"Deployment controller", YES), (r"scheduler", YES), (r"kubelet, \ on every node", DATA))
        watchers = VGroup(*[module_box(t, c, w=2.9, h=0.55, font=17) for t, c in kinds])
        watchers.arrange(DOWN, buff=0.3).move_to([4.6, 0.55, 0])
        wa = VGroup(*[Arrow(w.get_left(), api.get_right() + UP * 0.2 * (1 - k), buff=0.08, stroke_width=1.8,
                            color=GREY_B, max_tip_length_to_length_ratio=0.06) for k, w in enumerate(watchers)])
        wl = label(r"watch", font_size=16, color=GREY_A).next_to(wa[0], UP, buff=0.02)
        lines = VGroup(
            wrapped_label(r"every write needs a majority of etcd's members \ (Part 38): \ three survive one failure, \ "
                          r"five survive two", 12.4, font_size=20, color=LAM),
            wrapped_label(r"each object carries a version: \ an update based on a stale read is refused, \ like a "
                          r"compare-and-swap, \ so two controllers never silently overwrite each other", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"the scheduler is a controller too: \ it watches for pods with no machine and binds each "
                          r"to one \ --- \ the next chapter is how it chooses", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "All of this rests on one durable record of what is wanted. <bookmark mark='a'/> You write the goal"
            " to the API server, the only component that talks to storage. It keeps every object in etcd, a "
            "key-value store replicated by Raft, from Part 38, so every write is committed by a majority: three"
            " members survive one failure, five survive two. <bookmark mark='b'/> Controllers and node agents "
            "never talk to one another; each watches the API server for the objects it cares about. <bookmark "
            "mark='c'/> Every object carries a version, so an update based on a stale read is refused, like a "
            "compare-and-swap. <bookmark mark='d'/> Even the scheduler is a controller: it watches for pods "
            "with no machine, and binds each to a node. How it chooses is the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(user), GrowArrow(ua), FadeIn(ul), FadeIn(api))
            self.play(GrowArrow(ea), FadeIn(members), FadeIn(et))
            self.play(*[GrowArrow(r) for r in repl], FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(watchers), *[GrowArrow(a) for a in wa], FadeIn(wl))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(Indicate(watchers[1], color=HEAD), FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, LAM)
