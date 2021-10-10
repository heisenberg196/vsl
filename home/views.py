from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse

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
