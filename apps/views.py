from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa
from .models import Order, Order_item  # Import your order models here


def generate_pdf(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = Order_item.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }

    template_path = 'your_template.html'  # Change this to the path of your template
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{order.order_receiver_name}.pdf"'

    # Generate PDF from HTML
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response
