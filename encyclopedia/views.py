from django.shortcuts import render, redirect
from django import forms
from . import util
from markdown2 import markdown
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/not_found.html", {
            "title": title
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown(entry)
    })

def search(request):
    query = request.GET.get("q")
    if util.get_entry(query):
        return redirect("entry_page", title=query)
    else:
        results = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "results": results,
            "query": query
        })

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error": "Page with this title already exists."
                })
            util.save_entry(title, content)
            return redirect("entry_page", title=title)
    else:
        form = NewPageForm()
    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def edit_page(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("entry_page", title=title)
    else:
        content = util.get_entry(title)
        form = EditPageForm(initial={"content": content})
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": form
    })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect("entry_page", title=title)
