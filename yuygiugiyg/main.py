import datetime
import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
# For the line chart in ReportsScreen using Kivy Garden Graph:
from kivy.garden.graph import Graph, MeshLinePlot

# ---------------------------
# Custom Widgets for Reporting
# ---------------------------

class BarChart(Widget):
    """
    A simple bar chart that draws two bars for income and expense.
    """
    def __init__(self, income, expense, **kwargs):
        super(BarChart, self).__init__(**kwargs)
        self.income = income
        self.expense = expense
        self.bind(pos=self.update_chart, size=self.update_chart)
        self.update_chart()

    def update_chart(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Determine the maximum value to scale the bars.
            max_val = max(self.income, self.expense, 1)
            # Compute widths (we'll use 40% of the widget's width for each bar)
            bar_width = self.width * 0.4
            gap = self.width * 0.2  # gap between bars
            # Calculate heights (relative to widget height)
            income_height = (self.income / max_val) * self.height
            expense_height = (self.expense / max_val) * self.height
            # Draw income bar in green (left)
            Color(0, 1, 0, 1)
            Rectangle(pos=(self.x + gap * 0.5, self.y), size=(bar_width, income_height))
            # Draw expense bar in red (right)
            Color(1, 0, 0, 1)
            Rectangle(pos=(self.x + gap * 1.5 + bar_width, self.y), size=(bar_width, expense_height))
            # Optionally, you might add labels using CoreLabel, but that is beyond this simple example.

class PieChart(Widget):
    """
    A simple pie chart that draws arcs for each category.
    The data_dict should be a dictionary of {category: value}.
    """
    def __init__(self, data_dict, **kwargs):
        super(PieChart, self).__init__(**kwargs)
        self.data_dict = data_dict
        self.bind(pos=self.update_chart, size=self.update_chart)
        self.update_chart()

    def update_chart(self, *args):
        self.canvas.clear()
        total = sum(self.data_dict.values())
        if total == 0:
            return
        start_angle = 0
        # Predefined colors (cycle through them)
        colors = [(1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1), (1,0,1,1), (0,1,1,1)]
        with self.canvas:
            for key, value in self.data_dict.items():
                fraction = value / total
                angle = fraction * 360
                Color(*colors[hash(key) % len(colors)])
                # Draw an ellipse arc for this slice.
                # The PieChart fills its widget's size.
                Ellipse(pos=self.pos, size=self.size, angle_start=start_angle, angle_end=start_angle+angle)
                start_angle += angle

# ---------------------------
# Database Logic using JsonStore
# ---------------------------
class FinanceDatabase:
    def __init__(self):
        self.store = JsonStore("finance.json")
        # Initialize accounts as an empty dict if not exists.
        if not self.store.exists("accounts"):
            self.store.put("accounts", data={})
        if not self.store.exists("shopping_cart"):
            self.store.put("shopping_cart", items=[])
        if not self.store.exists("tags"):
            self.store.put("tags", data=["Salary", "Groceries", "Rent", "Entertainment"])

    # Account methods:
    def get_accounts(self):
        return self.store.get("accounts")["data"]

    def get_balance(self, account):
        accounts = self.get_accounts()
        return accounts.get(account, {}).get("balance", 0)

    def set_balance(self, account, amount):
        accounts = self.get_accounts()
        if account in accounts:
            accounts[account]["balance"] = amount
        else:
            accounts[account] = {"balance": amount, "transactions": [], "password": "", "budget": None}
        self.store.put("accounts", data=accounts)

    def add_transaction(self, account, amount, preset, specs, transaction_type):
        accounts = self.get_accounts()
        if account not in accounts:
            accounts[account] = {"balance": 0, "transactions": [], "password": "", "budget": None}
        current_balance = accounts[account].get("balance", 0)
        if transaction_type == "gain":
            current_balance += amount
        else:
            current_balance -= amount
        accounts[account]["balance"] = current_balance
        now_str = datetime.datetime.now().isoformat()
        accounts[account].setdefault("transactions", []).append({
            "amount": amount,
            "preset": preset,
            "specs": specs,
            "type": transaction_type,
            "date": now_str
        })
        self.store.put("accounts", data=accounts)

    def get_transactions(self, account):
        accounts = self.get_accounts()
        return accounts.get(account, {}).get("transactions", [])

    def add_account(self, account, initial_balance, password):
        accounts = self.get_accounts()
        if account in accounts:
            return False  # account already exists
        accounts[account] = {"balance": initial_balance, "transactions": [], "password": password, "budget": None}
        self.store.put("accounts", data=accounts)
        return True

    def set_accounts(self, accounts):
        self.store.put("accounts", data=accounts)

    def check_password(self, account, password):
        accounts = self.get_accounts()
        if account in accounts:
            return accounts[account].get("password") == password
        return False

    def set_password(self, account, new_password):
        accounts = self.get_accounts()
        if account in accounts:
            accounts[account]["password"] = new_password
            self.store.put("accounts", data=accounts)
            return True
        return False

    def get_budget(self, account):
        accounts = self.get_accounts()
        return accounts.get(account, {}).get("budget", None)

    def set_budget(self, account, budget):
        accounts = self.get_accounts()
        if account in accounts:
            accounts[account]["budget"] = budget
            self.store.put("accounts", data=accounts)
            return True
        return False

    # Shopping cart methods:
    def get_shopping_cart(self):
        return self.store.get("shopping_cart")["items"]

    def add_shopping_item(self, item, cost):
        items = self.get_shopping_cart()
        items.append({
            "item": item,
            "cost": cost,
            "confirmed": False,
            "purchased": False
        })
        self.store.put("shopping_cart", items=items)

    def update_shopping_cart(self, items):
        self.store.put("shopping_cart", items=items)

    # Tag management methods:
    def get_tags(self):
        return self.store.get("tags")["data"]

    def set_tags(self, tags):
        self.store.put("tags", data=tags)

    def add_tag(self, tag):
        tags = self.get_tags()
        if tag not in tags:
            tags.append(tag)
            self.set_tags(tags)

    def delete_tag(self, tag):
        tags = self.get_tags()
        if tag in tags:
            tags.remove(tag)
            self.set_tags(tags)

    def edit_tag(self, old_tag, new_tag):
        tags = self.get_tags()
        for i, t in enumerate(tags):
            if t == old_tag:
                tags[i] = new_tag
        self.set_tags(tags)

# ---------------------------
# UI Screens
# ---------------------------
# Standard Login Screen
class StandardLoginScreen(Screen):
    def login(self):
        account = self.ids.account_input.text
        password = self.ids.password_input.text
        if App.get_running_app().db.check_password(account, password):
            App.get_running_app().current_account = account
            self.manager.current = "home"
        else:
            Popup(title="Error", content=Label(text="Invalid credentials."),
                  size_hint=(None, None), size=(400,200)).open()

# Create Account Screen
class CreateAccountScreen(Screen):
    def create_account(self):
        account = self.ids.new_account_name.text.strip()
        balance_text = self.ids.new_account_balance.text.strip()
        password = self.ids.new_account_password.text.strip()
        if account == "" or balance_text == "" or password == "":
            Popup(title="Error", content=Label(text="Please fill in all fields."),
                  size_hint=(None, None), size=(400,200)).open()
            return
        try:
            initial_balance = float(balance_text)
        except ValueError:
            Popup(title="Error", content=Label(text="Invalid balance."),
                  size_hint=(None, None), size=(400,200)).open()
            return
        if App.get_running_app().db.add_account(account, initial_balance, password):
            App.get_running_app().current_account = account
            self.manager.current = "home"
        else:
            Popup(title="Error", content=Label(text="Account already exists."),
                  size_hint=(None, None), size=(400,200)).open()

# Home Screen with smaller buttons arranged in a GridLayout
class HomeScreen(Screen):
    def on_pre_enter(self):
        account = App.get_running_app().current_account
        balance = App.get_running_app().db.get_balance(account)
        self.ids.balance_label.text = f"Account: {account}\nCurrent Balance: ${balance}"

# Add Transaction Screen
class AddTransactionScreen(Screen):
    selected_preset = ""
    def on_pre_enter(self):
        self.ids.preset_tags_box.clear_widgets()
        tags = App.get_running_app().db.get_tags()
        from kivy.uix.button import Button
        for tag in tags:
            btn = Button(text=tag, size_hint_x=None, width=80)
            btn.bind(on_release=lambda btn, tag=tag: self.set_preset(tag))
            self.ids.preset_tags_box.add_widget(btn)
        edit_btn = Button(text="Edit Tags", size_hint_x=None, width=80)
        edit_btn.bind(on_release=lambda btn: setattr(App.get_running_app().root, "current", "edit_tags"))
        self.ids.preset_tags_box.add_widget(edit_btn)
    def set_preset(self, preset_value):
        self.selected_preset = preset_value
        self.ids.preset_label.text = "Preset: [" + preset_value + "]"
    def save_transaction(self, amount, specs, transaction_type):
        if not amount:
            Popup(title="Error", content=Label(text="Please enter an amount."),
                  size_hint=(None, None), size=(400,200)).open()
            return
        try:
            amount_value = float(amount)
        except ValueError:
            Popup(title="Error", content=Label(text="Invalid amount entered."),
                  size_hint=(None, None), size=(400,200)).open()
            return
        preset = self.selected_preset if self.selected_preset != "" else "None"
        account = App.get_running_app().current_account
        App.get_running_app().db.add_transaction(account, amount_value, preset, specs, transaction_type)
        self.manager.current = "home"

# History Screen (shows transactions with dates)
class HistoryScreen(Screen):
    def on_pre_enter(self):
        self.ids.incomes_container.clear_widgets()
        self.ids.expenses_container.clear_widgets()
        account = App.get_running_app().current_account
        transactions = App.get_running_app().db.get_transactions(account)
        transactions = list(reversed(transactions))
        for t in transactions:
            date_str = t.get("date", "")[:10]
            specs_text = f" ({t['specs']})" if t.get("specs") and t["specs"].strip() != "" else ""
            text = f"{t['type'].capitalize()}: ${t['amount']} [{t['preset']}] on {date_str} {specs_text}"
            if t["type"] == "gain":
                self.ids.incomes_container.add_widget(Label(text=text, size_hint_y=None, height=30))
            else:
                self.ids.expenses_container.add_widget(Label(text=text, size_hint_y=None, height=30))

# Shopping Cart Screen (with checkboxes for planned/confirmed)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox

class ShoppingCartScreen(Screen):
    def add_item(self, item_name, cost_text):
        if not item_name or not cost_text:
            Popup(title="Error", content=Label(text="Please enter both item name and cost."),
                  size_hint=(None, None), size=(400,200)).open()
            return
        try:
            cost = float(cost_text)
        except ValueError:
            Popup(title="Error", content=Label(text="Invalid cost entered."),
                  size_hint=(None, None), size=(400,200)).open()
            return
        App.get_running_app().db.add_shopping_item(item_name, cost)
        self.ids.item_name.text = ""
        self.ids.item_cost.text = ""
        self.load_items()
    def load_items(self):
        self.ids.shopping_items_container.clear_widgets()
        items = App.get_running_app().db.get_shopping_cart()
        total = 0
        for index, i in enumerate(items):
            total += i["cost"]
            status = "Confirmed" if i.get("confirmed", False) else "Planned"
            item_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
            chk = CheckBox(active=i.get("confirmed", False))
            chk.bind(active=lambda chk, value, idx=index: self.update_item_confirmed(idx, value))
            item_label = Label(text=f"{i['item']} - ${i['cost']} [{status}]", size_hint_x=0.8)
            item_box.add_widget(chk)
            item_box.add_widget(item_label)
            self.ids.shopping_items_container.add_widget(item_box)
        self.ids.total_price.text = "Total: $" + str(total)
    def update_item_confirmed(self, index, value):
        items = App.get_running_app().db.get_shopping_cart()
        if index < len(items):
            items[index]["confirmed"] = value
            App.get_running_app().db.update_shopping_cart(items)
            self.load_items()
    def on_pre_enter(self):
        self.load_items()

# Edit Tags Screen (remember to include this class!)
class EditTagsScreen(Screen):
    def load_tags(self):
        self.ids.tags_container.clear_widgets()
        tags = App.get_running_app().db.get_tags()
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        for tag in tags:
            tag_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
            tag_label = Label(text=tag, size_hint_x=0.6)
            edit_button = Button(text="Edit", size_hint_x=0.2)
            delete_button = Button(text="Delete", size_hint_x=0.2)
            edit_button.bind(on_release=lambda btn, tag=tag: self.edit_tag(tag))
            delete_button.bind(on_release=lambda btn, tag=tag: self.delete_tag(tag))
            tag_box.add_widget(tag_label)
            tag_box.add_widget(edit_button)
            tag_box.add_widget(delete_button)
            self.ids.tags_container.add_widget(tag_box)
    def edit_tag(self, tag):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        text_input = TextInput(text=tag, multiline=False)
        save_button = Button(text="Save", size_hint_y=None, height=40)
        content.add_widget(text_input)
        content.add_widget(save_button)
        popup = Popup(title="Edit Tag", content=content, size_hint=(None, None), size=(300,200))
        save_button.bind(on_release=lambda btn: self.save_edited_tag(popup, tag, text_input.text))
        popup.open()
    def save_edited_tag(self, popup, old_tag, new_tag):
        App.get_running_app().db.edit_tag(old_tag, new_tag)
        popup.dismiss()
        self.load_tags()
    def delete_tag(self, tag):
        App.get_running_app().db.delete_tag(tag)
        self.load_tags()
    def add_new_tag(self, tag_text):
        if tag_text.strip() == "":
            return
        App.get_running_app().db.add_tag(tag_text.strip())
        self.ids.new_tag_input.text = ""
        self.load_tags()
    def on_pre_enter(self):
        self.load_tags()

# Settings Screen (for changing password, deleting account, etc.)
class SettingsScreen(Screen):
    def change_password(self):
        new_password = self.ids.new_password_input.text.strip()
        if new_password == "":
            Popup(title="Error", content=Label(text="Please enter a new password."),
                  size_hint=(None, None), size=(400,200)).open()
            return
        account = App.get_running_app().current_account
        App.get_running_app().db.set_password(account, new_password)
        Popup(title="Success", content=Label(text="Password changed successfully."),
              size_hint=(None, None), size=(400,200)).open()
    def delete_account(self):
        account = App.get_running_app().current_account
        confirm = Popup(title="Confirm", content=Label(text="Are you sure you want to delete this account?"),
                        size_hint=(None, None), size=(400,200))
        def confirm_delete(instance):
            accounts = App.get_running_app().db.get_accounts()
            if account in accounts:
                accounts.pop(account)
                App.get_running_app().db.set_accounts(accounts)
                App.get_running_app().current_account = None
                confirm.dismiss()
                self.manager.current = "standard_login"
            else:
                confirm.dismiss()
                Popup(title="Error", content=Label(text="Account not found."),
                      size_hint=(None, None), size=(400,200)).open()
        confirm.bind(on_release=lambda instance: confirm_delete(instance))
        confirm.open()
    def logout(self):
        App.get_running_app().current_account = None
        self.manager.current = "standard_login"

# Budget Screen (separate budgeting section)
class BudgetScreen(Screen):
    def on_pre_enter(self):
        account = App.get_running_app().current_account
        budget = App.get_running_app().db.get_budget(account)
        if budget is None:
            budget = 0
        transactions = App.get_running_app().db.get_transactions(account)
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
        items = App.get_running_app().db.get_shopping_cart()
        confirmed_total = sum(i["cost"] for i in items if i.get("confirmed", False))
        planned_total = sum(i["cost"] for i in items if not i.get("confirmed", False))
        confirmed_expense = total_expense + confirmed_total
        remaining = budget - confirmed_expense
        info = f"Budget Limit: ${budget}\n" \
               f"Expense Transactions: ${total_expense}\n" \
               f"Confirmed Shopping Cart: ${confirmed_total}\n" \
               f"Total Confirmed Expense: ${confirmed_expense}\n" \
               f"Planned (Not Confirmed): ${planned_total}\n" \
               f"Remaining Budget: ${remaining}"
        if remaining < 0:
            info += "\n[Warning: Budget Exceeded!]"
        self.ids.budget_info.text = info
    def set_new_budget(self):
        budget_text = self.ids.new_budget_input.text.strip()
        if budget_text == "":
            Popup(title="Error", content=Label(text="Please enter a budget amount."),
                  size_hint=(None, None), size=(400,200)).open()
            return
        try:
            new_budget = float(budget_text)
        except ValueError:
            Popup(title="Error", content=Label(text="Invalid budget amount."),
                  size_hint=(None, None), size=(400,200)).open()
            return
        account = App.get_running_app().current_account
        App.get_running_app().db.set_budget(account, new_budget)
        Popup(title="Success", content=Label(text="Budget set successfully."),
              size_hint=(None, None), size=(400,200)).open()
        self.on_pre_enter()

# Reports Screen (Reporting and Visualizations using custom BarChart, PieChart, and a line chart)
class ReportsScreen(Screen):
    def generate_report(self):
        start_date_text = self.ids.start_date.text.strip()
        end_date_text = self.ids.end_date.text.strip()
        category_filter = self.ids.category_spinner.text
        if start_date_text == "":
            start_date = datetime.datetime.min
        else:
            try:
                start_date = datetime.datetime.strptime(start_date_text, "%Y-%m-%d")
            except:
                start_date = datetime.datetime.min
        if end_date_text == "":
            end_date = datetime.datetime.max
        else:
            try:
                end_date = datetime.datetime.strptime(end_date_text, "%Y-%m-%d")
            except:
                end_date = datetime.datetime.max
        account = App.get_running_app().current_account
        transactions = App.get_running_app().db.get_transactions(account)
        filtered = []
        for t in transactions:
            if "date" in t:
                t_date = datetime.datetime.fromisoformat(t["date"])
            else:
                continue
            if start_date <= t_date <= end_date:
                if category_filter != "All Categories" and t["preset"] != category_filter:
                    continue
                filtered.append(t)
        # Chart A: Bar chart for Income vs Expense
        income_total = sum(t["amount"] for t in filtered if t["type"] == "gain")
        expense_total = sum(t["amount"] for t in filtered if t["type"] == "expense")
        bar_chart = BarChart(income_total, expense_total, size_hint=(1, None), height=200)
        # Chart B: Pie chart for Expense by Category
        cat_totals = {}
        for t in filtered:
            if t["type"] == "expense":
                cat_totals[t["preset"]] = cat_totals.get(t["preset"], 0) + t["amount"]
        pie_chart = PieChart(cat_totals, size_hint=(1, None), height=200)
        # Chart C: Line chart for daily net expense
        daily_totals = {}
        for t in filtered:
            if "date" in t:
                d = datetime.datetime.fromisoformat(t["date"]).date()
                if t["type"] == "expense":
                    daily_totals[d] = daily_totals.get(d, 0) + t["amount"]
                elif t["type"] == "gain":
                    daily_totals[d] = daily_totals.get(d, 0) - t["amount"]
        dates = sorted(daily_totals.keys())
        totals = [daily_totals[d] for d in dates]
        # Use Graph from kivy.garden.graph for the line chart
        if dates:
            graph = Graph(xlabel='Day', ylabel='Net Expense', x_ticks_minor=1, x_ticks_major=1,
                          y_ticks_major=10, y_grid_label=True, x_grid_label=True, padding=5,
                          x_grid=True, y_grid=True, xmin=0, xmax=len(dates)-1,
                          ymin=min(totals) if totals else 0, ymax=max(totals) if totals else 0, size_hint=(1, None), height=200)
            plot = MeshLinePlot(color=[1, 0, 0, 1])
            plot.points = [(i, totals[i]) for i in range(len(totals))]
            graph.add_plot(plot)
        else:
            graph = Label(text="No data for line chart", size_hint=(1, None), height=200)
        self.ids.reports_grid.clear_widgets()
        self.ids.reports_grid.add_widget(bar_chart)
        self.ids.reports_grid.add_widget(pie_chart)
        self.ids.reports_grid.add_widget(graph)
    def on_pre_enter(self):
        tags = App.get_running_app().db.get_tags()
        self.ids.category_spinner.values = ["All Categories"] + tags
        self.ids.reports_grid.clear_widgets()

# ---------------------------
# The Main App Class
# ---------------------------
class FinanceApp(App):
    def build(self):
        self.db = FinanceDatabase()
        self.current_account = None
        sm = ScreenManager()
        sm.add_widget(StandardLoginScreen(name="standard_login"))
        sm.add_widget(CreateAccountScreen(name="create_account"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(AddTransactionScreen(name="add_transaction"))
        sm.add_widget(HistoryScreen(name="history"))
        sm.add_widget(ShoppingCartScreen(name="shopping_cart"))
        sm.add_widget(EditTagsScreen(name="edit_tags"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(BudgetScreen(name="budget"))
        sm.add_widget(ReportsScreen(name="reports"))
        sm.current = "standard_login"
        return sm
    def logout(self):
        self.current_account = None
        self.root.current = "standard_login"

if __name__ == "__main__":
    FinanceApp().run()
