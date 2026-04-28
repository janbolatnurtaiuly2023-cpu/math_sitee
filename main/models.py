from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField("Тақырып атауы", max_length=100)
    grade = models.IntegerField("Сынып", choices=[(5,5), (6,6)])
    icon = models.CharField("Иконка", max_length=10, default="📐")
    
    def __str__(self):
        return f"{self.grade}-сынып: {self.name}"

class Test(models.Model):
    title = models.CharField("Тест атауы", max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tests')
    description = models.TextField("Сипаттамасы")
    passing_score = models.IntegerField("Өту балы", default=50)
    time_limit = models.IntegerField("Уақыт шегі (минут)", default=30)
    
    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField("Сұрақ мәтіні")
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct = models.CharField("Дұрыс жауап", max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    points = models.IntegerField("Ұпай саны", default=1)
    
    def __str__(self):
        return self.text[:50]

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField("Алынған балл")
    total = models.IntegerField("Жалпы балл")
    percentage = models.FloatField("Пайыз")
    passed = models.BooleanField("Өтті ме")
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.test.title}"
    
class VideoLesson(models.Model):
    title = models.CharField("Видео атауы", max_length=200)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    youtube_url = models.URLField("YouTube сілтемесі")
    description = models.TextField("Сипаттамасы", blank=True)
    duration = models.CharField("Ұзақтығы", max_length=20, default="10 мин")
    order = models.IntegerField("Реттік нөмірі", default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Видеосабақ"
        verbose_name_plural = "Видеосабақтар"

class Formula(models.Model):
    title = models.CharField("Формула атауы", max_length=100)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='formulas', null=True, blank=True)
    formula_text = models.CharField("Формула мәтіні", max_length=200)
    description = models.TextField("Түсіндірмесі", blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Формула"
        verbose_name_plural = "Формулалар"

class Book(models.Model):
    title = models.CharField("Кітап атауы", max_length=200)
    author = models.CharField("Авторы", max_length=100)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='books', null=True, blank=True)
    description = models.TextField("Сипаттамасы")
    pdf_link = models.URLField("PDF сілтемесі", blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Кітап"
        verbose_name_plural = "Кітаптар"