import streamlit as st
import pandas as pd

def calculate_fire_number(annual_expenses):
    return annual_expenses * 25

def calculate_future_value(monthly_savings, years):
    months = years * 12
    return monthly_savings * months

def calculate_future_value_compound_growth(principal, interest_rate, years):
    interest_rate_decimal = interest_rate / 100
    future_value = principal * (1 + interest_rate_decimal) ** years
    return future_value

def calc_future_value_principal(principal, interest_rate, years):
    interest_rate_decimal = interest_rate / 100
    future_value = principal * (1 + interest_rate_decimal) ** years
    return future_value

def calc_future_value_contributions(monthly_contribution, annual_interest_rate, years):
    interest_rate_decimal = annual_interest_rate / 100

    if interest_rate_decimal == 0:
        return monthly_contribution * 12 * years

    pmt = monthly_contribution * 12
    future_value = pmt * ((1 + interest_rate_decimal) ** years - 1) / interest_rate_decimal
    return future_value

def calc_tax_advantaged_contributions(annual_contribution, interest_rate, years):
    interest_rate_decimal = interest_rate / 100

    if interest_rate_decimal == 0:
        return annual_contribution * years

    pmt = annual_contribution
    future_value = pmt * ((1 + interest_rate_decimal) ** years - 1) / interest_rate_decimal
    return future_value

def calc_future_value_combined(principal, monthly_contribution, saving_years, interest_rate):
    fv_principal = calc_future_value_principal(principal, interest_rate, saving_years)
    fv_monthly = calc_future_value_contributions(monthly_contribution, interest_rate, saving_years)
    fv_total = fv_principal + fv_monthly
    return fv_principal, fv_monthly, fv_total

def calculate_saving_years(current_age, retirement_age):
    return retirement_age - current_age

def calculate_savings_needed(fire_number, total_savings, saving_years):
    if saving_years == 0:
        st.warning("Warning: The number of saving years is zero. Please adjust your retirement age.")
        return 0, 0, 0  # Add a placeholder value for the third variable

    remaining_savings_needed = fire_number - total_savings
    annual_savings = remaining_savings_needed / saving_years
    monthly_savings = annual_savings / 12

    return annual_savings, monthly_savings, remaining_savings_needed

def calc_401k_ira_hsa_contributions(interest_rate, saving_years):
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

    total_401k = calc_tax_advantaged_contributions(max_401k + employer_match, interest_rate, saving_years)
    total_ira = calc_tax_advantaged_contributions(max_ira, interest_rate, saving_years)
    total_hsa = calc_tax_advantaged_contributions(max_hsa, interest_rate, saving_years)

    total_contributions = total_401k + total_ira + total_hsa

    return total_contributions, total_401k, total_ira, total_hsa, employer_match

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
    total_contributions, total_401k, total_ira, total_hsa, employer_match = calc_401k_ira_hsa_contributions(interest_rate, saving_years)

    # Calculate current gap based on current savings
    gap = fire_number - current_savings

    # Calculate value total with principal and monthly
    fv_principal, fv_monthly, fv_total = calc_future_value_combined(current_savings, monthly_contribution, saving_years, interest_rate)

    # Calculate savings needed
    total_savings = fv_total + total_contributions
    annual_savings, monthly_savings, remaining_savings_needed = calculate_savings_needed(fire_number, total_savings, saving_years)
    
    # Display FIRE Summary Line Chart
    st.write("\n**FIRE Summary**")
    
    # Create a dataframe for the line chart data
    fire_line_chart_data = {
        'Year': [str(year) for year in range(2023, 2023 + int(saving_years) + 1)],
        'FIRE Number': [fire_number] * int(saving_years + 1),
        'Remaining Savings Needed': [remaining_savings_needed] * int(saving_years + 1),
    }

    # Create the dataframe for the line chart
    fire_line_chart_df = pd.DataFrame(fire_line_chart_data)

    # Plotting
    st.line_chart(fire_line_chart_df.set_index('Year'))

    # Display Contributions Table
    st.write("\n**Contributions Summary**")

    # Create a dataframe for the contributions table
    contributions_table_data = {
        'Year': [str(year) for year in range(2023, 2023 + int(saving_years) + 1)],
        'Principal': [fv_principal] * int(saving_years + 1),
        'Monthly Contributions': [fv_monthly] * int(saving_years + 1),
        '401k': [total_401k] * int(saving_years + 1),
        '401k Employer Contributions': [employer_match] * int(saving_years + 1),
        'IRA': [total_ira] * int(saving_years + 1),
        'HSA': [total_hsa] * int(saving_years + 1),
        'Total': [total_contributions] * int(saving_years + 1),
    }

    # Create the dataframe for the contributions table
    contributions_table_df = pd.DataFrame(contributions_table_data)

    # Display the contributions table
    st.table(contributions_table_df)

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
