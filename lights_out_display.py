def display_bitstring_on_sensehat(hat, bitstring):
    """
    Displays a 9-bit solution bitstring (e.g. '101001101') on the Sense HAT LED matrix.
    Layout is centered in the 8x8 grid.

    Args:
        bitstring (str): A string of 9 binary digits representing on/off states
                         corresponding to the lights-out grid solution.
    """

    # Define color codes
    ON_COLOR = (0, 0, 255)       # Blue
    OFF_COLOR = (20, 20, 20)     # Dim grey

    # LED grid index mapping (Centered 3x3 grid on 8x8 matrix)
    index_map = [
        (2, 2), (2, 3), (2, 4),
        (3, 2), (3, 3), (3, 4),
        (4, 2), (4, 3), (4, 4)
    ]

    # hat = SenseHat()
    hat.clear()

    for i, bit in enumerate(bitstring):
        x, y = index_map[i]
        color = ON_COLOR if bit == '1' else OFF_COLOR
        hat.set_pixel(x, y, color)
