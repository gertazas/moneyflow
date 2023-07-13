import os
import gspread
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = '1MrGvUcus3F8fyGlqVvWYB-udybH0qNlq5JLQY2g_gMs'

def main():
    print("Welcome to Gary Murphy's MoneyFlow Automation")
    print("All data entries here:\n")

    # Load credentials from credentials.json
    creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)

    # Check if credentials are valid, refresh if necessary
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = creds.refresh(Request())

    try:
        # Authorize the credentials with gspread
        client = gspread.authorize(creds)

        # Open the spreadsheet by its ID
        spreadsheet = client.open_by_key(SPREADSHEET_ID)

        # Get the first worksheet in the spreadsheet
        worksheet = spreadsheet.get_worksheet(0)

        # Retrieve values from the worksheet
        values = worksheet.get_all_values()

        # Define the row numbers
        row_numbers = [5, 9, 13, 18, 23, 28, 33]

        # Initialize an empty list to store the values
        cell_values = []

        # Retrieve the values from the specified rows in column B
        for row_number in row_numbers:
            cell_value = worksheet.cell(row_number, 2).value
            cell_values.append(cell_value)

        # print("All week bank statement values:")
        # for value in cell_values:
        #     print(value)

        # Initialize a variable to store the sum
        statements_sum = 0

        # Retrieve the values from the specified rows in column B and calculate the sum
        for row_number in row_numbers:
            cell_value = worksheet.cell(row_number, 2).value
            if cell_value:
                # Remove the euro sign (€) from the cell value
                cell_value = cell_value.replace('€', '').replace(',', '')
                statements_sum += float(cell_value)

        print("Bank statements in total: €", statements_sum)

        all_weeks_total = worksheet.cell(34, 2).value.replace('€', '')
        print("Weeks in total: €", all_weeks_total)

        all_weeks_total = all_weeks_total.replace(',', '')
        expenses_cash = float(all_weeks_total) - float(statements_sum)
        print('Expenses_cash: €', expenses_cash)

        # Monday total
        monday_bank = worksheet.cell(5, 2).value.replace('€', '')
         # Convert to float
        monday_bank = float(monday_bank.replace(',', '')) 
        # Add 5% of expenses_cash
        monday_plus = float(expenses_cash * 0.05)
        monday = monday_bank + monday_plus
        print('Monday: €', monday)
        worksheet.update_cell(5, 2, monday)

        #Tuesday total
        tuesday_bank = worksheet.cell(9, 2).value.replace('€', '')
         # Convert to float
        tuesday_bank = float(tuesday_bank.replace(',', '')) 
        # Add 5% of expenses_cash
        tuesday_plus = float(expenses_cash * 0.05)
        tuesday = tuesday_bank + tuesday_plus
        print('Tuesday: €', tuesday)
        worksheet.update_cell(9, 2, tuesday)

        # Wednesday total
        wednesday_bank = worksheet.cell(13, 2).value.replace('€', '')
         # Convert to float
        wednesday_bank = float(wednesday_bank.replace(',', '')) 
        # Add 5% of expenses_cash
        wednesday_plus = float(expenses_cash * 0.07)
        wednesday = wednesday_bank + wednesday_plus
        print('Wednesday: €', wednesday)
        worksheet.update_cell(13, 2, wednesday)

        # Thursday total
        thursday_bank = worksheet.cell(18, 2).value.replace('€', '')
         # Convert to float
        thursday_bank = float(thursday_bank.replace(',', '')) 
        # Add 13% of expenses_cash
        thursday_plus = float(expenses_cash * 0.13)
        thursday = thursday_bank + thursday_plus
        print('Thursday: €', thursday)
        worksheet.update_cell(18, 2, thursday)

        # Friday total
        friday_bank = worksheet.cell(23, 2).value.replace('€', '')
         # Convert to float
        friday_bank = float(friday_bank.replace(',', '')) 
        # Add 22% of expenses_cash
        friday_plus = float(expenses_cash * 0.22)
        friday = friday_bank + friday_plus
        print('Friday: €', thursday)
        worksheet.update_cell(23, 2, friday)

        # Saturday total
        saturday_bank = worksheet.cell(28, 2).value.replace('€', '')
         # Convert to float
        saturday_bank = float(saturday_bank.replace(',', '')) 
        # Add 40% of expenses_cash
        saturday_plus = float(expenses_cash * 0.40)
        saturday = saturday_bank + saturday_plus
        print('Saturday: €', saturday)
        worksheet.update_cell(28, 2, saturday)

        # Sunday total
        sunday_bank = worksheet.cell(33, 2).value.replace('€', '')
         # Convert to float
        sunday_bank = float(sunday_bank.replace(',', '')) 
        # Add 18% of expenses_cash
        sunday_plus = float(expenses_cash * 0.18)
        sunday = sunday_bank + sunday_plus
        print('Sunday: €', sunday)
        worksheet.update_cell(33, 2, sunday)


    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()