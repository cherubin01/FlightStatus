# Real-Time Flight Status and Notifications System

## Overview

The Real-Time Flight Status and Notifications System is a comprehensive application designed to provide accurate and up-to-date flight information. This system allows users to track flight statuses in real-time, receive notifications about significant changes, and access detailed information about departures, arrivals, delays, and cancellations.

## Features

- **Search Functionality**: Search for flights by route or flight ID.
- **Real-Time Updates**: Retrieve the latest flight status data, including delays and cancellations.
- **Notifications**: Receive push notifications about critical flight status changes.
- **Local Data Storage**: Store airport and airline information in JSON files for efficient data retrieval.

## Technologies Used

- **Frontend**: HTML, CSS
- **Backend**: Python
- **Database**: MongoDB
- **Notifications**: Firebase Cloud Messaging
- **APIs**: FlightStats API

## Getting Started

### Prerequisites

- Python 3.x
- Node.js (for frontend development, if needed)
- MongoDB
- Firebase Account

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/flight-status-notifications.git
    cd flight-status-notifications
    ```

2. **Set up the Backend:**
    - Install the required Python packages:
      ```bash
      pip install -r requirements.txt
      ```
    - Configure Firebase and FlightStats API credentials in your backend configuration.

3. **Set up the Frontend:**
    - Navigate to the `frontend` directory (if separate) and install dependencies:
      ```bash
      npm install
      ```

4. **Start the Backend Server:**
    ```bash
    python app.py
    ```

5. **Run the Frontend Server (if applicable):**
    ```bash
    npm start
    ```

## Usage

1. **Access the Web Application:**
   Open your browser and navigate to `http://localhost:3000` (or the port configured for your frontend).

2. **Search for Flights:**
   Use the search functionality to find flights by route or flight ID.

3. **Receive Notifications:**
   Ensure push notifications are enabled in your browser or mobile device to receive updates.

## Configuration

- **Backend Configuration:**
  - Set `appID` and `apiKey` for the FlightStats API.
  - Configure Firebase credentials in `firebase_config.py`.

- **Frontend Configuration:**
  - Update API endpoints in the frontend code as needed.

## Contributing

We welcome contributions to improve this project! Please fork the repository and submit a pull request with your changes. Ensure your changes are well-documented and tested.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or issues, please reach out to [nainikachauhan12@gmail.com](mailto:your-email@example.com).

---

Feel free to customize this README with additional details specific to your project or any changes you've made.
