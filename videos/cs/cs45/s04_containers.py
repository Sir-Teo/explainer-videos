from __future__ import annotations

import hashlib

from explainer.cs import *  # noqa: F403
from videos.cs.cs45.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, mono, tag_box


def digest(content: str) -> str:
    """The first hex digits of a toy layer's SHA-256 (the real thing, of illustrative contents)."""
    return hashlib.sha256(content.encode()).hexdigest()[:8]


# toy layers: (Dockerfile step, what the layer holds); a layer's contents are what its step wrote
LAYERS = [(r"FROM debian:12-slim", "debian 12 base files"),
          (r"RUN apt-get install -y python3", "python3 and its libraries"),
          (r"COPY requirements.txt .", "requirements.txt"),
          (r"RUN pip install -r requirements.txt", "the installed packages"),
          (r"COPY app/ /app", "app/main.py, version 1")]
APP_V2 = "app/main.py, version 2"


class Containers(VoiceoverScene):
    def construct(self):
        self.card()
        self.walls()
        self.limits()
        self.layers()
        self.overlay()
        self.pull()

    def card(self):
        card = chapter_card(3, r"Containers", r"What is in a container, \ and what holds it in?", lit=(2008, 2015),
                            extra=((2008, r"cgroups in Linux"), (2013, r"Docker"),
                                   (2015, r"Open Container Initiative")), part=PART)
        with self.voiceover("Chapter three. Containers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def walls(self):
        head = label(r"Processes with walls", font_size=36).to_edge(UP, buff=0.3)
        kernel = RoundedRectangle(width=8.4, height=0.6, corner_radius=0.1, stroke_color=KERN, fill_color=KERN,
                                  fill_opacity=0.2)
        kernel_l = label(r"one Linux kernel", font_size=20, color=WHITE).move_to(kernel)
        specs = [("web", "10.0.0.2", r"0.5 CPU, \ 256 MiB"), ("db", "10.0.0.3", r"2 CPU, \ 4 GiB"),
                 ("batch", "10.0.0.4", r"1 CPU, \ 1 GiB")]
        boxes = VGroup()
        for name, ip, lim in specs:
            frame = RoundedRectangle(width=2.6, height=2.75, corner_radius=0.12, stroke_color=YES, stroke_width=2)
            inside = VGroup(tag_box("pid 1", color=DATA, size=16, w=2.2, h=0.42),
                            tag_box(f"hostname {name}", color=DATA, size=16, w=2.2, h=0.42),
                            tag_box(f"eth0 {ip}", color=DATA, size=16, w=2.2, h=0.42),
                            tag_box("/  its own root", color=DATA, size=16, w=2.2, h=0.42)).arrange(DOWN, buff=0.12)
            cg = label(lim, font_size=17, color=HEAD)
            VGroup(inside, cg).arrange(DOWN, buff=0.18).move_to(frame)
            boxes.add(VGroup(frame, inside, cg))
        boxes.arrange(RIGHT, buff=0.3)
        left = VGroup(boxes, VGroup(kernel, kernel_l)).arrange(DOWN, buff=0.3).scale(1.1)
        left.to_edge(LEFT, buff=0.35).set_y(-0.25)
        host = VGroup(label(r"the host's view", font_size=19, color=GREY_A),
                      code_block(["  PID  COMMAND", " 4242  web", " 4243  web worker", " 5117  db",
                                  " 6020  batch"], size=18)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        host.next_to(left, RIGHT, buff=0.45).align_to(left, UP)
        hi = SurroundingRectangle(host[1][1], color=HEAD, buff=0.05)
        link = SurroundingRectangle(boxes[0][1][0], color=HEAD, buff=0.05)
        notes = VGroup(
            wrapped_label(r"\textbf{namespaces}: \ what it can see \ (Part 32)", 2.9, font_size=19, color=DATA),
            wrapped_label(r"\textbf{cgroups}: \ how much it may use", 2.9, font_size=19, color=HEAD),
            wrapped_label(r"\textbf{an image}: \ the files it runs", 2.9, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(host, DOWN, buff=0.45).align_to(host, LEFT)
        ill = note(r"illustrative", font_size=16).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Part 32 took a container apart. <bookmark mark='a'/> It is a group of ordinary processes on one "
            "kernel. Namespaces decide what they can see: their own process numbers, so that the first is number "
            "one, their own host name, network interfaces and file tree. <bookmark mark='b'/> Outside, the host "
            "sees the same process as number four thousand two hundred and forty-two. <bookmark mark='c'/> Control "
            "groups decide how much the processes may use, and an image provides the files they run."
        ) as vo:
            self.play(FadeIn(head), FadeIn(kernel), FadeIn(kernel_l), FadeIn(ill))
            vo.wait_until("a")
            self.play(*[Create(b[0]) for b in boxes], *[FadeIn(b[1]) for b in boxes], FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(host), Create(hi), Create(link))
            vo.wait_until("c")
            self.play(*[FadeIn(b[2]) for b in boxes], FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def limits(self):
        head = label(r"Limits, \ enforced", font_size=36).to_edge(UP, buff=0.3)
        files = code_block(["/sys/fs/cgroup/web/cpu.max      50000 100000",
                            "/sys/fs/cgroup/web/memory.max   268435456"], size=17)
        files.next_to(head, DOWN, buff=0.35)
        x0, per, n = -6.0, 2.4, 5                    # five 100 ms periods across 12 units
        y = 0.75
        runs, stops = VGroup(), VGroup()
        for k in range(n):
            runs.add(Rectangle(width=per / 2, height=0.45, stroke_width=0, fill_color=YES, fill_opacity=0.85).move_to(
                [x0 + k * per + per / 4, y, 0]))
            stops.add(Rectangle(width=per / 2, height=0.45, stroke_width=1, stroke_color=NO, fill_color=NO,
                                fill_opacity=0.25).move_to([x0 + k * per + 3 * per / 4, y, 0]))
        ticks = VGroup(*[VGroup(Line([x0 + k * per, y - 0.32, 0], [x0 + k * per, y + 0.32, 0], color=GREY_B),
                                label(f"{100 * k}", font_size=16, color=GREY_B).move_to([x0 + k * per, y - 0.5, 0]))
                         for k in range(n + 1)])
        ms = label(r"ms", font_size=16, color=GREY_B).next_to(ticks[-1][1], RIGHT, buff=0.1)
        leg = VGroup(label(r"runs", font_size=17, color=YES), label(r"throttled", font_size=17, color=NO))
        leg[0].next_to(runs[0], UP, buff=0.1)
        leg[1].next_to(stops[0], UP, buff=0.1)
        arr_x = x0 + 2 * per + 0.55 * per
        req = Arrow([arr_x, y + 0.95, 0], [arr_x, y + 0.27, 0], buff=0, color=HEAD, stroke_width=3,
                    max_tip_length_to_length_ratio=0.3)
        req_l = label(r"a request arrives", font_size=17, color=HEAD).next_to(req, UP, buff=0.05)
        wait = Line([arr_x, y - 0.05, 0], [x0 + 3 * per, y - 0.05, 0], color=HEAD, stroke_width=5)
        wait_l = label(r"waits $\approx 45$ ms", font_size=17, color=HEAD).next_to(stops[2], UP, buff=0.1).shift(
            RIGHT * 0.9)
        cap = 256
        my = -1.15
        mem_x0, mem_w = -6.0, 9.0
        scale = mem_w / 320
        frame = Rectangle(width=mem_w, height=0.45, stroke_color=GREY_C, stroke_width=1.5).move_to(
            [mem_x0 + mem_w / 2, my, 0])
        fill = Rectangle(width=0.01, height=0.45, stroke_width=0, fill_color=DATA, fill_opacity=0.8).move_to(
            [mem_x0, my, 0], aligned_edge=LEFT)
        limit = DashedLine([mem_x0 + cap * scale, my - 0.4, 0], [mem_x0 + cap * scale, my + 0.4, 0], color=NO,
                           stroke_width=3)
        limit_l = label(r"memory.max: \ 256 MiB", font_size=17, color=NO).next_to(limit, UP, buff=0.05)
        mem_l = label(r"memory in use", font_size=17, color=DATA).next_to(frame, UP, buff=0.08).align_to(frame, LEFT)
        oom = label(r"out-of-memory killer: \ the process ends", font_size=18, color=NO).next_to(frame, RIGHT,
                                                                                               buff=0.15)
        if oom.get_right()[0] > 6.8:
            oom.next_to(frame, DOWN, buff=0.12).align_to(limit, LEFT)
        foot = wrapped_label(r"the same files limit the number of processes \ (pids.max) \ and disk input and output "
                             r"\ (io.max); \ a throttled container shows nothing wrong inside, \ only a slower tail "
                             r"\ (Part 39)", 12.4, font_size=19, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Control groups turn limits into arithmetic. <bookmark mark='a'/> This group may "
            "use fifty thousand microseconds of processor time in every period of a hundred thousand: half a "
            "processor. <bookmark mark='b'/> A busy process inside runs for fifty milliseconds, and then the "
            "scheduler stops it until the next period begins. <bookmark mark='c'/> A request that arrives just then "
            "waits, for no reason visible inside the container: a limit has become a tail latency, as in Part 39. "
            "<bookmark mark='d'/> Memory is harsher. The group may hold two hundred and fifty-six mebibytes. When it "
            "needs more and the kernel cannot reclaim enough, the out-of-memory killer ends a process in the group, "
            "and chapter four's orchestrator restarts it. <bookmark mark='e'/> The same files limit the number "
            "of processes and the rate of disk traffic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(files), FadeIn(ticks), FadeIn(ms))
            vo.wait_until("a")
            self.play(Indicate(files[0], color=HEAD, scale_factor=1.03))
            vo.wait_until("b")
            for r, s in zip(runs, stops):
                self.play(GrowFromEdge(r, LEFT), run_time=0.4)
                self.play(FadeIn(s), run_time=0.3)
            self.play(FadeIn(leg))
            vo.wait_until("c")
            self.play(GrowArrow(req), FadeIn(req_l))
            self.play(Create(wait), FadeIn(wait_l))
            vo.wait_until("d")
            self.play(FadeIn(frame), FadeIn(mem_l), Create(limit), FadeIn(limit_l), FadeIn(fill))
            self.play(fill.animate.stretch_to_fit_width(cap * scale * 0.97).align_to(frame, LEFT), run_time=2)
            self.play(fill.animate.stretch_to_fit_width(cap * scale * 1.06).align_to(frame, LEFT).set_fill(NO),
                      run_time=0.6)
            self.play(FadeIn(oom), Flash(limit.get_center(), color=NO))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def layers(self):
        head = label(r"An image is a stack of layers", font_size=36).to_edge(UP, buff=0.3)
        steps = [s for s, _ in LAYERS] + [r'CMD ["python3", "/app/main.py"]']
        df = VGroup(label(r"Dockerfile", font_size=19, color=GREY_A), code_block(steps, size=16)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15)
        df.to_edge(LEFT, buff=0.4).shift(UP * 1.0)
        colors = [GREY_B, LAM, DATA, DATA, YES]
        blocks = VGroup()
        for (step, content), c in zip(LAYERS, colors):
            r = Rectangle(width=5.0, height=0.48, stroke_color=c, stroke_width=1.8, fill_color=c, fill_opacity=0.15)
            t = VGroup(label(content, font_size=16, color=WHITE), mono("sha256:" + digest(content), size=16,
                                                                       color=c)).arrange(RIGHT, buff=0.25)
            if t.width > 4.8:
                t.width = 4.8
            blocks.add(VGroup(r, t.move_to(r)))
        blocks.arrange(UP, buff=0.08).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.55)
        man_d = digest("manifest " + " ".join(digest(c) for _, c in LAYERS))
        man = VGroup(RoundedRectangle(width=5.0, height=0.62, corner_radius=0.1, stroke_color=HEAD, stroke_width=2),
                     VGroup(label(r"manifest: \ the five names, \ in order", font_size=16, color=WHITE),
                            mono("image  sha256:" + man_d, size=16, color=HEAD)).arrange(DOWN, buff=0.05))
        man[1].move_to(man[0])
        man.next_to(blocks, UP, buff=0.3)
        man_links = VGroup(*[Line(man[0].get_bottom(), b[0].get_top(), color=GREY_D, stroke_width=1)
                             for b in blocks[-1:]])
        new_top = mono("sha256:" + digest(APP_V2), size=16, color=HEAD).move_to(blocks[-1][1][1])
        new_man_d = digest("manifest " + " ".join(digest(c) for _, c in LAYERS[:-1]) + " " + digest(APP_V2))
        new_man = mono("image  sha256:" + new_man_d, size=16, color=HEAD).move_to(man[1][1])
        ver = label(r"version 2", font_size=16, color=WHITE).move_to(blocks[-1][1][0], RIGHT)
        reused = VGroup(*[SurroundingRectangle(b, color=YES, buff=0.03, stroke_width=1.5) for b in blocks[:-1]])
        reused_l = label(r"same names: \ reused from the build cache", font_size=17, color=YES).next_to(
            blocks, DOWN, buff=0.15).align_to(blocks, RIGHT)
        notes = VGroup(
            wrapped_label(r"a layer is an archive of the files one step wrote, \ named by its \textbf{SHA-256}; \ the "
                          r"manifest names the layers, \ and the image is named by the manifest's hash: \ a Merkle "
                          r"tree \ (Part 41)", 6.0, font_size=19, color=WHITE),
            wrapped_label(r"the build is Part 41's build graph: \ a step reruns only if its inputs changed, \ so the "
                          r"code is copied \textit{last}", 6.0, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(df, DOWN, buff=0.5).align_to(df, LEFT)
        ill = note(r"toy layers; \ real hashes of their illustrative contents", font_size=16).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The files come from an image, and an image is content-addressed, like Part 41's git objects. "
            "<bookmark mark='a'/> Each Dockerfile step that writes files makes a layer: an archive of exactly what "
            "it added or changed, named by the SHA-256 hash of its bytes. <bookmark mark='b'/> A manifest lists the "
            "layers' names in order, and the image is named by the manifest's hash, so one name vouches for every "
            "byte: a Merkle tree again. <bookmark mark='c'/> Change one line of the application and rebuild. Only "
            "the last layer has new contents, so only it and the manifest get new names; the layers below come from "
            "the build cache. <bookmark mark='d'/> That is why a Dockerfile copies the code last: a step reruns only "
            "when its inputs change, as in Part 41's build graphs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(df), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in blocks], lag_ratio=0.3),
                      *[df[1][i].animate.set_color(c) for i, c in enumerate(colors)],
                      run_time=2.5)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(man), Create(man_links))
            vo.wait_until("c")
            self.play(Indicate(df[1][4], color=HEAD))
            self.play(Transform(blocks[-1][1][1], new_top), Transform(blocks[-1][1][0], ver),
                      blocks[-1][0].animate.set_stroke(HEAD))
            self.play(Transform(man[1][1], new_man))
            self.play(Create(reused), FadeIn(reused_l))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def overlay(self):
        head = label(r"Union and copy-on-write", font_size=36).to_edge(UP, buff=0.3)
        cols = [-5.0, -2.5, -0.2, 1.9]
        fnames = ["/bin/sh", "/etc/app.conf", "/lib/python3", "/app/main.py"]
        planes_spec = [(r"what the container sees", KERN, 2.2), (r"upper: \ writable, \ this container's", YES, 1.25),
                       (r"layer: \ the app", DATA, 0.3), (r"layer: \ python", LAM, -0.5),
                       (r"layer: \ debian", GREY_B, -1.3)]
        planes = VGroup()
        for t, c, y in planes_spec:
            r = Rectangle(width=9.0, height=0.56, stroke_color=c, stroke_width=1.6, fill_color=c,
                          fill_opacity=0.08).move_to([-1.6, y, 0])
            planes.add(VGroup(r, label(t, font_size=17, color=c).next_to(r, RIGHT, buff=0.2)))
        planes[1][0].set_stroke(YES, width=2)
        where = {0: 4, 1: 4, 2: 3, 3: 2}          # file index -> plane index holding it
        files = {i: tag_box(fnames[i], color=planes_spec[p][1], size=16).move_to([cols[i], planes_spec[p][2], 0])
                 for i, p in where.items()}
        merged = {i: tag_box(fnames[i], color=KERN, size=16).move_to([cols[i], 2.2, 0]) for i in range(4)}
        drops = VGroup(*[DashedLine(merged[i].get_bottom(), files[i].get_top(), color=GREY_D, stroke_width=1.2)
                         for i in range(4)])
        read = Arrow(merged[1].get_bottom(), files[1].get_top(), buff=0.03, color=HEAD, stroke_width=4,
                     max_tip_length_to_length_ratio=0.08)
        copy_up = tag_box(fnames[1] + "*", color=YES, size=16).move_to([cols[1], 1.25, 0])
        white = tag_box("whiteout sh", color=NO, size=16).move_to([cols[0], 1.25, 0])
        cross = Cross(merged[0], stroke_color=NO, stroke_width=4)
        notes = VGroup(
            wrapped_label(r"\textbf{OverlayFS} \ (Linux, \ 2014): \ the higher layer wins; \ a read falls through to "
                          r"the highest layer holding the path", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"the first write \textbf{copies the file up}, \ then changes the copy \ (Part 32's "
                          r"copy-on-write, \ for files); \ a delete writes a \textbf{whiteout}", 12.4, font_size=19,
                          color=YES),
            wrapped_label(r"a hundred containers of one image share the read-only layers, \ on disk and in the page "
                          r"cache; \ each pays only for what it writes", 12.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How do the layers become one file tree? <bookmark mark='a'/> Linux's overlay file system, merged in "
            "2014, stacks them, and the container sees their union. Where two layers hold the same path, the higher "
            "one wins. <bookmark mark='b'/> Reading a file falls through to the highest layer that has it. "
            "<bookmark mark='c'/> On top sits one writable layer for each container. The first write to a file "
            "copies it up from below, and changes the copy: Part 32's copy-on-write, applied to files. "
            "<bookmark mark='d'/> Deleting a file cannot change a read-only layer, so the upper layer records a "
            "whiteout that hides it. <bookmark mark='e'/> A hundred containers from one image share the read-only "
            "layers, on disk and in the page cache, and each pays only for what it writes."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(p) for p in planes[::-1]], lag_ratio=0.2),
                      *[FadeIn(f) for f in files.values()], run_time=2)
            vo.wait_until("a")
            self.play(*[FadeIn(m) for m in merged.values()], Create(drops), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(read))
            self.play(Indicate(files[1], color=HEAD))
            vo.wait_until("c")
            self.play(FadeOut(read), TransformFromCopy(files[1], copy_up), FadeIn(notes[1]))
            self.play(merged[1][0].animate.set_stroke(YES, width=3))
            vo.wait_until("d")
            self.play(FadeIn(white), Create(cross))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def pull(self):
        head = label(r"Pull only what you lack", font_size=36).to_edge(UP, buff=0.3)
        names = [c for _, c in LAYERS[:4]] + [LAYERS[4][1], APP_V2, "worker code"]
        short = ["debian", "python3", "requirements", "packages", "app v1", "app v2", "worker"]
        blob_col = [GREY_B, LAM, DATA, DATA, YES, HEAD, KERN]
        blobs = VGroup(*[tag_box(f"{s:<12} {digest(n)}", color=c, size=16, w=3.3, h=0.4)
                         for s, n, c in zip(short, names, blob_col)]).arrange(DOWN, buff=0.1)
        mans = VGroup(*[tag_box(t, color=WHITE, size=16, w=1.7, h=0.42) for t in ("web:v1", "web:v2", "worker")])
        mans.arrange(DOWN, buff=0.9)
        reg_inner = VGroup(mans, blobs).arrange(RIGHT, buff=0.8)
        reg = RoundedRectangle(width=reg_inner.width + 0.5, height=reg_inner.height + 0.8, corner_radius=0.15,
                               stroke_color=GREY_B, stroke_width=2)
        reg_inner.move_to(reg).shift(DOWN * 0.15)
        reg_l = label(r"a registry: \ each blob stored once, \ by hash", font_size=18, color=GREY_A).next_to(
            reg.get_top(), DOWN, buff=0.12)
        registry = VGroup(reg, reg_inner, reg_l).to_edge(LEFT, buff=0.35).shift(DOWN * 0.15)
        uses = {0: [0, 1, 2, 3, 4], 1: [0, 1, 2, 3, 5], 2: [0, 1, 6]}
        refs = VGroup()
        for m, bs in uses.items():
            for b in bs:
                refs.add(Line(mans[m].get_right(), blobs[b].get_left(), color=GREY_D, stroke_width=1.2))
        have = VGroup(*[tag_box(f"{s:<12} {digest(n)}", color=c, size=16, w=3.3, h=0.4)
                        for s, n, c in zip(short[:5], names[:5], blob_col[:5])]).arrange(DOWN, buff=0.1)
        hbox = RoundedRectangle(width=3.9, height=3.6, corner_radius=0.15, stroke_color=DATA, stroke_width=2)
        have.move_to(hbox).shift(UP * 0.1)
        host_l = label(r"a machine that ran web:v1", font_size=18, color=DATA).next_to(hbox, UP, buff=0.12)
        VGroup(hbox, have, host_l).to_edge(RIGHT, buff=0.4).align_to(registry, UP).shift(DOWN * 0.1)
        new = blobs[5].copy()
        target = new.copy().next_to(have, DOWN, buff=0.1)
        go = Arrow(blobs[5].get_right(), target.get_left(), buff=0.1, color=HEAD, stroke_width=3,
                   max_tip_length_to_length_ratio=0.06)
        got_l = wrapped_label(r"one layer downloaded, \ checked against its hash", 1.9, font_size=17,
                              color=HEAD).next_to(go, UP, buff=0.12)
        foot = wrapped_label(r"the \textbf{Open Container Initiative} \ (2015): \ one image format and one runtime "
                             r"specification, \ so an image built by one tool runs under any compliant runtime, \ "
                             r"such as runc", 12.4, font_size=19, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Content addressing pays again when images move. <bookmark mark='a'/> A registry stores each blob once, "
            "under its hash, and an image is only a manifest that points at blobs. Our images "
            "share their lower layers. <bookmark mark='b'/> A machine that already ran version one pulls version "
            "two by fetching the manifest, comparing names, and downloading the single layer it lacks, checking it "
            "against its hash as Part 41's store did. <bookmark mark='c'/> In 2015 Docker and others founded the "
            "Open Container Initiative, which standardized the image format and the runtime, so an image built "
            "with one tool runs under any compliant runtime, such as runc. Every orchestrator in the next chapter "
            "starts here: pull, unpack, and start a process with walls."
        ) as vo:
            self.play(FadeIn(head), Create(reg), FadeIn(reg_l), FadeIn(blobs))
            vo.wait_until("a")
            self.play(FadeIn(mans), Create(refs), run_time=2)
            vo.wait_until("b")
            self.play(Create(hbox), FadeIn(have), FadeIn(host_l))
            self.play(GrowArrow(go), FadeIn(got_l))
            self.play(Transform(new, target))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM)
