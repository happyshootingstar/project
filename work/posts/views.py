from audioop import reverse
from datetime import timezone
import datetime
from threading import Thread
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
# Create your views here.
from django.http import HttpResponse

def index(request):
    return render("board/index.html")

def create_thread(request):
    try:
        thread = Thread(
            thread_text=request.POST['thread_str'],
            pub_date=timezone.now(),
            latest_date=timezone.now(),
        )
    except (KeyError):
        # Redisplay the thread voting form.
        return render(request, 'board/index.html', {
            'error_message': "Error",
        })
    else:
        thread.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('board:index'))


def tweet(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    try:
        tweet = thread.response_set.create(
            response_text=request.POST['tweet_str'],
            name_text=request.POST['name_str'],
            tweet_date=datetime.now()
        )
    except (KeyError):
        # Redisplay the thread voting form.
        return render(request, 'board/detail.html', {
            'thread': thread,
            'error_message': "You didn't have a tweet.",
        })
    else:
        tweet.save()
        thread.update_date()
        thread.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('board:results', args=(thread.id,)))
    