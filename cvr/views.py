from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    template = loader.get_template('cvr/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def register(request):
    template = loader.get_template('cvr/register.html')
    context = {}
    return HttpResponse(template.render(context, request))

def new_user(request):
    name = request.POST['guest_name']
    phone = request.POST['guest_phone']
    answer = request.POST['guest_answer']
    guest = Guest(name=name, phone=phone)
    guest.save()
    if answer:
        Answer.objects.create(guest_id=guest.id, answer=answer, response_date=datetime.datetime.now())
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)