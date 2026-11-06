from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, fit_right, grid_table, load, mono)


def stack(title, layers, color):
    g = VGroup()
    for t, c, w in layers:
        r = RoundedRectangle(width=w, height=0.62, corner_radius=0.08, stroke_color=c, stroke_width=1.8,
                             fill_color=c, fill_opacity=0.18)
        g.add(VGroup(r, label(t, font_size=18, color=WHITE).move_to(r)))
    g.arrange(DOWN, buff=0.1)
    return VGroup(label(title, font_size=22, color=color).next_to(g, UP, buff=0.15), g)


class Containers(VoiceoverScene):
    def construct(self):
        self.card()
        self.compare()
        self.namespaces()
        self.cost()

    def card(self):
        card = chapter_card(13, r"Containers", r"Can you isolate programs without a second kernel?",
                            lit=(1979, 2000, 2008, 2013),
                            extra=((1979, r"chroot"), (2000, r"FreeBSD jails"), (2008, r"Linux cgroups"),
                                   (2013, r"Docker")), part=PART)
        with self.voiceover("Chapter thirteen. Containers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def compare(self):
        head = label(r"A virtual machine, \ and a container", font_size=36).to_edge(UP, buff=0.3)
        vm = stack(r"virtual machines", [(r"app \quad\quad app", DATA, 4.6), (r"guest kernel \quad guest kernel", HEAD,
                                                                              4.6),
                                         (r"hypervisor", KERN, 4.6), (r"hardware", GREY_B, 4.6)], HEAD)
        ct = stack(r"containers", [(r"app \quad\quad app", DATA, 4.6), (r"namespaces + cgroups", YES, 4.6),
                                   (r"\textbf{one} kernel", KERN, 4.6), (r"hardware", GREY_B, 4.6)], YES)
        VGroup(vm, ct).arrange(RIGHT, buff=1.4).next_to(head, DOWN, buff=0.5)
        lines = VGroup(
            label(r"a VM pretends to be a \textbf{machine}: \ each guest brings its own kernel", font_size=21,
                  color=HEAD),
            label(r"a container pretends to be a \textbf{system}: \ processes see their own pids, \ files, \ network, "
                  r"\ users", font_size=21, color=YES),
            label(r"starts in milliseconds, \ no second kernel's memory; \ but every container trusts the one "
                  r"kernel", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A virtual machine is one way to give a program its own world. <bookmark mark='a'/> Each guest brings its "
            "own kernel, running on a hypervisor. <bookmark mark='b'/> A container is the other way. There is one "
            "kernel, and it simply shows different groups of processes different views: their own process numbers, "
            "their own files, their own network and users. <bookmark mark='c'/> A container starts in milliseconds "
            "and carries no second kernel. But all the containers on a machine trust the same kernel, and that is "
            "the price we will come back to."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(vm), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(ct), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def namespaces(self):
        d = load("containers")
        head = label(r"Namespaces, \ on this machine", font_size=36).to_edge(UP, buff=0.3)
        cmd = VGroup(mono("unshare --user --pid --fork \\", 16, GREY_A),
                     mono("        --mount-proc --map-root-user sh", 16, GREY_A)).arrange(DOWN, buff=0.05,
                                                                                       aligned_edge=LEFT)
        out = VGroup(*[mono(s, 17, YES) for s in d["inside"]]).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        term = VGroup(cmd, out).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        box = SurroundingRectangle(term, color=GREY_D, buff=0.2, corner_radius=0.1)
        tg = VGroup(box, term).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        tab = grid_table([r"namespace", r"what it hides"], [
            [r"pid", r"other processes: \ the shell is pid 1"],
            [r"mnt", r"the file tree: \ its own mounts, \ its own \texttt{/}"],
            [r"net", r"interfaces, \ ports, \ routes"],
            [r"user", r"user ids: \ root inside, \ nobody outside"],
            [r"uts, \ ipc, \ cgroup, \ time", r"host name, \ shared memory, \ limits, \ clocks"],
        ], widths=[2.3, 4.4], row_h=0.5, font_size=19, mono_cols=())
        tab.next_to(tg, RIGHT, buff=0.4).align_to(tg, UP)
        fit_right(tab)
        cg = ", \\ ".join(c for c in d["cgroup"] if not c.startswith("name="))
        lines = VGroup(
            label(rf"inside: \ pid 1, \ uid 0, \ and three processes; \ outside, \ this machine runs {d['host_pids']}",
                  font_size=20, color=YES),
            label(r"\textbf{cgroups} limit what a group may use: \ the controllers here are", font_size=20,
                  color=HEAD),
            label(cg, font_size=18, color=GREY_A),
            label(r"a container image is just a file tree; \ Docker \ (2013) \ packaged all three", font_size=20,
                  color=WHITE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "On Linux the views are called namespaces. <bookmark mark='a'/> Here is one made on this machine, without "
            "any special privilege: a new user namespace and a new process namespace, and a shell inside them. "
            "<bookmark mark='b'/> The shell believes it is process number one, and that it is root, user zero. Ask "
            "it for the list of processes and it sees three: itself and the two commands it just ran. Outside, this "
            "machine is running eighty-two. <bookmark mark='c'/> There are eight kinds of namespace: processes, the "
            "file tree, the network, user ids, and four smaller ones. <bookmark mark='d'/> The second ingredient is "
            "control groups, which limit how much of each resource a group of processes may use: processor time, "
            "memory, the number of processes, and so on. <bookmark mark='e'/> Add a file tree to run in, and you have "
            "a container. Docker, in 2013, put the three together in a form everyone could use."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(box), FadeIn(cmd))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(o) for o in out], lag_ratio=0.2), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]), FadeIn(lines[2]))
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def cost(self):
        head = label(r"The cost: \ one kernel to trust", font_size=36).to_edge(UP, buff=0.3)
        tab = grid_table([r"", r"virtual machine", r"container"], [
            [r"starts in", r"seconds \ (a kernel boots)", r"milliseconds \ (a process starts)"],
            [r"memory", r"a whole guest kernel each", r"shared kernel and page cache"],
            [r"attack surface", r"the hypervisor: \ a few exits", r"the kernel: \ some 450 system calls"],
            [r"a kernel bug", r"breaks one guest", r"can break \textbf{every} container"],
        ], widths=[2.8, 4.6, 4.8], row_h=0.55, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45)
        lines = VGroup(
            label(r"Dirty COW \ (2016): \ a race in chapter 9's copy-on-write let any process write read-only "
                  r"files, \ containers included", font_size=20, color=NO),
            label(r"the middle ground: \ gVisor \ (2018) \ a kernel in user space; \ Firecracker \ (2020) \ tiny VMs, "
                  r"\ booting in 125 ms", font_size=20, color=LAM),
            label(r"AWS Lambda runs every function in a Firecracker microVM, \ not just a container", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.16).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Side by side. <bookmark mark='a'/> A virtual machine boots a kernel, in seconds; a container starts a "
            "process, in milliseconds. <bookmark mark='b'/> Each virtual machine holds a whole guest kernel in "
            "memory; containers share one kernel and its cache of the disk. <bookmark mark='c'/> But a virtual "
            "machine's only door to the host is the hypervisor and its few kinds of exit. A container's door is the "
            "whole Linux system call interface, some four hundred and fifty calls. <bookmark mark='d'/> So a single "
            "kernel bug can break out of every container. <bookmark mark='e'/> In 2016, Dirty COW, a race in exactly "
            "the copy-on-write code of chapter nine, let any process write to files it could only read. <bookmark "
            "mark='f'/> The industry's answer is a middle ground: Google's gVisor puts a second kernel in user space, "
            "and Amazon's Firecracker builds virtual machines small enough to boot in about a hundred and twenty-five "
            "milliseconds. <bookmark mark='g'/> Amazon's serverless functions each run in one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for mk, r in zip("abcd", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r)))
            for mk, ln in zip("efg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()
