from calendar import monthrange


def get_string_input(pre_message: str, post_message: str):
    if pre_message:
        print(pre_message, end="")

    return input()


def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


# Can be do better should remove condition and kwargs param and replace with min_val and max_val
# I do it this way because just for fun >.<
def get_integer_input(pre_message: str, post_message: str, condition=lambda x, **y: True, **kwargs):
    if pre_message:
        print(pre_message, end="")

    new_int = input()
    while not is_float(new_int) or not condition(new_int, **kwargs):
        if pre_message:
            pre_message = ""
            print()
        
        print("Please type an valid integer number: ", end="")
        new_int = input()
    
    if post_message:
        print()
        print(post_message)

    if new_int.isdigit():
        return int(new_int)
    else:
        return float(new_int)


def max_day_passed_logic_check(new_int, **kwargs):
    if int(float(new_int)) <= 0:
        return False
    
    if "max_val" in kwargs and kwargs["max_val"] < int(float(new_int)):
        return False

    return True


def get_balance_within_timerange(max_day_passed):
    days_passed = get_integer_input("Type your first N days passed (int): ", "", max_day_passed_logic_check, max_val=max_day_passed)
    balance_accumulated = get_integer_input("Type your balance during these N days (int): ", "")
    return days_passed * balance_accumulated, days_passed


def get_current_total_balance():
    total_days_passed = get_integer_input("How many days have passed (int): ", "")
    total_days_passed_counter = 0
    total_balance_accumulated = 0

    while total_days_passed_counter < total_days_passed:
        balance_accumulated, days_passed = get_balance_within_timerange(total_days_passed - total_days_passed_counter)
        total_days_passed_counter += days_passed
        total_balance_accumulated += balance_accumulated

        print("Days left to input: {}\n".format(total_days_passed - total_days_passed_counter))

    return total_balance_accumulated, total_days_passed


def sanity_check_year(new_int):
    if 2000 < int(float(new_int)) <= 2100:
        return True
    
    return False


def sanity_check_month(new_int):
    if 0 < int(float(new_int)) <= 12 :
        return True
    
    return False


def get_number_of_days_in_month():
    year = get_integer_input("Input year to evaluate (int): ", "", sanity_check_year)
    month = get_integer_input("Input month to evaluate (int): ", "", sanity_check_month)
    return monthrange(year, month)[1]


def pretty_print_day_balance(tuple_of_day_balances):
    print("-" * 16)
    print("{:<4s} | {:<10s}".format("Day", "Balance"))
    print("-" * 16)

    for day_num, balance in tuple_of_day_balances:
        print("{:<4d} | {:<10.2f}".format(day_num, balance))

    print()


def get_total_balance_from_tuple(tuple_of_day_balances):
    total_balance = 0

    for _, balance in tuple_of_day_balances:
        total_balance += balance

    return total_balance


def sanity_check_table_index(new_int, **kwargs):
    if "min_val" in kwargs and int(float(new_int)) < kwargs["min_val"]:
        return False

    if "max_val" in kwargs and kwargs["max_val"] < int(float(new_int)):
        return False

    return True


def evaluate_remaining_days_balance_needed(
    remaining_days, 
    target_avg_balance,
    number_of_days_in_month,
    curr_total_balance_accumulated
):
    target_total_balance = target_avg_balance * number_of_days_in_month
    remaining_balance_needed = target_total_balance - curr_total_balance_accumulated

    print("Remaining days to evaluate:", remaining_days)
    print("Remaining balance needed:", remaining_balance_needed)
    if remaining_balance_needed < 0:
        print("You have reached your target!")
        return

    tuple_of_day_balances = []

    for i in range(1, remaining_days + 1):
        balance = get_integer_input("Type your day#{0} balances: ".format(i), "")
        tuple_of_day_balances.append((i, balance))
    
    repeat = True
    while repeat:
        total_balance = get_total_balance_from_tuple(tuple_of_day_balances)
        
        pretty_print_day_balance(tuple_of_day_balances)
        if (total_balance >= remaining_balance_needed):
            new_avg_balance = (curr_total_balance_accumulated + total_balance) / number_of_days_in_month
            print("You exceeded the target balance. Your current average will be:", new_avg_balance)
        else:
            print("Additional balance needed to reach target:", remaining_balance_needed - total_balance)

        str_input = get_string_input("Do you want to edit the table fields (y/n)? ", "")
        if str_input != "y":
            repeat = False
            continue
        
        day_to_edit = get_integer_input("Which day from the table you want to edit? ", "", sanity_check_table_index, min_val=1, max_val=len(tuple_of_day_balances))
        balance = get_integer_input("Type your day#{0} balances: ".format(day_to_edit), "")
        tuple_of_day_balances[day_to_edit - 1] = (day_to_edit, balance)


if __name__ == "__main__":
    print("======================")
    print("Welcome to Banking App")
    print("======================")
    print("This script will provide the necessary money you need to save to reach target average per month")
    target_avg_balance = get_integer_input("Start by inputing your target average balance (int): ", "")
    number_of_days_in_month = get_number_of_days_in_month()
    curr_total_balance_accumulated, days_passed = get_current_total_balance()
    evaluate_remaining_days_balance_needed(
        number_of_days_in_month - days_passed, 
        target_avg_balance,
        number_of_days_in_month,
        curr_total_balance_accumulated
    )

    print("=======================================")
    print("Thank you for visiting our Banking App")
    print("=======================================")