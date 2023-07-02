from django.contrib import admin
from django.http import HttpResponse
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Customer)

admin.site.register(OrderItem)
admin.site.register(Message)


from django.contrib import admin
from django.http import HttpResponse
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'total_amount', 'status')
    actions = ['generate_report']

    def order_id(self, obj):
        return f"Order ID: {obj.pk}"
    order_id.short_description = 'Order ID'

    def customer_name(self, obj):
        return obj.customer.name
    customer_name.short_description = 'Customer'

    def generate_order_report(self, request, queryset):
        # Create a report format
        report = []
        headers = ['Order ID', 'Customer Name', 'Total Amount', 'Status', 'Product Name', 'Quantity', 'Price', 'Subtotal']
        report.append(headers)
        for order in queryset:
            for item in order.orderitem_set.all():
                order_row = [
                    f"Order ID: {order.pk}",
                    order.customer.name,
                    str(order.total_amount),
                    order.status,
                    item.product.name,
                    str(item.quantity),
                    str(item.price),
                    str(item.subtotal)
                ]
                report.append(order_row)

        # Generate report as a string
        report_str = '\n'.join('\t'.join(row) for row in report)

        # Download the report as a file
        response = HttpResponse(report_str, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=order_report.txt'
        return response

    generate_order_report.short_description = 'Generate Order Report'
