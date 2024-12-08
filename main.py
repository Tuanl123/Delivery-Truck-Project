import heapq
import tkinter as tk
from tkinter import ttk, messagebox

class TruckLoadingSystem:
    def __init__(self):
        """
        Basic truck loading system stuff
        """
        self.parcels = {} # Parcels dictionary
        self.truck_weight = 100 # truck weight allowance (can be modified)
        self.truck_volume = 69696969 # truck volume allowance (can be modified)
        self.city_map = { # Dictionary of city map, can be modified to match the real distance for cost calculations
            'Hanoi': {'Hai Phong': 105, 'Da Nang': 763, 'Nha Trang': 1280, 'Dalat': 1370, 'HCMC': 1730},
            'Hai Phong': {'Hanoi': 105},
            'Da Nang': {'Hanoi': 763},
            'Nha Trang': {'Hanoi': 1280},
            'Dalat': {'Hanoi': 1370},
            'HCMC': {'Hanoi': 1730},
        }

    def load_parcel(self):
        """
        Gets parcel data from user, adds to dictionary, check if parcels fits the truck
        weight and capacity limit
        """
        try:
            parcel_id = input("Enter parcel ID: ")
            destination = input("Enter destination city (HCMC, Da Nang, Dalat, Nha Trang, Hai Phong): ")
            weight = float(input("Enter parcel weight (kg): "))
            length = float(input("Enter parcel length (cm): "))
            width = float(input("Enter parcel width (cm): "))
            height = float(input("Enter parcel height (cm): "))

            # Check if the destination city is valid and print out error
            if destination not in self.city_map['Hanoi']:
                print("Invalid destination city")
                return # exit if city is invalid

            # Volume calculation
            volume = length * width * height

            # Check if parcel exceeds truck capacity, if exceeds, print out error
            if(self.get_volume() + volume > self.truck_volume or
              (self.get_weight() + weight) > self.truck_weight):
                print("Parcels exceeds capacity limit")
                return # exit if parcel is too heavy or big

            self.parcels[parcel_id] = {
                'destination': destination,
                'weight': weight,
                'length': length,
                'width': width,
                'height': height,
                'distance': self.city_map['Hanoi'][destination], # Calculates distance from Hanoi to the destination
                'volume': volume,
            }
            print(f"Parcel {parcel_id} loaded") # Print message for success loading with ID
        except ValueError: # Wrong input handling
            print("Invalid Input, please enter correct data type")

    def get_invoice(self):
        """
        Calculate and print invoice
        """
        parcel_id = input("Enter parcel ID: ")
        parcel = self.parcels.get(parcel_id) # retrieves parcel information from dictionary using ID
        if not parcel: # Check if parcel with that ID exists
            print(f"Parcel with ID {parcel_id} not found")
            return # Exit if parcel not found

        destination = parcel['destination']
        weight = parcel['weight']
        distance = self.city_map['Hanoi'][destination]
        cost_per_kg = 0.5 # Cost per KG of parcels, can be modified
        total_cost = weight * distance * cost_per_kg

        #prints stuff
        print("Invoice")
        print(f"Parcel ID: {parcel_id}")
        print(f"Destination: {destination}")
        print(f"Weight: {weight}")
        print(f"Distance: {distance} km")
        print(f"Total cost: ${total_cost:.2f}") # format to 2 decimal places

    def loading_plan(self):
        """
        Generates loading plan based on distance from Hanoi.
        Parcels with closest destination are loaded last.
        """
        if not self.parcels:  # Check if there are parcels to load
            print("No parcel data")
            return

        # Sort parcels by descending distance
        sorted_parcels = sorted(self.parcels.items(), key=lambda x: x[1]['distance'], reverse=True)

        # Generate loading plan list, contains just the IDs of the sorted parcels
        loading_plan = []
        for parcel_id, parcel in sorted_parcels:
            loading_plan.append(parcel_id)

        print("Loading plan:")
        for parcel_id in loading_plan:
            parcel = self.parcels[parcel_id]
            print(f"Load parcel {parcel_id} for {parcel['destination']} (Distance: {parcel['distance']} km)")


    def get_weight(self):
        """
        Calculates parcel weight
        """
        return sum(parcel['weight'] for parcel in self.parcels.values())


    def get_volume(self):
        """
        Calculates parcel volume
        """
        return sum(parcel.get('volume', 0) for parcel in self.parcels.values())

def main():
    system = TruckLoadingSystem()

    while True:
        print("\n--- Truck Loading and Route Finding System ---")
        print("1. Load Parcel")
        print("2. Load Invoice")
        print("3. Generate Loading Plan")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            system.load_parcel()
        elif choice == "2":
            system.get_invoice()
        elif choice == "3":
            system.loading_plan()
        elif choice == "4":
            print("Exiting, See ya")
            break
        else: print("Invalid Input, please enter correct data type")

if __name__ == "__main__":
    main()

