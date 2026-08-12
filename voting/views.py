from django.shortcuts import render

# Create your views here.
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse, HttpResponse
from .models import Project, Category, Vote, Feedback, Section
from .services import can_vote, record_vote, export_votes_xlsx
from django.views.decorators.http import require_POST
from django.shortcuts import render
from .models import Category, Section
import json
from .models import Category
from django.shortcuts import render
import qrcode
from io import BytesIO
from .models import Project, Vote
from django.shortcuts import get_object_or_404, render
from .models import Section
from django.utils.translation import gettext as _



@require_POST
@ratelimit(key='ip', rate='5/m', block=True)
def vote_api(request, project_id):
    ip = request.META['REMOTE_ADDR']
    ok, message = can_vote(ip, project_id)
    if not ok:
        return JsonResponse({"error": message}, status=400)
    record_vote(ip, project_id)
    return JsonResponse({"success": True})

@require_POST
def feedback_api(request):
    # save Feedback after first vote
    ...

# staff‑only export
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def export_xlsx(request):
    wb = export_votes_xlsx()
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="votes.xlsx"'
    wb.save(response)
    return response

def get_client_ip(request):
    """
    از هدر X-Forwarded-For (مثلاً وقتی پشت پروکسی هستید) استفاده می‌کند،
    وگرنه از REMOTE_ADDR.
    """
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        # ممکن است چند IP لیست شده باشد، اولین‌ش را برمی‌گردانیم
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


# def index(request):
#     # آرایهٔ حوزه‌ها از Enum
#     cats = [
#         {"value": c.value, "label": str(c.label)}
#         for c in Category
#     ]
#     # تبدیل به JSONِ امنِ UTF-8
#     cats_json = json.dumps(cats, ensure_ascii=False)

#     return render(request, "voting/index.html", {
#         "categories_json": cats_json   # ⬅️ پاس به قالب
#     })



from .models import Category, Section
import json


def index(request):
    categories = []
    for cat_value, cat_label in Category.choices:
        subs = Section.objects.filter(category=cat_value).order_by('order')
        sublist = [
            {"name": s.name, "slug": s.slug}
            for s in subs
        ]
        categories.append({
            "value": cat_value,
            "label": _(str(cat_label)),
            "subcategories": sublist
        })

    cats_data = json.dumps(categories, ensure_ascii=False)
    return render(request, "voting/index.html", {
        "cats_data": cats_data,
        "categories": categories
    })


def sections_htmx(request):
    cat = request.GET.get('cat')
    sections = Section.objects.filter(category=cat).order_by('order')
    return render(request, 'voting/partials/sections.html', {"sections": sections})



def qrcode_view(request):
    # URL اصلی سایت را در QR قرار می‌دهیم
    url = request.build_absolute_uri('/')
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf, format='PNG')
    return HttpResponse(buf.getvalue(), content_type='image/png')



def vote_view(request, project_id):
    ip = get_client_ip(request)
    project = Project.objects.get(pk=project_id)
    # count existing votes by this IP
    used = Vote.objects.filter(ip_address=ip).count()
    limit = 4 if project.is_artwork else 3
    if used >= limit:
        return HttpResponse("Rate limit exceeded", status=429)
    Vote.objects.create(project=project, ip_address=ip)
    return JsonResponse({"count": project.vote_set.count()})

def vote_count(request, project_id):
    project = Project.objects.get(pk=project_id)
    return JsonResponse({"count": project.vote_set.count()})


def subcategory_view(request, cat_value, sub_slug):
    section = get_object_or_404(Section, category=cat_value, slug=sub_slug)
    projects = section.projects.all()
    return render(request, 'voting/subcategory.html', {
        'section': section,
        'projects': projects
    })
