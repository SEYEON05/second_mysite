from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, get_list_or_404

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


class ResultDV(generic.ListView):
    model = Menu
    template_name = 'polls/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chosen_menu_ids = self.request.session.get('chosen_menu_ids', [])  # 세션에서 가져오기
        chosen_menus = get_list_or_404(Menu, pk__in=chosen_menu_ids)  # 선택된 메뉴 객체들 조회
        total_price = sum(menu.price for menu in chosen_menus)
        context['nickname_id'] = self.kwargs['nickname_id']
        context['chosen_menus'] = chosen_menus
        context['total_price'] = total_price
        context['chosen_menu_ids'] = chosen_menu_ids

        return context



def choose(request, cate_id, nickname_id):
    cate = get_object_or_404(Menu_Cate, pk=cate_id)
    nickname_id = nickname_id
    try:
        chosen_menu_ids = request.POST.getlist('menu') # 템플릿의 post로 받은 선택된 메뉴들의 id 리스트 만들기
        # 선택된 메뉴가 없는 경우 예외 처리
        if not chosen_menu_ids:
            raise ValueError
        
        request.session['chosen_menu_ids'] = chosen_menu_ids  # 세션에 저장
    
    except(KeyError, Menu.DoesNotExist, ValueError): # try 코드가 실행되지 않았을 때 context 형태
        return render(
            request,
            "polls/menu_cate_detail.html", 
            {
                "object":cate,
                "nickname_id": nickname_id,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        return HttpResponseRedirect(reverse("polls:result", kwargs={'nickname_id': nickname_id, 'cate_id': cate_id}))
    
def create_order(request, nickname_id):
    chosen_menu_ids = request.session.get('chosen_menu_ids', [])

    # customer = get_object_or_404(Customer, pk=nickname_id)
    for menu_id in chosen_menu_ids:
        menu = get_object_or_404(Menu, pk=menu_id)
        o = Order.objects.create(nickname_id=nickname_id, ordered_menu=menu)
        o.save()
    del request.session['chosen_menu_ids']
    
    return HttpResponseRedirect(reverse('home'))