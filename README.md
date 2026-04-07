# Routing-Automation
Repository created for the project related to automating truck routing, this repository uses Python and Google OR-Tools for optimization of these problems

As of now, this repository only contains dummy data for testing the functions

This repository is going to be used as a Undergraduate Thesis for Igor Cirne Borges de Oliveira

## Programs

This application currently has three functioning programs: Cargas and Routing

Cargas is used to load vehicles with items, it maximizes value and is constrained by the maximum weight and volume of each truck. 

Routing uses the data created and optimized on Cargas to create a route for a number of Vehicles that would supply different stores, using metaheuristics to define the best route possible.
As of now, the metaheuristic used is a guided local search, which is normally the best metaheuristic for vehicle routing as it escapes local minimums

The routing program must use penalties to drop certain locations when doing routing, that is because if the problem has more demand than the trucks can supply,
the program runs ad-infinitum because there are infinite optimal solutions, this does not happen the other way around

The distance program uses OSMNX to point two places using coordinates from OpenStreetMap, calculates the shortest route between these points, prints distance and expected travel time by car.
