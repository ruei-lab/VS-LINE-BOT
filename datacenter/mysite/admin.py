

# Register your models here.

from django.contrib import admin
from mysite.models import teacher, teacher_second, teacher_third, teacher_fourth, teacher_fifth,teacher_sixth,teacher_seventh, teacher_eighth, teacher_data
from mysite.models import syllabus, syllabus_second, user_rating
from import_export.admin import ImportExportModelAdmin



#老師資訊模組
class teacherAdmin(admin.ModelAdmin):
    list_display=('ccourse','csemester','cgrade','cName','cGender','cEmail','cdescription')
    list_filter=('ccourse','csemester') #過濾欄位
    search_fields=('ccourse',) #指定某欄位搜尋

class teacher_secondAdmin(admin.ModelAdmin):
    list_display=('acourse','asemester','agrade','aName','aGender','aEmail','adescription')
    list_filter=('acourse','asemester') #過濾欄位
    search_fields=('acourse',) #指定某欄位搜尋

class teacher_thirdAdmin(admin.ModelAdmin):
    list_display=('acourse','asemester','agrade','aName','aGender','aEmail','adescription')
    list_filter=('acourse','asemester') #過濾欄位
    search_fields=('acourse',) #指定某欄位搜尋

class teacher_fourthAdmin(admin.ModelAdmin):
    list_display=('acourse','asemester','agrade','aName','aGender','aEmail','adescription')
    list_filter=('acourse','asemester') #過濾欄位
    search_fields=('acourse',) #指定某欄位搜尋

class teacher_fifthAdmin(admin.ModelAdmin):
    list_display=('acourse','asemester','agrade','aName','aGender','aEmail','adescription')
    list_filter=('acourse','asemester') #過濾欄位
    search_fields=('acourse',) #指定某欄位搜尋

class teacher_sixthAdmin(admin.ModelAdmin):
    list_display=('acourse','asemester','agrade','aName','aGender','aEmail','adescription')
    list_filter=('acourse','asemester') #過濾欄位
    search_fields=('acourse',) #指定某欄位搜尋

class teacher_seventhAdmin(admin.ModelAdmin):
    list_display=('acourse','asemester','agrade','aName','aGender','aEmail','adescription')
    list_filter=('acourse','asemester') #過濾欄位
    search_fields=('acourse',) #指定某欄位搜尋

class teacher_eighthAdmin(admin.ModelAdmin):
    list_display=('acourse','asemester','agrade','aName','aGender','aEmail','adescription')
    list_filter=('acourse','asemester') #過濾欄位
    search_fields=('acourse',) #指定某欄位搜尋

class teacher_dataAdmin(admin.ModelAdmin):
    list_display=('name','position','strengths','tel','mail','website')
    list_filter=('name',) #過濾欄位


#教學大綱模組
class syllabusAdmin(admin.ModelAdmin):
    list_display=('ncourse','nname','nsemester','nbook','nschedule','ngrade')
    list_filter=('ncourse',)

class syllabus_secondAdmin(admin.ModelAdmin):
    list_display=('ncourse','nname','nsemester','nbook','nschedule','ngrade')
    list_filter=('ncourse',)


class user_ratingAdmin(ImportExportModelAdmin):
    list_display=('user_id','rating','created_at')
    list_filter=('rating',)
















admin.site.register(syllabus, syllabusAdmin)
admin.site.register(syllabus_second, syllabus_secondAdmin)


admin.site.register(teacher, teacherAdmin)
admin.site.register(teacher_second, teacher_secondAdmin)
admin.site.register(teacher_third, teacher_thirdAdmin)
admin.site.register(teacher_fourth, teacher_fourthAdmin)
admin.site.register(teacher_fifth, teacher_fifthAdmin)
admin.site.register(teacher_sixth, teacher_sixthAdmin)
admin.site.register(teacher_seventh, teacher_seventhAdmin)
admin.site.register(teacher_eighth, teacher_eighthAdmin)
admin.site.register(teacher_data, teacher_dataAdmin)

admin.site.register(user_rating, user_ratingAdmin)
