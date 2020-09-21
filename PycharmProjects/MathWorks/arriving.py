import random


class Truck:
    # Creates a truck capable of keeping track of its state and qualities
    def __init__(self, id, percent_charge=80):
        self.id = id
        self.percent_charge = percent_charge
        self.position = 0
        self.velocity = random.randint(55, 81) * 0.44704
        self.at_charge_station = False
        self.in_line = False
        self.resting = False
        self.life_time = 0
        self.rest_time = 0
        self.driving_time = 0
        self.wait_time = 0
        self.leaving_station = False
        self.charging = False
        self.time_at_station = 0
        truck_type = random.randint(0, 1)
        # Setting the name and specs of the truck to one of two trucks we had information about
        if truck_type == 0:
            self.name = "Chanje V8100"
            self.battery_size = 100
            self.mass = random.randint(16535, 22535) * 0.453592
        elif truck_type == 1:
            self.name = "Freightliner eCascadia"
            self.battery_size = 550
            self.mass = random.randint(26000, 80000) * 0.453592
        self.battery_life = 0.8 * self.battery_size
        self.charge_time = self.charging_time()

    def battery_use_start(self, distance, elevation_change=0):
        """
        Calculates the energy used to accelerate a truck and then drive a certain distance with it. We have refrained from
        using elevation change since we can not generally calculate that for any stretch of road

        :param distance: The distance traveled at constant velocity in miles
        """
        # Energy needed to achieve kinetic energy reflecting the truck's velocity and mass +
        # energy needed to overcome the Rotational Resistance Force +
        # energy needed to generate potential energy from change in height /
        # engine efficiency(80%) * charger efficiency(80%)
        # converted from joules to kilowatt hours. All units are converted to metric at some point or other
        return (((0.5 * self.mass * self.velocity ** 2) + (
                (0.01 * (1 + self.velocity / 147) * self.mass * 9.8
                 + (elevation_change / (distance * 1609.34)) * self.mass * 9.8 * self.velocity
                 ) * (distance * 1609.34 / self.velocity))) / 0.64) / (3.6 * 10 ** 6)

    def battery_use_hold(self, distance, elevation_change=0):
        """
        Calculates the energy used to drive a truck which is already in motion for a certain distance.

        :param distance: The distance traveled at constant velocity in miles
        """
        # Same as the previous calculation, except kinetic energy is already achieved and requires no more energy
        return (0.01 * (1 + self.velocity / 147) * self.mass * 9.8
                + (elevation_change / (distance * 1609.34)) * self.mass * 9.8 * self.velocity
                ) * ((distance * 1609.34 / self.velocity) / 0.64) / (3.6 * 10 ** 6)

    def drive(self, time=60, in_motion = False):
        """
        Adjusts the position of the truck by the distance it would drive in a given time

        :param time: time spent driving, in minutes. Defaults to 60
        :param in_motion: Whether or not the truck was in motion when it began driving for this time interval

        :return: returns nothing
        """
        self.position += self.velocity * 2.2369 * time/60
        if in_motion:
            self.battery_life -= self.battery_use_hold(self.velocity * 2.2369 * time / 60)
        else:
            self.battery_life -= self.battery_use_start(self.velocity * 2.2369 * time / 60)

    def driveTo(self, dist):
        """
        Drives the truck a certain distance

        :param dist: The distance to drive in miles
        :return: The amount of time in minutes that it takes for the truck to drive that distance
        """
        self.position += dist
        self.battery_life -= self.battery_use_hold(dist)
        return dist/(self.velocity*2.2369 / 60)

        return

    # Performs all of the internal interactions and operations that a truck would perform in one minute
    def time_tick(self):
        if self.battery_life <= 0:
            raise ValueError('Battery Life for', self.name, self.id, 'dropped below 0')
        if not self.at_charge_station:
            # time that truck has been on the road goes up
            self.life_time += 1
            if not self.resting:
                # time that truck driver has been driving goes up
                self.driving_time += 1
            else:
                # time that driver has been resting goes uo
                self.rest_time += 1
            if self.driving_time >= 840:
                # driver takes a break
                self.resting = True
                self.driving_time = 0
            if self.rest_time >= 600:
                # driver gets back on the road
                self.resting = False
                self.rest_time = 0
        # interactions for trucks currently waiting or charging at a station
        if self.in_line:
            self.wait_time += 1
        elif self.charging:
            self.charge_time -= 1

    # randomly generate the charging time of whatever type of vehicle this truck is
    def charging_time(self):
        if self.name == "Chanje V8100":
            if self.percent_charge == 100:
                return random.randint(60, 121)
            elif self.percent_charge == 80:
                return random.randint(30, 41)
        elif self.name == "Freightliner eCascadia":
            if self.percent_charge == 100:
                return random.randint(150, 211)
            elif self.percent_charge == 80:
                return random.randint(240, 361)


