from django.shortcuts import render

# Create your views here.


# pages/views.py
from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from pages.models import Item, ToDoList


def homePageView(request):
    # return request object and specify page.
    return render(request, 'home.html', {
        'mynumbers': [1, 2, 3, 4, 5, 6, ],
        'firstName': 'Victor',
        'lastName': 'Li'
    })


def aboutPageView(request):
    # return request object and specify page.
    return render(request, 'about.html')


def victorPageView(request):
    return render(request, 'victor.html')


def homePost(request):
    # Use request object to extract choice.

    choice = 1
    gmat = 1

    try:
        # Extract value from request object by control name.
        length = float(request.POST.get("length"))
        margin_low = float(request.POST.get("margin_low"))
        margin_up = float(request.POST.get("margin_up"))
        diagonal = float(request.POST.get("diagonal"))
        # currentChoice = request.POST['choice']
        # gmatStr = request.POST['gmat']

        # Crude debugging effort.
        print("values input are :   ", length, margin_up, margin_low, diagonal)
        # print("*** Years work experience: " + str(currentChoice))
        # choice = int(currentChoice)
        # gmat = float(gmatStr)
    # Enters 'except' block if integer cannot be created.
    except:
        return render(request, 'home.html', {
            'errorMessage': '*** The data submitted is invalid. Please try again.',
            'mynumbers': [1, 2, 3, 4, 5, 6, ]})
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # return HttpResponseRedirect(reverse('results',
        #                                     kwargs={'length': length, 'margin_low': margin_low, 'margin_up': margin_up,
        #                                             'diagonal': diagonal}, ))
        return HttpResponseRedirect(reverse('results', kwargs={'length': length, 'margin_low': margin_low, 'margin_up': margin_up, 'diagonal': diagonal}))


import pickle
import sklearn  # You must perform a pip install.
import pandas as pd


def results(request, length, margin_low, margin_up, diagonal):
    print("*** Inside results()")
    # load saved model
    with open('model_pkl', 'rb') as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    # singleSampleDf = pd.DataFrame(columns=['gmat', 'work_experience'])
    singleSampleDf = pd.DataFrame(columns=['length', 'margin_low', 'margin_up', 'diagonal'])

    # workExperience = float(choice)
    # print("*** GMAT Score: " + str(gmat))
    # print("*** Years experience: " + str(workExperience))
    singleSampleDf = singleSampleDf.append({'length': length,
                                            'margin_low': margin_low,
                                            'margin_up': margin_up,
                                            'diagonal': diagonal},
                                           ignore_index=True)

    singlePrediction = loadedModel.predict(singleSampleDf)

    print("Single prediction: " + str(singlePrediction))

    # return render(request, 'results.html', {'choice': workExperience, 'gmat':gmat,
    #             'prediction':singlePrediction})
    return render(request, "results.html", {"results": singlePrediction})
    # return HttpResponseRedirect(reverse('results', kwargs={'length': 150, 'margin_low': 3, 'margin_up': 4, 'diagonal': 150}))


def todos(request):
    print("*** Inside todos()")
    items = Item.objects
    itemErrandDetail = items.select_related('todolist')
    print(itemErrandDetail[0].todolist.name)
    return render(request, 'ToDoItems.html',
                  {'ToDoItemDetail': itemErrandDetail})


from django.shortcuts import render, redirect
from .forms import RegisterForm


def register(response):
    # Handle POST request.
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('message',
                                                kwargs={'msg': "Your are registered.", 'title': "Success!"}, ))
    # Handle GET request.
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form": form})


def message(request, msg, title):
    return render(request, 'message.html', {'msg': msg, 'title': title})


def secretArea(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('message',
                                            kwargs={'msg': "Please login to access this page.",
                                                    'title': "Login required."}, ))
    return render(request, 'secret.html', {'useremail': request.user.email})
