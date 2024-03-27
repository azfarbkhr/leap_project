from django.contrib import admin
from .models import Account, Contact, Transaction, BudgetingPeriod, BudgetingAmount

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'accounting_nature', 'type')
    search_fields = ('name', 'description')
    list_filter = ('accounting_nature', 'type')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'is_supplier', 'is_customer', 'is_employer', 'is_debtor', 'phone_number', 'email')
    search_fields = ('name', 'company_name', 'phone_number', 'email')
    list_filter = ('is_supplier', 'is_customer', 'is_employer', 'is_debtor')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'reference_number', 'description', 'account', 'payment_method', 'amount')
    search_fields = ('description',)
    list_filter = ('account', 'payment_method')
    date_hierarchy = 'date'



@admin.register(BudgetingAmount)
class BudgetingAmountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account', 'target_definition', 'target_amount')
    search_fields = ('account__name', 'target_definition')
    list_filter = ('user', 'account__name', 'target_definition')

    def get_inline_instances(self, request, obj=None):
        if obj:
            return [BudgetingAmountInline]
        return []

class BudgetingAmountInline(admin.TabularInline):
    model = BudgetingAmount
    extra = 1


@admin.register(BudgetingPeriod)
class BudgetingPeriodAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'description')
    search_fields = ('description',)
    list_filter = ('start_date', 'end_date')
    inlines = [BudgetingAmountInline]
