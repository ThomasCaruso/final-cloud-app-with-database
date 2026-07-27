from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Instructor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_time", models.BooleanField(default=True)),
                ("total_learners", models.IntegerField(default=0)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Learner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("occupation", models.CharField(choices=[("student", "Student"), ("developer", "Developer"), ("data_scientist", "Data Scientist"), ("dba", "Database Administrator")], default="student", max_length=20)),
                ("social_link", models.URLField(blank=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Online course", max_length=100)),
                ("image", models.ImageField(blank=True, upload_to="course_images/")),
                ("description", models.TextField()),
                ("pub_date", models.DateField(blank=True, null=True)),
                ("total_enrollment", models.IntegerField(default=0)),
                ("instructors", models.ManyToManyField(blank=True, to="onlinecourse.instructor")),
            ],
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="Lesson", max_length=200)),
                ("order", models.PositiveIntegerField(default=0)),
                ("content", models.TextField()),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lessons", to="onlinecourse.course")),
            ],
            options={"ordering": ["order", "id"]},
        ),
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date_enrolled", models.DateField(default=django.utils.timezone.now)),
                ("mode", models.CharField(choices=[("audit", "Audit"), ("honor", "Honor"), ("beta", "Beta")], default="audit", max_length=5)),
                ("rating", models.FloatField(default=5.0)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="onlinecourse.course")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name="enrollment",
            constraint=models.UniqueConstraint(fields=("user", "course"), name="unique_enrollment"),
        ),
        migrations.AddField(
            model_name="course",
            name="users",
            field=models.ManyToManyField(blank=True, through="onlinecourse.Enrollment", to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question_text", models.CharField(max_length=1000)),
                ("grade", models.PositiveIntegerField(default=1)),
                ("lesson", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="questions", to="onlinecourse.lesson")),
            ],
        ),
        migrations.CreateModel(
            name="Choice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("choice_text", models.CharField(max_length=500)),
                ("is_correct", models.BooleanField(default=False)),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="choices", to="onlinecourse.question")),
            ],
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                ("choices", models.ManyToManyField(blank=True, to="onlinecourse.choice")),
                ("enrollment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="submissions", to="onlinecourse.enrollment")),
            ],
        ),
    ]
