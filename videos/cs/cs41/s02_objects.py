from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs41.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, mono)


class Objects(VoiceoverScene):
    def construct(self):
        self.card()
        self.kinds()
        self.ripple()
        self.integrity()
        self.refs()
        self.three_trees()

    def card(self):
        card = chapter_card(1, r"Git's objects", r"What is a commit, \ exactly?", lit=(1979, 2005),
                            extra=((1979, r"Merkle: \ hash trees"), (2005, r"Torvalds: \ git")), part=PART)
        with self.voiceover("Chapter one. Git's objects."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def kinds(self):
        o = load("objects")
        head = label(r"Four kinds of object", font_size=36).to_edge(UP, buff=0.3)
        blob = code_block(["blob 43\\0The Job: count the words in", "thirty novels."], size=15)
        tree = code_block(["tree <size>\\0", "100644 README.md <20-byte id>", "40000 src <20-byte id>"], size=15)
        commit = code_block([f"tree {o['ours']['tree'][:12]}...", "parent <none>",
                             "author Ada <ada@example.com> 1700000000 +0000", "", "first"], size=15)
        boxes = VGroup()
        for title, body, col in ((r"blob: \ a file's bytes", blob, DATA), (r"tree: \ a directory", tree, YES),
                                 (r"commit: \ a snapshot and its parents", commit, HEAD)):
            t = label(title, font_size=20, color=col)
            g = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            fr = SurroundingRectangle(g, buff=0.18, color=col, corner_radius=0.1, stroke_width=1.5)
            boxes.add(VGroup(fr, g))
        boxes.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        notes = VGroup(
            wrapped_label(r"each object is stored compressed, \ under the name \texttt{SHA-1(kind size \textbackslash 0 "
                          r"content)}", 5.2, font_size=19, color=WHITE),
            wrapped_label(r"a \textbf{tag} names a commit, \ with a message and usually a signature", 5.2,
                          font_size=19, color=LAM),
            wrapped_label(r"nothing is ever overwritten: \ a new version is a new object with a new name, \ and the "
                          r"old one stays until garbage collection", 5.2, font_size=19, color=YES),
            wrapped_label(r"git is moving to SHA-256, \ since SHA-1 collisions became practical \ (SHAttered, "
                          r"2017)", 5.2, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.9, -0.2, 0])
        with self.voiceover(
            "Git stores four kinds of object, each named by the hash of its contents. <bookmark mark='a'/> A blob is "
            "a file's bytes and nothing else, not even its name. A tree is a directory: for each entry, its mode, "
            "its name and the name of the object it points to. A commit names one tree, the snapshot of the whole "
            "project, plus its parent commits, its author and a message. <bookmark mark='b'/> And a tag names a "
            "commit, usually with a signature. <bookmark mark='c'/> Nothing is ever overwritten. A new version of a "
            "file is a new blob with a new name; the old one stays. <bookmark mark='d'/> The hash was SHA-1, and "
            "since researchers produced a practical SHA-1 collision in 2017, git has been moving to SHA-256."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes[0]), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(boxes[1]), FadeIn(boxes[2]))
            for mk, n in zip("bcd", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n))
        self.wait(0.4)
        self.clear_scene()

    def _tree(self, ids, changed=()):
        pos = {"commit": [0, 2.2], "root": [0, 1.0], "README.md": [-2.4, -0.3], "src": [1.6, -0.3],
               "job.py": [0.4, -1.6], "util": [2.8, -1.6], "io.py": [2.8, -2.9]}
        edges = [("commit", "root"), ("root", "README.md"), ("root", "src"), ("src", "job.py"), ("src", "util"),
                 ("util", "io.py")]
        g = VGroup()
        nodes = {}
        for k, (x, y) in pos.items():
            col = NO if k in changed else (HEAD if k == "commit" else (YES if k in ("root", "src", "util") else DATA))
            box = RoundedRectangle(width=2.0, height=0.7, corner_radius=0.08, stroke_color=col, fill_color=col,
                                   fill_opacity=0.12).move_to([x, y, 0])
            t = VGroup(label(k.replace("_", r"\_"), font_size=16, color=WHITE), mono(ids.get(k, "")[:7], size=13,
                                                                                   color=col)).arrange(DOWN, buff=0.04)
            t.move_to(box)
            nodes[k] = VGroup(box, t)
        lines = VGroup(*[Line(nodes[a][0].get_bottom(), nodes[b][0].get_top(), color=GREY_C, stroke_width=1.5)
                         for a, b in edges])
        g.add(lines, *nodes.values())
        g.nodes = nodes
        return g

    def ripple(self):
        from explainer.cs.vcs import git as G
        r = load("ripple")
        from videos.cs.cs41.compute import FILES
        f2 = dict(FILES)
        f2["src/util/io.py"] = FILES["src/util/io.py"].replace(b"read()", b"read().lower()")

        def ids_for(files):
            s = G.Store()
            root = s.write_files(files)
            src = s.write_files({k[4:]: v for k, v in files.items() if k.startswith("src/")})
            util = s.write_files({k[9:]: v for k, v in files.items() if k.startswith("src/util/")})
            return {"commit": s.commit(root, [], "first"), "root": root, "README.md": G.obj_id("blob",
                    files["README.md"]), "src": src, "job.py": G.obj_id("blob", files["src/job.py"]),
                    "util": util, "io.py": G.obj_id("blob", files["src/util/io.py"])}
        a = self._tree(ids_for(FILES)).scale(0.9).move_to([-3.4, -0.4, 0])
        b = self._tree(ids_for(f2), changed=("commit", "root", "src", "util", "io.py")).scale(0.9).move_to(
            [3.4, -0.4, 0])
        head = label(r"A Merkle graph", font_size=36).to_edge(UP, buff=0.3)
        la = label(r"before", font_size=20, color=GREY_A).next_to(a, UP, buff=0.1)
        lb = label(r"after editing \texttt{src/util/io.py}", font_size=20, color=NO).next_to(b, UP, buff=0.1)
        foot = wrapped_label(rf"{r['changed']} of {r['objects']} objects get new names, \ every one on the path to "
                             rf"the root; \ the other {r['shared']} are shared, \ not copied", 12.4, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Because every name is a hash of contents that include other names, the objects form a Merkle graph, "
            "Ralph Merkle's tree of hashes from Part 39's anti-entropy. <bookmark mark='a'/> Here is our small "
            "project: a commit, its tree, and below it the files and subdirectories. <bookmark mark='b'/> Change one "
            "line of one file. Its blob gets a new name; so does the tree that lists it, and the tree above that, "
            "and the root, and the commit. Everything else keeps its name and is shared between the two snapshots, "
            "not copied. <bookmark mark='c'/> Two consequences. A commit's name vouches for every byte of the "
            "project and its whole history: change anything and the name changes. And comparing two snapshots is "
            "fast: equal names mean equal subtrees, so git skips them without looking inside."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb))
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(*[Indicate(b.nodes[k], color=NO) for k in ("io.py", "util", "src", "root", "commit")])
        self.wait(0.4)
        self.clear_scene()

    def refs(self):
        head = label(r"Names for commits", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"a \textbf{branch} is a file holding one commit's name; \ committing moves it forward; \ "
                          r"\textbf{HEAD} names the branch you are on", 12.4, font_size=23, color=YES),
            wrapped_label(r"the \textbf{index} is the next commit's tree, \ being assembled: \ \texttt{git add} writes "
                          r"blobs and updates it", 12.4, font_size=23, color=HEAD),
            wrapped_label(r"\texttt{checkout} rewrites the working files to match a tree, \ touching only the paths "
                          r"whose names differ", 12.4, font_size=23, color=DATA),
            wrapped_label(r"the \textbf{reflog} records where each branch has pointed: \ a commit you ``lost'' is "
                          r"still there, \ by name, \ until garbage collection", 12.4, font_size=23, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Hashes are not names people can use, so git adds a thin layer of mutable pointers. "
            "<bookmark mark='a'/> A branch is a small file containing one commit's name. Committing writes a new "
            "commit whose parent is the old one, and moves the branch to it. HEAD records which branch you are on. "
            "<bookmark mark='b'/> The index is the tree of the next commit, being assembled: adding a file writes its "
            "blob and records it there. <bookmark mark='c'/> Checking out another commit rewrites the working files "
            "to match its tree, touching only paths whose names differ. <bookmark mark='d'/> And the reflog records "
            "every position each branch has had, so a commit you think you lost is still there, by name, until "
            "garbage collection removes objects that nothing points to."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def integrity(self):
        c = load("corrupt")
        head = label(r"Integrity for free", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(label(r"stored under", font_size=20, color=GREY_A), mono(c["name"], size=17, color=YES)).arrange(
                RIGHT, buff=0.3),
            VGroup(label(r"one bit flipped on disk:", font_size=20, color=GREY_A),
                   mono(c["text"].strip(), size=17, color=NO)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"now hashes to", font_size=20, color=GREY_A), mono(c["rehash"], size=17, color=NO)).arrange(
                RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.6)
        lines = VGroup(
            wrapped_label(r"reading an object rehashes it: \ a bad disk, \ a bad network or a malicious server "
                          r"cannot hand you different content under the same name \ (\texttt{git fsck} checks "
                          r"everything)", 12.4, font_size=22, color=WHITE),
            wrapped_label(r"a signed tag or commit signs one hash, \ and so vouches for the entire history beneath "
                          r"it \ --- \ as long as the hash resists collisions", 12.4, font_size=22, color=YES),
            wrapped_label(r"SHAttered \ (2017): \ two different PDFs with the same SHA-1, \ after about $2^{63}$ "
                          r"computations; \ git now detects that attack's pattern, \ and supports SHA-256 "
                          r"repositories", 12.4, font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rows, DOWN, buff=0.55)
        with self.voiceover(
            "Content addressing gives integrity checking for free. <bookmark mark='a'/> We stored a file, then flipped "
            "a single bit of it, as a failing disk might: novels became novdls. Asked for the object, our store "
            "rehashes what it read, gets a completely different name, and refuses. <bookmark mark='b'/> No disk, "
            "network or malicious server can hand you different content under the same name, and git fsck checks "
            "every object this way. <bookmark mark='c'/> It also makes signatures cheap: signing one commit's "
            "hash vouches for the whole history beneath it. <bookmark mark='d'/> That depends on the hash. In 2017 "
            "researchers published two different PDF files with the same SHA-1, after about two to the sixty-three "
            "computations. Git now detects that attack's fingerprint, and supports repositories hashed with SHA-256."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.5), run_time=2.5)
            for mk, l in zip("bcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def three_trees(self):
        head = label(r"Three trees", font_size=36).to_edge(UP, buff=0.3)
        names = [(r"HEAD", r"the last commit's tree", HEAD), (r"the index", r"the next commit, \ being built", YES),
                 (r"the working tree", r"the files you edit", DATA)]
        boxes = VGroup()
        for t, sub, c in names:
            b = RoundedRectangle(width=3.4, height=1.4, corner_radius=0.12, stroke_color=c, fill_color=c,
                                 fill_opacity=0.12)
            g = VGroup(label(t, font_size=24, color=WHITE), label(sub, font_size=17, color=GREY_A)).arrange(
                DOWN, buff=0.12).move_to(b)
            boxes.add(VGroup(b, g))
        boxes.arrange(RIGHT, buff=1.3).next_to(head, DOWN, buff=0.8)
        a1 = Arrow(boxes[2].get_left(), boxes[1].get_right(), buff=0.1, color=YES)
        a2 = Arrow(boxes[1].get_left(), boxes[0].get_right(), buff=0.1, color=HEAD)
        l1 = label(r"\texttt{git add}", font_size=18, color=YES).next_to(a1, UP, buff=0.08)
        l2 = label(r"\texttt{git commit}", font_size=18, color=HEAD).next_to(a2, UP, buff=0.08)
        lines = VGroup(
            wrapped_label(r"\texttt{git status} compares the three: \ staged \ (index $\ne$ HEAD) \ and unstaged \ "
                          r"(working tree $\ne$ index); \ equal hashes are skipped without reading the files", 12.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"\texttt{git reset --soft}, \ \texttt{--mixed}, \ \texttt{--hard} \ move HEAD and then "
                          r"overwrite none, \ one, \ or both of the others: \ the most feared command is three "
                          r"assignments", 12.4, font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Most of git's confusing commands become simple once you see the three trees it keeps. "
            "<bookmark mark='a'/> HEAD is the tree of the last commit. The index is the next commit, being "
            "assembled. The working tree is the files you actually edit. Adding copies a file from the working tree "
            "into the index; committing turns the index into a new commit and moves HEAD. "
            "<bookmark mark='b'/> Status compares them pairwise: what is staged, and what is changed but not yet "
            "staged; files whose hashes agree are skipped without being read. <bookmark mark='c'/> And reset, the "
            "command people fear most, moves HEAD and then overwrites none, one or both of the other two trees, "
            "depending on whether it is soft, mixed or hard."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes), GrowArrow(a1), GrowArrow(a2), FadeIn(l1), FadeIn(l2))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN,)
