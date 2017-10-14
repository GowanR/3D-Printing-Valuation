from PrinterPartValuation import PartValuation

print_time = 20 # hours
material_usage = 0.644 # lbs
p = PartValuation(print_time, material_usage)
print "post processing time: ", p.get_post_processing_time()
print "raw cost: ", p.get_raw_cost()
