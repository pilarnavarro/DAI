from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Autor, Libro, Prestamo
from .forms import AutorForm, LibroForm, PrestamoForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    return render(request,'base.html',{})

def listaAutores(request):
    autores=Autor.objects.all().order_by('nombre')
    return render(request, 'autores.html', {'autores':autores})

def listaLibros(request):
    libros=Libro.objects.all().order_by('titulo')
    return render(request, 'libros.html', {'libros':libros})

def listaPrestamos(request):
    prestamos=Prestamo.objects.all().order_by('fecha')
    return render(request, 'prestamos.html', {'prestamos':prestamos})

@staff_member_required
def nuevoAutor(request):
    error=None
    if request.method=="POST":
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('autores')
        else:
            error=form.errors
    else:
        form = AutorForm()
    return render(request,'nuevo_autor.html', {'form':form,'error':error} )

@staff_member_required
def nuevoLibro(request):
    error=None
    if request.method=="POST":
        form = LibroForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('libros')
        else:
            error=form.errors
    else:
        form = LibroForm()
    return render(request,'nuevo_libro.html', {'form':form,'error':error})

@login_required
def nuevoPrestamo(request):
    error=None
    if request.method=="POST":
        form = PrestamoForm(request.POST)
        if form.is_valid():
            pr=form.save(commit=False)
            pr.fecha=timezone.now()
            pr.usuario=request.user
            pr.save()
            return redirect('prestamos')
        else:
            error=form.errors
    else:
        form = PrestamoForm()
    return render(request,'nuevo_prestamo.html', {'form':form,'error':error})

@staff_member_required
def editarAutor(request, pk):
    error=None
    autor=Autor.objects.get(id=pk)
    if request.method=="POST":
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect('autores')
        else:
            error=form.errors
    else:
        form = AutorForm(instance=autor)
    return render(request,'nuevo_autor.html', {'form':form,'error':error})

@staff_member_required
def editarLibro(request, pk):
    error=None
    libro=Libro.objects.get(codigo=pk)
    if request.method=="POST":
        form = LibroForm(request.POST,request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('libros')
        else:
            error=form.errors
    else:
        form = LibroForm(instance=libro)
    return render(request,'nuevo_libro.html', {'form':form,'error':error})

@login_required
def editarPrestamo(request, pk):
    error=None
    pr=Prestamo.objects.get(id=pk)
    if request.method=="POST":
        form = PrestamoForm(request.POST, instance=pr)
        if form.is_valid():
            p = form.save(commit=False)
            if p.usuario != request.user:
                error="Sólo puede editar los préstamos realizados por usted"
            else:
                p.fecha=timezone.now()
                p.save()
                return redirect('prestamos')
        else:
            error=form.errors
    else:
        form = PrestamoForm(instance=pr)
    return render(request,'editar_prestamo.html', {'form':form,'error':error,'pk':pk})

@staff_member_required
def eliminarAutor(request, pk):
    autor=Autor.objects.get(id=pk)
    if request.method=="POST":
        autor.delete()
        return redirect('autores')
    return render(request,'borrar_autor.html', {'autor':autor})

@staff_member_required
def eliminarLibro(request, pk):
    libro=Libro.objects.get(codigo=pk)
    if request.method=="POST":
        libro.delete()
        return redirect('libros')
    return render(request,'borrar_libro.html', {'libro':libro})

@login_required
def eliminarPrestamo(request, pk):
    error=None
    prestamo=Prestamo.objects.get(id=pk)
    if request.method=="POST":
        if prestamo.usuario!=request.user:
            error="Sólo puede eliminar los préstamos realizados por usted mismo"
        else:
            prestamo.delete()
            return redirect('prestamos')
    return render(request,'borrar_prestamo.html', {'prestamo':prestamo,'error':error})
