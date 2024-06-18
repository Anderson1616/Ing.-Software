from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from django.contrib.auth.models import User 
from .models import Pedido, Conductor, Camion
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@login_required
def home(request): #Por algún motivo si quito esto me da error la aplicación
   pedidos = Pedido.objects.all()
   return render(request, 'home.html', {'pedidos': pedidos})

@login_required
@never_cache
def crud_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'crud_pedidos.html', {'pedidos': pedidos})

@login_required
@never_cache
def crud_conductores(request):
    conductores = Conductor.objects.all()
    return render(request, 'crud_conductores.html', {'conductores': conductores})

@login_required
@never_cache
def crud_camion(request):
    camiones = Camion.objects.all()
    return render(request, 'crud_camion.html', {'camiones': camiones})


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Usuario creado y autenticado exitosamente')
                return redirect('home')
        else:
            messages.error(request, 'Las contraseñas no coinciden o los datos no son válidos')
            return render(request, 'signup.html', {
                'form': form
            })



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('home')
        else:
            messages.error(request, 'El usuario no existe o las credenciales son incorrectas.')
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'alert_message': True
            })
    return render(request, 'signup.html', {'form': UserCreationForm()})



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, 'Registro completado exitosamente.')
                # Redirige solo si el registro es exitoso
                return redirect('signup')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
                return redirect('register')
        else:
            messages.error(request, 'Error: Este usuario ya existe.')
            return redirect('register')
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('signup')

@login_required
@never_cache
def agregar_pedido_view(request):
    conductores = Conductor.objects.all()
    if request.method == 'POST':
        camion = request.POST.get('camion')
        modelo = request.POST.get('modelo')
        material = request.POST.get('material')
        cliente = request.POST.get('cliente')
        conductor_id = request.POST.get('conductor')
        ruta = request.POST.get('ruta')
        estado = request.POST.get('estado')
        fecha_pedido = timezone.now()

        try:
            conductor = Conductor.objects.get(id=conductor_id)
            pedido = Pedido.objects.create(
                camion=camion,
                modelo=modelo,
                material=material,
                cliente=cliente,
                conductor=conductor,
                ruta=ruta,
                estado=estado,
                fecha_pedido=fecha_pedido
            )
            messages.success(request, 'Pedido agregado exitosamente.')
            return redirect('crud_pedidos')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('agregar_pedido')
    return render(request, 'agregar_pedido.html', {'conductores': conductores})

@login_required
@never_cache
def ver_informacion(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'ver_informacion.html', {'pedido': pedido})

@login_required
@never_cache
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    conductores = Conductor.objects.all()
    
    if request.method == 'POST':
        pedido.camion = request.POST.get('camion')
        pedido.modelo = request.POST.get('modelo')
        pedido.material = request.POST.get('material')
        pedido.cliente = request.POST.get('cliente')
        pedido.conductor_id = request.POST.get('conductor')
        pedido.ruta = request.POST.get('ruta')
        pedido.estado = request.POST.get('estado')
        pedido.fecha_pedido = timezone.now()  # Si deseas actualizar la fecha al editar
        
        try:
            pedido.save()
            messages.success(request, 'Pedido editado exitosamente.')
            return redirect('crud_pedidos')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('editar_pedido', pedido_id=pedido_id)
    
    return render(request, 'editar.html', {'pedido': pedido, 'conductores': conductores})

@login_required
@never_cache
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    try:
        pedido.delete()
        messages.success(request, 'Pedido eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    return redirect('home')

@login_required
@never_cache
def agregar_conductor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido1 = request.POST.get('apellido1')
        apellido2 = request.POST.get('apellido2')

        try:
            conductor = Conductor.objects.create(
                nombre=nombre,
                apellido1=apellido1,
                apellido2=apellido2,
            )
            messages.success(request, 'Conductor agregado exitosamente.')
            return redirect('crud_conductores')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('agregar_conductor')
    return render(request, 'agregar_conductor.html')

@login_required
@never_cache
def agregar_camion(request):
    if request.method == 'POST':
        modelo = request.POST.get('modelo')
        tipoMarca = request.POST.get('tipoMarca')
        placa = request.POST.get('placa')

        try:
            camion = Camion.objects.create(
                modelo=modelo,
                tipoMarca=tipoMarca,
                placa=placa,
            )
            messages.success(request, 'Camión agregado exitosamente.')
            return redirect('crud_camion')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('agregar_camion')
    return render(request, 'agregar_camion.html')


@login_required
@never_cache
def eliminar_conductor(request, conductor_id):
    conductor = get_object_or_404(Conductor, id=conductor_id)
    try:
        conductor.delete()
        messages.success(request, 'Conductor eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    return redirect('crud_conductores')

@login_required
@never_cache
def eliminar_camion(request, camion_id):
    camion = get_object_or_404(Camion, id=camion_id)
    try:
        camion.delete()
        messages.success(request, 'Camión eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    return redirect('crud_camion')

@login_required
@never_cache
def editar_conductor(request, conductor_id):
    conductor = get_object_or_404(Conductor, id=conductor_id)
    
    if request.method == 'POST':
        conductor.nombre = request.POST.get('nombre')
        conductor.apellido1 = request.POST.get('apellido1')
        conductor.apellido2 = request.POST.get('apellido2') 
        
        try:
            conductor.save()
            messages.success(request, 'Conductor editado exitosamente.')
            return redirect('crud_conductores')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('editar_conductor', conductor_id=conductor_id)
    
    return render(request, 'editar_conductor.html', {'conductor': conductor})

@login_required
@never_cache
def editar_camion(request, camion_id):
    camion = get_object_or_404(Camion, id=camion_id)
    
    if request.method == 'POST':
        camion.modelo = request.POST.get('modelo')
        camion.tipoMarca = request.POST.get('tipoMarca')
        camion.placa = request.POST.get('placa') 
        
        try:
            camion.save()
            messages.success(request, 'Camión editado exitosamente.')
            return redirect('crud_camion')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('editar_camion', camion_id=camion_id)
    
    return render(request, 'editar_camion.html', {'camion': camion})


@login_required
@never_cache
def ver_info_conductor(request, conductor_id):
    conductor = get_object_or_404(Conductor, id=conductor_id)
    return render(request, 'ver_info_conductor.html', {'conductor': conductor})
 

@login_required
@never_cache
def ver_info_camion(request, camion_id):
    camion = get_object_or_404(Camion, id=camion_id)
    return render(request, 'ver_info_camion.html', {'camion': camion})
 

