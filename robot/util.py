def barcode_generator():
    initial_barcode = -1
    while True:
        initial_barcode += 1
        yield initial_barcode

barcode_iterator = barcode_generator()


def almost_equal(a, b, tol):
    return abs(a - b) < tol
