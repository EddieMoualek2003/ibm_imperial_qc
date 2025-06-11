def display_bitstring_on_sensehat(hat, bitstring, layout='tee'):
    """
    Displays a 5-qubit bitstring on the Sense HAT emulator in either 'tee' or 'bowtie' layout.

    Args:
        bitstring (str): e.g. '10101'
        layout (str): 'tee' (default) or 'bowtie'
    """
    hat.clear()

    # Define color codes
    RED    = [255, 0, 0]
    BLUE   = [0, 0, 255]
    PURPLE = [128, 0, 128]
    OFF    = [0, 0, 0]

    # Define layout mappings
    tee_map = [
        [0, 1, 8, 9],        # Q0
        [3, 4, 11, 12],      # Q1
        [6, 7, 14, 15],      # Q2
        [27, 28, 35, 36],    # Q3
        [51, 52, 59, 60]     # Q4
    ]

    bowtie_map = [
        [6, 7, 14, 15],    # Q0 - top right
        [54, 55, 62, 63],    # Q1 - bottom right
        [27, 28, 35, 36],    # Q2 - center
        [48, 49, 56, 57],    # Q3 - bottom left
        [0, 1, 8, 9]     # Q4 - top left
    ]

    hex_map = [
        [3],    # Q0
        [10],   # Q1
        [12],   # Q2
        [17],   # Q3
        [21],   # Q4
        [24],   # Q5
        [30],   # Q6
        [33],   # Q7
        [37],   # Q8
        [42],   # Q9
        [44],   # Q10
        [51]    # Q11
    ]

    if layout == "T":
        layout_map = tee_map
    elif layout == "B":
        layout_map = bowtie_map
    elif layout == "H":
        layout_map = hex_map

    # Prepare pixel grid
    pixels = [OFF[:] for _ in range(64)]

    for i in range(len(layout_map)):
        color = PURPLE  # default for unused or overflow
        if i < len(bitstring):
            color = BLUE if bitstring[i] == '1' else RED
        for idx in layout_map[i]:
            pixels[idx] = color

    hat.set_pixels(pixels)
