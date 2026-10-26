"""engine.py: Серверное ядро финансовых расчетов и стресс-тестирования."""

from dataclasses import dataclass
from typing import Any, Dict, List
import numpy as np


@dataclass
class ModelParams:
    start_month: int = 9  # Октябрь
    start_year: int = 2026
    period: int = 12
    vat_rate: float = 22.0
    margin_pct: float = 20.0
    initial_purchase: float = 25_000_000.0
    batch_cycle: int = 5
    cb_rate: float = 17.0
    comm_margin: float = 2.0
    aov: float = 150_000.0
    start_orders: int = 40
    growth_mode: str = "abs"  # 'abs' или 'pct'
    growth_val: float = 5.0
    max_orders_cap: int = 300
    fot: float = 500_000.0
    wh: float = 200_000.0
    office: float = 150_000.0
    prepayment_pct: float = 50.0
    factoring_share: float = 50.0
    scenario: str = "base"  # 'base', 'optimistic', 'stress'


def calculate_financial_model(params: ModelParams) -> Dict[str, Any]:
    # Корректировка параметров под сценарии
    growth_mult = 1.0
    cb_mult = 1.0
    if params.scenario == "optimistic":
        growth_mult = 1.3
        cb_mult = 0.9
    elif params.scenario == "stress":
        growth_mult = 0.6
        cb_mult = 1.25

    period = params.period
    vat_mult = 1.0 + (params.vat_rate / 100.0)
    cogs_pct = 1.0 - (params.margin_pct / 100.0)
    total_rate_annual = (params.cb_rate + params.comm_margin) * cb_mult
    monthly_rate = (total_rate_annual / 100.0) / 12.0

    short_months = [
        "Янв",
        "Фев",
        "Мар",
        "Апр",
        "Май",
        "Июн",
        "Июл",
        "Авг",
        "Сен",
        "Окт",
        "Ноя",
        "Дек",
    ]
    x_labels = []
    orders = []
    rev = []

    cur_orders = float(params.start_orders)
    effective_growth = params.growth_val * growth_mult

    for i in range(period):
        m_idx = (params.start_month + i) % 12
        y_off = (params.start_month + i) // 12
        x_labels.append(f"{short_months[m_idx]} {params.start_year + y_off}")

        if i > 0:
            if params.growth_mode == "abs":
                cur_orders += effective_growth
            else:
                cur_orders *= 1.0 + (effective_growth / 100.0)

        cur_orders_clamped = min(cur_orders, float(params.max_orders_cap))
        orders.append(int(round(cur_orders_clamped)))
        rev.append(cur_orders_clamped * params.aov)

    # Себестоимость и партии
    cogs_vat = [r * cogs_pct * vat_mult for r in rev]
    cogs_payments = [0.0] * period
    inventory_deliveries = [0.0] * period

    # Первая партия
    cogs_payments[0] += params.initial_purchase * (
        params.prepayment_pct / 100.0
    )
    if period > 1:
        cogs_payments[1] += params.initial_purchase * (
            (100.0 - params.prepayment_pct) / 100.0
        )
    inventory_deliveries[0] = params.initial_purchase

    # Последующие дискретные циклы
    for b in range(params.batch_cycle, period, params.batch_cycle):
        b_end = min(b + params.batch_cycle, period)
        batch_total = sum(cogs_vat[b:b_end])
        inventory_deliveries[b] = batch_total
        cogs_payments[b] += batch_total * (params.prepayment_pct / 100.0)
        if b + 1 < period:
            cogs_payments[b + 1] += batch_total * (
                (100.0 - params.prepayment_pct) / 100.0
            )

    # Остатки склада
    inventory_balance = []
    cur_stock = 0.0
    for i in range(period):
        cur_stock += inventory_deliveries[i] - cogs_vat[i]
        inventory_balance.append(max(cur_stock, 0.0))

    # Денежные притоки (факторинг + отсрочка)
    inflows = [0.0] * period
    fact_advance = 0.80
    fact_share = params.factoring_share / 100.0

    for i in range(period):
        inv_vat = rev[i] * vat_mult
        inflows[i] += inv_vat * fact_share * fact_advance
        target_m = i + 2
        if target_m < period:
            inflows[target_m] += inv_vat * (1.0 - fact_share)
            inflows[target_m] += inv_vat * fact_share * (1.0 - fact_advance)

    # Затраты OPEX и налоги
    base_fixed = 150_000.0 + params.wh + params.office + params.fot
    opex = [
        base_fixed * 1.2 if i >= 6 else base_fixed for i in range(period)
    ]
    taxes = [r * 0.05 for r in rev]  # УСН Доходы 5% / базовая ставка
    base_outflows = [
        cogs_payments[i] + opex[i] + taxes[i] for i in range(period)
    ]

    # Моделирование кредитного плеча, дефицита и обслуживания долга
    monthly_injections = [0.0] * period
    interest_payments = [0.0] * period
    debt_repayments = [0.0] * period
    debt_balance = [0.0] * period
    cash_balance = [0.0] * period

    current_debt = 0.0
    current_cash = 0.0
    first_gap_month = None

    for i in range(period):
        interest_due = current_debt * monthly_rate
        interest_payments[i] = interest_due
        net_before_fin = inflows[i] - (base_outflows[i] + interest_due)
        pot_cash = current_cash + net_before_fin

        if pot_cash < 0:
            deficit = abs(pot_cash)
            monthly_injections[i] = deficit
            current_debt += deficit
            current_cash = 0.0
            debt_repayments[i] = 0.0
            if first_gap_month is None and deficit > 1000:
                first_gap_month = x_labels[i]
        else:
            monthly_injections[i] = 0.0
            repay = min(pot_cash, current_debt)
            debt_repayments[i] = repay
            current_debt -= repay
            current_cash = pot_cash - repay

        debt_balance[i] = current_debt
        cash_balance[i] = current_cash

    sum_rev = float(sum(rev))
    sum_investments = float(sum(monthly_injections))
    sum_interest = float(sum(interest_payments))
    max_debt = float(max(debt_balance)) if debt_balance else 0.0
    sum_opex = float(sum(opex))
    sum_taxes = float(sum(taxes))
    net_profit = (
        sum_rev * (params.margin_pct / 100.0)
        - sum_opex
        - sum_taxes
        - sum_interest
    )
    roi = (net_profit / sum_rev * 100.0) if sum_rev > 0 else 0.0

    return {
        "x_labels": x_labels,
        "revenue": [round(x) for x in rev],
        "orders": orders,
        "monthly_injections": [round(x) for x in monthly_injections],
        "interest_payments": [round(x) for x in interest_payments],
        "debt_repayments": [round(x) for x in debt_repayments],
        "debt_balance": [round(x) for x in debt_balance],
        "cash_balance": [round(x) for x in cash_balance],
        "inventory_balance": [round(x) for x in inventory_balance],
        "cogs_payments": [round(x) for x in cogs_payments],
        "inflows": [round(x) for x in inflows],
        "outflows": [
            round(base_outflows[i] + interest_payments[i])
            for i in range(period)
        ],
        "kpi": {
            "sum_rev": round(sum_rev),
            "sum_injections": round(sum_investments),
            "sum_interest": round(sum_interest),
            "max_debt": round(max_debt),
            "net_profit": round(net_profit),
            "roi": round(roi, 1),
            "first_gap_month": first_gap_month or "Отсутствует",
            "total_rate_annual": round(total_rate_annual, 1),
        },
        "pie": {
            "wh": round(params.wh * period),
            "office": round(params.office * period),
            "fot": round(params.fot * period),
            "taxes": round(sum_taxes),
            "purchases": round(sum(cogs_payments)),
            "interest": round(sum_interest),
        },
    }
