from django.shortcuts import render
from django.http import HttpResponse
import requests
import random
import json
# Create your views here.
def homepage(request):
    return render(request, 'findverse/home.html')

def verse(request):

    book = request.GET.get('book')
    chapter = request.GET.get('chapter')
    verse = request.GET.get('verse')
    request.session['book'] = book
    request.session['chapter'] = chapter
    request.session['verse'] = verse
    request.session.modified = True
    verse_format = book.title() + " " + str(chapter) + ":" + str(verse)
    response = requests.get("http://bible-api.com/" + book + " " + str(chapter) + ":" + str(verse))
    try:
        text = response.json()["text"]
    except KeyError:
        return render(request, 'findverse/404.html')

    return render(request, 'findverse/verse.html', {'name': verse_format, 'verse': text})

def memorize(request):
    verse_format = (request.session['book'].title() + " "
                    + str(request.session['chapter']) + ":"
                    + str(request.session['verse']))
    response = requests.get("http://bible-api.com/" + verse_format)
    text = response.json()['text']
    find = []

    verse_list = []
    normal_list = []

    for i in range(0, len(text.split())):
        verse_list.append(text.split()[i])
    random.shuffle(verse_list)
    for i in range(0, len(text.split())):
        normal_list.append(text.split()[i])
    fulltuple = list(zip(verse_list, normal_list))

    return render(request, 'findverse/memorize.html', {'text': verse_list,
                                                       'verse': verse_format,
                                                       'full': fulltuple,
                                                       'find': find})

def score(request):
    score = 0

    book = request.session['book']
    chapter = request.session['chapter']
    verse = request.session['verse']
    response = requests.get("http://bible-api.com/" + book + " " + str(chapter) + ":" + str(verse))
    text = response.json()['text']
    text.split()
    verselist = []

    for i in range(0, len(text.split())):
        verselist.append(text.split()[i])


    for i in range(0, len(text.split())):
        answer = request.GET.get(text.split()[i])
        if answer == text.split()[i]:
            score += 1
    score /= len(text.split())
    score *= 100
    score = int(score)

    return render(request, 'findverse/score.html', {'score': score, 'verselist': verselist})





