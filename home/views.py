from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from home.forms import VideoUploadForm
from home.models import vidFile
from django.urls import reverse

from home.utils.vcs import VehicleCount

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def vidView(request, id):
    try:
        cam = VehicleCount()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass
    # context = {
    #     'title': 'Home Page',
    #     'content': 'Welcome to the home page.',
    # }

    # return render(request, 'home/vidView.html', context=context)


def vidUpload(request):
    if request.method == 'POST':
        print(request.POST.__dict__)
        location = request.POST.get('location', None)
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():

            instance = vidFile(file=request.FILES['file'], location=location)
            instance.save()
            print("hello")
            return HttpResponseRedirect(reverse('vid-view', args=[1]))
        else:
            print("invalid")
    else:
        form = VideoUploadForm()
    return render(request, 'home/upload.html', {'form': form})

def index(request):
    print("hello")
    return render(request, 'home/index.html', {})
