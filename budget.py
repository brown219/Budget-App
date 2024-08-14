class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        total = 0
        for item in self.ledger:
            total += item["amount"]
        return total

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        for item in self.ledger:
            amount = f"{item['amount']:.2f}"
            items += f"{item['description'][:23]:23}" + f"{amount:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total
def create_spend_chart(categories):
    # Calculate total spent in each category
    total_spent = 0
    category_spent = []
    for category in categories:
        spent = sum(-item['amount'] for item in category.ledger if item['amount'] < 0)
        category_spent.append(spent)
        total_spent += spent

    # Calculate percentage spent
    spent_percentage = [(spent / total_spent) * 100 for spent in category_spent]

    # Create chart
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}| "
        for percent in spent_percentage:
            if percent >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    # Bottom line of the chart
    chart += "    -" + "---" * len(categories) + "\n"

    # Get category names
    max_len = max(len(category.name) for category in categories)
    category_names = [category.name.ljust(max_len) for category in categories]

    # Add category names vertically
    for i in range(max_len):
        chart += "     "
        for name in category_names:
            chart += name[i] + "  "
        chart += "\n"

    return chart.rstrip("\n")
food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(food)
print(clothing)
print(auto)
print(create_spend_chart([food, clothing, auto]))

# # *************Food*************
# initial deposit        1000.00
# groceries               -10.15
# restaurant and more foo -15.89
# Transfer to Clothing    -50.00
# Total: 923.96
# ***********Clothing***********
# Transfer from Food        50.00
#                         -25.55
#                         -100.00
# Total: -75.55
# ************Auto*************
# initial deposit        1000.00
#                         -15.00
# Total: 985.00
# Percentage spent by category
# 100|          
#  90|          
#  80|          
#  70|          
#  60|          
#  50|          
#  40|    o     
#  30|    o     
#  20|    o  o  
#  10| o  o  o  
#   0| o  o  o  
#     ----------
#      F  C  A  
#      o  l  u  
#      o  o  t  
#      d  t  o  
#         h     
#         i     
#         n     
#         g     
