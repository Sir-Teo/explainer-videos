from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, FAIL, HIST, MONO, OBS, PART, REWARD, TOOL, WORLD, load, node_box, trace_box


class Loop(VoiceoverScene):
    def construct(self):
        self.card()
        self.react()
        self.trace()
        self.tools()
        self.mcp()

    def card(self):
        card = chapter_card(3, r"The agent loop", r"How does a language model act?", lit=(2026,), part=PART)
        with self.voiceover("Chapter three. The agent loop."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def react(self):
        ctx = RoundedRectangle(width=5.4, height=4.6, corner_radius=0.15, stroke_color=GREY_C, stroke_width=2)
        ctx.move_to([-3.6, -0.3, 0])
        cl = label(r"the context window", font_size=24, color=GREY_A).next_to(ctx, UP, buff=0.12)
        kinds = [(r"task", WORLD), (r"Thought", GREY_A), (r"Action", AGENT), (r"Observation", TOOL), (r"Thought", GREY_A),
                 (r"Action", AGENT), (r"Observation", TOOL), (r"Answer", REWARD)]
        rows = VGroup(*[node_box(k, c, 20, height=0.42, fill=0.12) for k, c in kinds])
        rows.arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(ctx).align_to(ctx, UP).shift(DOWN * 0.2)
        for r_ in rows:
            r_.align_to(ctx, LEFT).shift(RIGHT * 0.3)
        model = node_box(r"language model", AGENT, 26, height=0.9).move_to([2.6, 1.4, 0])
        env = node_box(r"tools: \ search, \ code, \ files", TOOL, 26, height=0.9).move_to([2.6, -1.6, 0])
        a1 = Arrow(model.get_bottom(), env.get_top(), buff=0.1, color=AGENT)
        a2 = CurvedArrow(env.get_left() + LEFT * 0.05, rows[3].get_right() + RIGHT * 0.1, angle=-0.5, color=TOOL)
        a3 = CurvedArrow(ctx.get_right() + UP * 1.6, model.get_left() + LEFT * 0.05, angle=-0.4, color=GREY_B)
        hist = history_card(2022, r"ReAct \ (Yao, Zhao, Yu, Du, Shafran, Narasimhan \& Cao)", r"interleave reasoning "
                            r"and acting: \ on two text games, \ $34$ and $10$ points more success than imitation "
                            r"and reinforcement learning, \ from one or two examples in the prompt", width=6.4,
                            color=HIST, font_size=19).to_corner(DR, buff=0.25)
        with self.voiceover(
            "A language model only writes text. To make it an agent, put it in a loop. <bookmark mark='a'/> The "
            "context starts with a task. The model writes a thought, <bookmark mark='b'/> then an action, in a form a "
            "program can read: search for this, run that. <bookmark mark='c'/> The program carries the action out "
            "and pastes the result back into the context as an observation. <bookmark mark='d'/> The model reads "
            "everything again and writes the next thought and action, until it writes an answer. "
            "<bookmark mark='e'/> This pattern, reasoning interleaved with acting, was named ReAct by Shunyu Yao and "
            "colleagues in 2022. With one or two worked examples in the prompt, it beat agents trained by imitation and "
            "reinforcement learning on two text-based tasks."
        ) as vo:
            self.play(Create(ctx), FadeIn(cl), FadeIn(rows[0]), FadeIn(model), FadeIn(env))
            vo.wait_until("a")
            self.play(Create(a3), FadeIn(rows[1], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.1), GrowArrow(a1))
            vo.wait_until("c")
            self.play(Create(a2), FadeIn(rows[3], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows[4:]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(hist, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trace(self):
        a = load("agent")
        tr = a["traces"]["react"]
        items = a["trace_items"]
        prices = a["trace_prices"]
        task = data_text(f'Task: what do one {items[0]}, one {items[1]} and one {items[2]} cost in all?', font=MONO,
                         font_size=20, color=WORLD)
        box = trace_box(tr["lines"], chars=46, font_size=19)
        col = Group(task, box).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([-2.3, -0.1, 0])
        if col.height > 6.9:
            col.height = 6.9
            col.move_to([-2.3, -0.1, 0])
        tools = code_block([r'shelf(k)    -> the items on shelf k', r'price(item) -> its price, or an error',
                            r'add(a, b)   -> a + b'], font_size=18)
        tools_t = label(r"the tools", font_size=24, color=TOOL)
        tbox = VGroup(tools_t, tools).arrange(DOWN, buff=0.15, aligned_edge=LEFT).to_corner(UR, buff=0.4)
        errs = [k for k, ln in enumerate(box.rows) if "error" in ln.text]
        tag = note(r"a simulated agent: \ the tools are real code, \ the ``model'' is a script with error rates we "
                   r"set, \ no language model", font_size=18).to_corner(DR, buff=0.25)
        if tag.width > 5.6:
            tag.width = 5.6
            tag.to_corner(DR, buff=0.25)
        total = sum(prices)
        n_err = len([ln for ln in tr["lines"] if "error" in ln])
        slip = "Here it misspells an item once." if n_err == 1 else f"Here it misspells an item {n_err} times."
        verdict = f"the answer, {total}, is right." if tr["right"] else "even so, this answer is wrong."
        with self.voiceover(
            "Here is a loop running for real, in a small warehouse of our own. The tools are a few functions: list "
            "a shelf, look up a price, add. <bookmark mark='a'/> The task: what do three items cost together? The "
            "agent's moves come from a script with error rates we chose, not from a language model, so we can "
            "count what goes wrong. <bookmark mark='b'/> It looks up a price, reads the observation, keeps a running "
            f"total. <bookmark mark='c'/> {slip} The tool answers with an error, "
            "the error lands in the context, and the agent tries again. <bookmark mark='d'/> Seeing the result of "
            f"every action is what lets it recover: {verdict}"
        ) as vo:
            self.play(FadeIn(tbox), FadeIn(task), FadeIn(tag), FadeIn(box[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in box.rows[:5]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            upto = errs[0] if errs else 6
            self.play(LaggedStart(*[FadeIn(r_) for r_ in box.rows[5:upto]], lag_ratio=0.4), run_time=1.0)
            vo.wait_until("c")
            last = errs[-1] + 1 if errs else upto
            self.play(LaggedStart(*[FadeIn(r_) for r_ in box.rows[upto:last]], lag_ratio=0.4), run_time=1.5)
            if errs:
                self.play(*[Indicate(box.rows[k], color=FAIL, scale_factor=1.03) for k in errs])
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in box.rows[last:]], lag_ratio=0.4), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tools(self):
        schema = code_block([r'{"name": "price",', r' "description": "The price of one item",',
                             r' "parameters": {"type": "object",', r'   "properties": {"item": {"type": "string"}},',
                             r'   "required": ["item"]}}'], font_size=19)
        st = label(r"the tool, \ described to the model \ (a JSON schema)", font_size=22, color=TOOL)
        left = VGroup(st, schema).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([-3.4, 1.4, 0])
        call = code_block([r'{"name": "price", "arguments": {"item": "valve"}}'], font_size=19, color=AGENT)
        ct = label(r"the model's call", font_size=22, color=AGENT)
        mid = VGroup(ct, call).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([-3.4, -1.0, 0])
        for g_ in (left, mid):
            if g_.width > 6.6:
                g_.width = 6.6
        res = code_block([r'{"result": 56}'], font_size=19, color=TOOL).next_to(mid, DOWN, buff=0.35).align_to(mid, LEFT)
        cards = VGroup(
            history_card(r"Feb 2023", r"Toolformer \ (Schick et al., Meta)", r"a model teaches itself when to call a "
                         r"calculator, \ a search engine, \ a calendar: \ it keeps the calls that make the following "
                         r"text easier to predict", width=5.6, color=HIST, font_size=19),
            history_card(r"Jun 2023", r"function calling \ (OpenAI's API)", r"describe any function with a JSON "
                         r"schema; \ the model, \ fine-tuned for it, \ answers with the name and arguments", width=5.6,
                         color=HIST, font_size=19),
        ).arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "How does a model learn to use tools at all? <bookmark mark='a'/> In February 2023 Meta's Toolformer "
            "taught itself: it tried inserting calls to a calculator or a search engine into ordinary text, and kept "
            "the calls whose results made the next words easier to predict. <bookmark mark='b'/> In June 2023 "
            "OpenAI made it a product. A program describes each tool to the model with a schema: its name, what it "
            "does, its arguments. <bookmark mark='c'/> The model, fine-tuned for this, answers with a structured "
            "call instead of prose. <bookmark mark='d'/> The program runs it and hands back the result. Every agent "
            "since, coding agents included, is built on this handshake."
        ) as vo:
            self.play(FadeIn(left))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.15), Indicate(schema, color=TOOL, scale_factor=1.02))
            vo.wait_until("c")
            self.play(FadeIn(mid))
            vo.wait_until("d")
            self.play(FadeIn(res, shift=DOWN * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mcp(self):
        hosts = VGroup(*[node_box(t, AGENT, 22, height=0.6) for t in (r"a chat app", r"a coding agent", r"an IDE")])
        hosts.arrange(DOWN, buff=0.4).move_to([-4.6, 0.0, 0])
        servers = VGroup(*[node_box(t, TOOL, 22, height=0.6) for t in (r"files", r"a database", r"a browser",
                                                                         r"the issue tracker")])
        servers.arrange(DOWN, buff=0.3).move_to([4.6, 0.0, 0])
        hub = VGroup(Circle(radius=0.75, stroke_color=WHITE, stroke_width=2.5, fill_color=WHITE, fill_opacity=0.05),
                     label(r"MCP", font_size=30))
        hub[1].move_to(hub[0])
        hl = label(r"one protocol: \ JSON-RPC messages; \ a server offers tools, \ resources, \ prompts", font_size=20,
                   color=GREY_A).next_to(hub, DOWN, buff=0.3)
        mess = VGroup(*[Line(h.get_right(), s_.get_left(), color=GREY_D, stroke_width=1.5) for h in hosts for s_ in servers])
        clean = VGroup(*[Line(h.get_right(), hub.get_left(), color=AGENT, stroke_width=2) for h in hosts],
                       *[Line(hub.get_right(), s_.get_left(), color=TOOL, stroke_width=2) for s_ in servers])
        nm = MathTex(r"3 \times 4 = 12", font_size=34, color=GREY_B).to_edge(UP, buff=0.6)
        np_ = MathTex(r"3 + 4 = 7", font_size=34, color=WHITE).to_edge(UP, buff=0.6)
        cards = VGroup(
            history_card(r"Nov 2024", r"Model Context Protocol \ (Anthropic)", r"an open standard for connecting "
                         r"models to tools and data", width=4.4, color=HIST, font_size=18),
            history_card(r"Dec 2025", r"the Agentic AI Foundation \ (Linux Foundation)", r"MCP, \ OpenAI's AGENTS.md "
                         r"and Block's goose given a neutral home; \ over $10{,}000$ MCP servers published", width=4.4,
                         color=HIST, font_size=18),
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.2)
        a2a = label(r"and agent to agent: \ Google's A2A protocol (2025)", font_size=20, color=GREY_B)
        with self.voiceover(
            "Every app that hosts a model needs its tools, and every tool wants to serve every app. "
            "<bookmark mark='a'/> Wired up one by one, three apps and four tools take twelve integrations. "
            "<bookmark mark='b'/> In November 2024 Anthropic published the Model Context Protocol, MCP: a tool is "
            "wrapped once, as a server that lists what it offers, and any app that speaks the protocol can use it. "
            "Three plus four instead of three times four. <bookmark mark='c'/> It spread fast. By December 2025 more "
            "than ten thousand servers had been published, and the protocol was handed to a new foundation under "
            "the Linux Foundation, alongside OpenAI's AGENTS dot md and Block's goose. <bookmark mark='d'/> Google's "
            "A2A protocol does the same for agents talking to other agents."
        ) as vo:
            self.play(FadeIn(hosts), FadeIn(servers))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in mess], lag_ratio=0.05), FadeIn(nm), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(mess), FadeIn(hub), FadeIn(hl), ReplacementTransform(nm, np_))
            self.play(LaggedStart(*[Create(l_) for l_ in clean], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(cards, shift=UP * 0.15))
            vo.wait_until("d")
            a2a.next_to(np_, DOWN, buff=0.2)
            self.play(FadeIn(a2a))
        self.wait(0.3)
        self.clear_scene()
