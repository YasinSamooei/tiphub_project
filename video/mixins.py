from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from home.models import Video

class FieldsMixin():
	def dispatch(self, request, *args, **kwargs):
		self.fields = [
			"title", "slug", "category",
			"description", "image", "publish",
			"video",'time'
		]
		if request.user.is_admin:
			self.fields.append("auther")
			self.fields.append("status")
		return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
	def form_valid(self, form):
		if self.request.user.is_admin:
			form.save()
		else:
			self.obj = form.save(commit=False)
			self.obj.auther = self.request.user
			self.obj.status = 'i'
		return super().form_valid(form)


class AuthorAccessMixin():
	def dispatch(self, request, pk, *args, **kwargs):
		video = get_object_or_404(Video, pk=pk)
		if video.auther == request.user and video.status in ['b', 'd'] or\
		request.user.is_admin:
			return super().dispatch(request, *args, **kwargs)
		else:
			raise Http404("You can't see this page.")


class AuthorsAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_admin or request.user.is_teacher:
				return super().dispatch(request, *args, **kwargs)
			else:
				return redirect("account:profile")
		else:
			return redirect("account:login")


class SuperUserAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_admin:
			return super().dispatch(request, *args, **kwargs)
		else:
			raise Http404("You can't see this page.")