from django.db import models

class Project(models.Model):
    version = models.CharField(verbose_name='Версия', max_length=20)
    description = models.TextField(verbose_name='Описание')
    class Meta:
        verbose_name = 'Описание' 
        verbose_name_plural = 'Описание' 
    def __str__(self):
        return f'{self.version} - {self.description}'

class Developer(models.Model):
    name = models.CharField(verbose_name='Имя разработчика', max_length=100)
    github_profile = models.URLField(verbose_name='Профиль GitHub', blank=True, null=True)
    class Meta:
        verbose_name = 'Разработчика'  
        verbose_name_plural = 'Разработчики' 
    def __str__(self):
         return f'{self.name}' 

class FAQ(models.Model):
    question = models.CharField(verbose_name='Вопрос', max_length=255)
    answer = models.TextField(verbose_name='Ответ')
    class Meta:
        verbose_name = 'Вопрос - ответ'  
        verbose_name_plural = 'Вопросы - ответы' 
    def __str__(self):
        return f'{self.question} - {self.answer}' 