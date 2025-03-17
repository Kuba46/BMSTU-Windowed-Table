# bauman-student-parser
A web scraper for extracting student data from the “Electronic University” (ЭУ) portal of Bauman Moscow State Technical University (BMSTU). It gathers student information such as names, departments, and academic details, automating the process for analysis or research.

## Requirements

To run this project, follow these steps:

### 1. Python
- Python 3.6 or higher is required. You can download the latest version of Python from [here](https://www.python.org/downloads/).

### 2. Selenium
- Selenium is a Python package used for browser automation. To install it, run:
  ```bash
  pip install selenium

### 3. Google Chrome
- The latest version of Google Chrome browser is required. Download it from [here](https://www.google.com/chrome/).

### 4. ChromeDriver
- ChromeDriver is needed for Selenium to interact with the Google Chrome browser. Download the appropriate version of ChromeDriver based on your installed version of Chrome from [here](https://developer.chrome.com/docs/chromedriver/downloads).

- After downloading, ensure that the chromedriver executable is available in your system’s PATH, or specify its path directly in your code.

### 5. Install Dependencies
- To install all the required dependencies for the project, run:
  ```bash
  pip install -r requirements.txt

### 6. Create credentials.json
- **Important**: Don’t forget to create and fill in the **credentials.json** file, which is required for authentication or connection settings in the project. This file should contain sensitive data (login and password), so make sure it is stored securely and do not commit it to your Git repository (it should be listed in .gitignore).
- Example structure of credentials.json:
  ```javascript
  {
    "login": "your_login",
    "password": "your_password"
  }
