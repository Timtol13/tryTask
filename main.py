import pandas as pd
import json

with open("tryData.json", "r", encoding='utf-8') as file:
    data = json.load(file)

# Задача 1: Найти тариф стоимости доставки для каждого склада
def find_warehouse_costs(data):
    warehouse_costs = {}
    for item in data:
        warehouse_name = item["warehouse_name"]
        highway_cost = item["highway_cost"]
        warehouse_costs[warehouse_name] = highway_cost
    return warehouse_costs

# Задача 2: Найти суммарное количество, суммарный доход, суммарный расход и суммарную прибыль для каждого товара
def calculate_product_stats(data):
    product_stats = {}
    for item in data:
        products = item["products"]
        for product in products:
            product_name = product["product"]
            price = product["price"]
            quantity = product["quantity"]
            income = price * quantity
            expenses = item["highway_cost"] * quantity
            profit = income - expenses
            if product_name not in product_stats:
                product_stats[product_name] = {
                    "quantity": quantity,
                    "income": income,
                    "expenses": expenses,
                    "profit": profit,
                }
            else:
                product_stats[product_name]["quantity"] += quantity
                product_stats[product_name]["income"] += income
                product_stats[product_name]["expenses"] += expenses
                product_stats[product_name]["profit"] += profit
    return product_stats

# Задача 3: Составить табличку со столбцами 'order_id' (id заказа) и 'order_profit' (прибыль полученная с заказа)
def calculate_order_profit(data):
    order_profits = {}
    for item in data:
        order_id = item["order_id"]
        order_profit = sum(product["price"] * product["quantity"] for product in item["products"]) + item["highway_cost"]
        order_profits[order_id] = order_profit
    return order_profits

# Задача 4: Составить табличку типа 'warehouse_name', 'product', 'quantity', 'profit', 'percent_profit_product_of_warehouse'
def calculate_product_warehouse_stats(data):
    product_warehouse_stats = []
    for item in data:
        warehouse_name = item["warehouse_name"]
        highway_cost = item["highway_cost"]
        for product in item["products"]:
            product_name = product["product"]
            price = product["price"]
            quantity = product["quantity"]
            income = price * quantity
            expenses = highway_cost * quantity
            profit = income - expenses
            percent_profit_product_of_warehouse = (profit / income) * 100 if income > 0 else 0
            product_warehouse_stats.append({
                "warehouse_name": warehouse_name,
                "product": product_name,
                "quantity": quantity,
                "profit": profit,
                "percent_profit_product_of_warehouse": percent_profit_product_of_warehouse,
            })
    return product_warehouse_stats

# Задача 5: Сортировать 'percent_profit_product_of_warehouse' по убыванию, после посчитать накопленный процент
def calculate_accumulated_percent_profit(data):
    product_warehouse_stats = calculate_product_warehouse_stats(data)
    df = pd.DataFrame(product_warehouse_stats)
    df_sorted = df.sort_values(by="percent_profit_product_of_warehouse", ascending=False)
    df_sorted["accumulated_percent_profit_product_of_warehouse"] = df_sorted["percent_profit_product_of_warehouse"].cumsum()
    return df_sorted

# Задача 6: Присвоить A,B,C - категории на основании значения накопленного процента
def categorize_accumulated_percent(df_sorted):
    def categorize(percent):
        if percent <= 70:
            return "A"
        elif 70 < percent <= 90:
            return "B"
        else:
            return "C"
    
    df_sorted["category"] = df_sorted["accumulated_percent_profit_product_of_warehouse"].apply(categorize)
    return df_sorted

if __name__ == "__main__":
    warehouse_costs = find_warehouse_costs(data)
    print("Задача 1:")
    for warehouse, cost in warehouse_costs.items():
        print(f"{warehouse}: {cost}")

    product_stats = calculate_product_stats(data)
    print("\nЗадача 2:")
    print("product | quantity | income | expenses | profit")
    for product, stats in product_stats.items():
        print(f"{product} | {stats['quantity']} | {stats['income']} | {stats['expenses']} | {stats['profit']}")

    order_profits = calculate_order_profit(data)
    print("\nЗадача 3:")
    print("order_id | order_profit")
    for order_id, profit in order_profits.items():
        print(f"{order_id} | {profit}")

    product_warehouse_stats = calculate_product_warehouse_stats(data)
    df_stats = pd.DataFrame(product_warehouse_stats)
    print("\nЗадача 4:")
    print(df_stats)

    df_sorted = calculate_accumulated_percent_profit(data)
    print("\nЗадача 5:")
    print(df_sorted)

    df_categorized = categorize_accumulated_percent(df_sorted)
    print("\nЗадача 6:")
    print(df_categorized)