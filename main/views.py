from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import TodoList, Item
from .forms import CreateNewList
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(response):
    return render(response, "main/home.html", {"name": "test"})

@login_required(login_url="/login/")
def index(response, id):
    todo = TodoList.objects.get(id=id)

    # Checks if the TodoList is made by the current user
    if todo in response.user.todolist.all():
        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in todo.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "checked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()

            elif response.POST.get("add-item"):
                text = response.POST.get("new")
                if len(text) > 2:
                    todo.item_set.create(text=text, complete=False)
                else:
                    print("Invalid text")
        return render(response, "main/todo.html", {"todo": todo})
    else:
        return render(response, "main/view.html", {})

@login_required(login_url="/login/")
def view(response):
    return render(response, "main/view.html", {})

@login_required(login_url="/login/")
def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            todo = TodoList(name=name)
            todo.save()
            response.user.todolist.add(todo)
        return HttpResponseRedirect("/%i" %todo.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form": form})
