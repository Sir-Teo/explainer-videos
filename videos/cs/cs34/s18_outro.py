from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (BG, BITS, DATA, HEAD, JRN, KERN, NO, PART, YES)


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
        head = label(rf"Part {PART}: \ Storage", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"475\times", font_size=56, color=NO), r"random against sequential", NO),
            tile(MathTex(r"\frac{1 + p}{2p}", font_size=56, color=DATA), r"flash's write amplification", DATA),
            tile(MathTex(r"2^k", font_size=60, color=HEAD), r"every crash point, \ checked", HEAD),
            tile(MathTex(r"\textsf{commit}", font_size=52, color=JRN), r"journals and replay", JRN),
            tile(MathTex(r"\frac{2}{1 - u}", font_size=56, color=YES), r"logs and their cleaners", YES),
            tile(MathTex(r"P \oplus Q", font_size=56, color=BITS), r"RAID, \ and real failure rates", BITS),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. A model of the disk, where reading in order is nearly five hundred times "
            "faster than reading at random, and a simulated flash drive with its translation layer and garbage "
            "collector. A Unix file system, crashed at every write and checked each time. The defences: careful "
            "ordering, journaling with its commit block, logs and their cleaners, copy-on-write trees with checksums, "
            "RAID and the failure rates disks really have. What fsync means, LSM trees, and PebbleOS reading the "
            "novels from a disk of its own."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"write-ahead logging, \ ARIES, \ B+ trees and LSM trees in a database", [35]),
            (r"replication: \ copies on other machines, \ quorums", [39]),
            (r"object storage and its durability, \ in dollars", [45]),
            (r"the partitioned log: \ streams built on sequential writes", [46]),
            (r"availability arithmetic and failure in production", [50]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 35's database keeps a write-ahead log, recovers with ARIES, and indexes with "
            "B-plus trees and this part's LSM trees. Part 39 puts copies on other machines, because one machine's "
            "disks are never enough. Part 45 prices durability in the cloud. Part 46 builds streaming systems on the "
            "partitioned log, the sequential write at datacenter scale. And Part 50 does availability arithmetic "
            "with the failure rates of chapter 12."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"file systems", r"ext4 or XFS by default; \ ZFS or btrfs when you want checksums and snapshots"),
            (r"durability", r"write a new file, \ fsync it, \ rename it, \ fsync the directory; \ never retry a "
                            r"failed fsync"),
            (r"flash", r"leave spare space, \ keep TRIM on, \ watch the wear counters; \ write sequentially when you "
                       r"can"),
            (r"redundancy", r"RAID 6 or mirrors for big disks; \ scrub regularly; \ RAID is not a backup"),
            (r"engines", r"LSM for write-heavy data, \ B-trees for reads; \ tune compaction for the workload"),
        ])
        with self.voiceover(
            "In practice. Use ext4 or XFS unless you need checksums and snapshots, which ZFS and btrfs give. To "
            "replace a file durably, write a new one, fsync it, rename it over the old, and fsync the directory; and "
            "if fsync ever fails, treat the data as lost. Leave flash some spare room, keep TRIM on, and watch its "
            "wear. Protect large disks with RAID 6 or mirrors, scrub them, and remember that RAID is not a backup: it "
            "faithfully copies your mistakes. And pick an LSM engine for write-heavy data, a B-tree for read-heavy, "
            "and tune compaction to the workload."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Derive the average seek of the square-root model: \ show $E\sqrt{|U - V|} = 8/15$ for independent "
            r"uniform $U, V$.",
            r"Show that a flash collector whose victims hold on average a fraction $u$ of live pages has write "
            r"amplification $1/(1 - u)$, \ and that LFS's cleaner, \ which also reads each segment, \ has write cost "
            r"$2/(1 - u)$.",
            r"Show that ordered journaling with a commit block leaves, \ after any crash and replay, \ either the old "
            r"file system or the new one.",
            r"For RAID 6, \ derive the formula that recovers two lost data blocks from $P$ and $Q$.",
            r"\textit{Build.} \ Give PebbleOS a \texttt{write} system call for files, \ allocating blocks with "
            r"\texttt{bread} and a bitmap; \ crash-test it with the checker.",
            r"$\bigstar$ \textit{Research.} \ Minimum flushes: \ for each PebbleFS operation, \ find the fewest "
            r"flushes \ (and a write order) \ so that every crash state is at worst a leak; \ is there a "
            r"polynomial algorithm from the dependency graph?",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: teach PebbleOS to write files, and crash-test your code with our checker. The last, marked with "
            "a star, is a research problem: the fewest flushes that make each operation safe, which careful ordering "
            "only approximates."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 35, \ Databases", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"ask for \textit{what}, \ never \textit{how}: \ Codd, \ 1970", HEAD),
            (r"relational algebra, \ joins, \ and an optimizer that searches", DATA),
            (r"transactions: \ serializability, \ two-phase locking, \ MVCC", YES),
            (r"recovery: \ ARIES, \ on this part's log", KERN))]).arrange(DOWN, buff=0.35)
        q = label(r"the Job becomes one line of SQL", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time, Part 35: Databases. In 1970 Codd said that programs should say what data they want, never how "
            "to find it. From that came relational algebra, an optimizer that searches for the cheapest plan, and "
            "transactions that let thousands of users act as if each were alone, even through crashes, using this "
            "part's log. The Job becomes one line of SQL. Part 35, Databases."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Arpaci-Dusseau and Arpaci-Dusseau, \textit{Operating Systems: Three Easy Pieces}, \ persistence",
             r"Petrov, \textit{Database Internals}, \ part I; \ Giampaolo, \textit{Practical File System Design}",
             r"McKusick and Neville-Neil, \textit{The Design and Implementation of the FreeBSD Operating System}"],
            [r"McKusick et al. \ (1984); \ Ganger and Patt \ (1994); \ Hagmann \ (1987); \ Rosenblum and Ousterhout "
             r"\ (1992)",
             r"Patterson, Gibson and Katz \ (1988); \ Schroeder and Gibson \ (2007); \ Bairavasundaram et al. \ "
             r"(2007, \ 2008)",
             r"Agrawal et al. \ (2008); \ Pillai et al. \ (2014); \ O'Neil et al. \ (1996); \ Athanassoulis et al. \ "
             r"(2016)",
             r"Chen et al., \ FSCQ \ (2015); \ Dayan et al., \ Monkey \ (2017); \ Bj{\o}rling et al., \ ZNS \ (2021)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
