# Book Exchange Platform  

## Overview  
The Book Exchange Platform is a web application designed to make sharing books easy and enjoyable. 
It allows users to list books they own, browse books shared by others, and arrange exchanges. 
The platform promotes sustainable reading practices and fosters a sense of community among book lovers.  

## Features  
- User registration and login. 
- Add your own books.   
- Browse books shared by others.  
- Search functionality to find specific titles or genres.  
- Arrange exchanges with other users.
- Wishlist page to save yout favorite books
- Remove your books from the app, if you change your mind.

## Technologies Used  
- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Python (Flask)  
- **Database**: SQLite

## Getting Started  
 
### Prerequisites  
Ensure you have the following installed:  
- [Python](https://www.python.org/) (3.8 or later)  
- [Pip](https://pip.pypa.io/en/stable/)  
- [Git](https://git-scm.com/) (for cloning the repository and version control)  

SQLite is already included with Python, but you can optionally install a database management tool like [DB Browser for SQLite](https://sqlitebrowser.org/) to view and edit the database directly.

### Installation  

### Step 1: Clone the Repository  
1. Open your terminal or command prompt.  
2. Clone the repository using Git:  
   ```bash
   git clone https://github.com/yourusername/book-exchange-platform.git
   
3. Navigate to the project directory:
   ```bash
   cd book-exchange-platform


### Step 2: Open the Project in VSCode
1. Open Visual Studio Code (VSCode).
2. Click on File > Open Folder (or Open... on macOS).
3. Select the folder where you cloned the project to open on your VSCode.


### Step 3: Set Up a Virtual Environment
Using a virtual environment is recommended to avoid conflicts between dependencies.

### Windows:
1. Open a terminal in VSCode by navigating to Terminal > New Terminal.
2. Run the following command to create a virtual environment:
   ```bash
    py -3 -m venv .venv

3. Activate the virtual environment:
   ```bash  
    .venv\Scripts\activate
   
4. You should see (venv) at the beginning of your terminal line.

### Linux/macOS:
1. Open a terminal in VSCode by navigating to Terminal > New Terminal.
2. Run the following command to create a virtual environment:
   ```bash
    python3 -m venv venv

3. Activate the virtual environment:
   ```bash  
    . .venv/bin/activate

4. You should see (venv) at the beginning of your terminal line.


### Step 4: Install Dependencies
1. With the virtual environment activated, install the necessary Python libraries:
   ```bash  
    pip install flask
    pip install flask-login
    pip install bcrypt

Advice: If you have problems with environment variables that may have already been created previously in your project, you should delete the ".venv" folder and create your environment variable again following the previous steps. 


### Step 5: Set Up the Database
If the database file (`book_trade.db`) already exists, you can skip this step. However, if you need to initialize or set up the database, follow these instructions:

1. Ensure the `book_trade.db` file is present in your project directory.

2. If the database doesn't exist or needs to be initialized, run the following command to set it up:  
   ```bash
    python setup_database.py

This will create or update the book_trade.db file with the necessary tables and schema.

Note: If the database already exists and has data, running this script may overwrite the existing database. Make sure to back up your data if needed.


### Step 6: Start the Application
1. Run the Flask development server:
   ```bash
    python app.py
    
2. By default, the application will be accessible at http://127.0.0.1:5000.

3. Make sure app.py contains your entire backend correctly or if you have your code in another python file. If this is the case, replace app.py with your correct file:
   ```bash
    python your_folder_name.py

If you already has your environment variables set in your local machine, you need only run the command to start the app. 


## Contributing  
Contributions are always welcome! Please follow these steps to contribute to the project:

1. **Fork** the repository to your own GitHub account.
2. **Clone** your fork to your local machine:
   ```bash
    git clone https://github.com/yourusername/book-exchange-platform.git

3. Create a new branch for your feature or bugfix:
   ```bash
    git checkout -b feature-name

4. Make your changes and test thoroughly. Commit your changes with a descriptive message:
   ```bash
    git commit -am 'Add new feature or fix bug'

5. Push your branch to your forked repository:
   ```bash
    git push origin feature-name


6. Submit a pull request to the main repository for review.

We encourage you to open an issue if you encounter any bugs or have suggestions for improvements.


### License
This project is licensed under the MIT License. See the LICENSE file for more information.

