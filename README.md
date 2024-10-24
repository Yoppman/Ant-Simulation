# Ant Simulation

This repository contains a simple Ant Simulation. The ants move around the environment following certain rules.

## Features

- Ants move randomly around the environment.
- Obstacles have been added for ants to navigate around.
- A steering algorithm is implemented to make ant movement more realistic.

## Cloning the Repository

To get started, clone the repository using the following command:

```bash
git clone https://github.com/Yoppman/Ant-Simulation.git
cd Ant-Simulation
```

## Installing Dependencies

Make sure you have Python installed. To install the required libraries, run the following command:

```bash
pip install -r requirements.txt
```

This will install `pygame` and any other dependencies required for the simulation.

## Running the Program

After installing the dependencies, you can run the simulation using the following command:

```bash
python main.py
```

## New Features Added

1. **Obstacles**: 
   - Obstacles have been added to the simulation, and ants will now avoid these obstacles as they navigate the environment.
   
2. **Steering Algorithm**:
   - Ants now have a more realistic movement pattern, using a basic steering algorithm to navigate the environment efficiently while avoiding obstacles.
   
## Additional Notes

- Ensure you have the latest version of `pygame` installed.
- The simulation may require additional setup or files specific to the repository, so please check the source code or documentation for any other steps.
- Feel free to enhance the project by adding more ant behaviors, food sources, or pheromone trails.
