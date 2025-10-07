from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, View

from .forms import FoodSearchForm
from .models import Food


class FoodListView(ListView):
    model = Food
    template_name = "foods/food_list.html"
    context_object_name = "foods"
    paginate_by = 20

    def get_queryset(self):
        queryset = Food.objects.filter(is_public=True).order_by("name")
        self.form = FoodSearchForm(self.request.GET or None)
        if self.form.is_valid():
            query = self.form.cleaned_data.get("query")
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) | Q(brand__icontains=query)
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = getattr(self, "form", FoodSearchForm())
        return context


class FoodAutocompleteView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        foods = Food.objects.filter(is_public=True)
        if query:
            foods = foods.filter(Q(name__icontains=query) | Q(brand__icontains=query))
        data = [
            {
                "id": food.id,
                "name": food.name,
                "brand": food.brand,
                "calories": float(food.calories),
            }
            for food in foods[:20]
        ]
        return JsonResponse({"results": data})
