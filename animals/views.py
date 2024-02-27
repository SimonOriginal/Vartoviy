from django.shortcuts import render
from django.views import View
from .models import Animal, Photo
from dashboard.models import Device
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class AnimalDetailView(View):
    template_name = 'medical_card/medical_card.html'

    def get(self, request, *args, **kwargs):
        # Get the device_id from the query parameters
        device_id = request.GET.get('device_id')

        # Fetch all devices belonging to the user
        devices = Device.objects.filter(user=request.user)

        if device_id:
            # If device_id is provided, fetch the corresponding animal and photos
            animal = get_object_or_404(Animal, device_id=device_id)
            photos = Photo.objects.filter(animal=animal)

            # Render the animal details and return as JSON response for AJAX
            context = {'animal': animal, 'photos': photos, 'devices': devices}
            return JsonResponse({'html': render(request, self.template_name, context).content})

        # If no device_id is provided, render the initial page
        context = {'devices': devices}
        return render(request, self.template_name, context)

