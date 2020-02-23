CITY_DATA = { 'chicago': 'chicago.csv',
        'new york city': 'new_york_city.csv',
        'washington': 'washington.csv' }

MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june']

DAY_OF_THE_WEEK_DATA = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']


def display_error_message(display_type, additional_msg = ""):
    """
    Displays an error message with given display_type in the output    
    """
    if display_type is not None:
        print(f"Invalid value entered for {display_type}. {additional_msg}")
    else:
        print(f"Invalid value entered. {additional_msg}")

def get_master_data(display_type):
    """
    Retrieves the corresponding master data object for the given display_type

    Returns:
        (object) the master data object for the given type (could be a dictionary, list, etc.)
    """
    if(display_type is None):
        return None
        
    if display_type.lower() == "city":
        return CITY_DATA
    elif display_type.lower() == "month":
        return MONTH_DATA
    elif display_type.lower() == "day_of_the_week":
        return DAY_OF_THE_WEEK_DATA
    else:
        return None


def prompt(say, type_of, display_type = None):
    """
    Prompts the user to specify a criteria to analyze the data (like city, month, and day).

    Parameters:
        (str) say - message that needs to be displayed to the user on the prompt
        (str) type_of - the type of input expected (str, int, float, etc.)
        (str) display_type - the display name for the input (city, month and day)

    Returns:
        (object) the value of user input converted to given type.
    """
    input_master_data = get_master_data(display_type)
    while True:
        try:
            input_value = input(say)
            input_value = type_of(input_value)

            # if it's not City, and the value is all, don't validate with master data
            if(display_type != "city" and input_value == "all"): 
                input_master_data = None

            if input_master_data is not None:
                if(hasattr(input_value, 'lower')): # handles case insensitive look up for strings
                    if input_value.lower() not in input_master_data:
                        display_error_message(display_type)
                        continue  
                else: # handles look up types other than string (int, float etc.)
                    if input_value not in input_master_data:
                        display_error_message(display_type)
                        continue  
            break
        except ValueError:
            display_error_message(display_type, f"The input must be of type {type_of.__name__}")
            continue        

    return input_value    
