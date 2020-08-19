from functools import reduce

from django.views.generic import FormView, RedirectView, DetailView
from core.forms import ShortenURLForm
from core.models import ShortenedURL


class ShortenURLView(FormView):
    """Receives a full url and returns a shortened version of it"""
    template_name = 'core/index.htm'
    form_class = ShortenURLForm

    def post(self, request, *args, **kwargs):
        url_code = request.POST.get('shortened_url', None)
        expanded_url = request.POST.get('expanded_url', None)
        if url_code:
            obj = ShortenedURL.objects.filter(shortened_url=url_code).first()
            if obj:
                return self.render_to_response(
                    self.get_context_data(result=obj.expanded_url))
            else:
                return self.render_to_response(
                    self.get_context_data(result="URL Doesn't exist."))
        if not url_code and not expanded_url:
            return self.render_to_response(
                self.get_context_data(result="Fill one of the input fields "
                                             "above."))
        return super(ShortenURLView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        obj = form.save()
        base_url = self.request.build_absolute_uri()
        return self.render_to_response(
            self.get_context_data(
                result=f'{base_url}{obj.shortened_url}'))

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(result=form.errors.as_text()))


class RedirectorView(RedirectView):
    """Given the shortened URL redirects the user directly to the expanded."""
    permanent = True

    def get(self, request, *args, **kwargs):
        # Remove the empty strings from the path, extracting the shortened code
        shortened_code = args[0] if args else None
        if not shortened_code:
            self.url = '/'
        else:
            obj = ShortenedURL.objects.get(shortened_url=shortened_code)
            self.url = obj.expanded_url
        return super().get(request, *args, **kwargs)
