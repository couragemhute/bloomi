# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Invoice, InvoiceItem
from django.views.generic import TemplateView

class InvoiceTemplateView(TemplateView):
    template_name = 'invoice/create.html'


@csrf_exempt
def create_invoice(request):
    if request.method == 'POST':
        invoice = Invoice.objects.create(
            invoice_no=request.POST['invoice_no'],
            invoice_date=request.POST['invoice_date'],
            from_business=request.POST['from_business'],
            to_business=request.POST['to_business'],
            total=0  # We'll calculate below
        )

        total = 0
        items = zip(
            request.POST.getlist('item_name[]'),
            request.POST.getlist('quantity[]'),
            request.POST.getlist('rate[]')
        )
        for name, qty, rate in items:
            amount = int(qty) * float(rate)
            InvoiceItem.objects.create(
                invoice=invoice,
                name=name,
                quantity=qty,
                rate=rate
            )
            total += amount

        invoice.total = total
        invoice.save()

        return JsonResponse({'success': True, 'invoice_id': invoice.id})
