### Prerequisites
- Python 3.x installed


## Setup project
1. Clone the repository (if not done already)
2. Create a venv (virtual environment) using ```python -m venv venv```
3. Activate venv  
   - on macOS/Linux ```source venv/bin/activate```  
   - on Windows ```venv\Scripts\activate```  
if you cannot run this script (check ```Get-ExecutionPolicy```)  
enable it using ```Set-ExecutionPolicy -Scope Process -ExecutionPolicy Unrestricted```  
after that you can change back to Restricted
4. Install Flask using ```python -m pip install flask```
5. Run ```python -m flask run``` to start an app
6. App will be running on http://127.0.0.1:5000