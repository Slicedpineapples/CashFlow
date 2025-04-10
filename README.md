## CashFlow: Your Personal Financial Journey
______


This application, "CashFlow," is designed to empower you with tools for effective financial tracking and management. It draws inspiration from Robert Kiyosaki's influential work, "The Cashflow Quadrant," a cornerstone of financial literacy. To delve deeper into the concepts that shaped this application, please explore [this link](https://www.richdad.com/cashflow-quadrant-fundamentals).

The user interface, or frontend, of this project is built using the dynamic trio of JavaScript, the structural foundation of HTML, and the stylistic elegance of CSS. Conversely, the backend, the engine driving the application's functionality, is crafted with the robust and versatile Python programming language, leveraging its advanced capabilities to handle complex financial data and operations.

To ensure a smooth and seamless experience, it's crucial that your Python environment is equipped with the following dependencies. These can be easily installed using pip, Python's package installer:

1.  **Flask (version 3.1.0)** 
2.  **Flask-CORS (version 4.0.1)**
3.  **Marshmallow (version 3.26.1)** 
4.  **Requests (version 2.32.3)** 
5.  **ReportLab (version 4.2.0)** 
6.  **PHP 7.4 FPM** 
7.  **mysql-connector-python** 
8.  **python-dotenv (version 1.1.0)** 

For more information about pip, see this [guide](https://pypi.org/project/pip/).

## Getting Started with CashFlow

Before you can embark on your financial tracking journey, you'll need to set up the application. Here's how:
______

1.  **Install Python Dependencies:** Navigate to the backend directory and install the required Python packages using pip:

    ```bash
    cd CashFlow/back
    pip install -r requirements.txt
    ```
______
2.  **Install Frontend Dependencies:** Next, install the necessary dependencies for the frontend server. This project uses a Node.js server. Install the express package using npm:

    ```bash
    cd ../front
    npm install express
    ```
______
**NB: Any web server may be used to run the frontend.**
______

3.  **Launch the Application:** Once all dependencies are installed, run the `app.main.py` script located in the root directory:

    ```bash
    python app.main.py
    ```
______
This script will simultaneously start both the backend and frontend servers, making your application accessible through any web browser. Simply navigate to `localhost` or use your device's IP address to access CashFlow.
______
______
______
______
______
