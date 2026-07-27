# OnlineCourse Assessment Feature

Completed Django project for the IBM final assignment **Add a New Assessment Feature to an Online Course App**.

## Implemented rubric items

- `Question`, `Choice`, and `Submission` models in `onlinecourse/models.py`
- Seven model imports and `QuestionInline`, `ChoiceInline`, `QuestionAdmin`, and `LessonAdmin` in `onlinecourse/admin.py`
- Bootstrap course detail template with lessons and exam form
- `submit` and `show_exam_result` views
- URL routes for exam submission and results
- Required screenshots generated as `03-admin-site.png` and `07-final.png`

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