class TruckStop:
    # Creates a truck stop where trucks can come to charge
    def __init__(self, stations, position, id):
        self.id = id
        self.time_cycle = 0
        self.position = position
        self.charging_station = []
        self.charging_station_slots = stations
        self.line = []
        self.total_wait_time = 0
        self.highest_wait_time = 0
        self.trucks_serviced = 0

    # Takes a truck and puts it in the line to begin charging
    def addTruck(self, truck):
        self.line.append(truck)
        truck.at_charge_station = True
        truck.in_line = True
        truck.wait_time = 0

    # Takes a truck that is done charging and sends it back out into the world
    def removeTruck(self, truck):
        self.charging_station.remove(truck)
        truck.charging = False
        truck.in_charge_station = False
        truck.leaving_station = True
        truck.battery_life = truck.percent_charge * truck.battery_size

    # Represents the interactions that happen within the charging station over a period of one hour
    def time_tick(self):
        # If there are trucks charging
        if not len(self.charging_station) == 0:
            for truck in self.charging_station:
                if truck.time_at_station == self.time_cycle:
                    # Each truck should handle it's internal interactions
                    truck.time_tick()
                    # If the truck has charged, take it off the charger and put it on the road
                    if truck.charge_time <= 0:
                        self.removeTruck(truck)
                    # If the truck was done charging and has just left the station
                    if truck not in self.charging_station:
                        # adjust statistics for station
                        self.trucks_serviced += 1
                        self.total_wait_time += truck.wait_time
                        if truck.wait_time > self.highest_wait_time:
                            self.highest_wait_time = truck.wait_time
        # If there are trucks waiting in line
        if not len(self.line) == 0:
            for truck in self.line:
                if truck.time_at_station == self.time_cycle:
                    # Handle internal interactions of each truck in line
                    truck.time_tick()
        # If there are more charging stations than there are trucks currently charging
        if len(self.charging_station) < self.charging_station_slots:
            # For each open charging station in the TruckStop
            for truck_num in range(self.charging_station_slots - len(self.charging_station)):
                # If there are still trucks waiting in line
                if not len(self.line) == 0:
                    # Move the truck which has been waiting the longest from the line to a charging station
                    self.line[0].in_line = False
                    self.line[0].charging = True
                    self.charging_station.append(self.line[0])
                    self.line.remove(self.line[0])
        self.time_cycle += 1
        for truck in self.charging_station:
            if self.time_cycle == 60:
                truck.time_at_station = 0
            else:
                truck.time_at_station += 1
        for truck in self.line:
            if self.time_cycle == 60:
                truck.time_at_station = 0
            else:
                if truck.time_at_station + 1 == self.time_cycle:
                    truck.time_at_station += 1


