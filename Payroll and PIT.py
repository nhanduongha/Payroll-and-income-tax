# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:18:18 2022

@author: Nhan Duong
"""

import pandas as pd
import math
import locale as lc
print(lc.getpreferredencoding())

SALARY_FOR_INSURANCE = 24200000
DEDUCTION_DEPENDENT = 4400000
DEDUCTION_TAX_PAYER = 11000000

df = pd.read_csv('Data.csv')
names = []
monthly_gross_salaries = []
total_deductions = []
taxable_incomes = []
PITs = []
monthly_net_salaries = []

for row in df.index[:-1]:
    name = df.at[row, "Name"]
    monthly_gross_salary = df.at[row, 'Monthly Gross Salary']
    names.append(name)
    monthly_gross_salaries.append(monthly_gross_salary)
    
    if monthly_gross_salary > SALARY_FOR_INSURANCE:
        social_insurance = 0.08 * SALARY_FOR_INSURANCE
        health_insurance = 0.015 * SALARY_FOR_INSURANCE
        unemployment_insurance = 0.01 * SALARY_FOR_INSURANCE
    else:
            social_insurance = monthly_gross_salary * 0.08
            health_insurance = monthly_gross_salary * 0.015
            unemployment_insurance = monthly_gross_salary * 0.01
                
    Number_of_dependents = df.at[row, 'Number of dependents']
    deduction_dependents = Number_of_dependents * DEDUCTION_DEPENDENT
    
    telephone_allowance = df.at[row, 'Telephone allowance']
    stationery_allowance = df.at[row, 'Stationery allowance']
    clothes_allowance = df.at[row, 'Clothes allowance']
    meal_allowance = df.at[row, 'Meal allowance']
    business_trip_allowance = df.at[row, 'Business trip allowance']
    
    total_deduction = social_insurance + health_insurance + unemployment_insurance\
         + deduction_dependents + DEDUCTION_TAX_PAYER + telephone_allowance \
             + stationery_allowance + clothes_allowance + meal_allowance \
                 + business_trip_allowance
    total_deductions.append(total_deduction)
    
    taxable_income = monthly_gross_salary - total_deduction
    if taxable_income < 0:
        taxable_income = 0
    taxable_incomes.append(taxable_income)
        
    def income_tax(taxable_income):
        tax = 0
        if taxable_income <= 5000000:
            tax += taxable_income * 0.05
        elif taxable_income <= 10000000:
            tax += taxable_income * 0.1 - 250000
        elif taxable_income <= 18000000:
            tax += taxable_income * 0.15 - 750000
        elif taxable_income <= 32000000:
            tax += taxable_income * 0.2 - 1650000
        elif taxable_income <= 52000000:
            tax += taxable_income * 0.25 - 3250000
        elif taxable_income <= 80000000:
            tax += taxable_income * 0.3 - 5850000
        elif taxable_income > 80000000:
            tax += taxable_income * 0.35 - 9850000
        return tax

    PIT = income_tax(taxable_income)
    PITs.append(PIT)
    
    monthly_net_salary = monthly_gross_salary - (social_insurance +\
                           health_insurance + unemployment_insurance) - PIT
    monthly_net_salaries.append(monthly_net_salary)
    
result = pd.DataFrame(
    {'Name': names,
     'Monthly gross salary': [(math.floor(mgs * 100) / 100) for mgs in monthly_gross_salaries],
     'Total deduction': [(math.floor(td * 100) / 100) for td in total_deductions],
     'Taxable income': [(math.floor(ti * 100) / 100) for ti in taxable_incomes],
     'PIT': [(math.floor(pit * 100) / 100) for pit in PITs],
     'Monthly net salary': [(math.floor(mns * 100) / 100) for mns in monthly_net_salaries]
     })

result.to_csv('Results.csv', encoding='utf-8-sig')


                                      