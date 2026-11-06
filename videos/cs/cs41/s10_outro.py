from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs41.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ Version Control, \ Builds and Dependencies", font_size=34).to_edge(UP,
                                                                                                    buff=0.3)
        tiles = Group(
            tile(MathTex(r"\text{id} = H(\text{content})", font_size=44, color=DATA), r"a Merkle graph", DATA),
            tile(MathTex(r"\text{base},\ \text{ours},\ \text{theirs}", font_size=40, color=HEAD),
                 r"three-way merge", HEAD),
            tile(MathTex(r"\lceil \log_2 n \rceil", font_size=60, color=YES), r"bisect", YES),
            tile(label(r"hash, \ not time", font_size=40, color=LAM), r"early cutoff", LAM),
            tile(MathTex(r"\text{3-SAT} \le \text{install}", font_size=44, color=NO), r"NP-complete versions", NO),
            tile(MathTex(r"(1-p)^b", font_size=60, color=KERN), r"merge queues", KERN),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. A git object store whose names match the real git, and the Merkle graph "
            "those names form. Merge bases, three-way merges and their conflicts, rebasing, and bisection in "
            "logarithmic time. Deltas that store forty versions of a file in a thirtieth of the space. A build "
            "system that trusts hashes rather than clocks and stops early, and the work and span of building in "
            "parallel. Package versions as satisfiability, NP-complete by a reduction you can read. And merge "
            "queues, test selection, canaries and migrations that deliver a change a little at a time. Three "
            "machines, one idea: name things by what they contain, and redo only what a change can reach."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the browser's caches and content-addressed assets", [42]),
            (r"service versions, \ API compatibility and rollouts", [43]),
            (r"experiments and the statistics of canaries", [44]),
            (r"releases under incident pressure; \ rollback", [50]),
            (r"software supply-chain security, \ trusting trust", [55, 61]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 42's browser caches assets by content hash. Part 43 versions the interfaces "
            "between services and rolls them out compatibly. Part 44 turns canaries into experiments with proper "
            "statistics. Part 50 releases and rolls back under the pressure of an incident. And Parts 55 and 61 "
            "return to the supply chain, and to whether a compiler can be trusted at all."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"git", r"small commits with messages that say why; \ rebase your own work, \ merge shared work"),
            (r"history", r"\texttt{git bisect run} with a test script; \ \texttt{git reflog} before panicking"),
            (r"builds", r"declare every input; \ hermetic, \ cached, \ reproducible where it matters"),
            (r"dependencies", r"lockfiles committed; \ update deliberately; \ fewer, \ better-kept dependencies"),
            (r"delivery", r"trunk-based development, \ a merge queue, \ canaries, \ flags and expand--contract"),
        ])
        with self.voiceover(
            "In practice. Make small commits whose messages say why, rebase work that is only yours and merge work "
            "that is shared. Let git bisect run your test script when something breaks, and check the reflog before "
            "you panic. Declare every input your build uses, and make it hermetic and cached. Commit lockfiles, "
            "update dependencies on purpose, and prefer fewer, better-kept ones. And deliver through a merge queue, "
            "a canary, feature flags and expand-and-contract migrations."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that changing one file changes the ids of exactly the trees on its path and the commit, \ and "
            r"that two snapshots share every other object.",
            r"Give a history with two merge bases, \ and show that merging with either one alone can produce a "
            r"different result.",
            r"Prove that bisection needs $\lceil \log_2 n \rceil$ tests on a linear history, \ and that no strategy "
            r"needs fewer in the worst case.",
            r"Show that a build with verifying traces is correct if every task is deterministic and declares all its "
            r"inputs, \ and give a timestamp scenario that makes Make incorrect.",
            r"\textit{Build.} \ Add constructive traces \ (a shared output cache) \ to our build engine, \ and "
            r"measure a second machine's build.",
            r"$\bigstar$ \textit{Research.} \ Find the merge-queue policy that maximizes throughput when each "
            r"change has its own learned failure probability.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give our build engine a shared cache of outputs, keyed by the hash of their inputs, and "
            "measure how little a second machine must do. The last, marked with a star, is a research problem: the "
            "best merge-queue policy when every change carries its own learned chance of failing."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 42, \ The Browser and the Web", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"from a URL to pixels: \ parsing, \ the DOM, \ layout and painting", HEAD),
            (r"JavaScript's event loop and the cost of a frame", YES),
            (r"the same-origin policy, \ cookies and cross-site attacks", NO),
            (r"caches, \ service workers and offline apps", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 42: the browser and the web. How a URL becomes pixels, through parsing, the document "
            "tree, layout and painting; JavaScript's event loop and the budget of a single frame; the same-origin "
            "policy and the attacks it stops; and caches and service workers that keep a web app working offline."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Chacon and Straub, \textit{Pro Git}; \ Humble and Farley, \textit{Continuous Delivery}",
             r"Winters, Manshreck and Wright, \textit{Software Engineering at Google}, \ ch. 16--24"],
            [r"Merkle \ (1979); \ Myers \ (1986); \ Feldman \ (1979); \ Dolstra \ (2006)",
             r"Mokhov, Mitchell and Peyton Jones \ (2018); \ Potvin and Levenberg \ (2016)",
             r"Di Cosmo et al. \ (2006); \ Weizenbaum \ (2018); \ Cox \ (2018, \ minimal version selection)",
             r"Apel et al. \ (2011); \ Spinellis \ (2012); \ Ananthanarayanan et al. \ (2019, \ SubmitQueue)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES)
