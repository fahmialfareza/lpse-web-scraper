import re
import locale
from datetime import datetime


def convert_currency_to_int(currency_string):
    """Convert Indonesian currency string to integer.

    Args:
        currency_string (str): The currency string to be converted.
    Returns:
        int: The converted integer value.
    Raises:
        ValueError: If the input string is not a valid currency format.
    """
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
    """Convert Indonesian date string to a datetime.date object.

    Args:
        indonesian_date (str): Indonesian date string in the format "DD MMM YYYY".
    Returns:
        datetime.date: The corresponding date object.
    Raises:
            ValueError: If the input string is not in the expected format.
    """

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
    """Represent number in Rupiah format

    Args:
        x (int): number to be formatted
        _ (str): currency code
    Returns:
        str: formatted number
    """

    return f"Rp {x:,.0f}".replace(",", ".")
