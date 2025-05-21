

def display_bitstring_on_sensehat(hat, bitstring):
    """
    Display a quantum bitstring on a SenseHat 8x8 LED matrix in a T layout.
    '1' is blue, '0' is red, unused qubits are purple.
    """

    # Initialize SenseHat
    
    hat.clear()

    # Define RGB colors
    RED = [255, 0, 0]
    BLUE = [0, 0, 255]
    PURPLE = [128, 0, 128]
    OFF = [0, 0, 0]

    # T-shaped layout for up to 5 qubits (bit index to LED positions)
    qubit_pixel_map = [
        [0, 1, 8, 9],       # qubit 0
        [3, 4, 11, 12],     # qubit 1
        [6, 7, 14, 15],     # qubit 2
        [27, 28, 35, 36],   # qubit 3
        [51, 52, 59, 60]    # qubit 4
    ]

    # Initialize all 64 pixels to OFF
    pixels = [OFF[:] for _ in range(64)]

    for i in range(len(qubit_pixel_map)):
        color = PURPLE  # Default for overflow/unassigned
        if i < len(bitstring):
            if bitstring[i] == '1':
                color = BLUE
            elif bitstring[i] == '0':
                color = RED
        for pixel_index in qubit_pixel_map[i]:
            pixels[pixel_index] = color

    # Update SenseHat display
    hat.set_pixels(pixels)
