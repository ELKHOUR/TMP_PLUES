from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import DetailView, FormView
from django.core.mail import EmailMessage, send_mail
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from site_app.models import Product, CompanyServices, PendingEmail, ConfirmedEmail, CompanyInfo
from django.http import JsonResponse



# Create your views here.
def index(request):
    query = request.GET.get('q')

    # Filter products first
    if query:
        products_list = Product.objects.filter(name__icontains=query)
    else:
        products_list = Product.objects.all()

    # Then paginate
    paginator = Paginator(products_list, 8)  # 8 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    services = CompanyServices.objects.all()
    infos = CompanyInfo.objects.all().order_by('id')
    values = [info.value for info in infos]

    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if ConfirmedEmail.objects.filter(email=email).exists():
                messages.info(request, "📬 You are already subscribed to the mailing list.")
                return redirect('home')

            pending, created = PendingEmail.objects.get_or_create(email=email)
            if not created:
                messages.info(request, "📬 We have already sent you the confirmation link, check your email.")
                return redirect('home')

            confirm_link = f"{request.scheme}://{request.get_host()}/confirm-email/{pending.token}/"
            send_mail(
                subject='Confirm your subscription to the mailing list',
                message=f'Click this link to confirm your email:\n{confirm_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
            )
            messages.success(request, "📬 A confirmation link has been sent to your email.")
            return redirect('home')

    return render(request, 'home.html', {'products': products, 'services': services, 'values': values})






def confirm_email(request, token):
    pending = get_object_or_404(PendingEmail, token=token)
    ConfirmedEmail.objects.get_or_create(email=pending.email)
    pending.delete()
    messages.success(request, "✅ Your email has been successfully verified!")
    return redirect('home')



class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'
    queryset = Product.objects.select_related('category').prefetch_related('size', 'material', 'images')


def application_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        city = request.POST.get('city')
        cv = request.FILES.get('cv')

        # ✉️ إرسال الإيميل
        subject = f"New Job Application from {name}"
        body = f"Name: {name}\nEmail: {email}\nPhone: {telephone}\nCity: {city}"
        mail = EmailMessage(subject, body, to=['mahmoud.reda45667@gmail.com'])
        if cv:
            mail.attach(cv.name, cv.read(), cv.content_type)
        mail.send()

        # ✅ إضافة رسالة نجاح
        messages.success(request, "✅ Your request has been submitted successfully! We will contact you soon.")

        # 🔁 إعادة التوجيه للصفحة الرئيسية
        return redirect('home')
    return render(request, 'application_form.html')



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            # Send email (adjust as needed)
            send_mail(
                subject=f"Client Message >>>>> {name}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
            )
            messages.success(request, "✅ Your message has been sent!")
            return redirect('contact')
        else:
            messages.error(request, "⚠️ Please fill in all fields.")

    return render(request, 'contact.html')
