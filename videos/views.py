# videos/views.py
import replicate
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.conf import settings
from .models import AIVideo
from .forms import VideoPromptForm

def generate_ai_video(request):
    if request.method == "POST":
        form = VideoPromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]

            # ✅ Create Replicate client using API key from settings.py
            replicate_client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)

            # ✅ Use a supported model (Google Veo 3 Fast)
            output = replicate_client.run(
                "google/veo-3-fast",
                input={"prompt": prompt}
            )

            # The API returns a list of FileOutput objects or URLs
            video_url = str(output[0])  # Convert to string if it's a FileOutput object
            video_data = requests.get(video_url).content

            # Save the video to your DB and storage
            ai_video = AIVideo(prompt=prompt)
            ai_video.video.save("generated.mp4", ContentFile(video_data))
            ai_video.save()

            return render(request, "video_success.html", {"video": ai_video})
    else:
        form = VideoPromptForm()

    return render(request, "videos/form.html", {"form": form})
