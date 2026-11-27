"""Dataset collections: combine several datasets into model attributes."""
from .electricity_demand import ElectricityDemand
from .electricity_trade import ElectricityTrade
from .fuel_prices import FuelPrices
from .hydro_availability import HydroAvailability
from .hydrogen_demand import HydrogenDemand
from .hydrogen_technology_costs import HydrogenTechnologyCosts
from .interconnectors import Interconnectors
from .monetary_conversion import MonetaryConversion
from .renewable_fleet import RenewableFleet
from .technology_costs import TechnologyCosts
from .thermal_availability import ThermalAvailability

__all__ = [
    "ElectricityDemand",
    "ElectricityTrade",
    "FuelPrices",
    "HydroAvailability",
    "HydrogenDemand",
    "HydrogenTechnologyCosts",
    "Interconnectors",
    "MonetaryConversion",
    "RenewableFleet",
    "TechnologyCosts",
    "ThermalAvailability",
]
