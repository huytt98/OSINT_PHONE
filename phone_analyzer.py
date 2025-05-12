import phonenumbers
from phonenumbers import carrier, geocoder, timezone

def analyze_phone_number(phone_number):
    """Analyze a phone number and return detailed information."""
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        
        if not phonenumbers.is_valid_number(parsed_number):
            print("Invalid phone number format")
            return None

        return {
            "country_code": parsed_number.country_code,
            "national_number": parsed_number.national_number,
            "country": geocoder.description_for_number(parsed_number, "en"),
            "carrier": carrier.name_for_number(parsed_number, "en"),
            "number_type": _get_number_type_description(phonenumbers.number_type(parsed_number)),
            "is_valid": phonenumbers.is_valid_number(parsed_number),
            "formatted": {
                "international": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "national": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL),
                "e164": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            },
            "timezones": timezone.time_zones_for_number(parsed_number),
            "possibility": phonenumbers.is_possible_number(parsed_number),
            "region": geocoder.description_for_number(parsed_number, "en"),
        }
    except phonenumbers.NumberParseException as e:
        print(f"Error parsing phone number: {e}")
        return None

def _get_number_type_description(number_type):
    types = {
        0: "FIXED_LINE",
        1: "MOBILE",
        2: "FIXED_LINE_OR_MOBILE",
        3: "TOLL_FREE",
        4: "PREMIUM_RATE",
        5: "SHARED_COST",
        6: "VOIP",
        7: "PERSONAL_NUMBER",
        8: "PAGER",
        9: "UAN",
        10: "UNKNOWN",
        27: "EMERGENCY",
        28: "VOICEMAIL"
    }
    return types.get(number_type, "UNKNOWN")
