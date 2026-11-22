from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, code_block, image, load, \
    module_box


def pixel_tri(cols: int, rows: int, cell: float, a, b, c):
    """Which cells of a cols x rows grid have their centre inside the triangle abc (grid units, y down)."""
    def e(p, q, x, y):
        return (q[0] - p[0]) * (y - p[1]) - (q[1] - p[1]) * (x - p[0])
    s = np.sign(e(a, b, *c))
    return {(i, j) for j in range(rows) for i in range(cols)
            if all(s * e(p, q, i + 0.5, j + 0.5) > 0 for p, q in ((a, b), (b, c), (c, a)))}


class Gpu(WatchScene):
    def construct(self):
        self.card()
        self.stages()
        self.shaders()
        self.simt()
        self.earlyz()

    def card(self):
        self.chapter(6, r"The GPU pipeline", r"How does a chip run one small program on every pixel?", lit=(1982, 2001, 2005), extra=((1982, r"Clark: \ the Geometry Engine"),
                                                           (2001, r"programmable shaders"),
                                                           (2005, r"unified shaders")), part=PART, said="Chapter six. The GPU pipeline.")

    def stages(self):
        head = label(r"The graphics pipeline", font_size=36).to_edge(UP, buff=0.3)
        spec = [(r"vertex fetch", KERN, r"vertices"), (r"vertex shader", YES, r"clip-space vertices"),
                (r"clip and divide", KERN, r"screen triangles"), (r"rasterize", KERN, r"fragments"),
                (r"fragment shader", YES, r"colours"), (r"depth and blend", KERN, r"pixels")]
        boxes = VGroup(*[module_box(t, c, w=2.0, h=0.95, font=19) for t, c, _ in spec]).arrange(RIGHT, buff=0.25)
        boxes.move_to([0, 0.75, 0])
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.03, stroke_width=2,
                                color=GREY_B, max_tip_length_to_length_ratio=0.4) for i in range(5)])
        flows = VGroup(*[label(f, font_size=17, color=GREY_A).next_to(bx, DOWN, buff=0.15)
                         for (_, _, f), bx in zip(spec, boxes)])
        # the token that flows along the pipeline, one shape per stage
        y = 2.3

        def at(k):
            return np.array([boxes[k].get_x(), y, 0])
        tri3 = [1.35 * np.array(p) for p in ((-0.45, -0.3, 0), (0.45, -0.25, 0), (0.05, 0.4, 0))]
        tokens = [VGroup(*[Dot(at(0) + 0.8 * p, radius=0.06, color=DATA) for p in tri3])]
        rot = np.array([[np.cos(0.5), -np.sin(0.5), 0], [np.sin(0.5), np.cos(0.5), 0], [0, 0, 1]])
        tokens.append(VGroup(*[Dot(at(1) + rot @ p, radius=0.06, color=YES) for p in tri3]))
        tokens.append(Polygon(*[at(2) + rot @ p for p in tri3], color=WHITE, stroke_width=2.5))
        cell = 0.13
        tri_px = [(rot @ p)[:2] for p in tri3]
        frag = VGroup()
        shaded = VGroup()
        for i in range(-8, 9):
            for j in range(-8, 9):
                q = np.array([i * cell, j * cell])
                ins = True
                for k in range(3):
                    p0, p1 = tri_px[k], tri_px[(k + 1) % 3]
                    if (p1[0] - p0[0]) * (q[1] - p0[1]) - (p1[1] - p0[1]) * (q[0] - p0[0]) < 0:
                        ins = False
                if ins:
                    frag.add(Square(cell, stroke_width=0.5, stroke_color=BG, fill_color=GREY_B,
                                    fill_opacity=0.9).move_to(at(3) + np.array([*q, 0])))
                    t = np.clip(0.5 + q[0] + 0.3 * q[1], 0, 1)
                    shaded.add(Square(cell, stroke_width=0.5, stroke_color=BG,
                                      fill_color=interpolate_color(ManimColor(DATA), ManimColor(HEAD), t),
                                      fill_opacity=1).move_to(at(4) + np.array([*q, 0])))
        tokens += [frag, shaded, shaded.copy().move_to(at(5))]
        legend = VGroup(label(r"green: \ programs you write", font_size=19, color=YES),
                        label(r"orange: \ fixed-function hardware", font_size=19, color=KERN)).arrange(RIGHT,
                                                                                                    buff=0.8)
        braces = VGroup()
        for grp, txt, col in (((1,), r"chapters 1--2", YES), ((2, 3), r"chapter 3", KERN),
                              ((4,), r"chapters 4--5", YES)):
            br = Brace(VGroup(*[flows[k] for k in grp], *[boxes[k] for k in grp]), DOWN, buff=0.12, color=col)
            braces.add(VGroup(br, label(txt, font_size=20, color=col).next_to(br, DOWN, buff=0.1)))
        legend.next_to(braces, DOWN, buff=0.5)
        notes = VGroup(
            braces,
            wrapped_label(r"OpenGL, \ Direct3D, \ Vulkan, \ Metal and WebGPU all expose this same shape", 12.4,
                          font_size=21, color=GREY_A).to_edge(DOWN, buff=0.5),
        )
        with self.voiceover(
            "Everything so far is what a graphics processor does in hardware, organised as a pipeline. "
            "<bookmark mark='a'/> Vertices are fetched from memory and handed to a small program, the vertex "
            "shader, which applies the matrices of chapters one and two and outputs each vertex in clip "
            "coordinates. <bookmark mark='b'/> Fixed hardware clips, divides by w and maps to the screen, "
            "<bookmark mark='c'/> then rasterizes with chapter three's edge functions, producing fragments: "
            "candidate pixels carrying interpolated values. <bookmark mark='d'/> A second program, the fragment "
            "shader, computes each fragment's colour: chapters four and five. <bookmark mark='e'/> Finally the depth "
            "test and blending write the framebuffer. <bookmark mark='f'/> The green stages are programs you write; "
            "the orange ones are silicon. OpenGL, Direct3D, Vulkan, Metal and WebGPU all expose this same shape."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.15), Create(arrows),
                      FadeIn(flows))
            tok = tokens[0]
            self.play(FadeIn(tok))
            vo.wait_until("a")
            nxt = tokens[1]
            self.play(Transform(tok, nxt), Indicate(boxes[1], color=YES, scale_factor=1.05), FadeIn(braces[0]))
            vo.wait_until("b")
            self.play(Transform(tok, tokens[2]), Indicate(boxes[2], color=KERN, scale_factor=1.05))
            vo.wait_until("c")
            self.play(Transform(tok, tokens[3]), Indicate(boxes[3], color=KERN, scale_factor=1.05), FadeIn(braces[1]))
            vo.wait_until("d")
            self.play(Transform(tok, tokens[4]), Indicate(boxes[4], color=YES, scale_factor=1.05), FadeIn(braces[2]))
            vo.wait_until("e")
            self.play(Transform(tok, tokens[5]), Indicate(boxes[5], color=KERN, scale_factor=1.05))
            vo.wait_until("f")
            self.play(FadeIn(legend), FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def shaders(self):
        head = label(r"Two small programs", font_size=36).to_edge(UP, buff=0.3)
        vs = code_block(["uniform mat4 MVP;", "uniform mat3 Nmat;", "in vec3 pos, normal;", "in vec2 uv;",
                         "out vec3 n;", "out vec2 tc;", "void main() {", "  gl_Position = MVP * vec4(pos, 1.0);",
                         "  n  = Nmat * normal;", "  tc = uv;", "}"], size=18)
        fs = code_block(["uniform sampler2D tex;", "uniform vec3 L;", "in vec3 n;", "in vec2 tc;",
                         "out vec4 colour;", "void main() {", "  float d = max(dot(normalize(n), L), 0.0);",
                         "  colour = texture(tex, tc) * d;", "}"], size=18)
        tv = label(r"vertex shader: \ once per vertex", font_size=20, color=YES)
        tf = label(r"fragment shader: \ once per fragment", font_size=20, color=YES)
        left = VGroup(tv, vs).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        right = VGroup(tf, fs).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).next_to(head, DOWN, buff=0.4)
        ill = note(r"illustrative, \ in the style of GLSL", font_size=16).next_to(right, DOWN, buff=0.15).align_to(
            right, RIGHT)

        def hl(lines, color):
            return SurroundingRectangle(VGroup(*lines), color=color, buff=0.05, stroke_width=2)
        h1 = hl([vs[7], vs[8]], HEAD)
        h2 = VGroup(hl([vs[4], vs[5]], DATA), hl([fs[2], fs[3]], DATA))
        h3 = hl([fs[6]], HEAD)
        h4 = hl([fs[7]], LAM)
        notes = VGroup(
            wrapped_label(r"\textbf{matrices}: \ one combined model--view--projection matrix \ (chapters 1--2); \ "
                          r"normals by the inverse transpose \ (chapter 4)", 12.4, font_size=19, color=HEAD),
            wrapped_label(r"\textbf{outputs} \ \texttt{n} and \texttt{tc} are interpolated across the triangle, \ "
                          r"perspective-correctly, \ with chapter 3's $1/w$", 12.4, font_size=19, color=DATA),
            wrapped_label(r"\textbf{Lambert} \ (chapter 4); \ \texttt{texture} is chapter 5's trilinear lookup, \ in "
                          r"dedicated hardware", 12.4, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here are the two programs, in the style of OpenGL's shading language. <bookmark mark='a'/> The vertex "
            "shader runs once per vertex. It multiplies the position by one combined model, view and projection "
            "matrix, and moves the normal by the normal matrix, chapter four's inverse transpose. "
            "<bookmark mark='b'/> Whatever it outputs, here the normal and the texture coordinates, the rasterizer "
            "interpolates across the triangle, perspective-correctly, with chapter three's one over w. "
            "<bookmark mark='c'/> The fragment shader runs once per fragment: renormalize the normal and take "
            "Lambert's cosine, <bookmark mark='d'/> then multiply by a texture lookup. That one call is chapter "
            "five's trilinear filter, in dedicated hardware. <bookmark mark='e'/> Neither program can see any other "
            "vertex or fragment, and that independence is what lets a GPU run millions of them at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tv), FadeIn(vs))
            vo.wait_until("a")
            self.play(Create(h1), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(tf), FadeIn(fs), FadeIn(ill))
            self.play(Create(h2), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(h3))
            vo.wait_until("d")
            self.play(Create(h4), FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(Indicate(VGroup(left, right), color=WHITE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def simt(self):
        self.ask(r"$1920 \times 1080$ at 60 frames a second. \\ Fragment shader runs per second:", [r"about 2 million",
                 r"over a hundred million"], 1,
                 say="A screen of nineteen twenty by ten eighty, sixty frames a second. How many fragment shader runs per second?",
                 reveal="Over a hundred million, at least, which is why the GPU runs them in lockstep groups.")
        head = label(r"Thousands of fragments, \ one instruction stream", font_size=36).to_edge(UP, buff=0.3)
        cols, rows, cell = 16, 8, 0.36
        o = np.array([-6.4, 2.4, 0])

        def S(i, j):
            return o + np.array([(i + 0.5) * cell, -(j + 0.5) * cell, 0])
        inside = pixel_tri(cols, rows, cell, (0.5, 7.8), (15.6, 6.5), (6.0, 0.2))
        grid = VGroup(*[Square(cell, stroke_color=GREY_D, stroke_width=0.8,
                               fill_color=DATA if (i, j) in inside else BG, fill_opacity=0.55 if (i, j) in inside
                               else 0).move_to(S(i, j)) for j in range(rows) for i in range(cols)])
        quads = VGroup(*[Square(2 * cell, stroke_color=GREY_B, stroke_width=2).move_to(
            (S(2 * a, 2 * b) + S(2 * a + 1, 2 * b + 1)) / 2) for b in range(rows // 2) for a in range(cols // 2)
            if any((2 * a + p, 2 * b + q) in inside for p in (0, 1) for q in (0, 1))])
        warp = Rectangle(width=8 * cell, height=4 * cell, color=HEAD, stroke_width=4).move_to(
            (S(4, 4) + S(11, 7)) / 2)
        wl = label(r"one warp: \ 8 quads, \ 32 lanes", font_size=18, color=HEAD).next_to(grid, DOWN, buff=0.15)
        wl.align_to(grid, LEFT)
        ill = note(r"illustrative", font_size=16).next_to(grid, DOWN, buff=0.15).align_to(grid, RIGHT)
        code = code_block(["if (d > 0.5) {", "  colour = A();", "} else {", "  colour = B();", "}"], size=16)
        code.move_to([3.6, 2.0, 0])
        lanes = VGroup(*[Square(0.17, stroke_color=GREY_B, stroke_width=1, fill_color=GREY_E, fill_opacity=1)
                         for _ in range(32)]).arrange(RIGHT, buff=0.03)
        rng = np.random.default_rng(6)
        take = rng.random(32) < 0.55
        rowA = lanes.copy()
        rowB = lanes.copy()
        for k in range(32):
            rowA[k].set_fill(YES if take[k] else GREY_E, 1)
            rowB[k].set_fill(LAM if not take[k] else GREY_E, 1)
        laneg = VGroup(rowA, rowB).arrange(DOWN, buff=0.35).move_to([3.4, -0.1, 0])
        la = VGroup(label(r"step 1: \ run A, \ others masked", font_size=17, color=YES).next_to(rowA, UP, buff=0.08),
                    label(r"step 2: \ run B, \ others masked", font_size=17, color=LAM).next_to(rowB, UP, buff=0.08))
        laneg.add(la)
        notes = VGroup(
            wrapped_label(r"1920 $\times$ 1080 is about 2 million pixels, \ each a fragment shader run, \ 60 times a "
                          r"second", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"a warp \ (32 lanes on NVIDIA GPUs) \ shares one instruction stream: \ SIMT, \ from Part 10 "
                          r"and \textit{AI, Built} \ 17; \ a branch that splits a warp costs both sides", 12.4,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How many runs is that? A screen of nineteen twenty by ten eighty has about two million pixels, and "
            "each needs its own fragment shader run, sixty times a second. <bookmark mark='a'/> Because every run "
            "is independent, the GPU packs fragments, in blocks of two by two called quads, <bookmark mark='b'/> "
            "into groups that share one instruction stream: on NVIDIA hardware a warp of thirty-two lanes, the SIMT "
            "model of Part 10 and of AI, Built part seventeen. <bookmark mark='c'/> The price is branching. If some "
            "fragments of a warp take one side of an if and the rest take the other, <bookmark mark='d'/> the warp "
            "runs both sides, one after the other, with part of its lanes switched off each time. A shader that "
            "branches pixel by pixel can run at half speed, or worse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(ill), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(quads), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(warp), FadeIn(wl), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(code))
            vo.wait_until("d")
            self.play(FadeIn(rowA), FadeIn(la[0]))
            self.play(FadeIn(rowB), FadeIn(la[1]))
        self.wait(0.4)
        self.clear_scene()


    def earlyz(self):
        z = load("zbuffer")
        c = z["counters_zbuffer"]
        visible = c["covered"] - z["overlap"]
        head = label(r"Test depth before shading", font_size=36).to_edge(UP, buff=0.3)
        img = image(z["zbuffer"], height=2.7).move_to([-4.2, 1.0, 0])
        il = label(r"chapter 3's crossing triangles", font_size=17, color=GREY_A).next_to(img, DOWN, buff=0.12)
        vals = [c["covered"], c["depth_pass"], visible]
        chart = bar_chart(vals, [r"shade, \ then test", r"test, \ then shade", r"visible pixels"], [NO, HEAD, YES],
                          height=2.6, bar_w=1.1, gap=1.2, vmax=c["covered"], fmt_=lambda v: f"{v:,}".replace(
                              ",", "{,}"), font_size=19)
        chart.move_to([2.6, 0.9, 0])
        cap = label(r"fragment shader runs", font_size=18, color=GREY_A).next_to(chart, UP, buff=0.15)
        notes = VGroup(
            wrapped_label(rf"early depth test: \ {c['depth_fail']:,} fragments fail and are never shaded".replace(
                ",", "{,}"), 12.4, font_size=19, color=HEAD),
            wrapped_label(rf"still {c['depth_pass'] - visible:,} are shaded and then painted over by a nearer fragment "
                          r"drawn later".replace(",", "{,}"), 12.4, font_size=19, color=NO),
            wrapped_label(r"engines draw opaque objects front to back, \ or lay down depth in a first pass, \ then "
                          r"shade each visible pixel once; \ a shader that writes depth or discards turns early "
                          r"testing off", 12.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Last, where the depth test sits. <bookmark mark='a'/> Chapter three's two crossing triangles produce "
            "six thousand five hundred and seventy-six fragments. If every fragment is shaded first and depth-tested "
            "afterwards, every one of them pays for a fragment shader. <bookmark mark='b'/> GPUs test depth before "
            "shading whenever the shader cannot change the outcome. In our run, six hundred and ninety-three "
            "fragments fail the test, and are never shaded. <bookmark mark='c'/> But only five thousand four hundred "
            "and twelve pixels are visible: four hundred and seventy-one fragments passed, were shaded, and were "
            "painted over by a nearer one drawn later. <bookmark mark='d'/> So engines draw opaque objects front to "
            "back, or lay down depth in a first pass, and then shade each visible pixel exactly once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(img), FadeIn(il))
            vo.wait_until("a")
            self.play(FadeIn(chart[0]), FadeIn(cap), FadeIn(chart.bars[0]), FadeIn(chart.vals[0]),
                      FadeIn(chart.names[0]))
            vo.wait_until("b")
            self.play(FadeIn(chart.bars[1]), FadeIn(chart.vals[1]), FadeIn(chart.names[1]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(chart.bars[2]), FadeIn(chart.vals[2]), FadeIn(chart.names[2]), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
