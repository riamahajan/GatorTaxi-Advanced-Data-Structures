
# GatorTaxi Project

## Overview
GatorTaxi is a ride-sharing platform designed to manage numerous ride requests efficiently. This project implements a system using custom-built data structures, specifically a Min Heap and a Red-Black Tree, to handle operations like ride requests, updates, and cancellations dynamically.

## Features
- **Custom Data Structures**: Implements Min Heap and Red-Black Tree from scratch.
- **Efficient Ride Management**: Optimized for fast retrieval, insertion, and update of ride requests.
- **Command-Line Interface**: Processes operations through command-line arguments, allowing for flexible interaction.

## Installation
Clone this repository to your local machine:
```bash
git clone https://github.com/yourusername/gatortaxi.git
```
Ensure you have Python installed, then navigate to the project directory.

## Usage
Run the project using the following command:
```bash
python gatorTaxi.py input.txt
```
- Replace `input.txt` with the path to your input file containing ride operations.

## Input Format
The input should be structured in commands as follows:
- `Insert(rideNumber, rideCost, tripDuration)`
- `Print(rideNumber)`
- `Print(rideNumber1, rideNumber2)`
- `UpdateTrip(rideNumber, newTripDuration)`
- `GetNextRide()`
- `CancelRide(rideNumber)`

## Output
Output will be directed to `output_file.txt`, detailing the results of the operations performed.

## Contributing
Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
