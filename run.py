import os
import gspread
import random
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

def random_number():
    rnumber = random.randint(50, 100)
    if rnumber % 5 == 0:
        print('rnumber:', rnumber)
        return rnumber
    else:
        random_number()


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

        #Weeks totals:
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

        # Sunday total
        sunday_bank = worksheet.cell(33, 2).value.replace('€', '')
         # Convert to float
        sunday_bank = float(sunday_bank.replace(',', '')) 
        # Add 18% of expenses_cash
        sunday_plus = float(expenses_cash * 0.18)
        sunday = sunday_bank + sunday_plus
        print('Sunday: €', sunday)
        worksheet.update_cell(33, 2, sunday)

        # Saturday total
        saturday = float(all_weeks_total) - monday - tuesday - wednesday - thursday - friday - sunday
        print('Saturday: €', saturday)
        worksheet.update_cell(28, 2, saturday)
        
    # Weekdays and Trailers 1, 2, and 3 only:
        def calculate_and_update_trailer(day, trailer_num, row, day_name):
            value = float(day * 0.65) if trailer_num == 1 else float(day * 0.21) if trailer_num == 2 else float(day * 0.14)
            worksheet.update_cell(row, 3, value)
            print(f'{day_name}trailer{trailer_num}: €', value)
            return value

        mondaytrailers = []
        # Monday
        for i in range(1, 4):
            mondaytrailer = calculate_and_update_trailer(monday, i, i+1, 'monday   ')
            mondaytrailers.append(mondaytrailer)
        print('mondaytrailers', mondaytrailers)
        print('_________________________________________________________________________')
        tuesdaytrailers = []
        # Tuesday
        for i in range(1, 4):
            tuesdaytrailer = calculate_and_update_trailer(tuesday, i, i+5, 'tuesday  ')
            tuesdaytrailers.append(tuesdaytrailer)
            print('tuesdaytrailers', tuesdaytrailers)
        print('_________________________________________________________________________')
        # Wednesday
        wednesdaytrailers = []
        for i in range(1, 4):
            wednesdaytrailer = calculate_and_update_trailer(wednesday, i, i+9, 'wednesday')
            wednesdaytrailers.append(wednesdaytrailer)
            print('wednesdaytrailers', wednesdaytrailers)
        print('_________________________________________________________________________')


    # Weekends and Trailers 1, 2, 3 and 4:
        def calculate_and_update_trailer4(day, trailer_num, row, day_name):
            value = float(day * 0.54) if trailer_num == 1 else float(day * 0.18) if trailer_num == 2 else float(day * 0.16) if trailer_num == 3 else float(day * 0.12)
            worksheet.update_cell(row, 3, value)
            print(f'{day_name}trailer{trailer_num}: €', value)
            return value

        # Thursday
        thursdaytrailers = []
        for i in range(1, 5):
            thursdaytrailer = calculate_and_update_trailer4(thursday, i, i+13, 'thursday ')
            thursdaytrailers.append(thursdaytrailer)
            print('thursdaytrailers', thursdaytrailers)
        print('_________________________________________________________________________')
        # Friday
        fridaytrailers = []
        for i in range(1, 5):
            fridaytrailer = calculate_and_update_trailer4(friday, i, i+18, 'friday   ')
            fridaytrailers.append(fridaytrailer)
            print('fridaytrailers', fridaytrailers)
        print('_________________________________________________________________________')
#         # Saturday
#         for i in range(1, 5):
#             saturdaytrailer = calculate_and_update_trailer4(saturday, i, i+23, 'saturday ')
#         print('_________________________________________________________________________')
#         # Sunday
#         for i in range(1, 5):
#             sundaytrailer = calculate_and_update_trailer4(sunday, i, i+28, 'sunday   ')
#         print('_________________________________________________________________________')
        print('_____________________________')
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#         monday_trailer1 = float(mondaytrailers[0])
#         print('Monday trailer1 total: €', monday_trailer1)

