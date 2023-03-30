import random
import csv

usernames = []
first_names = []
last_names = []
names = []
profiles = []
numbers = []
departments = []

from datetime import date, timedelta

# Define start and end dates
start_date = date(2002, 1, 1)
end_date = date(2004, 12, 31)

# Calculate the number of days between the start and end dates
days = (end_date - start_date).days

# List of possible mobile number prefixes in the Philippines
prefixes = ['0905', '0906', '0915', '0916', '0917', '0926', '0927', '0935', '0936', '0937', '0945', '0953', '0954', '0955', '0963', '0964', '0965', '0973', '0974', '0975', '0976', '0977', '0978', '0979', '0997', '0998', '0999']

with open('first_names.txt', 'r') as file:
    lines = file.readlines()
    
    # Remove any trailing newline characters from each line
    first_names = [line.rstrip('\n').lstrip() for line in lines]

with open('last_names.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    
    # Remove any trailing newline characters from each line
    last_names = [line.rstrip('\n').lstrip() for line in lines]

with open('departments.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    
    # Remove any trailing newline characters from each line
    departments = [line.rstrip('\n').lstrip() for line in lines]

for i in range(1000):
    profile = {}
    random_num = f"{random.randint(1,9999):04}"
    username = f"2021-{random_num}-MN-0"

    while True:
        if username not in usernames:
            usernames.append(username)
            break

        random_num = f"{random.randint(1,9999):04}"
        username = f"2021-{random_num}-MN-0"

    prefix = random.choice(prefixes)
    number = random.randint(1000000, 9999999)
    mobile_number = f'({prefix}) {number}'

    while True:
        if mobile_number not in numbers:
            numbers.append(mobile_number)
            break
        prefix = random.choice(prefixes)
        number = random.randint(1000000, 9999999)
        mobile_number = f'{prefix}{number}'

    # Generate a random number of days between the start and end dates
    random_days = random.randint(0, days)

    # Calculate the random date by adding the random number of days to the start date
    random_date = start_date + timedelta(days=random_days)
    date_string = random_date.strftime('%Y-%m-%d')

    department = random.choice(departments)

    profile['username'] = username
    profile['first_name'] = random.choice(first_names)
    profile['last_name'] = random.choice(last_names)
    profile['middle_name'] = random.choice(last_names)
    profile['email'] = f"{profile['first_name'][0].lower()}{profile['middle_name'][0].lower()}{profile['last_name'].lower().strip()}@iskolarngbayan.pup.edu.ph"
    profile['gender'] = random.choice(['M', 'F'])
    profile['birth_date'] = date_string
    profile['mobile_number'] = mobile_number
    profile['department'] = department

    profiles.append(profile)


# Define the output CSV file path
csv_path = 'output.csv'

# Open the output file in write mode
with open(csv_path, 'w', newline='') as csv_file:
    
    # Define the CSV writer with the same keys as the dictionaries
    fieldnames = profiles[0].keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row to the CSV file
    writer.writeheader()
    
    # Write each dictionary as a row to the CSV file
    for row in profiles:
        writer.writerow(row)

print("profiles were generated")