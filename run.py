import gspread
from pprint import pprint
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
    while True:
        print("enter sales data from last market")
        print("data should be six numbers seperated by commas")
        print("example: 10, 20, 30, 40, 50 , 60")

        data_str = input("enter your data here: ")
    
        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("data is valid")
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all strings into integers. 
    Raises value error if it cannot convert to integer or if there aren't 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required. You provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data: {e}, please try again")
        return False

    return True

# def update_sales_worksheet(data):
#     """
#     updates sales worksheet and adds a new row with the list data provided.
#     """
#     print("updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("sales worksheet updated successfully. \n")

# def update_surplus_worksheet(data):
#     """
#     updates surplus worksheet and adds a new row with the list data provided.
#     """
#     print("updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("surplus worksheet updated successfully. \n")

def update_worksheet(data, worksheet):
    """
    updates worksheets and adds a new row with the list data provided.
    """
    print(f"updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully. \n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("calculating surplus data... \n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def get_last_5_entries_sales():
    """
    gets columns of data for each sandwish sale from the worksheet for last 5 days of sales
    """
    sales = SHEET.worksheet("sales")
    collumns = []
    for ind in range(1, 7):
        collumn = sales.col_values(ind)
        collumns.append(collumn[-5:])
    return collumns

def calculate_stock_data(data):
    """
    calculates stock data
    """
    print("calculating stock data...\n")
    new_stock_data = []
    for collumn in data:
        int_collumn = [int(num) for num in collumn]
        average = sum(int_collumn) / len(int_collumn)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data


def main():
    """
    Runs all functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_collumns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_collumns)
    print(stock_data)
    update_worksheet(stock_data, "stock")

print("wlecome to love sandwiches data automation")
main()