#         def calculate_and_update_coffee(coffee1):
#             if coffee1 < 300:
#                 random_number = 0
#             elif coffee1 < 400:
#                 random_number = random.uniform(0, 50)
#             else:
#                 random_number = random.uniform(50, 100)
            
#             coffee = float(coffee1 * 0.45) + random_number
#             worksheet.update_cell(2, 4, coffee)
#             print(f'Trailer1_Coffee_section: €', coffee)
#             return coffee

#         coffee = calculate_and_update_coffee(monday_trailer1)

#         def calculate_and_update_mlksh(mlsh1):
#             mlksh = float(mlsh1 * 0.25) 
#             worksheet.update_cell(2, 5, mlksh)
#             print(f'Trailer1_Milkshake_section: €', mlksh)
#             return mlksh

#         mlksh = calculate_and_update_mlksh(monday_trailer1)

#         def calculate_and_update_23percent(coff, mlk):
#             trailer1_last_section = monday_trailer1 - coff - mlk
#             worksheet.update_cell(2, 6, trailer1_last_section)
#             print(f'Trailer1_23%_section: €', trailer1_last_section)
#             return trailer1_last_section

#         calculate_and_update_23percent(coffee, mlksh)
#         print('___________________')
#         monday_trailer2 = float(mondaytrailers[1])
#         print('Monday trailer1 total: €', monday_trailer2)

#         def calculate_and_update_mlksh2(mlsh2):
#             if mlsh2 < 200:
#                 random_number = 0
#             elif mlsh2 < 400:
#                 random_number = random.uniform(0, 50)
#             else:
#                 random_number = random.uniform(0, 75)

#             mlksh2 = float(mlsh2 * 0.45) + random_number
#             worksheet.update_cell(3, 5, mlksh2)
#             print(f'Trailer2_Milkshake_section: €', mlksh2)
#             return mlksh2

#         mlksh2 = calculate_and_update_mlksh2(monday_trailer2)

#         def calculate_and_update_23percent2(mlk):
#             trailer2_last_section = monday_trailer2 - mlk
#             worksheet.update_cell(3, 6, trailer2_last_section)
#             print(f'Trailer2_23%_section: €', trailer2_last_section)
#             return trailer2_last_section

#         calculate_and_update_23percent2(mlksh2)
#         print('___________________')
#         monday_trailer3 = float(mondaytrailers[2])
#         print('Monday trailer3 total: €', monday_trailer3)

#         def calculate_and_update_mlksh2(mlsh3):
#             if mlsh3 < 200:
#                 random_number = 0
#             elif mlsh3 < 400:
#                 random_number = random.uniform(0, 50)
#             else:
#                 random_number = random.uniform(0, 75)

#             mlksh3 = float(mlsh3 * 0.45) + random_number
#             worksheet.update_cell(4, 5, mlksh3)
#             print(f'Trailer2_Milkshake_section: €', mlksh3)
#             return mlksh3

#         mlksh3 = calculate_and_update_mlksh2(monday_trailer3)

#         def calculate_and_update_23percent3(mlk):
#             trailer3_last_section = monday_trailer3 - mlk
#             worksheet.update_cell(4, 6, trailer3_last_section)
#             print(f'Trailer3_23%_section: €', trailer3_last_section)
#             return trailer3_last_section

