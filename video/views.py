from django.shortcuts import render
from django.views.generic import View, CreateView, ListView
from .forms import *
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from .file_mixins import *
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import mimetypes
from django.core.files import File
import base64
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
# Create your views here.


class UploadVideo(CreateView):
    template_name = 'video_processing.html'
    form_class = VideoForm
    video_path = settings.INTENT_RESPONSE_VIDEO_FOLDER

    def video_upload_mixin(self, video=None, video_url=None):
        if video:
            # can add any unique identifier to identify the name of the video
            unique_id = 1
            video = VideoUploadMixin(video, unique_id, self.video_path)
            video.upload_file()
            video_name = video.get_media_file_access_path()
        else:
            raise Exception("No Video/URL is provided.")
        return video_name

    def dispatch(self, request, *args, **kwargs):
        self.form_data = dict()
        unique_id = 1
        if self.request.is_ajax():
            video_name_key = self.request.POST.get("video_name")
            try:
                if video_name_key:
                    video = self.request.FILES.get('video-file')
                    video_access_path = self.video_upload_mixin(video=video)
            except Exception as e:
                return HttpResponseBadRequest(content=json.dumps({"error": str(e)}))
            self.form_data['video_name'] = video_name_key
            self.form_data['video_access_path'] = video_access_path
            self.form_data['creator_id'] = unique_id
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if kwargs.get("data"):
            kwargs['data']._mutable = True
            kwargs['data'].update(
                {
                    'data': self.form_data,
                }
            )
            kwargs['data']._mutable = False

        return kwargs
    def form_valid(self, form):
        self.object = form.save()
        response_data = {"message": "Video Saved Successfully"}
        return JsonResponse(response_data)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)


class VideoReport(ListView):
    '''
    class to render Videos for a particular creator
    '''
    model = Videos
    template_name = 'video_report.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'video_list'  # Default: object_list
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['site_url'] = settings.SITE_URL
        return context_data
    def get_queryset(self):
        return Videos.objects.filter(creator_id="1").order_by('-time_created')

class DownloadVideo(View):
    http_method_names = ['get']
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DownloadVideo, self).dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
        try:
            decoded_url = base64.b64decode(self.request.GET.get('file_path')).decode("utf-8", "ignore")
            download_report_link = settings.MEDIA_ROOT+"/"+decoded_url
            f = open(download_report_link, 'rb')
            file_obj = File(f)
            content_type_ = mimetypes.guess_type(download_report_link)[0]
            response = HttpResponse(file_obj, content_type=content_type_)
            response['Content-Disposition'] = 'attachment; filename=' + "video.mp4"
            response['Content-length'] = file_obj.size
            return response
        except Exception as e:
            return redirect(reverse_lazy("video_report"))