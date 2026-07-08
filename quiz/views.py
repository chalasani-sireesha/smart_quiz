from django.shortcuts import render,get_object_or_404,redirect
from .models import Quiz,Category
from results.models import Result
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import random

def home(request):
    categories = Category.objects.all()

    quizzes = Quiz.objects.all()

    category = request.GET.get("category")

    query = request.GET.get("q")

    if category:
        quizzes = quizzes.filter(
            category__id=category
        )

    if query:
        quizzes = quizzes.filter(
            title__icontains=query
        )

    return render(
        request,
        "home.html",
        {
            "quizzes": quizzes,
            "categories": categories,
            "query": query
        }
    )
    

    
@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.question_set.all())

    random.shuffle(questions)

    questions = questions[:10]

   

    existing_result = Result.objects.filter(
        user=request.user,
        quiz=quiz
    ).exists()

    if existing_result:
        return render(
            request,
            "already_attempted.html",
        {
            "quiz": quiz
        }
        )

    

    if request.method == "POST":

        score = 0

        for question in questions:

            selected = request.POST.get(str(question.id))

            if selected == question.correct_answer:
                score += 1

        result = Result.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=questions.count()
        )

        answers = []

        for question in questions:
            answers.append({
            "question": question.question,
            "selected": request.POST.get(str(question.id)),
            "correct": question.correct_answer,
        })

        return render(
            request,
            "result.html",
            {
                "result": result,
                "answers": answers,
            }
        )
    return render(
        request,
        "quiz_detail.html",
        {
            "quiz": quiz,
            "questions": questions,
        }
    )

    
@login_required
def result(request):

    latest = Result.objects.filter(
        user=request.user
    ).last()

    return render(
        request,
        "result.html",
        {
            "result": latest
        }
    )

@login_required
def leaderboard(request):

    results = Result.objects.all().order_by("-score", "created_at")

    context = {
        "results": results
    }

    return render(request, "leaderboard.html", context)


@login_required
def download_certificate(request):

    latest = Result.objects.filter(
        user=request.user
    ).last()

    if latest is None:
        return HttpResponse("No quiz completed yet.")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="certificate.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(300, 800, "SMART QUIZ")

    p.setFont("Helvetica", 18)
    p.drawCentredString(300, 760, "Certificate of Achievement")

    p.setFont("Helvetica", 14)
    p.drawCentredString(
        300,
        700,
        f"This certifies that {request.user.username}"
    )

    p.drawCentredString(
        300,
        670,
        f"has completed the quiz: {latest.quiz.title}"
    )

    p.drawCentredString(
        300,
        640,
        f"Score: {latest.score}/{latest.total_questions}"
    )

    p.save()

    return response

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

# Create your views here.