#         calculate_and_update_23percent3(mlksh3)

        print('_____________________________')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        # tuesday_trailer1 = float(tuesdaytrailers[0])
        # print('Tuesday trailer1 total: €', tuesday_trailer1)

        # def tuesday_calculate_and_update_coffee(coffee):
        #     if coffee < 300:
        #         random_number = 0
        #     elif coffee < 400:
        #         random_number = random.uniform(0, 50)
        #     else:
        #         random_number = random.uniform(50, 100)
            
        #     coffee = float(coffee * 0.45) + random_number
        #     worksheet.update_cell(6, 4, coffee)
        #     print(f'Trailer1_Coffee_section: €', coffee)
        #     return coffee

        # tuesday_coffee = tuesday_calculate_and_update_coffee(tuesday_trailer1)

        # def tuesday_calculate_and_update_mlksh(mlsh1):
        #     mlksh = float(mlsh1 * 0.25) 
        #     worksheet.update_cell(6, 5, mlksh)
        #     print(f'Trailer1_Milkshake_section: €', mlksh)
        #     return mlksh

        # tuesday_mlksh = tuesday_calculate_and_update_mlksh(tuesday_trailer1)

        # def tuesday_calculate_and_update_23percent(coff, mlk):
        #     trailer1_last_section = tuesday_trailer1 - coff - mlk
        #     worksheet.update_cell(6, 6, trailer1_last_section)
        #     print(f'Trailer1_23%_section: €', trailer1_last_section)
        #     return trailer1_last_section

        # tuesday_calculate_and_update_23percent(tuesday_coffee, tuesday_mlksh)
#         print('___________________')
        # tuesday_trailer2 = float(tuesdaytrailers[1])
        # print('Tuesday trailer1 total: €', tuesday_trailer2)

        # def tuesday_calculate_and_update_mlksh2(mlsh2):
        #     if mlsh2 < 200:
        #         random_number = 0
        #     elif mlsh2 < 400:
        #         random_number = random.uniform(0, 50)
        #     else:
        #         random_number = random.uniform(0, 75)

        #     mlksh2 = float(mlsh2 * 0.45) + random_number
        #     worksheet.update_cell(7, 5, mlksh2)
        #     print(f'Trailer2_Milkshake_section: €', mlksh2)
        #     return mlksh2

        # tuesday_mlksh2 = tuesday_calculate_and_update_mlksh2(tuesday_trailer2)

        # def tuesday_calculate_and_update_23percent2(mlk):
        #     trailer2_last_section = tuesday_trailer2 - mlk
        #     worksheet.update_cell(7, 6, trailer2_last_section)
        #     print(f'Trailer2_23%_section: €', trailer2_last_section)
        #     return trailer2_last_section

        # tuesday_calculate_and_update_23percent2(tuesday_mlksh2)
        # print('___________________')
        # tuesday_trailer3 = float(tuesdaytrailers[2])
        # print('Tuesday trailer3 total: €', tuesday_trailer3)

        # def tuesday_calculate_and_update_mlksh2(mlsh3):
        #     if mlsh3 < 200:
        #         random_number = 0
        #     elif mlsh3 < 400:
        #         random_number = random.uniform(0, 50)
        #     else:
        #         random_number = random.uniform(0, 75)

        #     mlksh3 = float(mlsh3 * 0.45) + random_number
        #     worksheet.update_cell(8, 5, mlksh3)
        #     print(f'Trailer2_Milkshake_section: €', mlksh3)
        #     return mlksh3

        # tuesday_mlksh3 = tuesday_calculate_and_update_mlksh2(tuesday_trailer3)

        # def tuesday_calculate_and_update_23percent3(mlk):
        #     trailer3_last_section = tuesday_trailer3 - mlk
        #     worksheet.update_cell(8, 6, trailer3_last_section)
        #     print(f'Trailer3_23%_section: €', trailer3_last_section)
        #     return trailer3_last_section

        # tuesday_calculate_and_update_23percent3(tuesday_mlksh3)

        print('_____________________________')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # wednesday_trailer1 = float(wednesdaytrailers[0])
        # print('Wednesday trailer1 total: €', wednesday_trailer1)

        # def wednesday_calculate_and_update_coffee(coffee):
        #     if coffee < 300:
        #         random_number = 0
        #     elif coffee < 400:
        #         random_number = random.uniform(0, 50)
        #     else:
        #         random_number = random.uniform(50, 100)
            
        #     coffee = float(coffee * 0.45) + random_number
        #     worksheet.update_cell(10, 4, coffee)
        #     print(f'Trailer1_Coffee_section: €', coffee)
        #     return coffee

        # wednesday_coffee = wednesday_calculate_and_update_coffee(wednesday_trailer1)

        # def wednesday_calculate_and_update_mlksh(mlsh1):
        #     mlksh = float(mlsh1 * 0.25) 
        #     worksheet.update_cell(10, 5, mlksh)
        #     print(f'Trailer1_Milkshake_section: €', mlksh)
        #     return mlksh

        # wednesday_mlksh = wednesday_calculate_and_update_mlksh(wednesday_trailer1)

        # def wednesday_calculate_and_update_23percent(coff, mlk):
        #     trailer1_last_section = wednesday_trailer1 - coff - mlk
        #     worksheet.update_cell(10, 6, trailer1_last_section)
        #     print(f'Trailer1_23%_section: €', trailer1_last_section)
        #     return trailer1_last_section

        # wednesday_calculate_and_update_23percent(wednesday_coffee, wednesday_mlksh)