class Route:
    # Creates a route which has an amount of truck drivers constantly beginning to drive along it and
    # several truck stops spaced evenly along the route, each with the same number of charging stations.
    # Density represents the number of trucks that pass through any given point on average over the course of an hour
    def __init__(self, density, length, stops, stations):
        self.density = density
        self.length = length
        self.finished_trucks = 0
        self.stops = list()
        self.time = 0
        # Creates the evenly spaced stops with 10 charging stations each
        new_stops = [TruckStop(stations, int((i + 1) * length / stops), i) for i in range(stops)]
        for stop in new_stops:
            self.stops.append(stop)
        self.trucks = list()
        self.reachable_stop = self.stops[0]

    # Performs operations of all trucks and stops in the system over the course of an hour
    def time_tick(self):
        # Create a number of trucks which is the average number of trucks that pass through any point on the highway
        # over the period of an hour
        new_trucks = [Truck(i + self.time * self.density) for i in range(self.density)]
        for truck in new_trucks:
            self.trucks.append(truck)
        for truck in self.trucks:
            # Go through every truck which is not currently resting
            if not truck.resting:
                # If the truck is leaving from the start city
                if truck.position == 0 and not truck.at_charge_station:
                    # performs 60 minutes worth of internal operations for the trucks
                    for j in range(60):
                        truck.time_tick()
                    # adjust the truck position by the velocity. 2.2369 is a conversion factor from mps to mph
                    truck.drive()
                # If the truck has already left the start city and is not at a truck stop
                elif not truck.at_charge_station:
                    # Go through all the stops
                    for stop in self.stops:
                        if stop.position > truck.position:
                            # and determine which is the furthest station that the truck will be able to reach
                            if truck.battery_use_hold(stop.position - truck.position) < truck.battery_life \
                                    and len(stop.line) < len(self.reachable_stop.line):
                                self.reachable_stop = stop
                    for stop in self.stops:
                        # If that stop is the next stop
                        if stop.position > truck.position and self.reachable_stop.position - truck.position <= \
                                self.length / len(self.stops):
                            # Park the truck at the stop
                            stop.addTruck(truck)
                            truck.time_at_station = truck.driveTo(stop.position-truck.position)
                    # If after that the truck is not at a charging station, meaning it doesn't need to park
                    if not truck.at_charge_station:
                        # Drive the distance it will travel in an hour and perform 60 minutes of internal operations
                        for j in range(60):
                            truck.time_tick()
                        truck.drive()
            else:
                # If the truck is resting, do it's internal operations without moving it
                truck.time_tick()
        # For each stop
        for stop in self.stops:
            # Run internal operations 60 times
            stop.time_cycle = 0
            for j in range(60):
                stop.time_tick()
                for truck in self.trucks:
                    # Any truck which has just finished charging and departed
                    if truck.leaving_station:
                        # Should travel the distance it would travel and lose the energy it would lose in the rest of
                        # the hour
                        if j < 59:
                            truck.drive(time = 59-j)
                        # Indicate that the truck has left the station
                        truck.leaving_station = False
        # Print information for all of the stops
        for k in range(len(self.stops)):
            print("Stop", str((k + 1)) + ":")
            print("Charging:")
            for truck in self.stops[k].charging_station:
                print(truck.name, str(truck.id) + ":", truck.charge_time, "minutes remaining")
            print("Waiting:")
            for truck in self.stops[k].line:
                print(truck.name, str(truck.id) + ":", "waiting for", truck.wait_time, "minutes")
        # Print information of trucks which aren't at stops
        for truck in self.trucks:
            if truck.position >= self.length:
                print(truck.name, truck.id, "reached the end destination")
                self.trucks.remove(truck)
            elif not truck.at_charge_station and truck in self.trucks:
                print(truck.name, str(truck.id) + ":", truck.position, "miles")
                print("Energy:", truck.battery_life)
        self.time += 1


# Creating the routes which were given as examples
satx_nola = Route(600, 1108, 1000, 1000)
hours = 0
# Runs simulation for two days
while hours < 48:
    # Runs simulation for each route
    satx_nola.time_tick()
    hours += 1

# Prints final data for all routes and all stops
for h in range(len(satx_nola.stops)):
    print("Stop", str(satx_nola.stops[h].id) + ":")
    if satx_nola.stops[h].trucks_serviced == 0:
        print("Average Wait Time: N/A")
        print("Highest Wait Time: N/A")
    else:
        print("Average Wait Time:", satx_nola.stops[h].total_wait_time / satx_nola.stops[h].trucks_serviced)
        print("Highest Wait Time:", satx_nola.stops[h].highest_wait_time)
