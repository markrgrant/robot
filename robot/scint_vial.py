from barcoded_vial import BarcodedVial


class ScintVial(BarcodedVial):

    #FIXME: what's the max volume of a scint vial?

    def __init__(self, barcode):
        return super(ScintVial, self).__init__(
            container_type='gc_vial', barcode=barcode
        )
