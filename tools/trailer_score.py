"""Original score for the channel trailer (synthesized; no samples). Sections line up with tools/trailer.py's timeline."""
import numpy as np, wave, sys
SR = 44100
def render(path, T):
    dur = T["end"]; N = int(SR * dur); out = np.zeros(N); rng = np.random.default_rng(938749)
    def add(sig, t, g=1.0):
        i = int(t * SR)
        if i >= N or i < 0: return
        e = min(N, i + len(sig)); out[i:e] += sig[:e - i] * g
    def env(n, a=0.005, r=0.2):
        t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / r)
    def kick(p=1.0):
        t = np.arange(int(.4 * SR)) / SR; f = 45 + 140 * np.exp(-t * 32); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) * p
    def snare():
        t = np.arange(int(.22 * SR)) / SR; return (rng.standard_normal(len(t)) * .55 + np.sin(2 * np.pi * 185 * t) * .3) * np.exp(-t * 17)
    def hat(o=False):
        t = np.arange(int((.14 if o else .045) * SR)) / SR; return np.diff(rng.standard_normal(len(t)), prepend=0) * np.exp(-t * (22 if o else 90)) * .16
    def tone(f, l, kind="saw", g=.1, decay=3.0):
        t = np.arange(int(l * SR)) / SR
        if kind == "saw": s = 2 * ((f * t) % 1) - 1
        elif kind == "sq": s = np.sign(np.sin(2 * np.pi * f * t))
        else: s = np.sin(2 * np.pi * f * t)
        return s * g * np.exp(-t * decay) * np.minimum(1, (l - t) * 30)
    def bass(f, l):
        t = np.arange(int(l * SR)) / SR; s = np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * 2 * f * t); return np.tanh(2 * s) * .33 * np.minimum(1, (l - t) * 20)
    def boom():  # cinematic hit: sub drop + noise burst + low brass-ish chord
        t = np.arange(int(2.6 * SR)) / SR; f = 30 + 70 * np.exp(-t * 4)
        sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.4) * 1.2
        nz = rng.standard_normal(len(t)) * np.exp(-t * 6) * .35
        br = sum(np.tanh(3 * (2 * ((fr * t) % 1) - 1)) for fr in (55, 82.4, 110)) * .07 * np.exp(-t * 1.1)
        return sub + nz + br
    def riser(l):
        t = np.arange(int(l * SR)) / SR; n = rng.standard_normal(len(t)); f = 200 + 2400 * (t / l) ** 2
        return (n * .5 + np.sin(2 * np.pi * np.cumsum(f) / SR) * .25) * (t / l) ** 2 * .45
    def scratch():
        t = np.arange(int(.35 * SR)) / SR; f = 900 * (1 - t / .35) + 120
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * rng.standard_normal(len(t)) * .5 * np.exp(-t * 4)
    def ting():
        t = np.arange(int(1.2 * SR)) / SR; return sum(np.sin(2 * np.pi * fr * t) * a for fr, a in ((2637, .2), (3951, .12), (5274, .06))) * np.exp(-t * 3.5)
    root = 55.0
    # A: intro (cover + punch) ---------------------------------------------------
    add(riser(T["punch"]) * .8, 0); add(kick(1.4), T["punch"]); add(rng.standard_normal(int(.5 * SR)) * np.exp(-np.arange(int(.5 * SR)) / SR * 8) * .35, T["punch"])
    # B: groove under "AI does everything" -----------------------------------------
    bpm = 140; beat = 60 / bpm; t = T["ai0"]; b = 0
    prog = [0, 0, -4, -2]; mel = [0, 3, 7, 10, 12, 10, 7, 3]
    while t < T["but"] - 1e-6:
        bar = (b // 4) % 4; r = root * 2 ** (prog[bar] / 12)
        if b % 4 in (0, 2): add(kick(), t)
        if b % 4 in (1, 3): add(snare(), t)
        for k in range(4): add(hat(k == 2), t + k * beat / 4)
        if b % 2 == 0: add(bass(r, beat * 1.8), t)
        add(tone(r * 8 * 2 ** (mel[b % 8] / 12), beat * .9, "sq", .05, 4), t + beat / 2)
        t += beat; b += 1
    # C: "But…" record scratch then a heartbeat in silence ------------------------
    add(scratch(), T["but"]); add(kick(.7), T["but"] + .55); add(kick(.5), T["but"] + .78)
    # D: counters: drum roll speeding up + riser + pulsing bass on each counter -----
    t0, t1 = T["cnt0"], T["no0"]
    t = t0
    while t < t1:
        p = (t - t0) / (t1 - t0); step = .25 - .19 * p
        add(snare() * (.25 + .5 * p), t); t += step
    add(riser(t1 - t0) * .9, t0)
    for k, tc in enumerate(T["counters"]):
        add(kick(1.1), tc); add(bass(root * 2 ** ([0, 3, 5, 7][k % 4] / 12), .5), tc); add(tone(root * 16 * 2 ** ([0, 3, 5, 7][k % 4] / 12), .4, "saw", .06, 5), tc)
    # E: rejected turtles: comic stabs on every REJECTED stamp ----------------------
    for ts in T["stamps"]:
        add(tone(110, .18, "sq", .12, 12), ts); add(hat(True), ts)
    # F: the reveal: silence, low drone, three booms, ting on the aviators -----------
    td = T["dark"]; tr = T["reveal"]
    t = np.arange(int((tr - td + 1.5) * SR)) / SR
    drone = (np.sin(2 * np.pi * 41.2 * t) + .5 * np.sin(2 * np.pi * 61.7 * t + np.sin(2 * np.pi * .3 * t))) * .22 * np.minimum(1, t / 1.5)
    add(drone, td)
    for k, tb in enumerate(T["booms"]): add(boom() * (0.8 + 0.15 * k), tb)
    add(ting(), T["glint"])
    # G: lineup + title: the groove comes back bigger --------------------------------
    t = T["team"]; b = 0
    while t < T["end"] - .8:
        bar = (b // 4) % 4; r = root * 2 ** (prog[bar] / 12)
        if b % 2 == 0: add(kick(1.1), t)
        if b % 4 in (1, 3): add(snare() * 1.1, t)
        for k in range(4): add(hat(k == 2), t + k * beat / 4)
        if b % 2 == 0: add(bass(r, beat * 1.8), t)
        for iv in (0, 7, 12): add(tone(r * 4 * 2 ** (iv / 12), beat * .95, "saw", .035, 2), t)
        add(tone(r * 8 * 2 ** (mel[(b + 3) % 8] / 12), beat * .9, "sq", .05, 4), t + beat / 2)
        t += beat; b += 1
    fade = np.ones(N); fade[-int(1.0 * SR):] = np.linspace(1, 0, int(1.0 * SR)); out *= fade
    out = np.tanh(out / np.max(np.abs(out)) * 1.6) * .89
    data = (np.stack([out, out], 1) * 32767).astype("<i2")
    w = wave.open(path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes()); w.close()
