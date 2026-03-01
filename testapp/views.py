from django.shortcuts import render,redirect
from datetime import datetime
from .models import Question, UserScore, Category, Difficulty,Quiz
from .forms import QuizForm, QuizFilterForm,RegisterForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

@login_required
def quiz_view(request, category_id, difficulty_id):
    questions = Question.objects.filter(category_id=category_id, difficulty_id=difficulty_id)
    quiz = Quiz.objects.get(category_id=category_id, difficulty_id=difficulty_id)
    form = QuizForm(questions=questions)
    
    
    

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            results = []
            score = 0
            for question in questions:
                selected_choice = form.cleaned_data.get(f'question_{question.id}')
                
                correct = selected_choice.is_correct
                if correct:
                    score += 1
                
                results.append({
                    'question': question.text,
                    'selected': selected_choice.text,
                    'is_correct': correct,
                    'id':Quiz.id
                    
                })
          
            # Save user score
           
            UserScore.objects.create(
                user=request.user,
                score=score,
                total=len(questions),
                category_id=category_id,
                difficulty_id=difficulty_id
            )
            request.session['last_score'] = score
            percentage = round((score / len(questions)) * 100, 2)

            return render(request, 'testapp/quiz_result.html', {
                'results': results,
                'score': score,
                'percentage': percentage,
                'total': len(questions),
                'username': request.user.username,
               'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
               'quiz_id': quiz.id,
            })

    return render(request, 'testapp/quiz.html', {'form': form})



@login_required
def quiz_filter_view(request):
    if request.method == 'POST':
        form = QuizFilterForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            difficulty = form.cleaned_data['difficulty']
            return redirect('quiz', category_id=category.id, difficulty_id=difficulty.id)
    else:
        form = QuizFilterForm()
    return render(request, 'testapp/quiz_filter.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    # Optional: Redirect to OAuth provider logout URL
    # e.g., Google does not support full logout, but others might
    return redirect('/login')

def home(request):
    return render(request, 'testapp/Home.html')



# certificate code 
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML
import tempfile
from datetime import date
from django.shortcuts import get_object_or_404

import os
def generate_certificate_pdf(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user = request.user  # assuming login is required

    # Fetch score from session or database depending on your logic
    score = request.session.get('last_score')  # e.g., request.session.get('last_score')
    print(score)
    total = quiz.questions.count()+2
    percentage = int((score / total) * 100)

    context = {
        'user_first_name': user.first_name,
        'user_last_name': user.last_name,
        'quiz_title': quiz.name,
        'score': score,
        'total': total,
        'percentage': percentage,
        'date_completed': date.today().strftime('%B %d, %Y'),
    }

    template = get_template('testapp/certificate.html')
    html_string = template.render(context) 

    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file_path = temp_file.name

    try:
        HTML(string=html_string).write_pdf(target=temp_file_path)

        with open(temp_file_path, 'rb') as pdf_file:
            pdf = pdf_file.read()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificate_{user.username}.pdf"'
        return response

    finally:
        os.remove(temp_file_path)  



