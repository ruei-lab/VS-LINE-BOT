

# Create your models here.

from django.db import models

class teacher(models.Model): #定義老師數據庫模型
    ccourse = models.CharField(max_length=50, default='default_course')
    csemester=models.CharField(max_length=50, null=False)
    cgrade=models.CharField(max_length=50, default=0)
    cName=models.CharField(max_length=20, null=False) #字串型別欄位
    cGender=models.CharField(max_length=4, default='M', null=False)
    cEmail=models.EmailField(max_length=100, blank=True, default='')
    cdescription = models.TextField(max_length=2000,null=False,blank=False)

    def __str__(self) -> str:
        return self.cName

class teacher_second(models.Model):
    acourse = models.CharField(max_length=50, default='default_course')
    asemester=models.CharField(max_length=50, null=False)
    agrade=models.CharField(max_length=50, default=0)
    aName=models.CharField(max_length=20, null=False) #字串型別欄位
    aGender=models.CharField(max_length=4, default='M', null=False)
    aEmail=models.EmailField(max_length=100, blank=True, default='')
    adescription = models.TextField(max_length=2000,null=False,blank=False)

    def __str__(self) -> str:
        return self.aName
    
class teacher_third(models.Model):
    acourse = models.CharField(max_length=50, default='default_course')
    asemester=models.CharField(max_length=50, null=False)
    agrade=models.CharField(max_length=50, default=0)
    aName=models.CharField(max_length=20, null=False) #字串型別欄位
    aGender=models.CharField(max_length=4, default='M', null=False)
    aEmail=models.EmailField(max_length=100, blank=True, default='')
    adescription = models.TextField(max_length=2000,null=False,blank=False)

    def __str__(self) -> str:
        return self.aName
    
class teacher_fourth(models.Model):
    acourse = models.CharField(max_length=50, default='default_course')
    asemester=models.CharField(max_length=50, null=False)
    agrade=models.CharField(max_length=50, default=0)
    aName=models.CharField(max_length=20, null=False) #字串型別欄位
    aGender=models.CharField(max_length=4, default='M', null=False)
    aEmail=models.EmailField(max_length=100, blank=True, default='')
    adescription = models.TextField(max_length=2000,null=False,blank=False)

    def __str__(self) -> str:
        return self.aName
    
class teacher_fifth(models.Model):
    acourse = models.CharField(max_length=50, default='default_course')
    asemester=models.CharField(max_length=50, null=False)
    agrade=models.CharField(max_length=50, default=0)
    aName=models.CharField(max_length=20, null=False) #字串型別欄位
    aGender=models.CharField(max_length=4, default='M', null=False)
    aEmail=models.EmailField(max_length=100, blank=True, default='')
    adescription = models.TextField(max_length=2000,null=False,blank=False)

    def __str__(self) -> str:
        return self.aName

class teacher_sixth(models.Model):
    acourse = models.CharField(max_length=50, default='default_course')
    asemester=models.CharField(max_length=50, null=False)
    agrade=models.CharField(max_length=50, default=0)
    aName=models.CharField(max_length=100, null=False) #字串型別欄位
    aGender=models.CharField(max_length=4, default='M', null=False)
    aEmail=models.EmailField(max_length=100, blank=True, default='')
    adescription = models.TextField(max_length=2000,null=False,blank=False)

    def __str__(self) -> str:
        return self.aName

class teacher_seventh(models.Model):
    acourse = models.CharField(max_length=50, default='default_course')
    asemester=models.CharField(max_length=50, null=False)
    agrade=models.CharField(max_length=50, default=0)
    aName=models.CharField(max_length=100, null=False) #字串型別欄位
    aGender=models.CharField(max_length=4, default='M', null=False)
    aEmail=models.EmailField(max_length=100, blank=True, default='')
    adescription = models.TextField(max_length=2000,null=False,blank=False)

    def __str__(self) -> str:
        return self.aName
    
class teacher_eighth(models.Model):
    acourse = models.CharField(max_length=50, default='default_course')
    asemester=models.CharField(max_length=50, null=False)
    agrade=models.CharField(max_length=50, default=0)
    aName=models.CharField(max_length=20, null=False) #字串型別欄位
    aGender=models.CharField(max_length=4, default='M', null=False)
    aEmail=models.EmailField(max_length=100, blank=True, default='')
    adescription = models.TextField(max_length=2000,null=False,blank=False)

    def __str__(self) -> str:
        return self.aName

class teacher_data(models.Model):
    name=models.CharField(max_length=50, null=False)
    position=models.CharField(max_length=10, null=False)
    strengths=models.TextField(max_length=2000,null=False,blank=False)
    tel=models.CharField(max_length=100, null=False)
    mail=models.EmailField(max_length=100, blank=True, default='')
    website = models.URLField(max_length=200, blank=True, default='')

    def __str__(self) -> str:
        return self.name


class syllabus(models.Model):
    ncourse=models.CharField(max_length=50, default='default_course')
    nname=models.CharField(max_length=50, null=False)
    nsemester=models.CharField(max_length=50, null=False)
    nbook=models.CharField(max_length=50, default='default_book')
    nschedule=models.TextField(max_length=2000,null=False,blank=False)
    ngrade = models.TextField(max_length=2000,null=False,blank=False)

    def __str__(self) -> str:
        return self.ncourse
    
class syllabus_second(models.Model):
    ncourse=models.CharField(max_length=50, default='default_course')
    nname=models.CharField(max_length=50, null=False)
    nsemester=models.CharField(max_length=50, null=False)
    nbook=models.CharField(max_length=50, default='default_book')
    nschedule=models.TextField(max_length=2000,null=False,blank=False)
    ngrade = models.TextField(max_length=2000,null=False,blank=False)

    def __str__(self) -> str:
        return self.ncourse

class user_rating(models.Model):
    user_id = models.CharField(max_length=100)  # 儲存用戶的 ID
    user_name = models.CharField(max_length=255) # 儲存用戶的 LINE 名稱
    rating = models.IntegerField()  # 儲存用戶的評分
    created_at = models.DateTimeField(auto_now_add=True)  # 儲存評分時間
    
    def __str__(self) -> str:
        return self.user_name


























