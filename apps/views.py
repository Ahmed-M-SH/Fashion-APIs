from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa
from .models import Order, Order_item  # Import your order models here
from .models import Applcation as App


def generate_pdf(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = Order_item.objects.filter(order_id=order.id)

    context = {
        'order': order,
        'order_items': order_items,
    }

    # Change this to the path of your template
    template_path = 'pages/invoice_pdf.html'
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="فاتورة طلب {order.customer_name} رقم {order_id}.pdf"'

    # Generate PDF from HTML
    pisa_status = pisa.CreatePDF(html, dest=response, encoding="UTF-8")

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response


def generate_file_app(request, *args, **kwargs):
    # Assuming you want to download the first application in the database
    applcation = App.objects.first()

    # Get the file path
    file_path = applcation.app_file.path

    try:
        # Open the file for reading in binary mode
        with open(file_path, 'rb') as file:
            response = HttpResponse(
                file.read(), content_type='application/vnd.android.package-archive')
            response['Content-Disposition'] = f'attachment; filename="{applcation.app_name}.apk"'
            return response
    except FileNotFoundError:
        return HttpResponse('File not found', status=404)
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)


def download_app(request, *args, **kwargs):
    file = App.objects.order_by('-id').first()
    data = {
        # 'download_count': file.download_count,
        # 'app_name': file.app_name,
        # 'version': file.version,
        'app': file
    }
    return render(request, "pages/about.html", data)
