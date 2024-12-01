Truck management code

* Hanoi Roadways delivers to 5 different cities in Vietnam:
    - HCMC
    - Da Nang
    - Da Lat
    - Nha Trang
    - Hai Phong

* Currently all parcels and goods are loaded onto the trucks randomly,
it makes things messy for everyone involved

* We need a system to organize the parcels that are loaded onto the trucks

* We also need a system to print out cash invoice for customers who ordered goods to ship
based on weight and distance that the parcel needs to travel


* Code prequisites:

* Assume all trucks are two-door trucks (allows for cargo loading and off-loading
from front and back)

* Sample data for:

* parcels loaded onto the truck:
id: str, weight: float, destination: str, priority: int, sequence: int, dimensions: tuple[float, float, float]

* cities:
city: str, coordinates: tuple[float, float]



