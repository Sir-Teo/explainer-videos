"""Lab 29: run AES-128 from scratch, watch one flipped bit spread round by round, and find hash collisions at the birthday rate."""

from videos.coursekit import labs

import random

import numpy as np

from explainer.cs.algo import crypto as K

TITLE = "AES from scratch: the standard's vector, the avalanche, ECB, and the birthday bound"
GOAL = ("Check the series' AES-128 against the FIPS-197 example, flip one plaintext bit and count how many of the 128 "
        "state bits differ after each round, count distinct ciphertext blocks of a striped image under ECB and CBC, and "
        "compare the number of hashes needed for a collision on truncated SHA-256 with sqrt(pi/2) 2^(n/2).")
TASKS = [
    "Stop AES after 1, 2 and 3 rounds (rounds=) and count how many of the 16 bytes a one-bit change has reached. Why does full diffusion take two rounds?",
    "Encrypt the striped image in CTR mode with K.ctr_encrypt, then flip one ciphertext bit and decrypt. Which plaintext bits change, and what does that say about integrity?",
    "Run the birthday experiment at 24 bits. How many hashes do you predict, and how many would a 256-bit hash need?",
]
TRIALS = 150
BITS = (8, 12, 16, 20)


def run(seed=0):
    rng = random.Random(int(np.random.default_rng(seed).integers(2 ** 31)))
    lab = labs.Lab()

    # 1. the standard's example (FIPS-197, Appendix C.1), and decryption inverts encryption
    key = bytes(range(16))
    plain = bytes.fromhex("00112233445566778899aabbccddeeff")
    aes = K.AES(key)
    cipher = aes.enc(plain)
    lab.row("AES-128 on the FIPS-197 example", f"{cipher.hex()}   (the standard: 69c4e0d8...b4c55a)")
    assert cipher.hex() == "69c4e0d86a7b0430d8cdb78070b4c55a" and aes.dec(cipher) == plain

    # 2. the avalanche: one flipped plaintext bit, counted after every round
    diff = np.array(K.avalanche_by_round(rng, trials=TRIALS))
    mean, sd = diff.mean(axis=0), diff.std(axis=0)
    lab.row("bits differing after rounds 0, 1, 2", f"{mean[0]:.1f}, {mean[1]:.1f}, {mean[2]:.1f}   (the film: 1, 16.1, 64.4)")
    lab.row("after ten rounds", f"mean {mean[10]:.1f}, s.d. {sd[10]:.2f}   (Binomial(128, 1/2): 64, {np.sqrt(32):.2f})")
    assert mean[0] == 1 and 12 < mean[1] < 20, "one round reaches one column: about half of 32 bits"
    assert all(abs(m - 64) < 4 * np.sqrt(32 / TRIALS) + 0.2 for m in mean[2:]), "from round 2 on: half the bits"
    assert 4.3 < sd[10] < 7.2

    # 3. ECB leaks equal blocks; CBC does not
    image = bytes(40 + 50 * ((x // 8 + y // 4) % 4) for y in range(48) for x in range(64))      # diagonal stripes
    blocks = lambda data: {data[i:i + 16] for i in range(0, len(data), 16)}
    iv = bytes(rng.randrange(256) for _ in range(16))
    ecb, cbc = K.ecb_encrypt(aes, image), K.cbc_encrypt(aes, iv, image)
    lab.row(f"image of {len(image) // 16} blocks, {len(blocks(image))} distinct",
            f"ECB: {len(blocks(ecb))} distinct ciphertext blocks   CBC: {len(blocks(cbc))}")
    assert len(blocks(ecb)) == len(blocks(image)) < 10 and len(blocks(cbc)) == len(image) // 16
    assert K.cbc_decrypt(aes, iv, cbc) == image

    # 4. birthday collisions on SHA-256 cut to n bits
    need, theory = [], []
    for bits in BITS:
        trials = 200 if bits <= 16 else 40
        need.append(np.mean([K.birthday_trial(bits, rng) for _ in range(trials)]))
        theory.append(np.sqrt(np.pi / 2) * 2 ** (bits / 2))
        lab.row(f"collision on {bits} bits", f"{need[-1]:.0f} hashes on average   sqrt(pi/2) 2^(n/2) = {theory[-1]:.0f}")
        assert abs(need[-1] / theory[-1] - 1) < (0.2 if bits <= 16 else 0.4), "collisions come at the square root"
    lab.note = ("Two rounds of AES spread one bit over the whole state, and an n-bit hash resists collisions for only "
                "about 2^(n/2) tries; the cipher is sound, and the ECB leak comes from how it is used.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    r = np.arange(11)
    ax[0].fill_between(r, mean - sd, mean + sd, color=labs.BLUE, alpha=0.25, label="± one s.d.")
    ax[0].plot(r, mean, "o-", color=labs.BLUE, label=f"mean over {TRIALS} random keys and blocks")
    ax[0].axhline(64, color=labs.GOLD, ls="--", label="64: half of the 128 bits")
    ax[0].set(title="AES-128: state bits that differ after one flipped input bit", xlabel="rounds completed",
              ylabel="bits differing", xticks=r)
    ax[0].legend(loc="lower right")
    grid = np.linspace(7, 21, 50)
    ax[1].semilogy(grid, np.sqrt(np.pi / 2) * 2 ** (grid / 2), color=labs.GOLD, label="√(π/2) · 2^(n/2)")
    ax[1].semilogy(grid, 2.0 ** grid, color=labs.MUTED, ls="--", label="2ⁿ: one try per possible value")
    ax[1].semilogy(BITS, need, "o", color=labs.RED, label="measured, truncated SHA-256")
    ax[1].set(title="Hashes until two collide", xlabel="hash length n (bits)", ylabel="hashes", xticks=BITS)
    ax[1].legend()
    lab.fig = fig
    return lab