#         print('___________________')
        # wednesday_trailer2 = float(wednesdaytrailers[1])
        # print('Wednesday trailer1 total: €', wednesday_trailer2)

        # def wednesday_calculate_and_update_mlksh2(mlsh2):
        #     if mlsh2 < 200:
        #         random_number = 0
        #     elif mlsh2 < 400:
        #         random_number = random.uniform(0, 50)
        #     else:
        #         random_number = random.uniform(0, 75)

        #     mlksh2 = float(mlsh2 * 0.45) + random_number
        #     worksheet.update_cell(11, 5, mlksh2)
        #     print(f'Trailer2_Milkshake_section: €', mlksh2)
        #     return mlksh2

        # wednesday_mlksh2 = wednesday_calculate_and_update_mlksh2(wednesday_trailer2)

        # def wednesday_calculate_and_update_23percent2(mlk):
        #     trailer2_last_section = wednesday_trailer2 - mlk
        #     worksheet.update_cell(11, 6, trailer2_last_section)
        #     print(f'Trailer2_23%_section: €', trailer2_last_section)
        #     return trailer2_last_section

        # wednesday_calculate_and_update_23percent2(wednesday_mlksh2)
        # print('___________________')
        # wednesday_trailer3 = float(wednesdaytrailers[2])
        # print('Wednesday trailer3 total: €', wednesday_trailer3)

        # def wednesday_calculate_and_update_mlksh2(mlsh3):
        #     if mlsh3 < 200:
        #         random_number = 0
        #     elif mlsh3 < 400:
        #         random_number = random.uniform(0, 50)
        #     else:
        #         random_number = random.uniform(0, 75)

        #     mlksh3 = float(mlsh3 * 0.45) + random_number
        #     worksheet.update_cell(12, 5, mlksh3)
        #     print(f'Trailer2_Milkshake_section: €', mlksh3)
        #     return mlksh3

        # wednesday_mlksh3 = wednesday_calculate_and_update_mlksh2(wednesday_trailer3)

        # def wednesday_calculate_and_update_23percent3(mlk):
        #     trailer3_last_section = wednesday_trailer3 - mlk
        #     worksheet.update_cell(12, 6, trailer3_last_section)
        #     print(f'Trailer3_23%_section: €', trailer3_last_section)
        #     return trailer3_last_section

        # wednesday_calculate_and_update_23percent3(wednesday_mlksh3)
        print('_____________________________')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        thursday_trailer1 = float(thursdaytrailers[0])
        print('Thursday trailer1 total: €', thursday_trailer1)

        def thursday_calculate_and_update_coffee(coffee):
            if coffee < 300:
                random_number = 0
            elif coffee < 400:
                random_number = random.uniform(0, 50)
            else:
                random_number = random.uniform(50, 100)
            
            coffee = float(coffee * 0.45) + random_number
            worksheet.update_cell(14, 4, coffee)
            print(f'Trailer1_Coffee_section: €', coffee)
            return coffee

        thursday_coffee = thursday_calculate_and_update_coffee(thursday_trailer1)

        def thursday_calculate_and_update_mlksh(mlsh1):
            mlksh = float(mlsh1 * 0.25) 
            worksheet.update_cell(14, 5, mlksh)
            print(f'Trailer1_Milkshake_section: €', mlksh)
            return mlksh

        thursday_mlksh = thursday_calculate_and_update_mlksh(thursday_trailer1)

        def thursday_calculate_and_update_23percent(coff, mlk):
            trailer1_last_section = thursday_trailer1 - coff - mlk
            worksheet.update_cell(14, 6, trailer1_last_section)
            print(f'Trailer1_23%_section: €', trailer1_last_section)
            return trailer1_last_section

        thursday_calculate_and_update_23percent(thursday_coffee, thursday_mlksh)
        print('___________________')
        thursday_trailer2 = float(thursdaytrailers[1])
        print('Thursday trailer1 total: €', thursday_trailer2)

        def thursday_calculate_and_update_mlksh2(mlsh2):
            if mlsh2 < 200:
                random_number = 0
            elif mlsh2 < 400:
                random_number = random.uniform(0, 50)
            else:
                random_number = random.uniform(0, 75)

            mlksh2 = float(mlsh2 * 0.45) + random_number
            worksheet.update_cell(15, 5, mlksh2)
            print(f'Trailer2_Milkshake_section: €', mlksh2)
            return mlksh2

        thursday_mlksh2 = thursday_calculate_and_update_mlksh2(thursday_trailer2)

        def thursday_calculate_and_update_23percent2(mlk):
            trailer2_last_section = thursday_trailer2 - mlk
            worksheet.update_cell(15, 6, trailer2_last_section)
            print(f'Trailer2_23%_section: €', trailer2_last_section)
            return trailer2_last_section

        thursday_calculate_and_update_23percent2(thursday_mlksh2)
        print('___________________')
        thursday_trailer3 = float(thursdaytrailers[2])
        print('Thursday trailer3 total: €', thursday_trailer3)

        def thursday_calculate_and_update_mlksh3(mlsh3):
            if mlsh3 < 200:
                random_number = 0
            elif mlsh3 < 400:
                random_number = random.uniform(0, 50)
            else:
                random_number = random.uniform(0, 75)

            mlksh3 = float(mlsh3 * 0.45) + random_number
            worksheet.update_cell(16, 5, mlksh3)
            print(f'Trailer3_Milkshake_section: €', mlksh3)
            return mlksh3

        thursday_mlksh3 = thursday_calculate_and_update_mlksh3(thursday_trailer3)

        def thursday_calculate_and_update_23percent3(mlk):
            trailer3_last_section = thursday_trailer3 - mlk
            worksheet.update_cell(16, 6, trailer3_last_section)
            print(f'Trailer3_23%_section: €', trailer3_last_section)
            return trailer3_last_section

        thursday_calculate_and_update_23percent3(thursday_mlksh3)
        print('___________________')
        thursday_trailer4 = float(thursdaytrailers[3])
        print('Thursday trailer4 total: €', thursday_trailer4)

        def thursday_calculate_and_update_mlksh4(mlsh4):
            if mlsh4 < 200:
                random_number = 0
            elif mlsh4 < 400:
                random_number = random.uniform(0, 50)
            else:
                random_number = random.uniform(0, 75)

            mlksh4 = float(mlsh4 * 0.45) + random_number
            worksheet.update_cell(17, 5, mlksh4)
            print(f'Trailer4_Milkshake_section: €', mlksh4)
            return mlksh4

        thursday_mlksh4 = thursday_calculate_and_update_mlksh4(thursday_trailer4)

        def thursday_calculate_and_update_23percent4(mlk):
            trailer4_last_section = thursday_trailer4 - mlk
            worksheet.update_cell(17, 6, trailer4_last_section)
            print(f'Trailer4_23%_section: €', trailer4_last_section)
            return trailer4_last_section

        thursday_calculate_and_update_23percent4(thursday_mlksh4)
        print('_____________________________')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        friday_trailer1 = float(fridaytrailers[0])
        print('Friday trailer1 total: €', friday_trailer1)

        def friday_calculate_and_update_coffee(coffee):
            if coffee < 300:
                random_number = 0
            elif coffee < 400:
                random_number = random.uniform(0, 50)
            else:
                random_number = random.uniform(50, 100)
            
            coffee = float(coffee * 0.45) + random_number
            worksheet.update_cell(19, 4, coffee)
            print(f'Trailer1_Coffee_section: €', coffee)
            return coffee

        friday_coffee = friday_calculate_and_update_coffee(friday_trailer1)

        def friday_calculate_and_update_mlksh(mlsh1):
            mlksh = float(mlsh1 * 0.25) 
            worksheet.update_cell(19, 5, mlksh)
            print(f'Trailer1_Milkshake_section: €', mlksh)
            return mlksh

        friday_mlksh = friday_calculate_and_update_mlksh(friday_trailer1)

        def friday_calculate_and_update_23percent(coff, mlk):
            trailer1_last_section = friday_trailer1 - coff - mlk
            worksheet.update_cell(19, 6, trailer1_last_section)
            print(f'Trailer1_23%_section: €', trailer1_last_section)
            return trailer1_last_section

        friday_calculate_and_update_23percent(friday_coffee, friday_mlksh)
        print('___________________')
        friday_trailer2 = float(fridaytrailers[1])
        print('Friday trailer1 total: €', friday_trailer2)

        def friday_calculate_and_update_mlksh2(mlsh2):
            if mlsh2 < 200:
                random_number = 0
            elif mlsh2 < 400:
                random_number = random.uniform(0, 50)
            else:
                random_number = random.uniform(0, 75)

            mlksh2 = float(mlsh2 * 0.45) + random_number
            worksheet.update_cell(20, 5, mlksh2)
            print(f'Trailer2_Milkshake_section: €', mlksh2)
            return mlksh2

        friday_mlksh2 = friday_calculate_and_update_mlksh2(friday_trailer2)

        def friday_calculate_and_update_23percent2(mlk):
            trailer2_last_section = friday_trailer2 - mlk
            worksheet.update_cell(20, 6, trailer2_last_section)
            print(f'Trailer2_23%_section: €', trailer2_last_section)
            return trailer2_last_section

        friday_calculate_and_update_23percent2(friday_mlksh2)
        print('___________________')
        friday_trailer3 = float(fridaytrailers[2])
        print('Friday trailer3 total: €', friday_trailer3)

        def friday_calculate_and_update_mlksh3(mlsh3):
            if mlsh3 < 200:
                random_number = 0
            elif mlsh3 < 400:
                random_number = random.uniform(0, 50)
            else:
                random_number = random.uniform(0, 75)

            mlksh3 = float(mlsh3 * 0.45) + random_number
            worksheet.update_cell(21, 5, mlksh3)
            print(f'Trailer3_Milkshake_section: €', mlksh3)
            return mlksh3

        friday_mlksh3 = friday_calculate_and_update_mlksh3(friday_trailer3)

        def friday_calculate_and_update_23percent3(mlk):
            trailer3_last_section = friday_trailer3 - mlk
            worksheet.update_cell(21, 6, trailer3_last_section)
            print(f'Trailer3_23%_section: €', trailer3_last_section)
            return trailer3_last_section

        friday_calculate_and_update_23percent3(friday_mlksh3)
        print('___________________')
        friday_trailer4 = float(fridaytrailers[3])
        print('Friday trailer4 total: €', friday_trailer4)

        def friday_calculate_and_update_mlksh4(mlsh4):
            if mlsh4 < 200:
                random_number = 0
            elif mlsh4 < 400:
                random_number = random.uniform(0, 50)
            else:
                random_number = random.uniform(0, 75)

            mlksh4 = float(mlsh4 * 0.45) + random_number
            worksheet.update_cell(22, 5, mlksh4)
            print(f'Trailer4_Milkshake_section: €', mlksh4)
            return mlksh4

        friday_mlksh4 = friday_calculate_and_update_mlksh4(friday_trailer4)

        def friday_calculate_and_update_23percent4(mlk):
            trailer4_last_section = friday_trailer4 - mlk
            worksheet.update_cell(22, 6, trailer4_last_section)
            print(f'Trailer4_23%_section: €', trailer4_last_section)
            return trailer4_last_section

        friday_calculate_and_update_23percent4(friday_mlksh4)
        print('_____________________________')



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # def calculate_and_update_trailer(day, trailer_num, row, day_name):
    #     value = float(day * (0.54 if trailer_num == 1 else 0.18 if trailer_num == 2 else 0.16 if trailer_num == 3 else 0.12))
    #     worksheet.update_cell(row, 3, value)
    #     print(f'{day_name}trailer{trailer_num}: €', value)
    #     return value

    # def calculate_and_update_coffee(coffee1):
    #     if coffee1 < 300:
    #         random_number = 0
    #     elif coffee1 < 400:
    #         random_number = random.uniform(0, 50)
    #     else:
    #         random_number = random.uniform(50, 100)

    #     coffee = float(coffee1 * 0.45) + random_number
    #     worksheet.update_cell(2, 4, coffee)
    #     print(f'Trailer1_Coffee_section: €', coffee)
    #     return coffee

    # def calculate_and_update_milkshake(milkshake1, row, section_name):
    #     if milkshake1 < 200:
    #         random_number = 0
    #     elif milkshake1 < 400:
    #         random_number = random.uniform(0, 50)
    #     else:
    #         random_number = random.uniform(0, 75)

    #     milkshake = float(milkshake1 * 0.45) + random_number
    #     worksheet.update_cell(row, 5, milkshake)
    #     print(f'{section_name}: €', milkshake)
    #     return milkshake

    # def calculate_and_update_23_percent(trailer_total, coffee, milkshake, row, section_name):
    #     last_section = trailer_total - coffee - milkshake
    #     worksheet.update_cell(row, 6, last_section)
    #     print(f'{section_name}: €', last_section)
    #     return last_section

    # days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
    # trailers = []

    # for day_index, day_name in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
    #     for trailer_num in range(1, 4):
    #         trailer = calculate_and_update_trailer(days[day_index], trailer_num, trailer_num + day_index * 4, day_name)
    #         trailers.append(trailer)
    #     print('_________________________________________________________________________')

    # for trailer_index, trailer_total in enumerate(trailers):
    #     trailer_num = trailer_index + 1
    #     print(f'Monday trailer{trailer_num} total: €', trailer_total)

    #     coffee = calculate_and_update_coffee(trailer_total)

    #     milkshake = calculate_and_update_milkshake(trailer_total, trailer_num + 1, f'Trailer{trailer_num}_Milkshake_section')

    #     calculate_and_update_23_percent(trailer_total, coffee, milkshake, trailer_num + 1, f'Trailer{trailer_num}_23%_section')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def reset():
            inrow2 = [5, 9, 13, 18, 23, 28, 33, 34]
            for row2 in inrow2:
                worksheet.update_cell(row2, 2, 0)
            inrow3 = [2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16, 17, 19, 20, 21, 22, 24, 25, 26, 27, 29, 30, 31, 32]
            for row3 in inrow3:
                worksheet.update_cell(row3, 3, 0)
            inrow4 = [6, 10, 14, 19, 24, 29]
            for row4 in inrow4:
                worksheet.update_cell(row4, 4, 0)
            inrow5 = [2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 19, 10, 21, 22, 24, 25, 26, 27, 29, 30, 31, 32]
            for row5 in inrow5:
                worksheet.update_cell(row5, 5, 0)
            inrow6 = [2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 19, 10, 21, 22, 24, 25, 26, 27, 29, 30, 31, 32]
            for row6 in inrow6:
                worksheet.update_cell(row6, 6, 0)
        # reset()

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()