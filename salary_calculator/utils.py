TAX_RATES = [
    {"threshold": 2_400_000, "rate": 0.13},
    {"threshold": 5_000_000, "rate": 0.15},
    {"threshold": 20_000_000, "rate": 0.18},
    {"threshold": 50_000_000, "rate": 0.20},
    {"threshold": float("inf"), "rate": 0.22}
]

RKSN_TAX_RATES = [
    {"threshold": 5_000_000, "rate": 0.13},
    {"threshold": float("inf"), "rate": 0.15}
]

def calculate_tax(income, is_rksn=False):
    tax_rates = RKSN_TAX_RATES if is_rksn else TAX_RATES
    tax = 0
    rate_details = []
    remaining_income = income

    for i, bracket in enumerate(tax_rates):
        if remaining_income <= 0:
            break
        prev_threshold = tax_rates[i-1]["threshold"] if i > 0 else 0
        taxable_in_bracket = min(remaining_income, bracket["threshold"] - prev_threshold)
        if taxable_in_bracket > 0:
            tax += taxable_in_bracket * bracket["rate"]
            rate_details.append((bracket["rate"], taxable_in_bracket))
        remaining_income -= taxable_in_bracket

    return round(tax), rate_details

def format_number(n):
    return f"{n:,}".replace(",", " ")

def format_rate_details(regular_details, rksn_details):
    details = []
    for rate, amount in regular_details:
        if amount > 0:
            details.append(f"{int(rate * 100)}% на {format_number(round(amount))} руб.")
    for rate, amount in rksn_details:
        if amount > 0:
            details.append(f"{int(rate * 100)}% на {format_number(round(amount))} руб. (РК/СН)")
    return " + ".join(details) if details else "0% на 0 руб."

def validate_input(data):
    errors = []
    try:
        salary = float(data.get("salary", 0))
        if salary <= 0:
            errors.append("Оклад должен быть больше 0.")
    except (ValueError, TypeError):
        errors.append("Оклад должен быть числом.")

    try:
        monthly_bonus = float(data.get("monthly_bonus", 0)) if data.get("monthly_bonus") else 0
        if monthly_bonus < 0:
            errors.append("Ежемесячная премия не может быть отрицательной.")
    except (ValueError, TypeError):
        errors.append("Ежемесячная премия должна быть числом или пустой.")

    try:
        rk_rate = float(data.get("rk_rate", 1.0))
        if rk_rate < 1.0:
            errors.append("Районный коэффициент должен быть не менее 1.0.")
    except (ValueError, TypeError):
        errors.append("Районный коэффициент должен быть числом.")

    try:
        sn_percentage = float(data.get("sn_percentage", 0))
        if sn_percentage < 0:
            errors.append("Северная надбавка не может быть отрицательной.")
    except (ValueError, TypeError):
        errors.append("Северная надбавка должна быть числом.")

    if data.get("kpi_enabled") == "on":
        try:
            kpi_percentage = float(data.get("kpi_percentage") or 0)
            if kpi_percentage < 0:
                errors.append("Процент премии KPI не может быть отрицательным.")
        except (ValueError, TypeError):
            errors.append("Процент премии KPI должен быть числом.")
        
        kpi_period = data.get("kpi_period", "quarter")
        if kpi_period not in ["quarter", "halfyear"]:
            errors.append("Недопустимый период KPI.")

    return errors

def calculate_salary(salary, monthly_bonus, kpi_enabled, kpi_percentage, kpi_period, rk_rate, sn_percentage):
    months = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    results = []
    cumulative_income = 0
    cumulative_rksn_income = 0
    annual_income = 0
    annual_tax = 0
    annual_net_income = 0

    base_monthly_income = salary + (monthly_bonus or 0)
    rk_amount = base_monthly_income * (rk_rate - 1) if rk_rate > 1 else 0
    sn_amount = base_monthly_income * (sn_percentage / 100) if sn_percentage > 0 else 0
    rksn_monthly = rk_amount + sn_amount
    taxable_monthly = base_monthly_income + rksn_monthly

    kpi_payments = {}
    kpi_rksn_payments = {}
    kpi_notes = {}

    if kpi_enabled and kpi_percentage > 0:
        monthly_total_income = taxable_monthly
        kpi_percentage_decimal = kpi_percentage / 100
        
        if kpi_period == "quarter":
            periods = [(0, 2, 2, 2), (3, 5, 5, 5), (6, 8, 8, 8), (9, 11, 11, 11)]
        else:
            periods = [(0, 5, 7, 8), (6, 11, 1, 2)]

        for start, end, pay_month, rksn_month in periods:
            period_income = monthly_total_income * (end - start + 1)
            kpi_total = period_income * kpi_percentage_decimal
            rksn_part = kpi_total * (rksn_monthly / monthly_total_income) if monthly_total_income > 0 else 0
            kpi_payments[pay_month] = kpi_total - rksn_part
            kpi_rksn_payments[rksn_month] = rksn_part
            kpi_notes[rksn_month] = "РК/СН"

    for i, month in enumerate(months):
        monthly_income = taxable_monthly
        kpi_bonus = kpi_payments.get(i, 0)
        kpi_rksn_payment = kpi_rksn_payments.get(i, 0)
        total_income = monthly_income + kpi_bonus + kpi_rksn_payment

        rksn_income = rksn_monthly + kpi_rksn_payment
        regular_income = total_income - rksn_income

        cumulative_income += regular_income
        cumulative_rksn_income += rksn_income

        regular_tax, regular_details = calculate_tax(cumulative_income)
        rksn_tax, rksn_details = calculate_tax(cumulative_rksn_income, is_rksn=True)

        prev_reg_tax, prev_reg_det = calculate_tax(cumulative_income - regular_income) if cumulative_income > regular_income else (0, [])
        prev_rksn_tax, prev_rksn_det = calculate_tax(cumulative_rksn_income - rksn_income, is_rksn=True) if cumulative_rksn_income > rksn_income else (0, [])

        monthly_reg_tax = regular_tax - prev_reg_tax
        monthly_rksn_tax = rksn_tax - prev_rksn_tax
        total_tax = monthly_reg_tax + monthly_rksn_tax

        monthly_reg_details = []
        monthly_rksn_details = []

        if regular_income > 0:
            for rate, amount in regular_details:
                prev = sum(p_amt for r, p_amt in prev_reg_det if r == rate)
                delta = max(0, amount - prev)
                if delta > 0:
                    monthly_reg_details.append((rate, min(delta, regular_income)))

        if rksn_income > 0:
            for rate, amount in rksn_details:
                prev = sum(p_amt for r, p_amt in prev_rksn_det if r == rate)
                delta = max(0, amount - prev)
                if delta > 0:
                    monthly_rksn_details.append((rate, min(delta, rksn_income)))

        rate_details = format_rate_details(monthly_reg_details, monthly_rksn_details)

        annual_income += total_income
        annual_tax += total_tax
        annual_net_income += total_income - total_tax

        results.append({
            "month": month,
            "income": format_number(round(total_income)),
            "kpi_bonus": format_number(round(kpi_bonus + kpi_rksn_payment)),
            "kpi_note": kpi_notes.get(i, ""),
            "tax": format_number(round(total_tax)),
            "net_income": format_number(round(total_income - total_tax)),
            "rate_details": rate_details,
            "cumulative_income": format_number(round(cumulative_income + cumulative_rksn_income))
        })

    return results, {
        "annual_income": format_number(round(annual_income)),
        "annual_tax": format_number(round(annual_tax)),
        "annual_net_income": format_number(round(annual_net_income))
    }