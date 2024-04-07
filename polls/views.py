from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render

class CustomerCV(generic.CreateView):
    model = Customer
    fields = ['nickname']
    template_name = 'polls/customer_form.html'

    # def form_valid(self, form: BaseModelForm):
    #     return super().form_valid(form)
    
    # 'polls:cate'에 생성된 nickname의 pk 전달
    def get_success_url(self):
        return reverse('polls:cate', kwargs={'nickname_id':self.object.pk})

class CateLV(generic.ListView):
    model = Menu_Cate
    context_object_name = 'cate_list'

    # url을 "<int:nickname_id>/cate/<int:pk>/"로 받기 위해 context에 CustomerCV로부터 받은 nickname_id 추가
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nickname_id'] = self.kwargs['nickname_id']
        return context

class MenuDV(generic.DetailView):
    model = Menu_Cate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nickname_id'] = self.kwargs['nickname_id']
        return context

class ResultDV(generic.DetailView):
    model = Customer

def choose(request, cate_id):
    cate = get_object_or_404(Menu_Cate, pk=cate_id)
    try:
        chosen_menu_ids = request.POST.getlist('menu')
        chosen_menu_list = cate.menu_set.filter(pk__in=chosen_menu_ids)
    except(KeyError, Menu.DoesNotExist):
        return render(
            request,
            "polls:menu_cate_detail.html",
            {
                "object":cate,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        for chosen_menu in chosen_menu_list:
            print(chosen_menu)
        return HttpResponseRedirect(reverse("polls:result"))