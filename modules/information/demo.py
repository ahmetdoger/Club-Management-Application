import os
import sys


sys.path.append(os.getcwd())

from modules.information.implementations import ProfessionalAthlete, AmateurAthlete, YouthAthlete
from modules.information.repository import AthleteRepository
from modules.information.services import AthleteService

def run_demo_scenario():
    print("================================================================")
    print("      PLAYER INFORMATION MODULE - SCENARIO DEMO")
    print("================================================================\n")

   
    print("[1] SYSTEM SETUP")
    demo_db = "demo_scenario.json"
    if os.path.exists(demo_db): os.remove(demo_db) 
    
    repo = AthleteRepository(demo_db)
    service = AthleteService(repo)
    print(f"   -> Repository connected to {demo_db}")
    print(f"   -> Service initialized.\n")

    
    print("[2] CREATING ATHLETE INSTANCES (SUBCLASSES)")
    
    
    pro_athlete = ProfessionalAthlete(
        athlete_id=101, name="Cristiano", surname="Ronaldo", age=38, gender="Male",
        height=187, weight=83, sport_branch="Football", status="Active",
        strong_side="Right", salary=200000000.0, contract_end_date="2025-06-30"
    )
    print(f"   -> Professional Created: {pro_athlete.name} (Salary based)")

    
    amateur_athlete = AmateurAthlete(
        athlete_id=102, name="Local", surname="Hero", age=22, gender="Male",
        height=175, weight=70, sport_branch="Tennis", status="Active",
        strong_side="Right", licence_number="TENNIS-TR-001"
    )
    print(f"   -> Amateur Created: {amateur_athlete.name} (No Salary)")

    
    youth_athlete = YouthAthlete(
        athlete_id=103, name="Future", surname="Star", age=14, gender="Female",
        height=165, weight=55, sport_branch="Volleyball", status="Active",
        strong_side="Left", guardian_name="Mother Star", scholarship_amount=5000.0
    )
    print(f"   -> Youth Created: {youth_athlete.name} (Scholarship based)\n")

 
    print("[3] POLYMORPHISM IN ACTION")
    print("   (Iterating through a single list, calling same methods, getting different behaviors)")
    print("-" * 70)
    print(f"   {'NAME':<20} | {'ROLE':<20} | {'CALCULATED COST'}")
    print("-" * 70)

    
    roster_list = [pro_athlete, amateur_athlete, youth_athlete]

    for athlete in roster_list:
     
        cost = athlete.calculate_salary()
        role = type(athlete).__name__ 
        
        print(f"   {athlete.name:<20} | {role:<20} | {cost:,.2f} TL")
        
       
        print(f"      -> Detail: {athlete.branch_strong_side()}")
    print("-" * 70 + "\n")

    
    print("[4] SAVING TO DATABASE via SERVICE")
    ,
    service.repository.add(pro_athlete)
    service.repository.add(amateur_athlete)
    service.repository.add(youth_athlete)
    
    saved_count = len(service.repository.get_all())
    print(f"   -> {saved_count} athletes successfully saved to JSON.\n")

    
    print("[5] BUSINESS LOGIC: STATUS UPDATE")
    print(f"   -> Current Status of {pro_athlete.name}: {pro_athlete.status}")
    
    service.update_athlete_status(101, "Injured")
    updated_pro = service.repository.get_by_id(101)
    
    print(f"   -> New Status: {updated_pro['status']}")
    print("   -> Status update logic verified.\n")

    print("================================================================")
    print("      DEMO COMPLETED SUCCESSFULLY")
    print("================================================================")

   
if __name__ == "__main__":
    run_demo_scenario()