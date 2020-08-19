"""
The whole app comprises of two views at this moment, one that will receive
the form post and process full urls into shortened codes and vice versa; And
another one that will be redirecting clients based off the request argument,
which is supposed to be the shortened code.
"""
from django.views.generic import FormView, RedirectView
from core.forms import ShortenURLForm
from core.models import ShortenedURL


class ShortenURLView(FormView):
    """
    This view will allow the user to submit either a full url to be shortened
    or a shortened code to be expanded back into a full url.
    """
    template_name = 'core/index.htm'
    form_class = ShortenURLForm

    def post(self, request, *args, **kwargs):
        short_code = request.POST.get('shortened_url', None)
        expanded_url = request.POST.get('expanded_url', None)
        # At this point there is no much validation going on with the form
        # but the user may send in empty fields.

        # In case the user is submitting a shortened code
        if short_code:
            # try and fetch from database
            obj = ShortenedURL.objects.filter(shortened_url=short_code).first()
            # if existing, add the result to the template's context_data
            if obj:
                return self.render_to_response(
                    self.get_context_data(result=obj.expanded_url))
            # Otherwise, indicate it wasn't found
            else:
                return self.render_to_response(
                    self.get_context_data(result="URL Doesn't exist."))
        # In case of empty fields, indicate the user must fill either one
        if not short_code and not expanded_url:
            return self.render_to_response(
                self.get_context_data(result="Fill one of the input fields "
                                             "above."))
        # Otherwise, the `expanded_url` was provided and shall undergo the
        # super `FormView` process of form validation and object saving
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model and
        respond the resulted shortened_url"""
        obj = form.save()
        base_url = self.request.build_absolute_uri()
        return self.render_to_response(
            self.get_context_data(
                result=f'{base_url}{obj.shortened_url}'))

    def form_invalid(self, form):
        """
        If form is invalid, show errors as text.
        TODO: Add proper URL Validation and better error messages
        """
        return self.render_to_response(
            self.get_context_data(result=form.errors.as_text()))


class RedirectorView(RedirectView):
    """Given the shortened URL redirects the user directly to the expanded."""
    permanent = True

    def get(self, request, *args, **kwargs):
        """Gets the argument provided (shortened code) and update `self.url`
        so super can be used to redirect the client."""
        shortened_code = args[0] if args else None
        if not shortened_code:
            self.url = '/'
        else:
            obj = ShortenedURL.objects.get(shortened_url=shortened_code)
            self.url = obj.expanded_url
        return super().get(request, *args, **kwargs)
