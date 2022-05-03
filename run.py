import gspread
from google.oauth2.service_account import Credentials
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')
sales = SHEET.worksheet('sales')

data = sales.get_all_values()

print(data)

def get_sales_data():
    """
    Gets sales figures from user
    """
    print("enter sales data from last market")
    print("data should be six numbers seperated by commas")
    print("example: 10, 20, 30, 40, 50 , 60")

    data_str = input("enter your data here: ")
    
    sales_data = data_str.split(",")
    validate_data(sales_data)

def validate_data(values):
    """
    Inside the try, converts all strings into integers. 
    Raises value error if it cannot convert to integer or if there aren't 6 values
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required. You provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data: {e}, please try again")

    print(values)

get_sales_data()