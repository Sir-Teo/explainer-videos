"""Lab 19: count Karatsuba's leaves and the FFT's butterflies, multiply by FFT, and solve one problem four ways."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.algo import paradigms as pd

TITLE = "Three products, n log n butterflies, and one problem four ways"
GOAL = ("Count the digit products of school multiplication and of Karatsuba, and the butterflies of the FFT, against "
        "n^2, 3^lg n and (n/2) lg n; multiply by FFT and check every coefficient against the exact convolution; then "
        "run the four maximum-subarray algorithms on the same arrays.")
TASKS = [
    "Call pd.karatsuba with cutoff=32 and count again. How many digit products does the cutoff add at n = 128, and why is it still faster in wall-clock time?",
    "Draw the digits from 0..9 instead of 1..9. The Karatsuba count drops below 3^k: find the line of school_mul that explains it.",
    "Raise the chunk in the FFT experiment from 4 decimal digits to 6 and find the length at which a rounded coefficient is first wrong.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Karatsuba: 3^k digit products for two n = 2^k digit numbers, against the school method's n^2
    ks = np.arange(1, 8)
    school, kara = [], []
    for k in ks:
        n = 2 ** int(k)
        a = [int(d) for d in rng.integers(1, 10, n)]  # no zero digits: the school leaf skips a zero row
        b = [int(d) for d in rng.integers(1, 10, n)]
        cs, ck = [0], [0]
        ps, pk = pd.school_mul(a, b, cs), pd.karatsuba(a, b, ck)
        exact = pd.from_digits(a) * pd.from_digits(b)
        assert pd.from_digits(ps) == exact and pd.from_digits(pk) == exact, "both multiply correctly"
        school.append(cs[0])
        kara.append(ck[0])
    assert school == [4 ** int(k) for k in ks], "the school method does n^2 digit products"
    assert kara == [3 ** int(k) for k in ks], "Karatsuba does 3^k digit products"
    lab.row("128 digits, school", f"{school[-1]:,} digit products   (n^2 = {128 * 128:,})")
    lab.row("128 digits, Karatsuba", f"{kara[-1]:,} digit products   (3^7 = {3 ** 7:,})")

    # 2. the FFT: (n/2) lg n butterflies, the same numbers as the n^2 sum
    fs = np.arange(1, 11)
    flies = []
    for k in fs:
        n = 2 ** int(k)
        x = list(rng.standard_normal(n) + 1j * rng.standard_normal(n))
        c = [0]
        y = pd.fft(x, c)
        flies.append(c[0])
        assert np.allclose(y, np.fft.fft(x), atol=1e-8), "the recursive FFT agrees with numpy"
        if n <= 128:
            d = [0]
            assert np.allclose(pd.dft(x, d), y, atol=1e-7) and d[0] == n * n, "and with the n^2 definition"
        assert np.allclose(pd.ifft(y), x, atol=1e-9), "the inverse is the conjugate transform over n"
    assert flies == [(2 ** int(k) // 2) * int(k) for k in fs], "(n/2) lg n butterflies"
    lab.row("1,024 points, FFT", f"{flies[-1]:,} butterflies   ((n/2) lg n = {512 * 10:,}; the definition: {1024 ** 2:,} products)")

    # 3. multiplying by FFT: every rounded coefficient against the exact integer convolution
    ms, gaps = 2 ** np.arange(4, 13), []
    for m in ms:
        a, b = rng.integers(0, 10 ** 4, m), rng.integers(0, 10 ** 4, m)  # four decimal digits per coefficient
        n = 2 * int(m)
        c = np.fft.irfft(np.fft.rfft(a.astype(float), n) * np.fft.rfft(b.astype(float), n), n)[:2 * m - 1]
        gaps.append(float(np.abs(c - np.rint(c)).max()))
        assert np.array_equal(np.rint(c).astype(np.int64), np.convolve(a, b)), "the rounded FFT is the convolution"
    x = pd.from_digits([int(d) for d in rng.integers(0, 10, 19_999)] + [7])
    y = pd.from_digits([int(d) for d in rng.integers(0, 10, 19_999)] + [3])
    assert pd.fft_bigmul(x, y) == x * y, "a 20,000-digit product, exact"
    p, q = [int(d) for d in rng.integers(0, 10, 64)], [int(d) for d in rng.integers(0, 10, 64)]
    assert pd.poly_mul_fft(p, q) == pd.school_mul(p, q)[:127], "the series' own FFT, against the school product"
    lab.row("FFT product, 4,096 coefficients", f"all exact; farthest from an integer before rounding: {gaps[-1]:.1e}")
    lab.row("20,000 digits by FFT", "equal to Python's exact product")

    # 4. one problem, four paradigms
    for _ in range(40):
        arr = [int(v) for v in rng.integers(-9, 10, int(rng.integers(1, 60)))]
        answers = {pd.maxsub_cubic(arr), pd.maxsub_quadratic(arr), pd.maxsub_divide(arr), pd.maxsub_kadane(arr)}
        assert len(answers) == 1, "the four algorithms agree"
    assert pd.maxsub_kadane([-5, -2, -7]) == -2, "a nonempty answer: the largest element when all are negative"
    lab.row("maximum subarray", "cubic, quadratic, divide and conquer and Kadane agree on 40 arrays")
    lab.note = ("A better identity changes the exponent: 3^k leaves instead of 4^k, and (n/2) lg n butterflies "
                "instead of n^2 products. The small distance to an integer is a diagnostic, not a proof; the proof "
                "here is the comparison with the exact convolution.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    n = 2.0 ** ks
    ax[0].loglog(n, school, "o-", color=labs.RED, label="school: n²")
    ax[0].loglog(n, kara, "o-", color=labs.GOLD, label="Karatsuba: 3^lg n = n^1.585")
    ax[0].loglog(n, [3 * m * np.log2(2 * m) for m in n], "o-", color=labs.BLUE,
                 label="three FFTs of length 2n: 3n lg 2n butterflies")
    ax[0].set(title="Multiplications to multiply two n-digit numbers", xlabel="digits n", ylabel="count")
    ax[0].legend()
    ax[1].loglog(ms, gaps, "o-", color=labs.GOLD, label="largest distance to an integer")
    ax[1].axhline(0.5, color=labs.RED, ls="--", label="0.5: rounding could go wrong")
    ax[1].set(title="Floating FFT convolution, base 10⁴: rounding margin", xlabel="coefficients per factor",
              ylabel="|value − nearest integer|", ylim=(1e-9, 2))
    ax[1].legend(loc=(0.04, 0.62))
    lab.fig = fig
    return lab
