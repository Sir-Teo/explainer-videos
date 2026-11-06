from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs41.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, code_block, grid_table, load, mono, trace)


class Builds(VoiceoverScene):
    def construct(self):
        self.card()
        self.make()
        self.lies()
        self.recursive()
        self.lighting()
        self.carte()
        self.cache()
        self.parallel()
        self.hermetic()
        self.nix()

    def card(self):
        card = chapter_card(4, r"Build systems", r"What is the least work that brings everything up to date?",
                            lit=(1976, 2018), extra=((1976, r"Feldman: \ Make"), (2006, r"Dolstra: \ Nix"),
                                                     (2018, r"Mokhov, Mitchell and Peyton Jones: \ à la carte")),
                            part=PART)
        with self.voiceover("Chapter four. Build systems."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def make(self):
        head = label(r"Make", font_size=36).to_edge(UP, buff=0.3)
        mk = code_block(["job: main.o count.o io.o", "\tcc -o job main.o count.o io.o", "",
                         "main.o: main.c count.h", "\tcc -c main.c", "", "count.o: count.c count.h",
                         "\tcc -c count.c"], size=17).move_to([-3.6, 0.3, 0])
        nodes = {}
        pos = {"job": [3.4, 2.0], "main.o": [1.6, 0.6], "count.o": [3.4, 0.6], "io.o": [5.2, 0.6],
               "main.c": [1.0, -0.9], "count.h": [2.6, -0.9], "count.c": [4.2, -0.9], "io.c": [5.6, -0.9]}
        for k, (x, y) in pos.items():
            col = HEAD if k == "job" else (DATA if k.endswith(".o") else YES)
            r = RoundedRectangle(width=1.3, height=0.5, corner_radius=0.08, stroke_color=col, fill_color=col,
                                 fill_opacity=0.12).move_to([x, y, 0])
            nodes[k] = VGroup(r, label(rf"\texttt{{{k}}}", font_size=15, color=WHITE).move_to(r))
        deps = [("job", "main.o"), ("job", "count.o"), ("job", "io.o"), ("main.o", "main.c"), ("main.o", "count.h"),
                ("count.o", "count.c"), ("count.o", "count.h"), ("io.o", "io.c")]
        lines = VGroup(*[Arrow(nodes[a][0].get_bottom(), nodes[b][0].get_top(), buff=0.05, stroke_width=1.8,
                               color=GREY_B, max_tip_length_to_length_ratio=0.12) for a, b in deps])
        notes = VGroup(
            wrapped_label(r"Stuart Feldman \ (Bell Labs, 1976): \ targets, \ their prerequisites, \ and the "
                          r"commands that make them", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"rebuild a target whose prerequisites are newer than it, \ in an order where everything "
                          r"comes after what it needs: \ a topological sort \ (Part 18)", 12.4, font_size=21,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Stuart Feldman wrote Make at Bell Labs in 1976, the story goes, after a colleague lost a morning "
            "debugging a program that had simply not been recompiled. <bookmark mark='a'/> A makefile lists targets, "
            "the files each one needs, and the command that makes it. Together they form a directed acyclic graph. "
            "<bookmark mark='b'/> Make walks it in topological order, Part 18's algorithm, so that every target is "
            "built after what it needs, and rebuilds a target only when one of its prerequisites is newer than it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(mk))
            vo.wait_until("a")
            self.play(*[FadeIn(v) for v in nodes.values()], Create(lines), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def lies(self):
        b = load("builds")
        head = label(r"Timestamps lie", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r["edit"], f"{r['make']}", f"{r['traces']}"] for r in b["rows"]]
        tab = grid_table([rf"after this edit \ ({b['targets']} targets)", r"make rebuilds",
                          r"hashes + early cutoff"], rows, widths=[5.8, 2.6, 3.6], row_h=0.48, font_size=20,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for i, r in enumerate(b["rows"], 1):
            if r["make"] > r["traces"]:
                tab.cells[i][1].set_color(NO)
                tab.cells[i][2].set_color(YES)
        lines = VGroup(
            wrapped_label(rf"{b['sources']} source files and {b['headers']} headers; \ one header is included by "
                          rf"{b['h3_users']} sources", 12.4, font_size=19, color=GREY_A),
            wrapped_label(r"\textbf{verifying traces}: \ remember the hash of every input a target was built from; \ "
                          r"rebuild only if one differs; \ \textbf{early cutoff}: \ if a rebuilt object is "
                          r"identical, \ stop there", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Modification times are a guess about content, and the guess is often wrong. We built both kinds of "
            "build system, on a project of two hundred source files and twenty headers. <bookmark mark='a'/> "
            "Change a comment in one source file. Make recompiles it, then relinks the library and reruns the tests, "
            "although the compiled object is byte for byte the same. A build that remembers the hash of every input, "
            "and stops when a rebuilt output is unchanged, recompiles one file and stops. <bookmark mark='b'/> A real "
            "change in a header used by thirty-nine files rebuilds the same forty-one targets in both. "
            "<bookmark mark='c'/> But check out the project afresh, which gives every file a new time and the same "
            "content: Make rebuilds all two hundred and two targets, and the hashing build rebuilds none."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule),
                      FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[2])), FadeIn(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(VGroup(*tab.cells[4])), FadeIn(VGroup(*tab.cells[5])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[6])))
        self.wait(0.4)
        self.clear_scene()

    def carte(self):
        head = label(r"Build systems \`a la carte", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"topological", r"Make", r"Ninja", r"CloudBuild, \ Buck"],
                [r"restarting", r"Excel", r"---", r"Bazel"],
                [r"suspending", r"---", r"Shake", r"Cloud Shake, \ Nix"]]
        tab = grid_table([r"scheduler $\downarrow$ \ rebuilder $\to$", r"dirty bit", r"verifying traces",
                          r"constructive traces"], rows, widths=[3.6, 2.8, 3.2, 3.2], row_h=0.55, font_size=20,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        lines = VGroup(
            wrapped_label(r"Mokhov, Mitchell and Peyton Jones \ (2018): \ every build system is a \textbf{scheduler} "
                          r"\ (in what order to visit tasks) \ times a \textbf{rebuilder} \ (whether a task must rerun); "
                          r"\ the table above is a simplified version of theirs", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"\textbf{constructive traces} store outputs too, \ by the hash of their inputs: \ a "
                          r"\textbf{shared cache}, \ so a file compiled on one machine is downloaded by every other",
                          12.4, font_size=20, color=YES),
            wrapped_label(r"a spreadsheet is a build system: \ cells are targets, \ formulas are rules, \ and "
                          r"\textit{dynamic} dependencies \ (\texttt{INDIRECT}) \ are discovered while building", 12.4,
                          font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "In 2018 Andrey Mokhov, Neil Mitchell and Simon Peyton Jones showed that the whole zoo of build systems "
            "comes from two independent choices. <bookmark mark='a'/> A scheduler decides the order in which tasks "
            "are visited: in topological order, or by starting a task and restarting or suspending it when it "
            "discovers a dependency it did not declare. A rebuilder decides whether a task must run again: a dirty "
            "bit, verifying traces like ours, or constructive traces. <bookmark mark='b'/> Constructive traces store "
            "the outputs too, keyed by the hash of the inputs, which turns the build into a shared cache: a file "
            "compiled on one machine is downloaded by everyone else. <bookmark mark='c'/> And Excel is a build "
            "system: cells are targets and formulas are rules, with dependencies that are only discovered while "
            "computing."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def parallel(self):
        p = load("parallel")
        head = label(r"Parallel builds: \ work and span", font_size=36).to_edge(UP, buff=0.3)
        import math
        rows = p["rows"]
        g = axes([0, 8.3, 1], [0, 260, 50], x_length=6.6, y_length=3.8, x_label=r"workers \ (log$_2$)",
                 y_label=r"seconds for a clean build", xticks=range(0, 9, 2), yticks=range(50, 251, 50),
                 fx=lambda v: f"{2 ** int(v)}").move_to([-2.8, -0.4, 0])
        ax = g.ax
        meas = VGroup(trace(ax, [(math.log2(r["workers"]), r["time"]) for r in rows], HEAD, width=3),
                      *[Dot(ax.c2p(math.log2(r["workers"]), r["time"]), radius=0.06, color=HEAD) for r in rows])
        span = DashedLine(ax.c2p(0, p["span"]), ax.c2p(8.3, p["span"]), color=NO)
        sl = label(rf"span: \ {p['span']:.0f} s", font_size=17, color=NO).next_to(ax.c2p(8.3, p["span"]), UP,
                                                                                buff=0.08).shift(LEFT * 0.8)
        notes = VGroup(
            wrapped_label(rf"200 compiles averaging 1 s, \ then an 8 s link and 20 s of tests: \ work "
                          rf"$W = {p['work']:.0f}$ s, \ span $S = {p['span']:.0f}$ s", 5.0, font_size=19,
                          color=GREY_A),
            MathTex(r"\max\!\left(\tfrac{W}{P},\ S\right) \le T_P \le \tfrac{W}{P} + S", font_size=30, color=YES),
            wrapped_label(r"Brent's bound \ (Part 10): \ past 32 workers the link and the tests, \ which cannot be "
                          r"split, \ are all that is left", 5.0, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.1, -0.2, 0])
        with self.voiceover(
            "Independent tasks can be built at the same time. <bookmark mark='a'/> A clean build of our project "
            "has two hundred compiles of about a second each, then an eight-second link and twenty seconds of "
            "tests: two hundred and thirty-five seconds of work in total, and a longest chain, the span, of "
            "thirty-four. <bookmark mark='b'/> Part 10's bound says the time on P workers lies between the larger "
            "of work over P and the span, and their sum. <bookmark mark='c'/> One worker takes the full two hundred "
            "and thirty-five seconds; eight take fifty-four; beyond thirty-two, nothing improves, because the "
            "link and the tests cannot be split. Speeding up builds past that point means making the critical "
            "path itself shorter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(span), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(meas), FadeIn(notes[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def hermetic(self):
        head = label(r"Hermetic and reproducible", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{hermetic}: \ a task sees only its declared inputs \ (a sandbox), \ so its "
                          r"hash really does name everything it depends on", 12.4, font_size=23, color=YES),
            wrapped_label(r"\textbf{reproducible}: \ the same inputs give bit-identical outputs \ --- \ no timestamps, "
                          r"\ paths or random orders baked into the files", 12.4, font_size=23, color=HEAD),
            wrapped_label(r"\textbf{Nix} \ (Dolstra, 2006): \ every package lives under the hash of all its "
                          r"inputs, \ \texttt{/nix/store/<hash>-name}; \ \textbf{Bazel} \ (Google, \ open-sourced "
                          r"2015): \ remote execution and caching for huge builds", 12.4, font_size=23, color=DATA),
            wrapped_label(r"the payoff: \ anyone can rebuild a released binary and check that it matches \ --- \ a "
                          r"defence against a compromised build machine \ (Chapter 7)", 12.4, font_size=23,
                          color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Hash-based building only works if the hashes are honest. <bookmark mark='a'/> A hermetic build runs each "
            "task in a sandbox that sees only its declared inputs, so that the hash of those inputs really names "
            "everything the result depends on. <bookmark mark='b'/> A reproducible build produces bit-identical "
            "outputs from the same inputs, which means banishing timestamps, absolute paths and random orders from "
            "the files it writes. <bookmark mark='c'/> Eelco Dolstra's Nix stores every package under the hash of "
            "all its inputs; Google's Bazel distributes execution and caching across machines. "
            "<bookmark mark='d'/> The payoff goes beyond speed: if builds are reproducible, anyone can rebuild a "
            "released program and check that it matches, which defends against a build machine that has been "
            "compromised."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def cache(self):
        c = load("cache")
        head = label(r"A shared cache", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r["step"], f"{r['ran']}", f"{r['fetched']}"] for r in c["rows"]]
        tab = grid_table([r"what happens", r"tasks run", r"outputs downloaded"], rows, widths=[5.0, 2.4, 3.6],
                         row_h=0.5, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).set_x(0)
        for i in range(1, len(rows) + 1):
            tab.cells[i][2].set_color(YES if c["rows"][i - 1]["fetched"] else WHITE)
        lines = VGroup(
            wrapped_label(r"constructive traces: \ every output is stored under the hash of the task and of all its "
                          r"inputs; \ any machine whose inputs hash the same downloads it instead of building", 12.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"a team builds each distinct thing once: \ the second engineer, \ and the CI machine, \ "
                          r"start where the first left off", 12.4, font_size=21, color=YES),
            wrapped_label(r"it is safe only if tasks are hermetic and deterministic: \ a cached output built from an "
                          r"undeclared input poisons everyone's build", 12.4, font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "We added constructive traces to our build engine: a cache shared between machines, holding every "
            "output under the hash of the task and all of its inputs. <bookmark mark='a'/> Machine A builds the "
            "project from scratch: two hundred and two tasks. Machine B checks out the same commit: it runs nothing "
            "and downloads all two hundred and two outputs. A changes a header and rebuilds the forty-one affected "
            "targets; B pulls the change and downloads those forty-one. <bookmark mark='b'/> A team builds each "
            "distinct thing once, and every other engineer and every CI machine starts where the first left off. "
            "<bookmark mark='c'/> The price is discipline: a task that reads an input it did not declare can put a "
            "wrong output in the cache, and then everyone's build is wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def recursive(self):
        head = label(r"Recursive Make considered harmful", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"large projects once ran one Make per directory, \ each seeing only its own part of the "
                          r"graph", 12.4, font_size=23, color=WHITE),
            wrapped_label(r"Peter Miller \ (1997): \ a dependency that crosses directories is invisible, \ so builds "
                          r"are either wrong \ (something stale is not rebuilt) \ or slow \ (everything is rebuilt to "
                          r"be safe)", 12.4, font_size=23, color=NO),
            wrapped_label(r"the cure is the whole graph in one place: \ a build is only as correct as the dependency "
                          r"graph it can see", 12.4, font_size=23, color=YES),
            wrapped_label(r"modern build files \ (Bazel's \texttt{BUILD}, \ Buck, \ Pants) \ declare small targets "
                          r"everywhere, \ but one tool loads them all into one graph", 12.4, font_size=23,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "One famous mistake shows what a build needs. <bookmark mark='a'/> Large projects used to run a separate "
            "Make in each directory, each one seeing only its own part of the dependency graph. "
            "<bookmark mark='b'/> In 1997 Peter Miller explained why this fails: a dependency that crosses "
            "directories is invisible, so the build is either wrong, leaving something stale, or slow, rebuilding "
            "everything just to be safe. <bookmark mark='c'/> The cure is to give one tool the whole graph: a build "
            "can only be as correct as the dependencies it can see. <bookmark mark='d'/> Modern build files, Bazel's "
            "among them, declare small targets in every directory, but a single tool loads all of them into one "
            "graph before doing anything."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def lighting(self):
        d = load("smallgraph")
        head = label(r"The minimal rebuild", font_size=36).to_edge(UP, buff=0.3)
        objs = [t for t in d["order"] if t.endswith(".o")]
        pos = {}
        for j, h in enumerate(d["headers"]):
            pos[h] = [-4.5 + j * 3.0, -2.4]
        for i, s in enumerate(d["sources"]):
            pos[s] = [-6.2 + i * 1.13, -1.2]
        for i, o in enumerate(objs):
            pos[o] = [-6.2 + i * 1.13, 0.4]
        pos["lib.a"] = [0, 1.7]
        pos["tests.log"] = [0, 2.6]
        nodes = {}
        for k, (x, y) in pos.items():
            col = HEAD if k.endswith(".h") else (DATA if k.endswith(".c") else (LAM if k.endswith(".o") else YES))
            w = 0.95 if not k.endswith(".h") else 1.1
            r = RoundedRectangle(width=w, height=0.42, corner_radius=0.06, stroke_color=col, fill_color=col,
                                 fill_opacity=0.12).move_to([x, y, 0])
            nodes[k] = VGroup(r, label(rf"\texttt{{{k}}}", font_size=12, color=WHITE).move_to(r))
        edges = VGroup()
        for t, ins in d["deps"].items():
            for x in ins:
                if x in nodes:
                    edges.add(Line(nodes[x][0].get_top(), nodes[t][0].get_bottom(), color=GREY_D,
                                   stroke_width=1))
        hit = [nodes[t] for t in d["rebuilt"]]
        notes = wrapped_label(rf"change \texttt{{{d['changed']}}}: \ {len(d['rebuilt'])} of {len(d['order'])} targets "
                              r"rebuild \ --- \ exactly those reachable from it in the graph; \ the others keep their "
                              r"traces and are skipped", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Here is the idea of a minimal rebuild on a project small enough to draw: twelve sources, four headers, "
            "twelve objects, a library and a test report. <bookmark mark='a'/> Change one header. "
            "<bookmark mark='b'/> The targets that must be rebuilt are exactly those reachable from it along the "
            "graph's edges: the six objects whose sources include it, then the library and the tests. Every other "
            "target's recorded inputs still match, so it is skipped without being looked at again. "
            "<bookmark mark='c'/> That reachable set is the least work any correct build system can do, and it is "
            "the same set that test selection computed over imports: one idea, used twice."
        ) as vo:
            self.play(FadeIn(head), Create(edges), *[FadeIn(n) for n in nodes.values()])
            vo.wait_until("a")
            self.play(nodes[d["changed"]][0].animate.set_fill(NO, 0.7))
            vo.wait_until("b")
            self.play(LaggedStart(*[n[0].animate.set_fill(NO, 0.5) for n in hit], lag_ratio=0.2), FadeIn(notes),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(*[Indicate(n, color=NO) for n in hit[-2:]])
        self.wait(0.4)
        self.clear_scene()

    def nix(self):
        from explainer.cs.vcs.build import _h
        head = label(r"A package named by its inputs", font_size=36).to_edge(UP, buff=0.3)
        inputs = [("source", "job-1.0.tar.gz"), ("compiler", "gcc-13.2"), ("libc", "glibc-2.38"),
                  ("flags", "-O2")]
        h1 = _h(*[v for _, v in inputs])
        h2 = _h(*[v if k != "flags" else "-O3" for k, v in inputs])
        rows = VGroup(*[VGroup(label(k, font_size=19, color=GREY_A), mono(v, size=17, color=WHITE)).arrange(
            RIGHT, buff=0.3) for k, v in inputs]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rows.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        p1 = mono(f"/nix/store/{h1}-job-1.0", size=19, color=YES)
        p2 = mono(f"/nix/store/{h2}-job-1.0", size=19, color=HEAD)
        paths = VGroup(VGroup(label(r"installed at", font_size=19, color=GREY_A), p1).arrange(DOWN,
                       aligned_edge=LEFT, buff=0.1),
                       VGroup(label(r"with \texttt{-O3} instead: \ a different package, \ side by side", font_size=19,
                                    color=GREY_A), p2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.6, 0.9, 0])
        lines = VGroup(
            wrapped_label(r"every input, \ including the compiler and every library, \ goes into the name: \ two "
                          r"builds with the same name are the same build, \ and two versions of anything can be "
                          r"installed at once \ --- \ the diamond disappears here too", 12.4, font_size=21,
                          color=WHITE),
            wrapped_label(r"upgrading is installing new paths and switching one pointer; \ rolling back is "
                          r"switching it back", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Nix takes content addressing all the way. <bookmark mark='a'/> A package is described by every input "
            "that goes into building it: its source, the exact compiler, the exact libraries, the flags. "
            "<bookmark mark='b'/> It is installed under a directory named by the hash of all of them. Change one "
            "flag and you get a different name, a different package, installed side by side with the first. "
            "<bookmark mark='c'/> Two builds with the same name are the same build, two versions of anything can "
            "coexist, so the diamond disappears here too, and upgrading means installing new paths and switching "
            "one pointer, which is also how you roll back: switch it again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows))
            vo.wait_until("b")
            self.play(FadeIn(paths))
            vo.wait_until("c")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, NO)
