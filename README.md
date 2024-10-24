# currency_converter

This is a simple Python-based currency converter that fetches live exchange rates using the ExchangeRate-API (or similar APIs) and converts a specified amount from one currency to another.

**Features
Fetches live exchange rates.
Converts between multiple currencies.
Provides error handling for invalid currencies or API issues.
**Requirements

Python 3.x
An API key from a currency conversion API provider, such as:
ExchangeRate-API
CurrencyLayer
Open Exchange Rates

**Libraries Used
requests (to handle HTTP requests)
datetime and timedelta (for handling date and time operations)


**Input Data: When prompted, input:

The amount you want to convert.
The currency code to convert from (e.g., USD, EUR).
The currency code to convert to (e.g., GBP, INR)


Examble :-

Enter the amount: 100
From currency (e.g., USD): USD
To currency (e.g., EUR): EUR
100 USD = 85.00 EUR
