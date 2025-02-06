from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.models import User
from cine.models import Pelicula
from .forms import ComentarioForm, RegistroForm, LoginForm
from django.contrib.auth.decorators import login_required

from cine.models import Pelicula, Comentario
from django.utils import timezone
def crud(request):
    peliculas = Pelicula.objects.all()  # Obtener todas las películas
    return render(request, 'crud.html', {'peliculas': peliculas})

def home(request):
    form_registro = RegistroForm()
    form_login = LoginForm()

    if request.method == "POST":
        if request.POST.get('accion') == 'registro':
            form_registro = RegistroForm(request.POST)
            if form_registro.is_valid():
                nombre = form_registro.cleaned_data['nombre']
                apellido = form_registro.cleaned_data['apellido']
                email = form_registro.cleaned_data['email']
                contraseña = form_registro.cleaned_data['contraseña']
                user = User.objects.create_user(username=email, email=email, password=contraseña, first_name=nombre, last_name=apellido)
                auth_login(request, user)
                return redirect('home')

        elif request.POST.get('accion') == 'login':
            form_login = LoginForm(request.POST)
            if form_login.is_valid():
                email = form_login.cleaned_data['email']
                contraseña = form_login.cleaned_data['contraseña']

                users = User.objects.filter(email=email)
                if users.exists():
                    user = users.first()
                    if user.check_password(contraseña):
                        auth_login(request, user)
                        return redirect('crud')  # Redirige a la página de CRUD
                else:
                    form_login.add_error(None, "Credenciales inválidas.")

    return render(request, 'home.html', {'form_registro': form_registro, 'form_login': form_login})

def custom_logout(request):
    logout(request)
    return redirect('home')  # Redirige a home.html después de cerrar sesión
@login_required
def ver_pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    return render(request, 'ver_pelicula.html', {'pelicula': pelicula})
@login_required
def editar_pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)

    if pelicula.author != request.user:
        return redirect('crud')  # Redirige si el usuario no es el autor

    if request.method == 'POST':
        pelicula.nombre_pelicula = request.POST.get('nombre_pelicula')
        pelicula.director = request.POST.get('director')
        pelicula.fecha_estreno = request.POST.get('fecha_estreno')
        pelicula.sinopsis = request.POST.get('sinopsis')
        pelicula.save()
        return redirect('crud')  # Redirige a la lista de películas

    return render(request, 'editar_pelicula.html', {'pelicula': pelicula})

@login_required
def borrar_pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    if request.method == 'POST':
        pelicula.delete()  # Eliminar la película
        return redirect('crud')  # Redirigir de vuelta a la lista de películas
    return redirect('crud')  # Si no es POST, redirigir igualmente
@login_required
def agregar_pelicula(request):
    if request.method == 'POST':
        nombre_pelicula = request.POST.get('nombre_pelicula')
        director = request.POST.get('director')
        fecha_estreno = request.POST.get('fecha_estreno')
        sinopsis = request.POST.get('sinopsis')

        if len(nombre_pelicula) < 3 or len(director) < 3 or len(sinopsis) < 3:
            mensaje_error = "Todos los campos deben tener al menos 3 caracteres."
            return render(request, 'agregar_pelicula.html', {'mensaje_error': mensaje_error})

        if Pelicula.objects.filter(nombre_pelicula=nombre_pelicula).exists():
            mensaje_error = "No se ha podido registrar la película porque ya existe una con el mismo nombre."
            return render(request, 'agregar_pelicula.html', {'mensaje_error': mensaje_error})

        nueva_pelicula = Pelicula(
            nombre_pelicula=nombre_pelicula,
            director=director,
            fecha_estreno=fecha_estreno,
            sinopsis=sinopsis,
            author=request.user  # Asumimos que la película es agregada por el usuario actual
        )
        nueva_pelicula.save()
        
        return redirect('crud')
    
    return render(request, 'agregar_pelicula.html')
    
@login_required
def ver_pelicula(request, pelicula_id):
    pelicula = Pelicula.objects.get(id=pelicula_id)

    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario')
        
        if comentario_texto and len(comentario_texto) >= 3:  # Asegurarse de que no sea None
            comentario = Comentario(
                pelicula=pelicula,
                autor=request.user,
                comentario=comentario_texto,
                fecha_comentario=timezone.now()
            )
            comentario.save()

    comentarios = Comentario.objects.filter(pelicula=pelicula)

    if 'delete_comentario' in request.POST:
        comentario_id = request.POST.get('comentario_id')
        comentario = get_object_or_404(Comentario, id=comentario_id)

        # Asegurarse de que solo el autor del comentario pueda eliminarlo
        if comentario.autor == request.user:
            comentario.delete()

    return render(request, 'ver_pelicula.html', {
        'pelicula': pelicula,
        'comentarios': comentarios
    })
