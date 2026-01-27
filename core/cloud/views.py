from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import MediaFile, Folder
from .forms import FolderForm, MoveFileForm
import cloudinary.uploader
import logging

logger = logging.getLogger(__name__)
# Завантаження файлу
@login_required
def upload_file(request):
    folders = Folder.objects.filter(user=request.user)
    return render(request, 'cloud/upload_file.html', {'folders': folders})

import logging

logger = logging.getLogger(__name__)

@login_required
def save_file(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        logger.info(f"Received POST request with data: {request.POST}")
        file = request.FILES.get('file')
        folder_id = request.POST.get('folder')
        
        if file:
            if file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                return JsonResponse({'error': 'File type is not supported. Please upload an image file (JPEG, PNG, GIF).'}, status=400)
            
            try:
                upload_result = cloudinary.uploader.upload(file)
                public_id = upload_result.get('public_id')
                url = upload_result.get('secure_url')

                folder = Folder.objects.get(id=folder_id) if folder_id else None
                MediaFile.objects.create(user=request.user, file=public_id, folder=folder)

                return JsonResponse({'success': True, 'message': 'File uploaded successfully!'})
            except Exception as e:
                logger.error(f"Error uploading file: {str(e)}")
                return JsonResponse({'error': f'Error uploading file: {str(e)}'}, status=500)
        
        logger.error("No file provided.")
        return JsonResponse({'error': 'No file provided.'}, status=400)

    logger.error("Invalid request method or CSRF token missing.")
    return JsonResponse({'error': 'Invalid request method or CSRF token missing.'}, status=400)


# Перегляд списку файлів
@login_required
def file_list(request):
    folders = Folder.objects.filter(user=request.user)
    files = MediaFile.objects.filter(user=request.user)
    return render(request, 'cloud/file_list.html', {'files': files, 'folders': folders})


# Створення папки
@login_required
def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            messages.success(request, 'Folder created successfully!')
            return redirect('cloud:file_list')
        else:
            messages.error(request, 'Invalid folder name.')
    else:
        form = FolderForm()
    return render(request, 'cloud/create_folder.html', {'form': form})


# Переміщення файлу між папками
@login_required
def move_file(request, file_id):
    media_file = get_object_or_404(MediaFile, id=file_id, user=request.user)

    if request.method == 'POST':
        form = MoveFileForm(request.user, request.POST)
        if form.is_valid():
            new_folder = form.cleaned_data['folder']
            media_file.folder = new_folder
            media_file.save()
            messages.success(request, 'File moved successfully!')
            return redirect('cloud:file_list')
        else:
            messages.error(request, 'Invalid folder selected.')
    else:
        form = MoveFileForm(request.user)

    return render(request, 'cloud/move_file.html', {'form': form, 'file': media_file})


# Видалення файлу
@login_required
def delete_file(request, public_id):
    try:
        media_file = MediaFile.objects.get(user=request.user, file=public_id)
        media_file.delete()
        cloudinary.uploader.destroy(public_id)
        messages.success(request, 'File deleted successfully!')
        return redirect('cloud:file_list')
    except MediaFile.DoesNotExist:
        logger.error(f"MediaFile with public_id {public_id} does not exist for user {request.user.username}")
        raise Http404("MediaFile matching query does not exist.")