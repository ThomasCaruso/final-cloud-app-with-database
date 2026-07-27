from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Choice, Course, Enrollment, Question, Submission


def course_details(request, course_id):
    course = get_object_or_404(
        Course.objects.prefetch_related("lessons__questions__choices"),
        pk=course_id,
    )
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(
            user=request.user, course=course
        ).first()
    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course, "enrollment": enrollment},
    )


@login_required
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment, _ = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )

    valid_choice_ids = set(
        Choice.objects.filter(question__lesson__course=course).values_list(
            "id", flat=True
        )
    )
    selected_choice_ids = []
    for key, value in request.POST.items():
        if not key.startswith("choice_"):
            continue
        try:
            choice_id = int(value)
        except (TypeError, ValueError):
            continue
        if choice_id in valid_choice_ids:
            selected_choice_ids.append(choice_id)

    if not selected_choice_ids:
        return HttpResponseBadRequest(
            "Select at least one answer before submitting the exam."
        )

    submission = Submission.objects.create(enrollment=enrollment)
    submission.choices.set(selected_choice_ids)
    return redirect(
        "onlinecourse:show_exam_result",
        course_id=course.id,
        submission_id=submission.id,
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission.objects.select_related("enrollment").prefetch_related("choices"),
        pk=submission_id,
        enrollment__user=request.user,
        enrollment__course=course,
    )

    selected_choice_ids = set(submission.choices.values_list("id", flat=True))
    questions = Question.objects.filter(
        lesson__course=course
    ).prefetch_related("choices")
    exam_results = []
    score = 0
    total = 0

    for question in questions:
        selected_choices = [
            choice
            for choice in question.choices.all()
            if choice.id in selected_choice_ids
        ]
        correct_choices = [
            choice for choice in question.choices.all() if choice.is_correct
        ]
        is_correct = question.is_get_score(selected_choice_ids)
        if is_correct:
            score += question.grade
        total += question.grade
        exam_results.append(
            {
                "question": question,
                "selected_choices": selected_choices,
                "correct_choices": correct_choices,
                "is_correct": is_correct,
            }
        )

    percentage = round((score / total) * 100) if total else 0
    return render(
        request,
        "onlinecourse/exam_result_bootstrap.html",
        {
            "course": course,
            "submission": submission,
            "exam_results": exam_results,
            "score": score,
            "total": total,
            "percentage": percentage,
            "passed": percentage >= 70,
        },
    )
