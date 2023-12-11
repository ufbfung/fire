# -*- coding: utf-8 -*-
"""fire streamlit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b9bSnTCijnv7uN3Uz1GBf-isbLcq0fp8
"""

import streamlit as st

def calculate_fire_number(annual_expenses):
    return annual_expenses * 25

def calculate_future_value(monthly_savings, years):
    months = years * 12
    return monthly_savings * months

def calculate_future_value_compound_growth(principal, interest_rate, years):
    # Convert interest rate to a decimal
    interest_rate_decimal = interest_rate / 100

    # Calculate future value using the compound growth formula
    future_value = principal * (1 + interest_rate_decimal) ** years

    return future_value

def calc_future_value_principal(principal, interest_rate, years):
    interest_rate_decimal = interest_rate / 100
    future_value = principal * (1 + interest_rate_decimal) ** years
    return future_value

def calc_future_value_contributions(monthly_contribution, annual_interest_rate, years):
    # Convert annual interest rate to a decimal
    interest_rate_decimal = annual_interest_rate / 100

    # Check if interest_rate_decimal is zero
    if interest_rate_decimal == 0:
        return monthly_contribution * 12 * years

    # Calculate pmt for a year
    pmt = monthly_contribution * 12

    # Calculate the future value using the provided formula
    future_value = pmt * ((1 + interest_rate_decimal) ** years - 1) / interest_rate_decimal

    return future_value

def calc_tax_advantaged_contributions(annual_contribution, interest_rate, years):
    # Convert annual interest rate to a decimal
    interest_rate_decimal = interest_rate / 100

    # Check if interest_rate_decimal is zero
    if interest_rate_decimal == 0:
        return annual_contribution * years

    # Calculate pmt for a year
    pmt = annual_contribution

    # Calculate the future value using the provided formula
    future_value = pmt * ((1 + interest_rate_decimal) ** years - 1) / interest_rate_decimal

    return future_value

def calc_future_value_combined(principal, monthly_contribution, saving_years, interest_rate):
    # Calculate the future value with compounding on the principal
    fv_principal = calc_future_value_principal(principal, interest_rate, saving_years)

    # Calculate the future value contributed by monthly contributions
    fv_monthly = calc_future_value_contributions(monthly_contribution, interest_rate, saving_years)

    # Add the future value of the principal and contributions
    fv_total = fv_principal + fv_monthly

    return fv_principal, fv_monthly, fv_total

def calculate_saving_years(current_age, retirement_age):
    saving_years = retirement_age - current_age
    return saving_years

def calculate_savings_needed(fire_number, total_savings, saving_years):
    # Check if saving_years is zero
    if saving_years == 0:
        st.warning("Warning: The number of saving years is zero. Please adjust your retirement age.")
        return 0, 0

    # Calculate the savings needed
    remaining_savings_needed = fire_number - total_savings

    # Calculate annual and monthly savings needed based on the remaining savings goal
    annual_savings = remaining_savings_needed / saving_years
    monthly_savings = annual_savings / 12

    return annual_savings, monthly_savings, remaining_savings_needed

def calc_401k_ira_hsa_contributions(interest_rate, saving_years):
    # If the user wants to set the max for all three accounts
    set_max = st.checkbox("Do you want to set the max for 401k, IRA, and HSA?")
    employer_match = st.number_input("Enter total annual amount of employer match:", value=0)

    if set_max:
        max_401k = 23000
        max_ira = 7000
        max_hsa = 4150
    else:
        max_401k = st.number_input("Enter the max 401k contribution:", value=0)
        max_ira = st.number_input("Enter the max IRA contribution:", value=0)
        max_hsa = st.number_input("Enter the max HSA contribution:", value=0)

    # Calculate the total future value across all three accounts
    total_401k = calc_tax_advantaged_contributions(max_401k + employer_match, interest_rate, saving_years)
    total_ira = calc_tax_advantaged_contributions(max_ira, interest_rate, saving_years)
    total_hsa = calc_tax_advantaged_contributions(max_hsa, interest_rate, saving_years)

    total_contributions = total_401k + total_ira + total_hsa

    return total_contributions, total_401k, total_ira, total_hsa

def main():
    # Get FIRE Goals
    current_age = int(st.number_input("Enter your current age:", value=0))
    retirement_age = int(st.number_input("Enter your retirement age:", value=0))

    # Get current savings
    current_savings = st.number_input("Enter your current savings:", value=0)

    # Calculate future value with existing monthly contribution
    monthly_contribution = st.number_input("Enter your monthly contribution to taxable accounts:", value=0)

    # Calculate saving years
    saving_years = calculate_saving_years(current_age, retirement_age)

    # Set an interest rate
    interest_rate = st.number_input("Enter interest rate to use for investments:", value=0)

    # Calculate FIRE number
    annual_expenses = st.number_input("Enter your annual expenses:")
    fire_number = calculate_fire_number(annual_expenses)

    # Calculate 401k, IRA, HSA contributions
    total_contributions, total_401k, total_ira, total_hsa = calc_401k_ira_hsa_contributions(interest_rate, saving_years)

    # Calculate current gap based on current savings
    gap = fire_number - current_savings

    # Calculate value total with principal and monthly
    fv_principal, fv_monthly, fv_total = calc_future_value_combined(current_savings, monthly_contribution, saving_years, interest_rate)

    # Calculate savings needed
    total_savings = fv_total + total_contributions
    annual_savings, monthly_savings, remaining_savings_needed = calculate_savings_needed(fire_number, total_savings, saving_years)
    
    # Display Tables
    st.write("\n**FIRE Summary**")
    fire_summary_data = {
        "Summary": ["FIRE Number", "Current Gap", "Years to retirement", "Future Gap"],
        "Result": [f"${fire_number:,.2f}", f"${gap:,.2f}", f"${saving_years:,.2f}",f"${remaining_savings_needed:,.2f}"]
    }
    fire_summary_table = st.table(fire_summary_data)
    
    # Current savings + monthly contributions
    st.write("\n**Future Value of Current Savings + Monthly Contributions**")
    projected_values_data = {
        "Category": ["Current Savings", "Monthly Contributions", "Total"],
        "Projected Value": [f"${fv_principal:,.2f}", f"${fv_monthly:,.2f}", f"${fv_total:,.2f}"]
    }
    projected_values_table = st.table(projected_values_data)

    st.write("\n**Future Value of Tax-Advantaged Accounts**")
    contributions_data = {
        "Account": ["401k", "IRA", "HSA", "Total"],
        "Contributions": [f"${total_401k:,.2f}", f"${total_ira:,.2f}", f"${total_hsa:,.2f}", f"${total_contributions:,.2f}"]
    }
    contributions_table = st.table(contributions_data)

    st.write("\n**Action Needed**")
    st.write(f"   This translates to the following additional amounts to hit your FIRE number over the next {saving_years:,.0f} years.")
    savings_needed_data = {
        "Timeframe": ["Annual", "Monthly"],
        "Savings Needed": [f"${annual_savings:,.2f}", f"${monthly_savings:,.2f}"]
    }
    savings_needed_table = st.table(savings_needed_data)

if __name__ == "__main__":
    main()
