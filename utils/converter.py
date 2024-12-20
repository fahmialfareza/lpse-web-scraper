import re
import locale
from datetime import datetime


def convert_currency_to_int(currency_string):
    # Remove non-numeric characters except ',' and '.'
    cleaned_string = re.sub(r"[^\d.,]", "", currency_string)

    # Split into main part and fractional part (after the last ',')
    if "," in cleaned_string:
        main_part, decimal_part = cleaned_string.rsplit(",", 1)
        main_part = main_part.replace(".", "")  # Remove thousand separators
        result = float(f"{main_part}.{decimal_part}")
    else:
        # If no decimal separator, handle as an integer
        result = int(cleaned_string.replace(".", ""))

    return result


def convert_date_string_to_date(indonesian_date):
    # Map Indonesian month names to English
    month_mapping = {
        "Januari": "January",
        "Februari": "February",
        "Maret": "March",
        "April": "April",
        "Mei": "May",
        "Juni": "June",
        "Juli": "July",
        "Agustus": "August",
        "September": "September",
        "Oktober": "October",
        "November": "November",
        "Desember": "December",
    }

    # Replace Indonesian month with English equivalent
    for indo_month, eng_month in month_mapping.items():
        indonesian_date = indonesian_date.replace(indo_month, eng_month)

    # Convert to datetime
    date_object = datetime.strptime(indonesian_date, "%d %B %Y")
    return date_object.isoformat()


def rupiah_format(x, _):
    return f"Rp {x:,.0f}".replace(",", ".")
