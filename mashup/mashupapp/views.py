import os
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from .models import mashup_data
from .forms import mashup_form  
from django.http import FileResponse
# Create your views here.
from zipfile import ZipFile
from pytube import Search
import sys
import moviepy.editor as mp
import re
def mashup_func(a,b,c,d):
    data=[]
    try:
        # if(len(sys.argv)!=5):
        #     print('Please Enter all the required command line parameters')
        if(int(b)<=10):  
            print("Number of videos to be downloaded must be greater than 10")  
        elif(int(c)<=20):  
            print("Seconds to be cut in each video must be greater than 20")     
        else:
            x=Search(a+" Songs")
            counter=0
            idx=0
            while(counter<(int(b))):
                if(x.results[idx].length<600):
                    n=(re.sub("[|\\:\/*<>?\"]",'',str(x.results[idx].title))+".mp4")
                    try:
                        m=x.results[idx].streams.filter(progressive=True, file_extension='mp4').first().download(output_path=os.path.join(settings.MEDIA_ROOT),filename=n)
                        clip = mp.VideoFileClip(os.path.join(settings.MEDIA_ROOT,n)).subclip(0,int(c))
                        data.append(clip) 
                        counter+=1
                    except:
                        pass    
                idx+=1
                if idx>=len(x.results):
                    x.get_next_results()
            final_clip = mp.concatenate_videoclips(data)    
            aud = final_clip.audio.set_fps(44100)
            final_clip = final_clip.without_audio().set_audio(aud)
            final_clip.audio.write_audiofile(os.path.join(settings.MEDIA_ROOT,d))
            z=ZipFile(os.path.join(settings.MEDIA_ROOT,d[:-4]+".zip"),'w')
            z.write(os.path.join(settings.MEDIA_ROOT,d))
            return str(d[:-4]+".zip")
    except Exception as e:
        print("Exception has occured",e)

# def download(request, d):
#     filename=os.path.join(settings.MEDIA_ROOT,d)
#     # response = FileResponse(open(filename, 'rb'),as_attachment=True)
#     file = open(filename, "rb").read()
#     response['Content-Disposition'] = 'attachment; filename=filename.mp3'
#     return HttpResponse(file, mimetype="audio/mpeg")

#     return response


def home(request):
    if request.method == 'POST':
        form = mashup_form(request.POST)
        if form.is_valid():
            form.save()
            # f=request.FILES['dataset']
            # f2=topsis_data.objects.filter(dataset=f.name)
            # print(f.name)
            # settings.MEDIA_ROOT, 
            # print(os.path.join(settings.MEDIA_ROOT,'topsis_data_store',f.name))
            # send_mail('hi', 'hello world message', 'topsiswebservice@gmail.com', ['udayuppal2@gmail.com'],fail_silently=False)
            # print("////////////////////",os.path.join(settings.MEDIA_ROOT,'outputfile.mp3'),"//////////////////////")
            res=mashup_func(request.POST['singername'],request.POST['n_videos'],request.POST['duration'], 'outputfile.mp3')
            email = EmailMessage('Mashup Result', 'The Mashup of your favourite singer '+request.POST['singername']+ ' is generated. Kindly find the attched mp3 file. Thank you for using our services. ', 'topsiswebservice@gmail.com', [str(request.POST['email'])])
            email.attach_file(os.path.join(settings.MEDIA_ROOT,res))
            email.send()
            # redirect("/download", d=(res[:-4]+".mp3"))
            
    else:
        form = mashup_form()
    return render(request, 'index.html',{
        'form': form
    }) 
