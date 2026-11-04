"""Chiptune sound effects, synthesized (no samples, nothing licensed): the way NES/SNES-era SFX were built.
NES 2A03 had 2 pulse channels (duty 12.5/25/50/75 %), 1 triangle, 1 noise, 1 DPCM; SNES SPC700/DSP has 8 sample voices
with ADSR, pitch modulation, a noise generator and echo (FIR) in 64 KB of audio RAM. So a classic SFX is: one or two short
voices, a fast pitch sweep or an arpeggio, a hard envelope, maybe a noise burst on the attack, and a touch of echo.

    import sfx; bus = sfx.Bus(total_s); bus.add(sfx.click(), at=1.25, gain=0.12); bus.mix_into(music_np)   (mono float32, 44.1 kHz)
Recipes: click, key_slam, impact, ding (pickup), arp_up, bonk, zap, heal, roar, wipe, coin, whoosh, pop, step, thump, sparkle.
Mixing rules (the boss 2026-11-04 "SFX at ~50 %"): SFX sit under the music except on 2-3 hero moments; the music ducks ~5 dB
for 250 ms on a hero hit instead of the hit getting louder; vary repeats (pitch/time) so 20 key clicks don't sound like one loop."""
import numpy as np
SR = 44100
rng = np.random.default_rng(7)

def _t(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.002, d=0.08, s=0.0, r=0.02, sus=None):
    """ADSR on n samples (SNES-style hard attack, exponential-ish decay)."""
    a, r = int(a * SR), int(r * SR); e = np.ones(n, np.float32)
    if a: e[:a] = np.linspace(0, 1, a)
    dn = max(1, n - a - r); dec = np.exp(-np.arange(dn) / max(1, d * SR)); e[a:a + dn] = s + (1 - s) * dec[:len(e[a:a + dn])]
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e
def pulse(freq, d, duty=0.5):
    """Square/pulse with a per-sample frequency curve (array or float): phase-accumulated, so sweeps are clean."""
    n = int(d * SR); f = np.broadcast_to(np.asarray(freq, np.float64), (n,)) if np.ndim(freq) == 0 else np.interp(np.arange(n), np.linspace(0, n - 1, len(freq)), freq)
    ph = np.cumsum(f / SR) % 1.0; return np.where(ph < duty, 1.0, -1.0).astype(np.float32)
def tri(freq, d):
    n = int(d * SR); f = np.broadcast_to(np.asarray(freq, np.float64), (n,)) if np.ndim(freq) == 0 else np.interp(np.arange(n), np.linspace(0, n - 1, len(freq)), freq)
    ph = np.cumsum(f / SR) % 1.0; return (4 * np.abs(ph - 0.5) - 1).astype(np.float32)
