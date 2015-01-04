from barcoded_vial import BarcodedVial


class GCVial(BarcodedVial):

    # FIXME: what's the max volume of a GC Vial?

    def __init__(self, barcode):
        return super(GCVial, self).__init__(
            container_type='gc_vial', barcode=barcode
        )
