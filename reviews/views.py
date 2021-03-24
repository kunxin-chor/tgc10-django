from django.shortcuts import render
from .forms import ReviewForm


# Create your views here.
def create_review(request):
    # create a new instance of ReviewForm
    create_form = ReviewForm()

    return render(request, 'reviews/create-template.html', {
        'form': create_form
    })
