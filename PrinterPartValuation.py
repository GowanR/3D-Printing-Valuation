from enum import Enum

class PrintComplexity(Enum):
    VERY_COMPLEX = 5 # Part is complex with detailed aspects
    MODERATELY_COMPLEX = 3 # Part has relatively complex features
    NOT_COMPLEX = 1 # Part is a 2D extruded profile
class PartUseCase(Enum):
    HIGH_LOAD = 5 # Parts are expected to endure 100+ cycles
    MODERATE_LOAD = 3 # Part will be handled most of the time
    DISPLAY_ONLY = 1 # Part is for representation or display
class MaterialRemoval(Enum):
    INTERNAL_SUPPORT = 5 # Part has internal Features that need support
    EXTERNAL_SUPPORT = 3 # Part has open features that need support
    NO_SUPPORT = 1 # No support is needed
class WallThickness(Enum):
    WALL_UNDER_2MM = 5 # Part has walls less that 2mm (0.04in)
    WALL_BETWEEN_2MM_3MM = 3 # Part has walls between 2mm and 3mm
    WALL_OVER_3MM = 1 # Part has Walls larger that 3mm (0.1)
class StressPoints(Enum):
    NO_CORNER_SUPPORT = 5 # Part has no supporting feature on corners
    SOME_CORNER_SUPPORT = 3 # Part has minimal support on corners
    GENEROUS_CORNER_SUPPORT = 1 # Parts has generous support on corners
class Tolerance(Enum):
    HIGH_TOLERANCE = 5 # Tolerance needs to be exact through the part
    SOME_HIGH_TOLERANCE = 3 # Some features need a higher tolerance
    NO_TOLERANCE = 1 # No tolerance needs to be met
class Shipping(Enum):
    NONE = 0
    ECONOMY = 5
    THREE_DAY = 10
    OVERNIGHT = 15
class PartValuation:
    # Personal Rates
    HOURLY_LABOR_RATE = 30.0 # $/hr

    # Spool Costs
    SPOOL_PRICE = 30.0 # Price Per Spool	$30.00
    SPOOL_WEIGHT = 2.2 # Weight of spool	2.2LBS
    ITEMS_PURCHASED = 8.0 # Items Purchased	$8.00

    # Energy Costs
    PRINTER_CONSUMPTION = 0.15 # $ kWh/hr
    CITY_ENERGY_COST = 0.12 # $ kWh/hr
    ELECTRICAL_STARTUP_COST = 0.30 # $
    HOURLY_ENERGY_RATE = PRINTER_CONSUMPTION + CITY_ENERGY_COST + ELECTRICAL_STARTUP_COST

    # Tax Rate
    AZ_TAX_RATE = 0.0560
    def __init__(self, print_time, material_usage, model_clean_up=0,slice_time=5,material_change=0,part_removal=5,support_removal=5,assembly=5,cure_time=5,cure_time_rate=0,bulk_discount=0.2,n_parts=1,discount_cutoff=9):
        self.print_complexity = PrintComplexity(3)
        self.part_use_case = PartUseCase(1)
        self.material_removal = MaterialRemoval(3)
        self.wall_thickness = WallThickness(1)
        self.stress_points = StressPoints(1)
        self.tolerance = Tolerance(3)

        self.print_time = print_time
        self.material_usage = material_usage

        # Labor times
        self.model_clean_up = model_clean_up
        self.slice_time = slice_time
        self.material_change = material_change
        self.part_removal = part_removal
        self.support_removal = support_removal
        self.assembly = assembly
        self.cure_time = cure_time
        self.cure_time_rate = cure_time_rate

        # Discounts
        self.bulk_discount = bulk_discount
        self.n_parts = n_parts
        self.discount_cutoff = discount_cutoff

        self.shipping_cost = Shipping(5)
    def get_labor_costs(self):
        return (self.HOURLY_LABOR_RATE/60) * self.get_total_work_time()
    def get_material_costs(self):
        return (self.SPOOL_PRICE/self.SPOOL_WEIGHT) * self.material_usage
    def get_total_energy_cost(self):
        return self.HOURLY_ENERGY_RATE * self.print_time
    def get_cure_cost(self):
        return self.cure_time * self.cure_time_rate
    def get_raw_cost(self):
        return self.get_labor_costs() + self.get_material_costs() + self.get_total_energy_cost() + self.get_cure_cost()
    def get_customer_adjusted_cost(self):
        return (self.get_markup() * self.get_raw_cost()) * self.get_discount_coef()
    def get_total_cost(self): # adjusted for tax and shipping_cost
        return (self.get_customer_adjusted_cost() * (1 + self.AZ_TAX_RATE)) + self.shipping_cost.value
    def get_spools_needed(self):
        return self.material_usage / self.SPOOL_WEIGHT
    def get_total_profit(self):
        return self.get_customer_adjusted_cost() - self.get_raw_cost()
    def get_profit_margin(self):
        return self.get_total_profit() / self.get_customer_adjusted_cost()
    def get_preparation_time(self):
        return self.model_clean_up + self.slice_time + self.material_change
    def get_post_processing_time(self):
        return self.part_removal + self.support_removal + self.assembly
    def get_total_work_time(self):
        return self.get_preparation_time() + self.get_post_processing_time()
    def get_discount_coef(self):
        if self.n_parts > self.discount_cutoff:
            return 1 - self.bulk_discount
        return 1
    def get_markup(self):
        return (self.print_complexity.value + self.part_use_case.value + self.material_removal.value + self.wall_thickness.value + self.stress_points.value + self.tolerance.value)/10.0
