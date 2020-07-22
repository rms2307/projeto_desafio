from django.shortcuts import render
from django.views import View


class Home(View):
    template_name = 'home/index.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.renderizar = render(
            self.request, self.template_name)

    def get(self, *args, **kwargs):
        return self.renderizar
