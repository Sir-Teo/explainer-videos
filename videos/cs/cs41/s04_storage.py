from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs41.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace)


class Storage(VoiceoverScene):
    def construct(self):
        self.card()
        self.packs()
        self.sizes()
        self.window()
        self.monorepo()
        self.patches()

    def card(self):
        card = chapter_card(3, r"Storing history", r"How can every version of everything fit?", lit=(2005, 2016),
                            extra=((2005, r"packfiles"), (2016, r"Potvin and Levenberg: \ Google's monorepo")),
                            part=PART)
        with self.voiceover("Chapter three. Storing history."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def packs(self):
        d = load("delta")
        rows = d["rows"]
        head = label(r"Deltas", font_size=36).to_edge(UP, buff=0.3)
        n = len(rows)
        top = max(r["loose"] for r in rows) / 1024
        g = axes([0, n + 1, 10], [0, top * 1.1, 40], x_length=7.4, y_length=3.6, x_label=r"version of "
                 r"\texttt{videos/cs/SYLLABUS.md}, \ oldest first", y_label=r"KB stored", xticks=(1, 10, 20, 30, 40),
                 yticks=range(40, int(top * 1.1), 40)).move_to([-2.4, -0.4, 0])
        ax = g.ax
        loose = trace(ax, [(i + 1, r["loose"] / 1024) for i, r in enumerate(rows)], NO, width=3)
        delta = trace(ax, [(i + 1, r["delta"] / 1024) for i, r in enumerate(rows)], YES, width=3)
        notes = VGroup(
            label(rf"{d['versions']} committed versions of this series' syllabus", font_size=19, color=GREY_A),
            label(rf"each stored whole, \ compressed: \ {d['loose_total'] / 2 ** 20:.1f} MB", font_size=20,
                  color=NO),
            label(rf"each as a delta from the last: \ {d['delta_total'] / 1024:.0f} KB", font_size=20, color=YES),
            wrapped_label(r"loose objects are whole files; \ \texttt{git gc} packs them, \ storing most as "
                          r"deltas against a similar object \ (often a later version, \ so the newest is fast), \ "
                          r"in chains of bounded depth", 5.0, font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, 0.0, 0])
        with self.voiceover(
            "If every version of every file is a whole object, history should be enormous. <bookmark mark='a'/> "
            "This repository's syllabus has been committed forty times, growing to three hundred kilobytes. Stored "
            "whole, even compressed, the forty versions take four megabytes. <bookmark mark='b'/> Stored as the "
            "difference from the version before, a hundred and fifty kilobytes: nearly thirty times less. "
            "<bookmark mark='c'/> Git does this when it packs objects: it finds similar objects, often versions of "
            "the same path, and stores all but one as deltas, copy instructions and new bytes, the same idea as "
            "Part 21's diff, in chains of bounded depth so that reading any version stays fast. The object names do "
            "not change when objects are packed: content addressing describes what an object is, and packing is "
            "only a decision about how to store it, made again whenever git finds a better one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(loose), FadeIn(notes[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(delta), FadeIn(notes[2]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def monorepo(self):
        head = label(r"One repository, \ or many?", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{Google's monorepo} \ (Potvin and Levenberg, 2016): \ one repository for most of "
                          r"the company's code: \ about two billion lines and 86 TB, \ some 25{,}000 engineers \ "
                          r"making about 16{,}000 changes a day, \ automated systems 24{,}000 more, \ on a custom system \ (Piper)", 12.4,
                          font_size=22, color=HEAD),
            wrapped_label(r"gains: \ one version of everything, \ atomic changes across projects, \ refactoring "
                          r"everywhere at once; \ costs: \ custom tooling, \ builds that must be incremental", 12.4,
                          font_size=22, color=YES),
            wrapped_label(r"\textbf{polyrepos}: \ independent histories and releases, \ at the price of versioning "
                          r"between them \ --- \ Chapter 5's dependency problem", 12.4, font_size=22, color=DATA),
            wrapped_label(r"git at scale: \ shallow clones \ (recent history only), \ partial clones \ (blobs on "
                          r"demand), \ sparse checkouts \ (some directories)", 12.4, font_size=22, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "How much code can one history hold? <bookmark mark='a'/> In 2016 Rachel Potvin and Josh Levenberg "
            "described Google's monorepo: most of the company's code in a single repository, about two billion lines "
            "and eighty-six terabytes, changed by some twenty-five thousand engineers, on a custom system called "
            "Piper. <bookmark mark='b'/> One repository means one version of everything and atomic changes across "
            "projects; it requires tooling that git alone does not provide, and builds that only redo what changed. "
            "<bookmark mark='c'/> The alternative, many repositories, gives each project its own history and "
            "releases, at the price of the version management of this part's dependency chapter. "
            "<bookmark mark='d'/> Git itself has grown tools for size: shallow clones fetch recent history only, "
            "partial clones fetch file contents on demand, sparse checkouts materialize only some directories."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def patches(self):
        head = label(r"Other models of history", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"git stores \textbf{snapshots} and computes diffs when asked", 12.4, font_size=23,
                          color=WHITE),
            wrapped_label(r"\textbf{patch theory} \ (Darcs, 2003; \ Pijul): \ the history \textit{is} a set of "
                          r"patches; \ two patches that commute can be applied in either order, \ so cherry-picking "
                          r"is exact and merges never depend on the path taken", 12.4, font_size=23, color=YES),
            wrapped_label(r"Pijul's patches act on a graph of lines in which a conflict is a legitimate state, \ "
                          r"resolved later by another patch", 12.4, font_size=23, color=HEAD),
            wrapped_label(r"CRDT-based version control and local-first editors \ (Part 39): \ merges that cannot "
                          r"conflict, \ for the structures where that is possible", 12.4, font_size=23, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Git's model is not the only possible one. <bookmark mark='a'/> Git stores snapshots and computes "
            "differences when you ask for them. <bookmark mark='b'/> Patch-based systems, Darcs from 2003 and now "
            "Pijul, store the changes themselves, and reason about when two patches commute, meaning they can be "
            "applied in either order with the same result. Then cherry-picking is exact, and the result of a merge "
            "never depends on the order in which branches were combined. <bookmark mark='c'/> Pijul represents a "
            "file as a graph of lines in which a conflict is a perfectly valid state, recorded and resolved later by "
            "another patch. <bookmark mark='d'/> And for data whose merges can be made conflict-free, Part 39's "
            "CRDTs offer version control in which merging never needs a person at all."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def sizes(self):
        z = load("sizes")
        head = label(r"How big is a history?", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"commits", f"{z['commits']:,}"], [r"objects \ (blobs, \ trees, \ commits)",
                f"{z['kinds'].get('blob', 0):,}, \\ {z['kinds'].get('tree', 0):,}, \\ {z['kinds'].get('commit', 0):,}"],
                [r"files in the current commit", f"{z['head_files']:,}"],
                [r"their size", f"{z['head_bytes'] / 2 ** 20:,.0f} MB"],
                [r"every object ever, \ uncompressed", f"{z['uncompressed_bytes'] / 2 ** 20:,.0f} MB"],
                [r"on disk, \ compressed and packed", f"{z['on_disk_bytes'] / 2 ** 20:,.0f} MB"]]
        tab = grid_table([r"this repository", r""], rows, widths=[6.0, 4.0], row_h=0.48, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        lines = VGroup(
            wrapped_label(r"the whole history costs barely more than one snapshot: \ most files were added once and "
                          r"rarely changed, \ and the ones that change \ (the syllabus, \ the translation tables) \ "
                          r"pack into deltas", 12.4, font_size=21, color=YES),
            wrapped_label(r"a \textbf{shallow clone} \ (\texttt{--depth 1}) \ would fetch only the last commit's "
                          r"objects; \ a \textbf{partial clone} \ (\texttt{--filter=blob:none}) \ fetches file contents "
                          r"only when they are needed", 12.4, font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "How much does history cost in practice? We asked this repository. <bookmark mark='a'/> A hundred and "
            "sixty commits, seventeen thousand objects. The current commit's files take about nine hundred "
            "megabytes. Every object ever stored, uncompressed, is only a little more, and packed on disk it is "
            "less than the snapshot alone. <bookmark mark='b'/> Most files here were written once and rarely "
            "changed, and the few that change constantly, like the syllabus and the translation tables, pack into "
            "deltas. <bookmark mark='c'/> For repositories whose history is far larger than any snapshot, a shallow "
            "clone fetches only the latest commit, and a partial clone defers each file's contents until something "
            "actually reads it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def window(self):
        head = label(r"Choosing what to delta against", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"any object can be stored as a delta against any other: \ the best choice is a "
                          r"search problem", 12.4, font_size=23, color=WHITE),
            wrapped_label(r"git's heuristic: \ sort objects by type, \ by a hash of their path's last characters, "
                          r"\ and by size \ (largest first); \ try each against the previous ten \ (the "
                          r"\textbf{window}) \ and keep the smallest delta", 12.4, font_size=23, color=YES),
            wrapped_label(r"bounded \textbf{depth} \ (50 by default): \ reading an object applies at most that many "
                          r"deltas; \ larger is smaller on disk and slower to read", 12.4, font_size=23, color=HEAD),
            wrapped_label(r"the same packs travel over the network: \ a fetch sends only the objects the other side "
                          r"lacks, \ found by the walk of Chapter 2", 12.4, font_size=23, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Which object should each delta be taken against? <bookmark mark='a'/> Any object could serve as the "
            "base for any other, so the best packing is a search problem, and git uses a heuristic. "
            "<bookmark mark='b'/> It sorts objects by type, by a hash of the end of their path, so that versions of "
            "the same file sit together, and by size, largest first; then tries each object against the ten before "
            "it, its window, and keeps the smallest delta. <bookmark mark='c'/> Chains have a bounded depth, fifty "
            "by default, so that reading any object applies at most fifty deltas: deeper chains are smaller on disk "
            "and slower to read. <bookmark mark='d'/> The same packs travel over the network. A fetch sends only "
            "the objects the other side lacks, found by the walk of the merging chapter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN,)
