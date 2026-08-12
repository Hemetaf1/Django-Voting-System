from voting.models import Project, Vote


MAX_NON_ART = 3
MAX_ART     = 1

def categorize(project):
    return 'art' if project.is_artwork else 'non'

def votes_by_ip(ip):
    from .models import Vote
    qs = Vote.objects.filter(ip_address=ip)
    counter = {'art': qs.filter(project__is_artwork=True).count(),
               'non': qs.filter(project__is_artwork=False).count()}
    return counter

def can_vote(ip, project_id):
    project = Project.objects.get(pk=project_id)
    cat = categorize(project)
    counts = votes_by_ip(ip)
    limit = MAX_ART if cat=='art' else MAX_NON_ART
    if counts[cat] >= limit:
        return False, "حداکثر تعداد رأی در این بخش تکمیل شده است."
    return True, "ok"

def record_vote(ip, project_id):
    Vote.objects.create(project_id=project_id, ip_address=ip)



#  hemetaf
import openpyxl
from django.http import HttpResponse
from .models import Vote  # مطمئن شو مدل Vote وجود داره، اسمشو تغییر بده اگه فرق داره

def export_votes_xlsx():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Votes"

    # عنوان ستون‌ها
    ws.append(["ID", "User", "Choice", "Date"])

    # گرفتن دیتا از دیتابیس
    for vote in Vote.objects.all():
        ws.append([
            vote.id,
            str(vote.user),  # بستگی داره به مدل چطور تعریف شده
            str(vote.choice),
            vote.created_at.strftime("%Y-%m-%d %H:%M")  # فرض کردیم فیلد تاریخ این شکلیه
        ])

    # ساخت فایل اکسل در رم و ارسال به عنوان دانلود
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="votes.xlsx"'
    wb.save(response)
    return response
