from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Notification
from django.core.paginator import Paginator

@method_decorator(login_required(login_url='login'), name='dispatch')
class NotificationsView(View):
    template_name = 'notices/notifications.html'
    notifications_per_page = 6

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(device__user=request.user).order_by('-timestamp')

        # Pagination
        paginator = Paginator(notifications, self.notifications_per_page)
        page = request.GET.get('page', 1)
        paginated_notifications = paginator.get_page(page)

        # Mark notifications as viewed
        viewed_notifications = Notification.objects.filter(id__in=paginated_notifications.object_list, viewed=False)
        viewed_notifications.update(viewed=True)

        data = [
            {
                'id': notification.id,
                'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'message': notification.message,
                'viewed': notification.viewed,
            } for notification in paginated_notifications
        ]

        if request.GET.get('format') == 'json':
            return JsonResponse(data, safe=False)
        else:
            return render(request, self.template_name, {'notifications': paginated_notifications})
        

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        notification_id = request.POST.get('notification_id')

        if action == 'delete_all':
            Notification.objects.filter(device__user=request.user).delete()
            return JsonResponse({'status': 'success', 'message': 'All notifications deleted.'})
        elif action == 'delete_single' and notification_id:
            notification = get_object_or_404(Notification, id=notification_id)
            notification.delete()
            return JsonResponse({'status': 'success', 'message': 'Notification deleted.'})

        return JsonResponse({'status': 'error', 'message': 'Invalid action or notification ID not provided.'})

class UnviewedNotificationsCountView(View):
    def get(self, request, *args, **kwargs):
        unviewed_count = Notification.objects.filter(device__user=request.user, viewed=False).count()
        return JsonResponse({'unviewed_count': unviewed_count})