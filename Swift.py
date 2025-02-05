from datetime import datetime

class MT101Message:
    def __init__(self, sender, receiver, reference, date, currency, amount, debtor, creditor, intermediary=None):
        self.sender = sender
        self.receiver = receiver
        self.reference = reference
        self.date = date
        self.currency = currency
        self.amount = amount
        self.debtor = debtor
        self.creditor = creditor
        self.intermediary = intermediary

    def generate_message(self):
        mt101 = f"""
        {1:F01{self.sender}XXXX0000000000}{2:I101{self.receiver}XXXXN}{4:
        :20:{self.reference}
        :25:{self.debtor['account']}
        :28D:1/1
        :50K:{self.debtor['name']}
        :52A:{self.intermediary if self.intermediary else ''}
        :57A:{self.creditor['bic']}
        :59:/{self.creditor['account']}
        {self.creditor['name']}
        :70:/RFB/{self.reference}/
        :71A:SHA
        :32B:{self.currency}{self.amount}
        :33B:USD{self.amount if self.currency == 'USD' else '0.00'}
        :71F:/BEN/{self.amount * 0.01}
        -}
        """
        return mt101.strip()

# Sample data
sender = "BANKUS33"
receiver = "BANKGB22"
reference = "REFERENCE123"
date = datetime.now().strftime("%y%m%d")
currency = "USD"
amount = 1000.00
debtor = {"name": "John Doe", "account": "123456789"}
creditor = {"name": "Jane Smith", "account": "987654321", "bic": "BANKGB22"}
intermediary = "INTERBANKXX"

# Domestic Transfer in USD
domestic_transfer = MT101Message(sender, receiver, reference, date, currency, amount, debtor, creditor)
print("Domestic Transfer in USD:")
print(domestic_transfer.generate_message())

# International Transfer in USD
international_transfer = MT101Message(sender, receiver, reference, date, currency, amount, debtor, creditor)
print("\nInternational Transfer in USD:")
print(international_transfer.generate_message())

# International Transfer with Intermediary Bank
international_transfer_with_intermediary = MT101Message(sender, receiver, reference, date, currency, amount, debtor, creditor, intermediary)
print("\nInternational Transfer with Intermediary Bank:")
print(international_transfer_with_intermediary.generate_message())
