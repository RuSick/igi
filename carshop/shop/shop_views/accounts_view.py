#регистрация
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Перенаправление на страницу входа после регистрации
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})