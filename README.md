# BusTicketReservation


## Overview
This is a bus ticket booking system developed using **Python** and **PyQt6**. It allows users to select departure and arrival cities, choose a bus company, pick travel dates and times, and reserve seats. The application ensures proper user input validation and includes additional features such as multi-passenger booking and a system tray notification for ticket confirmation.
## Screenshot
<img width="1105" alt="interface" src="https://github.com/user-attachments/assets/26da1e09-4d09-4a9c-ac93-780990917169" />

## Features
- User-friendly graphical interface built with **PyQt6**
- City selection with validation (departure and arrival cities cannot be the same)
- One-way and round-trip ticket booking options
- Seat selection with **checkbox grid (5x10 layout)**
- Additional passenger details entry with a pop-up dialog
- Price calculation for single and round-trip tickets
- Data validation for **TC Number, phone number, email, and name fields**
- Purchase summary displayed in a ticket list
- System tray notifications upon successful booking

## PS
Originally, this project was a Windows Forms application, but I wanted to explore how it could be implemented in a more modern way. Due to issues with my Windows PC, I revised it using this approach.

* You can watch a demo of the project on my YouTube Chanell: [Project Demo](https://youtu.be/0vy5g4874Og)

## Technologies Used
- **Python** (Programming Language)
- **PyQt6** (GUI Development)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/osmanveyetkin/BusTicketReservation.git
   cd PyBusReservation
   ```
2. Install dependencies:
   ```bash
   pip install PyQt6
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## How to Use
1. Enter passenger details (Name, TC Number, Phone, Email, Gender).
2. Select a bus company from the dropdown menu.
3. Choose departure and arrival cities.
4. Pick travel dates and times (Dönüş Tarihi is enabled only for round-trip tickets).
5. Select available seats.
6. Click **"Satın Al"** to complete the reservation.
7. View purchased tickets in the **ticket list**.
8. Receive a notification via **system tray icon**.



## Author
- **Osman Yetkin**

## Contributions
Feel free to submit issues and pull requests to enhance this project!

