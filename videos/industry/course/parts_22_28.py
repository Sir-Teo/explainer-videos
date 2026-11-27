"""Parts 22-28."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=22, level="U", widget="brandrun", prereq=(3, 4, 5, 20),
        question="Why can a company charge double for soap, for a hundred years?",
        story="The part opens on Procter & Gamble: $87.0bn of sales in fiscal 2026 against $43.4bn of cost of products, "
              "2.01 times; $10.2bn of advertising; Walmart 16% of its sales and its ten largest customers 43%. The viewer "
              "runs a detergent brand beside a store label at half the price: cutting the advertising earns $13m more in "
              "the first year and loses about a billion dollars of value over eight as share slides from 45% to 30%; cutting "
              "the price wins 67% of the shelf and earns less on every bottle. A dollar of P&G's sales is 50 cents of making, "
              "12 of advertising and 23 of operating profit; advertising is five times research. Gross margins run from "
              "Philip Morris International's 67% and Coca-Cola's 62% to Mondelez's 28%. Advertising wears off and is a fixed "
              "cost, so the biggest spenders pay least per unit: P&G's budget is larger than all of Clorox's sales. Walmart "
              "takes 26% of Clorox's sales and 22% of General Mills'; Costco's own label earns it higher margins than "
              "national brands. Coca-Cola's concentrate is 85% of its cases and 59% of its revenue, at a 62% gross margin "
              "against its bottler's 40%. P&G raised prices 9% in fiscal 2023 and lost 3% of volume; Hershey's margin fell "
              "from 47.3% to 33.5% on cocoa and tariffs. Altria shipped 10% fewer cigarettes in 2025 and offset most of it "
              "with price, at a 63% margin; Marlboro has led for over fifty years; PMI's smoke-free products reached 41% of "
              "its revenue. P&G's guidance ran high in fiscal 2025 and 2026; the series gives fiscal 2027 organic growth of "
              "3% or more 40%.",
        handoff="Part 23, fashion and luxury, turns to two industries that sell clothes and run on opposite rules.",
        outside="Percentages and present value; Part 3's accounts; Part 4's fixed costs; Part 5's moats; Economics, Built's "
                "logit demand, high-low pricing and reference prices.",
        objectives={
            "U": ["Explain why a branded product sells far above its cost and what the gap pays for.",
                  "Explain why advertising is a fixed cost that favours the biggest brands.",
                  "Explain the retailer's power: its size, its shelf and its own label."],
            "M": ["Model a brand's share with an advertising stock and a logit, and value holding, cutting and promoting.",
                  "Split a company's dollar of sales into making, advertising, other costs and profit.",
                  "Split sales growth into volume, price, mix and currency."],
            "D": ["Score a consumer-goods company's organic sales guidance against outcomes.",
                  "Make and state a dated, scorable forecast against a company's guidance range."],
            "I": ["Read a maker's largest-customer disclosure, advertising costs and net sales change drivers.",
                  "Read a beverage company's concentrate and finished-product split."],
        },
        results=[
            ("Advertising stock", r"S_t = (1-\delta) S_{t-1} + A_t,\quad S^* = A/\delta"),
            ("The brand's share (logit)", r"s = \frac{e^{k\sqrt{S} - \beta p + c}}{e^{k\sqrt{S} - \beta p + c} + e^{-\beta p_s}}"),
            ("Price over cost", r"\frac{\text{sales}}{\text{cost of sales}} = \frac{1}{1 - \text{gross margin}}"),
            ("Sales growth", r"g \approx g_{\text{volume}} + g_{\text{price}} + g_{\text{mix}} + g_{\text{fx}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, "s08_intermission", 7, 8), I=(9,), D=(10,),
        also=(("The Register's rows for Part 22", "explainer/industry/data/rows_p22.py"),
              ("The brand against a store label", "explainer/industry/works/brand.py"),
              ("The SEC and FRED extracts", "explainer/industry/data/SOURCES.md")),
    ),
]
