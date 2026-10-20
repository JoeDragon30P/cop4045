"""
Problem 2: Parking Permit Class Hierarchy
"""

from typing import Dict, List, Any

class ParkingPermit:
    """Base class for generic parking permits."""

    def __init__(self, owner_name: str, months: int, fee_schedule: Dict[str, float]) -> None:
        """
        Initializes base permit parameters.
        
        Parameters:
            owner_name: Name of permit owner.
            months: Number of months active.
            fee_schedule: Dictionary mapping fee keys to monthly rates.
        """
        self.owner_name: str = owner_name
        self.months: int = months
        self.fee_schedule: Dict[str, float] = fee_schedule

    def cost(self) -> float:
        """Calculates total cost. Base implementation uses standard fee schedule."""
        base_rate = self.fee_schedule.get("base", 0.0)
        return self.months * base_rate

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.__class__.__name__} for {self.owner_name} ({self.months} months) - Cost: ${self.cost():.2f}"

    def __repr__(self) -> str:
        """Technical representation."""
        return f"{self.__class__.__name__}(owner_name='{self.owner_name}', months={self.months})"

class StudentPermit(ParkingPermit):
    """Subclass representing student parking permits."""

    def __init__(self, owner_name: str, months: int, num_vehicles: int, fee_schedule: Dict[str, float]) -> None:
        super().__init__(owner_name, months, fee_schedule)
        self.num_vehicles: int = num_vehicles

    def cost(self) -> float:
        """
        Cost rule: $25/month + $10 one-time fee per extra vehicle after 1st.
        """
        base_rate = self.fee_schedule.get("Student_base", 25.0)
        extra_vehicle_fee = self.fee_schedule.get("extra_vehicle", 10.0)

        monthly_cost = self.months * base_rate
        vehicle_cost = max(0, self.num_vehicles - 1) * extra_vehicle_fee
        return monthly_cost + vehicle_cost

class FacultyPermit(ParkingPermit):
    """Subclass representing faculty parking permits."""
    
    def __init__(self, owner_name: str, months: int, garage_access: bool, fee_schedule: Dict[str, float]) -> None:
        super().__init__(owner_name, months, fee_schedule)
        self.garage_access: bool = garage_access

    def cost(self) -> float:
        """
        Cost rule: $40/month + optional $15/month garage access.
        """
        base_rate = self.fee_schedule.get("faculty_base", 40.0)
        garage_rate = self.fee_schedule.get("garage_rate", 15.0) if self.garage_access else 0.0

        return self.months * (base_rate + garage_rate)

def summarize_list(permits: List[ParkingPermit]) -> float:
    """
    Prints individual permit cost details and returns grand total revenue.
    """
    total_revenue: float = 0.0
    print("\n--- Permit Summary List ---")
    for p in permits:
        p_cost = p.cost()
        total_revenue += p_cost
        print(f"Owner: {p.owner_name:<15} | Type: {p.__class__.__name__:<15} | Cost: ${p_cost:>7.2f}")
    print("----------------------------")
    print(f"Total Revenue Generated: ${total_revenue:.2f}\n")
    return total_revenue

def main() -> None:
    """Demonstrates class usage and revenue calculation."""
    # Shared configurable fee schedule dictionary
    schedule = {
        "student_base": 25.0,
        "extra_vehicle": 10.0,
        "faculty_base": 40.0,
        "garage_rate": 15.0
    }

    # Instantiating objects
    sp1 = StudentPermit("Alice Smith", 4, 1, schedule) # $100
    sp2 = StudentPermit("Bob Jones", 4, 3, schedule) # $100 + $20 = $120
    fp1 = FacultyPermit("Dr. Aris", 6, True, schedule) # 6 * ($40 + $15) = $330
    fp2 = FacultyPermit("Prof. Clara", 3, False, schedule)# 3 * $40 = $120

    permit_list: List[ParkingPermit] = [sp1, sp2, fp1, fp2]

    # Display str and repr outputs
    print("Representation Demonstration:")
    for p in permit_list:
        print("str :", str(p))
        print("repr:", repr(p))

    # Summarize and compute revenue
    summarize_list(permit_list)

if __name__ == "__main__":
    main()