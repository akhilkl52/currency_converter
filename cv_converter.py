import requests
import sqlite3
from datetime import datetime, timedelta

def store_conversion(amount, from_currency, to_currency, result):
    conn = sqlite3.connect('conversions.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS conversions
                   (amount REAL, from_currency TEXT, to_currency TEXT, result REAL)''')
    cursor.execute("INSERT INTO conversions VALUES (?, ?, ?, ?)", (amount, from_currency, to_currency, result))
    conn.commit()
    conn.close()

		

def get_exchange_rate(from_currency, to_currency, api_key):
    url = "https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
    

    response = requests.get(url)
    
    print("API Response:", response.text) 
    
    if response.status_code == 200:
        data = response.json()
        
        if 'conversion_rates' in data:
            rate = data['conversion_rates'].get(to_currency)
            
            if rate:
                return rate
            else:
                print(f"Error: Currency code '{to_currency}' not found in the conversion rates.")
                return None
        else:
            print("Error: 'conversion_rates' not found in the API response.")
            return None
    else:
      
        print(f"Error fetching exchange rate. Status code: {response.status_code}")
        
        if response.status_code == 401:
            print("Unauthorized: Invalid API key.")
        elif response.status_code == 404:
            print("Not Found: The resource could not be found. Check the currency codes and API URL.")
        elif response.status_code == 429:
            print("Rate limit exceeded: You've made too many requests. Try again later.")
        else:
            print(f"Unknown error occurred. Response: {response.text}")
        
        return None



def get_historical_rate(from_currency, to_currency, api_key, date):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/history/{from_currency}/{date}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['conversion_rates'].get(to_currency)
    else:
        print(f"Error fetching historical rate for {date}.")
        return None


def convert_currency(amount, from_currency, to_currency, api_key):
    rate = get_exchange_rate(from_currency, to_currency, api_key)
    if rate:
        return amount * rate
    else:
        return None

def store_conversion(amount, from_currency, to_currency, result):
    conn = sqlite3.connect('conversions.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS conversions
                   (date TEXT, amount REAL, from_currency TEXT, to_currency TEXT, result REAL)''')
    cursor.execute("INSERT INTO conversions VALUES (?, ?, ?, ?, ?)",
                   (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), amount, from_currency, to_currency, result))
    conn.commit()
    conn.close()


def view_history():
    conn = sqlite3.connect('conversions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversions")
    rows = cursor.fetchall()
    if rows:
        print("Conversion History:")
        for row in rows:
            print(f"Date: {row[0]}, Amount: {row[1]}, From: {row[2]}, To: {row[3]}, Result: {row[4]}")
    else:
        print("No history available.")
    conn.close()


def main():
    api_key = "YOUR_API_KEY_HERE"  

    while True:
        print("\nCurrency Converter")
        print("1. Convert Currency")
        print("2. View Last 5 Days Historical Rates (Optional)")
        print("3. View Conversion History (Optional)")
        print("4. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            amount = float(input("Enter the amount: "))
            from_currency = input("From currency (e.g., USD): ").upper()
            to_currency = input("To currency (e.g., EUR): ").upper()

            result = convert_currency(amount, from_currency, to_currency, api_key)
            if result:
                print(f"{amount} {from_currency} = {result:.2f} {to_currency}")
                store_conversion(amount, from_currency, to_currency, result)

        elif choice == '2':
            from_currency = input("From currency (e.g., USD): ").upper()
            to_currency = input("To currency (e.g., EUR): ").upper()

            for i in range(5):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                historical_rate = get_historical_rate(from_currency, to_currency, api_key, date)
                if historical_rate:
                    print(f"Rate on {date}: 1 {from_currency} = {historical_rate} {to_currency}")
                else:
                    print(f"No historical data available for {date}")

        elif choice == '3':
            view_history()

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
