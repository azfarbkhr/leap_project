from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    accounting_nature = models.CharField(max_length=20, choices=[
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('income', 'Income'),
        ('expense', 'Expense'),
    ])

    type = models.CharField(max_length=20, choices=[
        ('bank_account', 'Bank Account'),
        ('payables_account', 'Payables Account'),
        ('fixed_assets', 'Fixed Assets'),
        
    ],blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.accounting_nature}"

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    is_supplier = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_debtor = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    reference_number = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_as_account')
    payment_method = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_as_payment_method')
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Transaction on {self.date}: {self.description} - {self.amount}"

class BudgetingPeriod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.start_date} - {self.end_date}: {self.description}"

class BudgetingAmount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    budget_period = models.ForeignKey(BudgetingPeriod, on_delete=models.CASCADE)
    target_definition = models.CharField(max_length=20, choices=[
        ('at_least', 'At least'),
        ('less_than', 'Less than'),
        ('exactly', 'Exactly'),
        ('any_value', 'Any value'),
    ], default='at_least')
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.account}: {self.target_definition} - {self.target_amount}"