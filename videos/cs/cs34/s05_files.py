from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (DATA, FILEC, HEAD, LAM, META, PART, YES, code, load)


def node(text, color, w=1.9, h=0.5, font=18):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=1.8,
                         fill_color=color, fill_opacity=0.12)
    return VGroup(r, label(text, font_size=font, color=WHITE).move_to(r))


class Files(VoiceoverScene):
    def construct(self):
        self.card()
        self.tree()
        self.api()
        self.links()

    def card(self):
        card = chapter_card(4, r"Files and directories", r"What is a file, to the operating system?",
                            lit=(1965, 1974), extra=((1965, r"Multics: \ a tree of directories"),
                                                     (1974, r"Ritchie and Thompson: \ Unix")), part=PART)
        with self.voiceover("Chapter four. Files and directories."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tree(self):
        d = load("fs")
        head = label(r"Names, \ inodes, \ and bytes", font_size=36).to_edge(UP, buff=0.3)
        root = node(r"\texttt{/}", YES).move_to([-4.2, 1.6, 0])
        kids = VGroup(*[node(rf"\texttt{{{n}/}}", YES) for n in sorted(d["dirs"]["/"])]).arrange(DOWN, buff=0.9)
        kids.move_to([-1.6, 0.9, 0])
        leaves = VGroup(node(r"\texttt{notes}", FILEC), node(r"\texttt{emma}", FILEC)).arrange(DOWN, buff=0.9)
        leaves.move_to([1.0, 0.9, 0])
        edges = VGroup(*[Line(root.get_right(), k.get_left(), color=GREY_B, stroke_width=1.5) for k in kids])
        edges.add(Line(kids[0].get_right(), leaves[0].get_left(), color=GREY_B, stroke_width=1.5))
        edges.add(Line(kids[1].get_right(), leaves[1].get_left(), color=GREY_B, stroke_width=1.5))
        ino = d["inode"]
        card = VGroup(
            label(r"the inode of \texttt{emma}", font_size=20, color=META),
            label(rf"type: \ file; \ links: \ {ino['nlink']}; \ size: \ {ino['size']:,}".replace(",", "{,}") +
                  r" bytes", font_size=18, color=WHITE),
            label(r"owner, \ permissions, \ times", font_size=18, color=GREY_A),
            label(r"where its blocks are", font_size=18, color=FILEC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        frame = SurroundingRectangle(card, color=META, buff=0.18, corner_radius=0.08)
        icard = VGroup(frame, card).move_to([4.6, 0.9, 0])
        arr = Arrow(leaves[1].get_right(), icard.get_left(), buff=0.1, color=META, stroke_width=2)
        lines = VGroup(
            label(r"a \textbf{file}: \ an array of bytes, \ and an \textbf{inode} that says where they are and who "
                  r"may touch them", font_size=21, color=WHITE),
            label(r"a \textbf{directory}: \ a file whose contents are a table of names and inode numbers",
                  font_size=21, color=YES),
            label(r"a \textbf{path} is walked one directory at a time: \ \texttt{/}, \ then \texttt{novels}, \ then "
                  r"\texttt{emma}", font_size=21, color=HEAD),
            label(r"the name is not in the inode: \ one inode can have several names", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "To a program, a file is a name and an array of bytes. The operating system splits that in two. "
            "<bookmark mark='a'/> The bytes, wherever they are on the disk, are described by an inode: a small "
            "record of the file's type, size, owner, permissions and times, and where its blocks lie. Inodes are "
            "numbered. <bookmark mark='b'/> A directory is just another file, whose contents are a table pairing "
            "names with inode numbers. <bookmark mark='c'/> So a path is followed one step at a time: the root "
            "directory's table gives the inode of novels, whose table gives the inode of emma. Multics introduced this "
            "tree of directories in 1965, and Unix made it simple. <bookmark mark='d'/> Notice that the name is not "
            "part of the file. It lives in a directory, so a file can have several."
        ) as vo:
            self.play(FadeIn(head), FadeIn(root), FadeIn(kids), FadeIn(leaves), Create(edges))
            vo.wait_until("a")
            self.play(GrowArrow(arr), FadeIn(icard), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), *[k[0].animate.set_stroke(width=3.5) for k in kids])
            vo.wait_until("c")
            path = VGroup(root, kids[1], leaves[1])
            self.play(FadeIn(lines[2]), LaggedStart(*[Indicate(p, color=HEAD) for p in path], lag_ratio=0.5))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def api(self):
        head = label(r"The Unix interface", font_size=36).to_edge(UP, buff=0.3)
        src = code([
            'fd = open("/novels/emma", O_RDONLY);  // walk the path; get a descriptor',
            "n  = read(fd, buf, 4096);             // copy bytes; the offset advances",
            "lseek(fd, 0, SEEK_SET);               // move the offset",
            "w  = write(out, buf, n);              // into the page cache, usually",
            "fsync(out);                           // wait until it is on the disk",
            "close(fd);",
        ], size=19).next_to(head, DOWN, buff=0.4)
        cols = VGroup()
        for title, items, c in ((r"the process's descriptors", [r"0 \ stdin", r"1 \ stdout", r"3 \ $\rightarrow$"],
                                 DATA),
                                (r"open files \ (shared)", [r"offset 4096, \ read-only"], HEAD),
                                (r"inodes in memory", [r"\texttt{emma}"], META)):
            rows = VGroup(*[node(t, c, w=2.6, h=0.45, font=17) for t in items]).arrange(DOWN, buff=0.1)
            cols.add(VGroup(label(title, font_size=18, color=c), rows).arrange(DOWN, buff=0.15))
        cols.arrange(RIGHT, buff=0.9).next_to(src, DOWN, buff=0.45)
        a1 = Arrow(cols[0][1][2].get_right(), cols[1][1][0].get_left(), buff=0.08, color=GREY_B, stroke_width=2)
        a2 = Arrow(cols[1][1][0].get_right(), cols[2][1][0].get_left(), buff=0.08, color=GREY_B, stroke_width=2)
        foot = label(r"a descriptor is a small integer; \ the kernel keeps the offset, \ and checks permission once, "
                     r"at \texttt{open}", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Programs reach files through a handful of system calls, unchanged since early Unix. <bookmark mark='a'/> "
            "Open walks the path, checks permission once, and returns a small integer, the file descriptor. "
            "<bookmark mark='b'/> Read copies bytes from the current offset and moves it forward; lseek moves it "
            "anywhere. <bookmark mark='c'/> Write copies bytes in, but usually only into memory, the page cache. It "
            "returns long before the data is on the disk. Fsync is the call that waits until it is: chapter 13 is "
            "about what that really means. <bookmark mark='d'/> Inside the kernel, the descriptor indexes the "
            "process's table, which points to an open-file entry holding the offset, which points to the inode."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src[0]))
            vo.wait_until("b")
            self.play(FadeIn(src[1]), FadeIn(src[2]))
            vo.wait_until("c")
            self.play(FadeIn(src[3]), FadeIn(src[4]), FadeIn(src[5]))
            vo.wait_until("d")
            self.play(FadeIn(cols), GrowArrow(a1), GrowArrow(a2), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def links(self):
        head = label(r"Links, \ unlink, \ rename", font_size=36).to_edge(UP, buff=0.3)
        d1 = node(r"\texttt{/home/x}", YES, w=2.4).move_to([-4.0, 1.4, 0])
        d2 = node(r"\texttt{/backup/y}", YES, w=2.4).move_to([-4.0, 0.2, 0])
        ino = node(r"inode 7: \ links \ 2", META, w=2.8).move_to([0.2, 0.8, 0])
        data = VGroup(*[Rectangle(width=0.45, height=0.45, stroke_color=FILEC, fill_color=FILEC, fill_opacity=0.3)
                        for _ in range(4)]).arrange(RIGHT, buff=0.05).move_to([3.8, 0.8, 0])
        e1 = Arrow(d1.get_right(), ino.get_left(), buff=0.08, color=GREY_B, stroke_width=2)
        e2 = Arrow(d2.get_right(), ino.get_left(), buff=0.08, color=GREY_B, stroke_width=2)
        e3 = Arrow(ino.get_right(), data.get_left(), buff=0.08, color=GREY_B, stroke_width=2)
        lines = VGroup(
            label(r"\texttt{link(x, y)}: \ a second name, \ the same inode; \ its count of links goes to 2",
                  font_size=21, color=WHITE),
            label(r"\texttt{unlink(x)}: \ remove a name; \ the blocks are freed only when the count reaches 0 \ "
                  r"(and nobody has it open)", font_size=21, color=HEAD),
            label(r"\texttt{rename(a, b)}: \ atomic, \ even when \texttt{b} exists: \ the tool for replacing a file "
                  r"safely \ (chapter 13)", font_size=21, color=YES),
            label(r"a \textbf{symbolic} link is a different thing: \ a small file holding a path", font_size=21,
                  color=LAM),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Because names live in directories, a file can have more than one. <bookmark mark='a'/> Link adds a "
            "second directory entry for the same inode, and the inode counts its links: two. <bookmark mark='b'/> "
            "Unlink removes one name. There is no call to delete a file: its blocks are freed when the last name is "
            "gone and no process still has it open. <bookmark mark='c'/> Rename moves a name, atomically, even over "
            "an existing file; we will lean on that. <bookmark mark='d'/> A symbolic link is something else: a tiny "
            "file containing a path, followed when it is opened. Our file system has the first three, and the "
            "tests check every one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(d1), FadeIn(ino), FadeIn(data), GrowArrow(e1), GrowArrow(e3))
            vo.wait_until("a")
            self.play(FadeIn(d2), GrowArrow(e2), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeOut(d1), FadeOut(e1), FadeIn(lines[1]),
                      ino[1].animate.become(label(r"inode 7: \ links \ 1", font_size=18, color=WHITE).move_to(ino)))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
