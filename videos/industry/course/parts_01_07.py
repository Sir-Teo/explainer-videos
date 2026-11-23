"""Act I, Reading an Industry (Parts 1-7)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=1, level="U", widget="splitprice",
        question="When you pay for something, who gets the money, and why them?",
        story="The part opens in 2007 with a $299 iPod that said assembled in China: Linden, Kraemer and Dedrick "
              "followed its money and found that assembly came to $3.70, of which the assembler kept about 11 cents, "
              "while Apple took $80 and a Toshiba hard drive $73. The viewer then guesses how the $1,099 of a 256GB "
              "iPhone 17 Pro divides into five piles. The phone is taken apart into six layers made by companies in at "
              "least six economies; its parts cost about $520; value added shows why adding up sales counts the same "
              "dollar again at every link. The Dollar of one phone gives about $66 to the shop or carrier, $520 to the "
              "parts, $30 to assembly and about $244 of profit to Apple, checked against Apple's own 28 cents of profit "
              "per dollar of sales. Margins from filings, from Foxconn's 6% to Apple's services' 76%, show that the "
              "links hardest to replace keep the most; an iPhone leaves about eighteen times the gross profit of a "
              "Xiaomi phone. After an intermission of iPhone sales since 2008, the label is set against value added "
              "(the iPhone 3G's $178.96 import with $6.50 of Chinese work), and then the turn: in 2026 memory became "
              "the scarce link, memory prices rose five- to sevenfold, Micron's gross margin went from 40% to 81% and "
              "Samsung's chip division earned 106.5 trillion won in a quarter while its phones lost money. The part "
              "ends on the landscape as of November 2026, Ballmer's 2007 forecast, and the series' first call.",
        handoff="Part 2 measures every industry three ways with Leontief's input-output table; Part 3 reads the "
                "accounts behind the margins; Part 4 is the cost curve behind one more phone against the next design; "
                "Part 5 is the moat; Part 15 returns to the chips and Part 16 to the assemblers; Part 57 joins every "
                "model company into one web and looks for the chokepoints.",
        outside="Percentages and arithmetic. Nothing else.",
        objectives={
            "U": ["Explain why the factory named on a label can keep a few cents of a product's price.",
                  "Split a retail price into the shop, the parts, assembly, the brand's costs and its profit, and say "
                  "which pile is largest for a premium phone.",
                  "Explain why the companies hardest to replace keep the most, with an example from the phone."],
            "M": ["Compute value added along a chain from each firm's sales and show it sums to the final price.",
                  "Compute revenue and gross profit per unit from a company's segment revenue, units and margin.",
                  "Compare a price rise with a cost rise tier by tier and say who absorbs the difference."],
            "D": ["Bound a modelled profit per phone from the ranges of its inputs, and say which input matters most.",
                  "State a forecast about the industry with a date and a scoring rule, and say what would make it "
                  "wrong."],
            "I": ["Find a company's segment sales, margins, channel mix and manufacturing locations in its 10-K.",
                  "Tell a gross margin from an operating or pre-tax margin, and a unit share from a revenue share, "
                  "when comparing companies.",
                  "Draw a dated landscape of an industry's links and companies, by region."],
        },
        results=[
            ("Value added sums to the price", r"\sum_i (S_i - S_{i-1}) = S_n = \text{price}"),
            ("The Dollar", r"p = c + b + a + o + \text{opex} + \text{tax} + \pi"),
            ("Profit per unit", r"\pi_{\text{unit}} = \frac{\text{segment revenue}}{\text{units}} \times "
                                r"\text{gross margin}"),
            ("Who keeps the money", r"\text{margin rises as the number of substitutes falls}"),
            ("Pass-through by tier", r"\Delta p_k \;\text{vs}\; \Delta\text{DRAM} + G_k\,\Delta(\text{flash per GB})"),
        ],
        U=(0, 1, 2, 3, 4, 5, 7, "s09_intermission", 9), I=(6, 8, 11), D=(10, 12),
        also=(("The Register's rows for Part 1", "explainer/industry/data/rows_p01.py"),
              ("The chain arithmetic", "explainer/industry/works/chain.py")),
    ),
]
