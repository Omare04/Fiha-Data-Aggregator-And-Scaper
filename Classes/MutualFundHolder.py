class MutualFundHolder:
    def __init__(self, fund_name, shares, percentage, value, fund_manager):
        self.fund_name = fund_name
        self.shares = shares
        self.percentage = percentage
        self.value = value
        self.fund_manager = fund_manager

    def update_holdings(self, shares, percentage, value):
        self.shares = shares
        self.percentage = percentage
        self.value = value

    def display_info(self):
        print(f"Fund Name: {self.fund_name}")
        print(f"Shares: {self.shares}")
        print(f"Ownership Percentage: {self.percentage:.2f}%")
        print(f"Value: ${self.value:,.2f}")
        print(f"Fund Manager: {self.fund_manager}")