def noise(d, rate=None, lp=None):
    """NES-style noise: random levels held for SR/rate samples (lower rate = darker)."""
    n = int(d * SR); hold = 1 if not rate else max(1, int(SR / rate))
    x = np.repeat(rng.choice([-1.0, 1.0], n // hold + 2), hold)[:n].astype(np.float32)
    if lp: k = max(1, int(SR / lp)); x = np.convolve(x, np.ones(k) / k, mode="same").astype(np.float32)
    return x
def echo(x, delay=0.09, fb=0.35, mix=0.3, taps=3):
    """SNES-flavoured echo: a few feedback taps, darker each time."""
    out = np.concatenate([x, np.zeros(int(delay * SR * taps), np.float32)]); dl = int(delay * SR); g = mix
    y = x.copy()
    for i in range(1, taps + 1):
        y = np.convolve(y, [0.5, 0.5], mode="same"); out[i * dl:i * dl + len(y)] += y * g; g *= fb
    return out
def note(n): return 440.0 * 2 ** ((n - 69) / 12)

# ---- recipes ----
def click(var=0.0):            # one keyboard key: short noise tick + tiny high blip
    d = 0.035; x = noise(d, rate=12000) * env(int(d * SR), d=0.006) * 0.8 + pulse(2400 * (1 + var), d, 0.125) * env(int(d * SR), d=0.004) * 0.3
    return x
def key_slam():                # the big AUTOMATE key: heavy switch clack + low body
    d = 0.22; n = int(d * SR)
    x = noise(d, rate=6000, lp=4000) * env(n, d=0.02) * 0.9 + pulse(np.linspace(220, 70, n), d, 0.25) * env(n, d=0.06) * 0.6
    return echo(x, 0.07, 0.3, 0.25)
def impact():                  # boom under the slam: sine-ish drop + noise tail
    d = 0.6; n = int(d * SR); f = np.geomspace(140, 38, n)
    x = tri(f, d) * env(n, d=0.25) * 1.0 + noise(d, rate=3000, lp=1200) * env(n, d=0.12) * 0.5
    return x
def ding(base=83):             # pickup: two quick notes up a fourth (B5 -> E6 by default)
    a = pulse(note(base), 0.07, 0.25) * env(int(0.07 * SR), d=0.2); b = pulse(note(base + 5), 0.22, 0.25) * env(int(0.22 * SR), d=0.09)
    return echo(np.concatenate([a, b]) * 0.7, 0.08, 0.3, 0.25)
def arp_up(root=72, steps=(0, 4, 7, 12, 16, 19, 24), each=0.045, duty=0.5):
    return echo(np.concatenate([pulse(note(root + s), each, duty) * env(int(each * SR), d=0.05) for s in steps]) * 0.6, 0.1, 0.35, 0.3)
def arp_down(root=84, steps=(0, -3, -7, -12, -15, -19, -24), each=0.06): return arp_up(root, steps, each, 0.25)
def bonk():                    # melee hit: noise crack + falling square
    d = 0.16; n = int(d * SR); return (noise(d, rate=9000) * env(n, d=0.02) * 0.8 + pulse(np.geomspace(600, 120, n), d, 0.5) * env(n, d=0.05) * 0.5)
def zap():                     # spell: rising pulse sweep with vibrato, 12.5 % duty
    d = 0.22; n = int(d * SR); f = np.geomspace(300, 1800, n) * (1 + 0.04 * np.sin(np.arange(n) / SR * 2 * np.pi * 30))
    return echo(pulse(f, d, 0.125) * env(n, d=0.12) * 0.55, 0.06, 0.3, 0.2)
def heal():                    # triangle arpeggio, soft, with echo
    return echo(np.concatenate([tri(note(n), 0.06) * env(int(0.06 * SR), d=0.1) for n in (76, 79, 84, 88, 91)]) * 0.6, 0.12, 0.45, 0.35)
def roar():                    # boss lunge: dark noise swell + low pulse growl
    d = 0.55; n = int(d * SR); e = np.concatenate([np.linspace(0, 1, n // 3), np.exp(-np.arange(n - n // 3) / (0.2 * SR))])
    return (noise(d, rate=1500, lp=900) * 0.8 + pulse(np.linspace(70, 55, n) * (1 + 0.08 * np.sin(np.arange(n) / SR * 2 * np.pi * 18)), d, 0.5) * 0.4) * e
def wipe():                    # party wiped: the classic falling glissando
    d = 0.9; n = int(d * SR); f = np.geomspace(880, 80, n); return echo(pulse(f, d, 0.5) * env(n, d=0.5, r=0.08) * 0.5, 0.11, 0.35, 0.3)
def coin(var=0):               # one coin: two-note blip, a semitone apart per variant
    return ding(88 + var)[: int(0.25 * SR)] * 0.6
def whoosh(d=0.6, up=True):    # filtered noise swell (push-ins, cuts)
    n = int(d * SR); x = noise(d); k = np.linspace(40, 4, n) if up else np.linspace(4, 40, n); y = np.zeros(n, np.float32); acc = 0.0
    for i in range(0, n, 64):
        seg = x[i:i + 64]; w = max(1, min(int(k[i]), len(seg))); y[i:i + 64] = np.convolve(seg, np.ones(w) / w, mode="same")
    e = np.sin(np.linspace(0, np.pi, n)) ** 1.5; return y * e * 0.7
def pop():                     # speech/thought bubble appears
    d = 0.08; n = int(d * SR); return pulse(np.geomspace(500, 1400, n), d, 0.5) * env(n, d=0.03) * 0.4
def step(var=0):               # soft footstep
    d = 0.09; n = int(d * SR); return noise(d, rate=2500 + 300 * var, lp=900) * env(n, d=0.03) * 0.6
def thump():                   # title stamp landing
    d = 0.2; n = int(d * SR); return (tri(np.geomspace(160, 50, n), d) * 1.0 + noise(d, rate=4000, lp=2000) * 0.3) * env(n, d=0.07)
def sparkle():                 # CTA shimmer
    return echo(np.concatenate([pulse(note(n), 0.035, 0.125) * env(int(0.035 * SR), d=0.05) for n in (96, 91, 98, 93, 100, 95, 103)]) * 0.35, 0.09, 0.5, 0.4)

class Bus:
    def __init__(self, total): self.x = np.zeros(int(total * SR) + SR, np.float32); self.duck = []
    def add(self, s, at, gain=0.3, duck=0.0):
        i = int(at * SR); s = s[: len(self.x) - i]; self.x[i:i + len(s)] += s * gain
        if duck: self.duck.append((at, duck))
    def mix_into(self, music):
        """music: float32 (n,) or (n, 2). Ducks music around hero hits, adds SFX, soft-limits."""
        m = music.astype(np.float32).copy(); n = len(m); g = np.ones(n, np.float32)
        for at, db in self.duck:
            a = int(at * SR); r = int(0.25 * SR); f = int(0.2 * SR); lv = 10 ** (-db / 20)
            seg = np.concatenate([np.full(r, lv), np.linspace(lv, 1, f)]); g[a:a + len(seg)] = np.minimum(g[a:a + len(seg)], seg[: max(0, n - a)])
        if m.ndim == 2: m *= g[:, None]; s = self.x[:n, None]
        else: m *= g; s = self.x[:n]
        y = m + s; return np.tanh(y * 1.1) / np.tanh(1.1)
