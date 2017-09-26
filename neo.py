def run(r,g,b):
    import neopixel, machine

    np = neopixel.NeoPixel(machine.Pin(4),1)
    np[0] = (r,g,b)
    np.write()