from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, mono, tag_box

# The inputs of the planner's example (explainer/cs/cloud/control.py, plan_example): each resource's one property
# that the scenes show.  The cache holds the kinds and the plan itself; these strings only label them.
PROP_ACTUAL = {"vpc": "10.0.0.0/16", "subnet": "10.0.1.0/24", "db": "small", "old-cache": "2 nodes"}
PROP_DESIRED = {"vpc": "10.0.0.0/16", "subnet": "10.0.1.0/24", "db": "large", "queue": "fifo", "service": "4 replicas"}
DEPS = {"subnet": ["vpc"], "db": ["subnet"], "old-cache": ["subnet"], "service": ["subnet", "db", "queue"]}
SIGN = {"create": "+", "update": "~", "destroy": "-"}


def node(name, color, w=1.7, h=0.55, dashed=False):
    """A resource as a rounded box with its name in monospace."""
    r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2,
                         fill_color=color, fill_opacity=0.12)
    if dashed:
        r = DashedVMobject(r, num_dashes=28)
    return VGroup(r, mono(name, size=16, color=WHITE).move_to(r))


def edge_point(box, v):
    """Where a ray from the centre of a box, in direction v, leaves it (plus a small gap)."""
    hw, hh = box.width / 2, box.height / 2
    k = min(hw / abs(v[0]) if abs(v[0]) > 1e-6 else 1e9, hh / abs(v[1]) if abs(v[1]) > 1e-6 else 1e9)
    return box.get_center() + v * (k + 0.06)


