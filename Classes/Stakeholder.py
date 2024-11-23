class Stakeholder:
    def __init__(self, name, shares, percentage, value):
        """
        Initialize a Stakeholder object.

        :param name: str - The name of the stakeholder.
        :param shares: int - The number of shares owned by the stakeholder.
        :param percentage: float - The percentage of ownership.
        :param value: float - The monetary value of the shares.
        """
        self.name = name
        self.shares = shares
        self.percentage = percentage
        self.value = value

    def update_holdings(self, shares, percentage, value):
        """
        Update the stakeholder's holdings.

        :param shares: int - New number of shares.
        :param percentage: float - New percentage of ownership.
        :param value: float - New monetary value of shares.
        """
        self.shares = shares
        self.percentage = percentage
        self.value = value

    def display_info(self):
        """
        Display the stakeholder's details in a readable format.
        """
        print(f"Name: {self.name}")
        print(f"Shares: {self.shares}")
        print(f"Ownership Percentage: {self.percentage:.2f}%")
        print(f"Value: ${self.value:,.2f}")
