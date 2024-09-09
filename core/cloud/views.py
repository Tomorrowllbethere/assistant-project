
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MediaFile
from django.http import Http404
import cloudinary.uploader

import logging

logger = logging.getLogger(__name__)


@login_required
def upload_file(request):
    return render(request, 'cloud/upload_file.html')


@login_required
def file_list(request):
    files = MediaFile.objects.filter(user=request.user)
    return render(request, 'cloud/file_list.html', {'files': files})


@login_required
def save_file(request):
    if request.method == 'POST':
        public_id = request.POST.get('public_id')
        url = request.POST.get('url')
        if public_id and url:
            MediaFile.objects.create(
                user=request.user,
                file=public_id
            )
        return redirect('cloud:file_list')
    return redirect('cloud:upload_file')


@login_required
def delete_file(request, public_id: any):
    try:
        media_file = MediaFile.objects.get(user=request.user, file=public_id)
        logger.info(f"Found MediaFile: {media_file}")
        media_file.delete()
        cloudinary.uploader.destroy(public_id)
        logger.info(f"Successfully deleted file with public_id: {public_id}")
        return redirect('cloud:file_list')
    except MediaFile.DoesNotExist:
        logger.error(f"MediaFile with public_id {public_id} does not exist for user {request.user.username}")
        raise Http404("MediaFile matching query does not exist.")
