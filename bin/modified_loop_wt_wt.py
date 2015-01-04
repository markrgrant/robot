"""
A version of the wt/wt protocol that uses a sequence of nested loops for executing a
wt/wt protocol
"""

from commands import (
    scan_barcode,
    scan_barcodes,
    create_barcodes,
    prime,
    weigh,
    uncap,
    dispense,
    wash_tip,
    aspirate,
    cap,
    vortex,
    blow_off,
    add_hexane,
)

# sample vial = source vial (vial type = GC vial)
# intermediate vial (vial type = 'scint vial') = dilution vial
# final vial (vial type= GC vial)
# internal standard vial (vial type = GC vial)

def wt_wt_prep_plan(num_samples, num_replicates):
    vial_type = 'sample_vial'
    sample_barcodes = scan_barcodes(vial_type, num_samples)
    dilution_vial_barcodes = {}
    prime()
    for sample_barcode in sample_barcodes:
        dilution_vial_barcodes[sample_barcode] = create_barcodes('dilution_vial', num_replicates)
        aspirate('tetradecane')
        for dilution_vial in dilution_vial_barcodes[sample_barcode]:
            weigh(dilution_vial)
            uncap(dilution_vial)
            dispense('tetradecane', dilution_vial)
            cap(dilution_vial)
            weigh(dilution_vial)
    wash_tip()
    for sample_barcode in sample_barcodes:
        aspirate(sample_barcode)
        for dilution_vial in dilution_vial_barcodes[sample_barcode]:
            uncap(dilution_vial)
            dispense(sample_barcode, dilution_vial)
            cap(dilution_vial)
            weigh(dilution_vial)
        wash_tip()  # once per sample here, to clean out the tip
    for sample_barcode in sample_barcodes:
        for dilution_vial in dilution_vial_barcodes[sample_barcode]:
            add_hexane(dilution_vial)
        blow_off()
        for i, dilution_vial in enumerate(dilution_vial_barcodes[sample_barcode]):
            vortex(dilution_vial)
            uncap(dilution_vial)
            aspirate(dilution_vial)
            cap(dilution_vial)
            final_vial_barcode = scan_barcode('final_vial', i)
            uncap(final_vial_barcode)
            dispense(dilution_vial, final_vial_barcode)
            cap(final_vial_barcode)

wt_wt_prep_plan(2, 3)
