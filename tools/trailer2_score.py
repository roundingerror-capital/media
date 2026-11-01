"""Original score for MEET THE FUND (tools/trailer2.py). Synthesized from scratch, no samples, no Gemini songs: safe for paid / ad use.
Sections follow trailer2.T: slam open, 140 bpm groove under the roster with a hit per card, drone + booms + ting for the Boss,
tape-stop rewind, a wobbly music-box flashback with comic plinks, tape-start fast-forward, then the groove comes back bigger."""
import numpy as np, wave
SR = 44100
def render(path, T):
    N = int(SR * T["end"]); out = np.zeros(N); rng = np.random.default_rng(20261101)
    def add(sig, t, g=1.0):
        i = int(t * SR)
        if i >= N or i < 0: return
        e = min(N, i + len(sig)); out[i:e] += sig[:e - i] * g
    def ts(l): return np.arange(int(l * SR)) / SR
    def kick(p=1.0):
        t = ts(.4); f = 45 + 140 * np.exp(-t * 32); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) * p
    def snare():
        t = ts(.22); return (rng.standard_normal(len(t)) * .55 + np.sin(2 * np.pi * 185 * t) * .3) * np.exp(-t * 17)
    def clap():
        t = ts(.25); n = rng.standard_normal(len(t)); e = sum(np.exp(-np.maximum(0, t - d) * 40) * (t >= d) for d in (0, .012, .024)); return n * e * .35
    def hat(o=False):
        t = ts(.14 if o else .045); return np.diff(rng.standard_normal(len(t)), prepend=0) * np.exp(-t * (22 if o else 90)) * .16
    def tone(f, l, kind="saw", g=.1, decay=3.0, vib=0):
        t = ts(l); ph = 2 * np.pi * np.cumsum(f * (1 + vib * np.sin(2 * np.pi * 5 * t))) / SR
        s = {"saw": (ph / (2 * np.pi)) % 1 * 2 - 1, "sq": np.sign(np.sin(ph)), "sin": np.sin(ph), "tri": 2 * np.abs(2 * ((ph / (2 * np.pi)) % 1) - 1) - 1}[kind]
        return s * g * np.exp(-t * decay) * np.minimum(1, (l - t) * 30) * np.minimum(1, t * 400)
    def bass(f, l):
        t = ts(l); s = np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * 2 * f * t); return np.tanh(2 * s) * .33 * np.minimum(1, (l - t) * 20)
    def boom(g=1.0):
        t = ts(2.6); f = 30 + 70 * np.exp(-t * 4)
        sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.4) * 1.2; nz = rng.standard_normal(len(t)) * np.exp(-t * 6) * .35
        br = sum(np.tanh(3 * (2 * ((fr * t) % 1) - 1)) for fr in (55, 82.4, 110)) * .07 * np.exp(-t * 1.1)
        return (sub + nz + br) * g
    def riser(l):
        t = ts(l); f = 200 + 2400 * (t / l) ** 2
        return (rng.standard_normal(len(t)) * .5 + np.sin(2 * np.pi * np.cumsum(f) / SR) * .25) * (t / l) ** 2 * .45
    def whoosh(l=.35):
        t = ts(l); n = rng.standard_normal(len(t)); return np.convolve(n, np.ones(8) / 8, "same") * np.sin(np.pi * t / l) ** 2 * .5
    def ting():
        t = ts(1.2); return sum(np.sin(2 * np.pi * fr * t) * a for fr, a in ((2637, .2), (3951, .12), (5274, .06))) * np.exp(-t * 3.5)
    def coin():
        t = ts(.35); return (np.sin(2 * np.pi * 1975 * t) * (t < .06) + np.sin(2 * np.pi * 2637 * t) * (t >= .06)) * np.exp(-t * 9) * .25
    def tape(l, down=True):  # tape stop / tape start sweep over a chord
        t = ts(l); k = t / l; sp = (1 - k) if down else k; f = sp * np.array([[220], [277], [330]])
        return np.sum(np.sin(2 * np.pi * np.cumsum(f, axis=1) / SR), 0) * .12 * (np.minimum(1, (1 - k) * 8) if down else 1)
    root = 55.0; bpm = 140; beat = 60 / bpm; prog = [0, 0, -4, -2]; mel = [0, 3, 7, 10, 12, 10, 7, 3]
    def groove(t0, t1, big=False):
        t = t0; b = 0
        while t < t1 - 1e-6:
            bar = (b // 4) % 4; r = root * 2 ** (prog[bar] / 12)
            if b % 2 == 0 or (big and b % 4 == 3): add(kick(1.1 if big else 1), t)
            if b % 4 in (1, 3): add(snare() * (1.1 if big else 1), t); add(clap(), t) if big else None
            for k in range(4): add(hat(k == 2), t + k * beat / 4)
            if b % 2 == 0: add(bass(r, beat * 1.8), t)
            if big:
                for iv in (0, 7, 12): add(tone(r * 4 * 2 ** (iv / 12), beat * .95, "saw", .035, 2), t)
            add(tone(r * 8 * 2 ** (mel[(b + (3 if big else 0)) % 8] / 12), beat * .9, "sq", .05, 4), t + beat / 2)
            t += beat; b += 1
    # cold open: riser into two slams
    add(riser(T["meet"]) * .8, 0); add(boom(.7), T["meet"]); add(kick(1.4), T["meet"]); add(boom(.9), T["fund"]); add(kick(1.5), T["fund"])
    # "I'm an AI trading bot": the groove starts, filtered-feel (no kick) then full
    t = T["bot"]
    while t < T["roster"]:
        for k in range(4): add(hat(k == 2), t + k * beat / 4)
        add(tone(root * 8 * 2 ** (mel[int((t - T["bot"]) / beat) % 8] / 12), beat * .9, "sq", .05, 4), t + beat / 2); t += beat
    add(riser(T["roster"] - T["bot"]) * .5, T["bot"])
    # roster: full groove with a whoosh + hit on every card
    groove(T["roster"], T["above"])
    for tc in T["cards"]: add(whoosh(), tc - .25); add(kick(1.3), tc); add(tone(root * 16, .3, "saw", .07, 6), tc)
    add(kick(1.4), T["team"]); add(tone(root * 4, 1.2, "saw", .08, 1.5), T["team"])
    # the boss: silence + drone, three booms, ting on the aviators, a regal brass stab
    t = ts(T["no1"] - T["above"])
    add((np.sin(2 * np.pi * 41.2 * t) + .5 * np.sin(2 * np.pi * 61.7 * t + np.sin(2 * np.pi * .3 * t))) * .22 * np.minimum(1, t / 1.0), T["above"])
    for k, tb in enumerate(T["booms"]): add(boom(.8 + .15 * k), tb)
    add(ting(), T["glint"]); add(ting() * .7, T["glint"] + .18)
    for iv in (0, 4, 7, 12): add(tone(110 * 2 ** (iv / 12), 2.4, "saw", .05, .8), T["boss"] + .1)
    # "THE BOSS IS #1.": hit + gold brass; "YET...": a hard stop, one low hit, a ting
    add(boom(.9), T["no1"] + .35); add(kick(1.5), T["no1"] + .35)
    for iv in (0, 4, 7, 12, 16): add(tone(146.8 * 2 ** (iv / 12), 1.3, "saw", .045, 1.2), T["no1"] + .35)
    add(boom(.6), T["yet"]); add(ting() * .8, T["yet"] + .9)
    # power rankings (glass): whoosh as the new #1 drops in, riser while her bar fills, crack, then shatter + boom
    add(whoosh(.4), T["slide"] - .1); add(kick(1.2), T["slide"] + .3)
    add(riser(T["crack"] - T["fill"]) * 1.1, T["fill"])
    tt = ts(T["crack"] - T["fill"]); add(np.sin(2 * np.pi * np.cumsum(220 + 880 * tt / tt[-1]) / SR) * .12 * (tt / tt[-1]), T["fill"])
    nz = rng.standard_normal(int(.12 * SR)); add(np.diff(nz, prepend=0) * np.exp(-np.arange(len(nz)) / SR * 30) * .9, T["crack"])
    nz = rng.standard_normal(int(1.2 * SR)); add(np.diff(nz, prepend=0) * np.exp(-np.arange(len(nz)) / SR * 4) * .7, T["shatter"])
    for k in range(14): add(tone(rng.uniform(2000, 6000), .5, "sin", .08, 6), T["shatter"] + k * .04)
    add(boom(1.0), T["shatter"])
    # rewind: tape stop
    add(tape(.7, True), T["rew"]); add(whoosh(.7) * .8, T["rew"])
    # flashback: wobbly music box (VHS vibe) + plinks on each please, a "?" on the ask, coins on yes
    t = T["fb"]; mb = [0, 4, 7, 12, 7, 4, 2, 5, 9, 14, 9, 5]; i = 0
    while t < T["ff"]:
        add(tone(523.25 * 2 ** (mb[i % len(mb)] / 12), .6, "tri", .05, 3, vib=.006), t); i += 1; t += .3
    for k, tb in enumerate(T["beg"]): add(tone(330 * 2 ** (k * 4 / 12), .18, "sq", .06, 10), tb)
    add(tone(392, .12, "sq", .05, 12), T["ask"]); add(tone(523, .2, "sq", .05, 10), T["ask"] + .12)
    add(tone(660, .14, "sq", .05, 10), T["fancy"]); add(tone(880, .25, "sq", .05, 8), T["fancy"] + .14)
    add(tone(1046, .3, "tri", .06, 6), T["what"]); add(tone(988, .3, "tri", .06, 6), T["what"] + .14)      # her: soft bells
    add(tone(1318, .45, "tri", .07, 5), T["why"])
    add(tone(784, .5, "tri", .06, 4), T["fine"]); add(tone(196, .6, "saw", .06, 4), T["fine"] + .1)
    for k in range(12): add(coin(), T["coins"] + k * .09 + rng.uniform(0, .04))
    # fast-forward: tape start, then the groove comes back bigger
    add(tape(.7, False), T["ff"]); add(whoosh(.7) * .8, T["ff"])
    add(boom(.8), T["biz"]); groove(T["biz"], T["end"] - .6, big=True)
    for tb in T["biz_lines"]: add(kick(1.3), tb)
    add(boom(.6), T["title"]); add(boom(.5), T["outro"])
    fade = np.ones(N); fade[-int(1.0 * SR):] = np.linspace(1, 0, int(1.0 * SR)); out *= fade
    out = np.tanh(out / np.max(np.abs(out)) * 1.6) * .89
    data = (np.stack([out, out], 1) * 32767).astype("<i2")
    w = wave.open(path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes()); w.close()