class Iac(VoiceoverScene):
    def construct(self):
        self.card()
        self.declare()
        self.diff()
        self.order()
        self.drift()
        self.immutable()

    def card(self):
        card = chapter_card(10, r"Infrastructure as code", r"How do you put a datacentre under version control?",
                            lit=(1993, 2014), extra=((1993, r"Burgess: \ CFEngine"), (2014, r"Terraform")),
                            part=PART)
        with self.voiceover("Chapter ten. Infrastructure as code."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def declare(self):
        head = label(r"From clicks to code", font_size=36).to_edge(UP, buff=0.3)
        frame = RoundedRectangle(width=4.4, height=3.3, corner_radius=0.12, stroke_color=GREY_B, stroke_width=1.5)
        ftitle = label(r"a web console", font_size=19, color=GREY_B).next_to(frame.get_top(), DOWN, buff=0.2)
        buttons = VGroup(*[tag_box(t, color=KERN, size=16, w=3.4, h=0.5)
                           for t in ("Create network", "Create subnet", "Create database")])
        buttons.arrange(DOWN, buff=0.3).next_to(ftitle, DOWN, buff=0.3)
        console = VGroup(frame, ftitle, buttons).move_to([-4.4, 0.45, 0])
        cursor = Triangle(color=WHITE, fill_color=WHITE, fill_opacity=1).scale(0.12).rotate(PI / 7)
        cursor.move_to(buttons[0].get_right() + LEFT * 0.4 + DOWN * 0.1)
        ask = wrapped_label(r"who clicked what, \ when, \ and could anyone do it again in another region?", 4.4,
                            font_size=19, color=NO).next_to(frame, DOWN, buff=0.25)
        lines = ['network  "vpc"     { cidr = "10.0.0.0/16" }',
                 'subnet   "subnet"  { cidr = "10.0.1.0/24", in = vpc }',
                 'database "db"      { size = "large", in = subnet }',
                 'queue    "queue"   { fifo = true }',
                 'service  "service" {',
                 '  replicas = 4',
                 '  uses     = [subnet, db, queue]',
                 '}']
        code = code_block(lines, size=16, buff=0.1)
        box = SurroundingRectangle(code, buff=0.2, color=DATA, stroke_width=1.5, corner_radius=0.08)
        ctitle = label(r"\texttt{infra.tf}: \ the desired state, \ in a file", font_size=19,
                       color=DATA).next_to(box, UP, buff=0.12).align_to(box, LEFT)
        right = VGroup(ctitle, box, code).move_to([2.6, 0.85, 0])
        flow = VGroup(*[tag_box(t, color=c, size=18, h=0.55) for t, c in
                        (("commit", DATA), ("plan", HEAD), ("review", LAM), ("apply", YES))]).arrange(RIGHT, buff=0.6)
        flow.next_to(right, DOWN, buff=0.4)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, stroke_width=2, color=GREY_B,
                                max_tip_length_to_length_ratio=0.3) for a, b in zip(flow, flow[1:])])
        foot = wrapped_label(r"CFEngine \ (Mark Burgess, 1993) \ and Puppet \ (2005) \ configured machines; \ AWS "
                             r"CloudFormation \ (2011) \ and HashiCorp's Terraform \ (2014) \ declare whole clouds; "
                             r"\ the syntax here is a simplified, \ Terraform-like one", 12.4, font_size=19,
                             color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Cloud resources can be made by hand, by clicking through a web console. <bookmark mark='a'/> A "
            "network, then a subnet inside it, then a database. It works once. But nobody can say afterwards who "
            "clicked what, and nobody can build the same thing again in another region. <bookmark mark='b'/> "
            "Infrastructure as code writes the desired state down instead: every network, database and service, "
            "with its settings and the other resources it uses, in a file. <bookmark mark='c'/> The file lives in "
            "version control, so a change to production is a commit: it gets a plan, a review and an apply, like "
            "any other change to code. <bookmark mark='d'/> Mark Burgess's CFEngine did this for the configuration "
            "of machines in 1993; CloudFormation in 2011 and Terraform in 2014 did it for whole clouds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(console))
            vo.wait_until("a")
            self.play(FadeIn(cursor))
            for b in buttons:
                self.play(cursor.animate.move_to(b.get_right() + LEFT * 0.4 + DOWN * 0.1), run_time=0.5)
                self.play(Indicate(b, color=HEAD, scale_factor=1.05), run_time=0.5)
            self.play(FadeIn(ask))
            vo.wait_until("b")
            self.play(FadeIn(ctitle), Create(box), LaggedStart(*[FadeIn(ln) for ln in code], lag_ratio=0.25),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(f) for f in flow], lag_ratio=0.3), Create(arrows), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def diff(self):
        p = load("plan")
        head = label(r"A plan is a diff", font_size=36).to_edge(UP, buff=0.3)
        widths = [1.8, 2.6, 1.9]
        act = grid_table([r"name", r"kind", r"setting"], [[n, k, PROP_ACTUAL[n]] for n, k in p["actual"].items()],
                         widths=widths, row_h=0.42, font_size=18, mono_cols=(0, 1, 2))
        des = grid_table([r"name", r"kind", r"setting"], [[n, k, PROP_DESIRED[n]] for n, k in p["desired"].items()],
                         widths=widths, row_h=0.42, font_size=18, mono_cols=(0, 1, 2))
        at = label(r"actual: \ the state file, \ refreshed from the cloud", font_size=19, color=KERN)
        dt = label(r"desired: \ the code", font_size=19, color=DATA)
        left = VGroup(at, act).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        right = VGroup(dt, des).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        tables = VGroup(left, right).arrange(RIGHT, buff=0.5, aligned_edge=UP).next_to(head, DOWN, buff=0.35)
        a_rows = {n: VGroup(*act.cells[i + 1]) for i, n in enumerate(p["actual"])}
        d_rows = {n: VGroup(*des.cells[i + 1]) for i, n in enumerate(p["desired"])}
        out = []
        for n in p["desired"]:
            if n in p["create"]:
                out.append((f"+ {n:<10} create", YES, n))
            elif n in p["update"]:
                out.append((f"~ {n:<10} update   size: {PROP_ACTUAL[n]} -> {PROP_DESIRED[n]}", HEAD, n))
            else:
                out.append((f"  {n:<10} no change", GREY_B, n))
        out += [(f"- {n:<10} destroy", NO, n) for n in p["destroy"]]
        plan = VGroup(*[mono(t, size=16, color=c) for t, c, _ in out]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        summary = mono(f"Plan: {len(p['create'])} to add, {len(p['update'])} to change, {len(p['destroy'])} to "
                       "destroy.", size=16, color=WHITE)
        pblock = VGroup(plan, summary).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        pblock.next_to(tables, DOWN, buff=0.4).align_to(left, LEFT)
        notes = VGroup(
            wrapped_label(r"create what is declared but missing; \ update what differs; \ destroy what exists but "
                          r"is no longer declared", 5.0, font_size=19, color=WHITE),
            wrapped_label(r"the plan is read in review before anything changes: \ a \textbf{destroy} on a database is "
                          r"where mistakes are caught", 5.0, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(pblock, RIGHT, buff=0.6).align_to(pblock, UP)
        notes.align_to(right, LEFT)
        with self.voiceover(
            "How does a tool turn that file into a cloud? It compares two descriptions. <bookmark mark='a'/> On one "
            "side, what exists: Terraform keeps a state file of everything it has made, and refreshes it from the "
            "cloud's own interface. On the other, what the code declares. <bookmark mark='b'/> Match them by name. "
            "The network and the subnet agree, so nothing happens to them. The database exists but is too small, "
            "so it is updated. The queue and the service are declared but missing, so they are created. And the "
            "old cache exists but is no longer declared, so it is destroyed. <bookmark mark='c'/> That diff is the "
            "plan: two to add, one to change, one to destroy. It is printed and reviewed before anything is "
            "touched, and a line that says destroy next to a database is exactly what reviewers look for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(at), FadeIn(dt), FadeIn(act), FadeIn(des))
            vo.wait_until("a")
            self.play(Indicate(act, color=KERN, scale_factor=1.02), run_time=0.8)
            self.play(Indicate(des, color=DATA, scale_factor=1.02), run_time=0.8)
            vo.wait_until("b")
            for (t, c, n), ln in zip(out, plan):
                anims = [FadeIn(ln, shift=RIGHT * 0.15)]
                if n in d_rows and n not in p["destroy"]:
                    anims.append(d_rows[n].animate.set_color(c))
                if n in a_rows:
                    anims.append(a_rows[n].animate.set_color(c))
                self.play(*anims, run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(summary), FadeIn(notes[0]))
            self.play(FadeIn(notes[1]), Indicate(plan[-1], color=NO))
        self.wait(0.4)
        self.clear_scene()

    def order(self):
        p = load("plan")
        head = label(r"Applied in dependency order", font_size=36).to_edge(UP, buff=0.3)
        action = {n: a for a, n in p["steps"]}
        col = {"create": YES, "update": HEAD, "destroy": NO}
        pos = {"vpc": [-5.1, -2.0], "subnet": [-5.1, -0.5], "old-cache": [-5.1, 1.3], "db": [-3.2, 1.0],
               "queue": [-3.2, -2.0], "service": [-1.3, -0.5]}
        nodes = {n: node(n, col.get(action.get(n), GREY_B), dashed=action.get(n) == "destroy").move_to([*xy, 0])
                 for n, xy in pos.items()}
        edges = VGroup()
        for a, ds in DEPS.items():
            for b in ds:
                edges.add(Arrow(nodes[a][0].get_center(), nodes[b][0].get_center(), buff=0.0, stroke_width=2,
                                color=GREY_C, max_tip_length_to_length_ratio=0.1))
        for e, (a, b) in zip(edges, [(a, b) for a, ds in DEPS.items() for b in ds]):    # clip to the boxes' edges
            s, t = nodes[a][0], nodes[b][0]
            d = t.get_center() - s.get_center()
            d = d / np.linalg.norm(d)
            e.put_start_and_end_on(edge_point(s, d), edge_point(t, -d))
        legend = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=0.9),
                                 label(t, font_size=17, color=c)).arrange(RIGHT, buff=0.1)
                          for t, c in ((r"unchanged", GREY_B), (r"update", HEAD), (r"create", YES),
                                       (r"destroy", NO))]).arrange(RIGHT, buff=0.35)
        arrow_key = label(r"arrow: \ \textit{uses}", font_size=17, color=GREY_B)
        VGroup(legend, arrow_key).arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.3).set_x(-3.1)
        steps = VGroup(*[mono(f"{i + 1}  {SIGN[a]} {a:<8} {n}", size=17, color=col[a])
                         for i, (a, n) in enumerate(p["steps"])]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        stitle = label(r"the apply, \ step by step", font_size=20, color=WHITE)
        sblock = VGroup(stitle, steps).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.0, 1.0, 0])
        sblock.align_to([1.0, 0, 0], LEFT)
        badges = {}
        for i, (a, n) in enumerate(p["steps"]):
            ring = Circle(radius=0.17, color=col[a], stroke_width=2, fill_color=BG, fill_opacity=1)
            badges[n] = VGroup(ring, label(f"{i + 1}", font_size=17, color=col[a]).move_to(ring)).next_to(
                nodes[n], UP, buff=0.06).align_to(nodes[n], LEFT if n == "queue" else RIGHT)
        notes = VGroup(
            wrapped_label(r"references in the code are the edges; \ creates and updates run in a topological order "
                          r"\ (Part 18), \ dependencies first; \ destroys run in reverse, \ dependents first", 5.6,
                          font_size=19, color=WHITE),
            wrapped_label(r"\texttt{db} and \texttt{queue} share no path, \ so they can be applied at the same "
                          r"time: \ Part 41's build graph, \ with clouds for files", 5.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(sblock, DOWN, buff=0.45).align_to(sblock, LEFT)
        with self.voiceover(
            "The plan says what to do, but not in what order. <bookmark mark='a'/> The references in the code say "
            "that: the service uses the subnet, the database and the queue; the database lives in the subnet; the "
            "subnet in the network. They form a directed acyclic graph. <bookmark mark='b'/> The tool applies "
            "changes in topological order, the algorithm of Part 18, so that nothing is created before what it "
            "needs. First the database grows; then the queue appears; only then the service, which uses both. "
            "Destroys go the other way, each resource before what it uses, and our planner runs them after "
            "everything else, so the old cache goes last. "
            "<bookmark mark='c'/> And because the database and the queue do not depend on each other, they can be "
            "changed at the same time. It is Part 41's build system again, with machines and networks where the "
            "files were."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(v) for v in nodes.values()], FadeIn(legend), FadeIn(arrow_key))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(e) for e in edges], lag_ratio=0.15), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(stitle), FadeIn(notes[0]))
            for (a, n), ln in zip(p["steps"], steps):
                self.play(Indicate(nodes[n], color=col[a], scale_factor=1.15), FadeIn(badges[n]), FadeIn(ln),
                          run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), Indicate(nodes["db"], color=YES), Indicate(nodes["queue"], color=YES))
        self.wait(0.4)
        self.clear_scene()

    def drift(self):
        head = label(r"Drift", font_size=36).to_edge(UP, buff=0.3)

        def panel(title, color, value):
            frame = RoundedRectangle(width=3.6, height=1.9, corner_radius=0.12, stroke_color=color, stroke_width=2)
            t = label(title, font_size=20, color=color).next_to(frame.get_top(), DOWN, buff=0.18)
            v = mono(f'db  size = "{value}"', size=17, color=WHITE).move_to(frame).shift(DOWN * 0.2)
            return VGroup(frame, t, v)
        code = panel(r"the code", DATA, "large")
        state = panel(r"the state file", KERN, "large")
        cloud = panel(r"the cloud", LAM, "large")
        row = VGroup(code, state, cloud).arrange(RIGHT, buff=0.85).next_to(head, DOWN, buff=0.45)
        hand = wrapped_label(r"someone resizes the database by hand, \ in the console, \ during an incident", 3.6,
                             font_size=18, color=NO).next_to(cloud, DOWN, buff=0.25)
        illus = label(r"illustrative", font_size=16, color=GREY_B).next_to(hand, DOWN, buff=0.12)
        new_cloud = mono('db  size = "xlarge"', size=17, color=NO).move_to(cloud[2])
        new_state = mono('db  size = "xlarge"', size=17, color=NO).move_to(state[2])
        refresh = Arrow(cloud[0].get_left(), state[0].get_right(), buff=0.05, color=GREY_B, stroke_width=2,
                        max_tip_length_to_length_ratio=0.3)
        rl = label(r"refresh", font_size=16, color=GREY_B).next_to(refresh, UP, buff=0.08)
        planl = mono("~ db  update   size: xlarge -> large", size=17, color=HEAD).next_to(row, DOWN, buff=1.2)
        planl.set_x(-1.9)
        choices = VGroup(
            tag_box("apply: put it back", color=YES, size=16),
            tag_box("edit the code: keep it", color=DATA, size=16),
        ).arrange(RIGHT, buff=0.6).next_to(planl, DOWN, buff=0.35).align_to(planl, LEFT)
        note = wrapped_label(r"run the plan on a schedule, \ and alert on any diff no one wrote; \ a Kubernetes "
                             r"controller \ (chapter 4) \ is the same idea run continuously: \ level-triggered "
                             r"reconciliation, \ forever", 12.4, font_size=19, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Code and cloud agree only until someone changes the cloud directly. <bookmark mark='a'/> After apply, "
            "all three agree: the code, the state file and the real database. <bookmark mark='b'/> Then, during "
            "an incident, someone makes the database bigger by hand, in the console. The cloud has drifted from "
            "the code, and nothing says so. <bookmark mark='c'/> The next plan refreshes its state from the cloud, "
            "finds the difference, and proposes to undo it: a change nobody wrote. <bookmark mark='d'/> Someone "
            "must decide: apply, and put it back, or edit the code to keep it. <bookmark mark='e'/> Teams run the "
            "plan on a schedule and alert on any difference. A Kubernetes controller, from chapter four, is the "
            "same idea run without stopping: it reconciles the level, again and again, and drift lasts seconds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row))
            vo.wait_until("a")
            self.play(*[Indicate(p[2], color=YES) for p in row])
            vo.wait_until("b")
            self.play(FadeIn(hand), FadeIn(illus), Transform(cloud[2], new_cloud), cloud[0].animate.set_stroke(NO))
            vo.wait_until("c")
            self.play(GrowArrow(refresh), FadeIn(rl))
            self.play(Transform(state[2], new_state))
            self.play(Indicate(code[2], color=DATA), Indicate(state[2], color=NO))
            self.play(FadeIn(planl, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c) for c in choices], lag_ratio=0.4))
            vo.wait_until("e")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    def immutable(self):
        head = label(r"Immutable infrastructure", font_size=36).to_edge(UP, buff=0.3)
        lt = label(r"patched in place", font_size=22, color=NO)
        rt = label(r"replaced from an image", font_size=22, color=YES)

        def server(color=GREY_B):
            return RoundedRectangle(width=1.6, height=0.7, corner_radius=0.08, stroke_color=color, stroke_width=2,
                                    fill_color=color, fill_opacity=0.12)
        sa, sb = server(), server()
        VGroup(sa, sb).arrange(RIGHT, buff=0.7)
        for s, n in ((sa, "web-1"), (sb, "web-2")):
            s.add(mono(n, size=16, color=WHITE).move_to(s))
        mut = VGroup(sa, sb)
        VGroup(lt, mut).arrange(DOWN, buff=0.35)
        patches_a = ["v1.0", "patch 7", "edit by hand", "patch 8"]
        patches_b = ["v1.0", "patch 8", "hotfix"]

        def stack(srv, items):
            g = VGroup(*[tag_box(t, color=KERN if k else GREY_B, size=15, w=1.6, h=0.38) for k, t in enumerate(items)])
            g.arrange(UP, buff=0.06).next_to(srv, UP, buff=0.08)
            return g
        left = VGroup(lt, mut).move_to([-3.6, -0.2, 0])
        lt.next_to(head, DOWN, buff=0.35).set_x(left.get_x())
        sta, stb = stack(sa, patches_a), stack(sb, patches_b)
        snow = wrapped_label(r"same role, \ different machines: \ \textbf{snowflakes} nobody can rebuild", 4.6,
                             font_size=19, color=NO).next_to(mut, DOWN, buff=0.3)
        img = tag_box("image a41f", color=DATA, size=16, w=2.0)
        insts = VGroup(*[server(DATA) for _ in range(3)]).arrange(RIGHT, buff=0.25)
        for s in insts:
            s.add(mono("a41f", size=15, color=WHITE).move_to(s))
        VGroup(img, insts).arrange(DOWN, buff=0.6)
        VGroup(img, insts).move_to([3.4, 1.0, 0])
        rt.move_to([3.4, lt.get_y(), 0])
        links = VGroup(*[Line(img.get_bottom(), s.get_top(), color=GREY_C, stroke_width=1.5) for s in insts])
        img2 = tag_box("image c93e", color=YES, size=16, w=2.0).next_to(img, RIGHT, buff=0.35)
        news = VGroup()
        for s in insts:
            n = server(YES).move_to(s)
            n.add(mono("c93e", size=15, color=WHITE).move_to(n))
            news.add(n)
        links2 = VGroup(*[Line(img2.get_bottom(), s.get_top(), color=GREY_C, stroke_width=1.5) for s in insts])
        rnote = wrapped_label(r"build a new image, \ start new machines from it, \ retire the old ones; \ rollback "
                              r"is pointing back at \texttt{a41f}", 5.4, font_size=19,
                              color=YES).next_to(insts, DOWN, buff=0.35)
        illus = label(r"image names illustrative", font_size=16, color=GREY_B).next_to(rnote, DOWN, buff=0.2)
        foot = wrapped_label(r"images are content-addressed \ (chapter 3, \ Part 41), \ so a name means exactly one "
                             r"set of bytes; \ Kief Morris, \ \textit{Infrastructure as Code}", 12.4, font_size=19,
                             color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Drift has a deeper cure: never change a running machine at all. <bookmark mark='a'/> A server that is "
            "patched in place collects history. One got patch seven and an edit by hand; its twin got patch eight "
            "and a hotfix. Both are called web servers, and no two are the same: snowflakes, that nobody could "
            "build again. <bookmark mark='b'/> Immutable infrastructure bakes everything into an image, and every "
            "machine starts from it unchanged. <bookmark mark='c'/> To change anything, build a new image, start "
            "new machines from it, and retire the old ones, one at a time. To roll back, point at the old image "
            "again. <bookmark mark='d'/> Because images are content-addressed, as in chapter three and Part 41, "
            "a name means exactly one set of bytes, and every machine started from it is the same."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lt), FadeIn(rt), FadeIn(mut))
            vo.wait_until("a")
            for k in range(max(len(patches_a), len(patches_b))):
                anims = [FadeIn(st[k], shift=DOWN * 0.15) for st in (sta, stb) if k < len(st)]
                self.play(*anims, run_time=0.6)
            self.play(FadeIn(snow))
            vo.wait_until("b")
            self.play(FadeIn(img), Create(links), LaggedStart(*[FadeIn(s) for s in insts], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(img2, shift=LEFT * 0.2))
            for s, n in zip(insts, news):
                self.play(FadeOut(s, shift=DOWN * 0.2), FadeIn(n, shift=DOWN * 0.2), run_time=0.6)
            self.play(ReplacementTransform(links, links2))
            self.play(FadeIn(rnote), FadeIn(illus))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, grid_table)
