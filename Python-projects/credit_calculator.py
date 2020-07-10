# calculate payment, principal, periods based on user input on command line
# alternative calc with user prompt commented out below
# from jetbrains project credit calc https://hyperskill.org/projects/90?track=2

import math
import argparse
import sys

# argparse config
parser = argparse.ArgumentParser()
parser.add_argument("--type", help="annuity or diff payment")
parser.add_argument("--payment", type=int, help="monthly payment")
parser.add_argument("--principal", type=int, help="principal amount")
parser.add_argument("--periods", type=int, help="number of mths/yrs to repay")
parser.add_argument("--interest", type=float, help="i/r as float, without percent sign")
args = parser.parse_args()

# argparse validation. sys.exit() to stop the function if params not valid
if args.type not in ("annuity", "diff"):
    print("Incorrect parameters")
    sys.exit()
if args.type == "diff" and args.payment != None:
    print("Incorrect parameters")
    sys.exit()
if args.interest == None:
    print("Incorrect parameters")
    sys.exit()
# check num of params https://stackoverflow.com/a/10699527
if len(sys.argv) < 5:
    print("Incorrect parameters")
    sys.exit()
# check +ve values params https://stackoverflow.com/questions/19907442/explain-dict-attribute    
for i in args.__dict__.values():
    if type(i) != str and i != None and i < 0:
        print("Incorrect parameters")
        sys.exit()

# functions for each calc
def over_payment(total_pay, principal):
    over_pay = total_pay - principal
    print(f"Overpayment = {over_pay}")
    
def period_format(periods):
    y_num = periods // 12
    m_num = periods % 12
    if y_num == 1:
        y = " year"
    else:
        y = " years"
    if m_num == 1:
        m = " month"
    else:
        m = " months"
    # catch the zero year or zero month cases
    if y_num == 0:
        return str(m_num) + m
    elif m_num == 0:
        return str(y_num) + y
    else:
        return str(y_num) + y + " and " + str(m_num) + m   
            
def annuity_payment(principal, periods, ir):
    ir = ir / (12 * 100)  # convert units
    annuity_pay = (principal * (ir * math.pow((1 + ir), periods)) 
                / (math.pow((1 + ir), periods) - 1))
    annuity_pay = math.ceil(annuity_pay)  # round the payment 
    total_pay = annuity_pay * periods  # since payment rounded, total doesn't need to be
    print(f"Your annuity payment = {annuity_pay}!")
    over_payment(total_pay, principal)
    
def diff_payment(principal, periods, ir):
    ir = ir / (12 * 100)
    total_pay = 0
    for i in range(1, periods + 1):
        diff_pay = (principal / periods 
                + ir * (principal - (principal * (i - 1) / periods)))
        diff_pay = math.ceil(diff_pay)
        total_pay += diff_pay
        print(f"Month {i}: paid out {diff_pay}")
    print("")
    over_payment(total_pay, principal)    

def calc_principal(payment, periods, ir):
    ir = ir / (12 * 100)  
    principal = payment / ((ir * math.pow((1 + ir), periods)) / (math.pow((1+ ir), periods) - 1))
    principal = math.ceil(principal)
    total_pay = payment * periods
    print(f"Your credit principal = {principal}!")
    over_payment(total_pay, principal)
    
def calc_periods(payment, principal, ir):
    ir = ir / (12 * 100)  
    periods = math.log(payment / (payment - ir * principal), (1 + ir))
    periods = math.ceil(periods)
    text = period_format(periods)
    total_pay = payment * periods
    print(f"You need {text} to repay this credit!")
    over_payment(total_pay, principal)

# if/else based on user choice
if args.type == "diff":
    diff_payment(args.principal, args.periods, args.interest)
elif args.type == "annuity":
    if args.payment == None:
        annuity_payment(args.principal, args.periods, args.interest)
    elif args.principal == None:
        calc_principal(args.payment, args.periods, args.interest)
    elif args.periods == None:
        calc_periods(args.payment, args.principal, args.interest)

##### [old] take input by prompt not command line #####
# choice = input('''What do you want to calculate?
# type "n" - for count of months, 
# type "a" - for annuity monthly payment,
# type "p" - for credit principal: 
# ''')
# 
# if choice == 'n':
#     p = float(input('Enter credit principal:'))
#     a = float(input('Enter monthly payment:'))
#     # convert interest to float
#     i = (float(input('Enter credit interest:'))) / (12 * 100)
#     n = math.log(a / (a - i * p), (1 + i))
#     rounded_n = math.ceil(n)
#     if rounded_n < 12:
#         if rounded_n == 1:
#             n_string = str(rounded_n) + ' month'
#         else:
#             n_string = str(rounded_n) + ' months'
#     elif 12 <= rounded_n < 24:
#         yrs = int(rounded_n / 12)
#         mths = rounded_n % 12
#         if mths == 0:
#             n_string = str(yrs) + ' year'
#         elif mths == 1:
#             n_string = str(yrs) + ' year and ' + str(mths) + ' month'
#         else:
#             n_string = str(yrs) + ' year and ' + str(mths) + ' months'
#     else:
#         yrs = int(rounded_n / 12)
#         mths = rounded_n % 12
#         if mths == 0:
#             n_string = str(yrs) + ' years'
#         elif mths == 1:
#             n_string = str(yrs) + ' years and ' + str(mths) + ' month'
#         else:
#             n_string = str(yrs) + ' years and ' + str(mths) + ' months'
#     print('You need', n_string, 'to repay this credit!')
# elif choice == 'a':
#     p = float(input('Enter credit principal:'))
#     n = float(input('Enter count of periods:'))
#     i = (float(input('Enter credit interest:'))) / (12 * 100)
#     a = p * (i * math.pow((1 + i), n)) / (math.pow((1 + i), n) - 1)
#     rounded_a = math.ceil(a)
#     print('Your annunity payment =', rounded_a)
# elif choice == 'p':
#     a = float(input('Enter monthly payment:'))
#     n = float(input('Enter count of periods:'))
#     i = (float(input('Enter credit interest:'))) / (12 * 100)
#     p = a / ((i * math.pow((1 + i), n)) / (math.pow((1+ i), n) - 1))
#     rounded_p = math.ceil(p)
#     print('Your credit principal =', rounded_p)  
