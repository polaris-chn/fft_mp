# generate_twiddle.py
import math

N = 2048
with open("twiddle_2048_re.hex", "w") as fr, open("twiddle_2048_im.hex", "w") as fi:
    for k in range(N // 2):
        angle = 2 * math.pi * k / N
        re = int(round(math.cos(angle) * 32767))
        im = int(round(-math.sin(angle) * 32767))
        re = max(-32768, min(32767, re))
        im = max(-32768, min(32767, im))
        fr.write(f"{re & 0xFFFF:04x}\n")
        fi.write(f"{im & 0xFFFF:04x}\n")