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
        # Dictionary of city map, can be modified to match the real distance for cost calculations
        self.city_map = {
            'Hanoi': {'Hai Phong': 105, 'Da Nang': 763, 'Nha Trang': 1280, 'Dalat': 1370, 'HCMC': 1730},
            'Hai Phong': {'Hanoi': 105},
            'Da Nang': {'Hanoi': 763},
            'Nha Trang': {'Hanoi': 1280},
            'Dalat': {'Hanoi': 1370},
            'HCMC': {'Hanoi': 1730},
        }
        # city coordinates, can be implemented into the path finding algorithm in the future
        # or act as a backup
        self.city_coordinates = {
            'Hanoi': (106.0, 21.0),
            'Hai Phong': (106.7, 20.9),
            'Da Nang': (108.2, 16.1),
            'Dalat': (108.4, 11.9),
            'HCMC': (106.7, 10.8)
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

    def generate_route(self):
        """
        Generate the optimal delivery route
        """
        if not self.parcels:
            print("No parcels to deliver")
            return

        # Identify cities
        delivery_cities = set(parcel["destination"] for parcel in self.parcels.values())

        # If no cities have parcel, return empty
        if not delivery_cities:
            return [], 0

        try:
            optimized_route, total_distance = self.shortest_path('Hanoi', delivery_cities)
            print("Delivery route:")
            for city in optimized_route:
                print(city)
            print(f"Total route distance: {total_distance} km")

            return optimized_route, total_distance

        except ValueError as e:
            print(f"Route optimize error: {e}")
            return [], 0


    def shortest_path(self, start, destinations):
        """
        Find the shortest path to travel to all destinations using Dijkstra's algorithm
        :param start: starting city
        :param destinations: set of cities that must be visited
        :return: Optimized route and total distance
        """
        # If there are no destinations, return empty route list

        if not destinations:
            return [], 0

        remaining_destinations = destinations.copy()
        current_route = [start]
        total_distance = 0
        current_city = start

        while remaining_destinations:
        # Find the nearest unvisited destination
            shortest_distance = float('inf')
            next_city = None

            for dest in remaining_destinations:
                # Find the shortest path form curent city to destination
                distance = self.shortest_distance(current_city, dest)  # calculates distance
                if distance < shortest_distance:
                    shortest_distance = distance
                    next_city = dest

        # If no path is found, raise error
            if next_city is None:
                raise ValueError(f"No path exists to {remaining_destinations}")

        # Update the route and distance
            current_route.append(next_city)
            total_distance += shortest_distance
            current_city = next_city
            remaining_destinations.remove(next_city)

        # return to Hanoi
        final_distance = self.shortest_distance(current_city, start)
        current_route.append(start)
        total_distance += final_distance

        return current_route, total_distance

    def shortest_distance(self, start, end):
        """
        Find the shortest distance between the two cities using Dijkstra's algorithm
        :param start: Starting city
        :param end: Destination city
        :return: Shortest distance between cities
        """
        # define distances and previous nodes
        distances = {city: float("inf") for city in self.city_map} # initialize dictionary with all cities distance set to infinite
        distances[start] = 0
        pq = [(0, start)] # priority queue setup
        visited = set() # keep track of already visited cities

        while pq:
            current_distance, current_city = heapq.heappop(pq) # return smallest distance first

            # If reached the end city, return distance
            if current_city == end:
                return current_distance

            # If already visited, skip
            if current_city in visited:
                continue

            visited.add(current_city)

            # check for neighbors
            for neighbor, weight in self.city_map.get(current_city, {}).items():
                distance = current_distance + weight

                # update distance if shorter path is found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        # if there are no paths
        raise ValueError(f"No paths exists between {start} and {end}")


def main():
    system = TruckLoadingSystem()

    while True:
        print("\n--- Truck Loading and Route Finding System ---")
        print("1. Load Parcel")
        print("2. Load Invoice")
        print("3. Generate Loading Plan")
        print("4. Generate Route")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            system.load_parcel()
        elif choice == "2":
            system.get_invoice()
        elif choice == "3":
            system.loading_plan()
        elif choice == "4":
            system.generate_route()
        elif choice == "5":
            print("Exiting, See ya")
            break
        else:
            print("Invalid Input, please enter correct data type")


if __name__ == "__main__":
    main()
