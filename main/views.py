from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Subject, Test, Question, TestResult, VideoLesson, Formula, Book

def home(request):
    return render(request, 'home.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Бұл логин бос емес')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Құпия сөздер сәйкес келмейді')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Логин немесе құпия сөз қате')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def tests(request):
    # Сынып бойынша тесттерді бөлу
    tests_grade_5 = Test.objects.filter(subject__grade=5)
    tests_grade_6 = Test.objects.filter(subject__grade=6)
    results = TestResult.objects.filter(user=request.user)
    completed_tests = {r.test_id: r for r in results}
    
    return render(request, 'tests.html', {
        'tests_grade_5': tests_grade_5,
        'tests_grade_6': tests_grade_6,
        'completed_tests': completed_tests
    })

@login_required
def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all()
    
    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            if user_answer == question.correct:
                score += question.points
        
        total = sum(q.points for q in questions)
        percentage = (score / total) * 100
        passed = percentage >= test.passing_score
        
        TestResult.objects.create(
            user=request.user,
            test=test,
            score=score,
            total=total,
            percentage=percentage,
            passed=passed
        )
        
        return render(request, 'test_result.html', {
            'test': test,
            'score': score,
            'total': total,
            'percentage': percentage,
            'passed': passed
        })
    
    return render(request, 'test_detail.html', {
        'test': test,
        'questions': questions
    })

@login_required
def videos(request, grade=None):
    # Сынып бойынша видеосабақтарды бөлу
    videos_grade_5 = VideoLesson.objects.filter(subject__grade=5).order_by('order')
    videos_grade_6 = VideoLesson.objects.filter(subject__grade=6).order_by('order')
    
    return render(request, 'videos.html', {
        'videos_grade_5': videos_grade_5,
        'videos_grade_6': videos_grade_6
    })

@login_required
def formulas(request, grade=None):
    # Сынып бойынша формулаларды бөлу
    formulas_grade_5 = Formula.objects.filter(subject__grade=5)
    formulas_grade_6 = Formula.objects.filter(subject__grade=6)
    
    return render(request, 'formulas.html', {
        'formulas_grade_5': formulas_grade_5,
        'formulas_grade_6': formulas_grade_6
    })

@login_required
def library(request):
    books_grade_5 = Book.objects.filter(subject__grade=5)
    books_grade_6 = Book.objects.filter(subject__grade=6)
    return render(request, 'library.html', {
        'books_grade_5': books_grade_5,
        'books_grade_6': books_grade_6
    })