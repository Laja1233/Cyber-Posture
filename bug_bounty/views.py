from django.shortcuts import render
from bug_bounty.models import Company, Program, Reports
from bug_bounty.forms import ProgramModelForm, CompanyModelForm, ReportModelForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
# Create your views here.

# View for bug bounty landing page
def parse_time(report):
    days_diff = timezone.now() - report.created
    return days_diff.days

def bug_bounty_landing(request):
    companies = Company.objects.all()
    return render(request, "bug_bounty/bug_bounty_landing.html", {
        'companies': companies
    })

# View for bug bounty registration page
def bounty_registration(request):
    if request.method == 'POST':
        company_form = CompanyModelForm(request.POST)
        program_form = ProgramModelForm(request.POST)
        if company_form.is_valid() and program_form.is_valid():
            program = program_form.save()
            company = company_form.save(commit=False)
            company.program = program
            company.save()
        else:
            print(company_form.errors)
            print(program_form.errors)
            print('an error')
    else:
        company_form = CompanyModelForm()
        program_form = ProgramModelForm()
    
    context = {
        'company_form' : company_form,
        'program_form' : program_form
    }

    return render(request, "bug_bounty/bugbounty_reg.html", context)

# View for bug bounty submissions page, to be viewed by admins
def bounty_submissions(request):
    reports = Reports.objects.all()
    for report in reports:
        report.days_ago = parse_time(report)
    return render(request, "bug_bounty/bug_submission.html", { 'reports' : reports })

def bounty_submissions_details(request, id):
    report = get_object_or_404(Reports, id= id)
    return render(request, "bug_bounty/bug_submission1.html", {'report' : report})

# View for bug bounty templates page
def documents_templates(request):
    return render(request, "bug_bounty/template_document.html")

# View for bug bounty ai page 
def compliance_ai(request):
    return render(request, "bug_bounty/chat_ai.html")

# View for bug bounty document verification page
def verify_document(request):
    return render(request, "bug_bounty/document_verification.html")

# View for background check
def backgroud_check(request):
    return render(request, "bug_bounty/resume.html")

# View for bug list per banks
def bug_list_bank(request, id):
    company = get_object_or_404(Company, id=id)
    program_scope = company.program.target_asset
    program_scope = program_scope.split('\n') 
    if request.method == 'POST':
        form = ReportModelForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.company = company
            report.save()
    else:
        form = ReportModelForm()
    return render(request, "bug_bounty/bug_list1.html", { 'company': company, 'program_scope': program_scope, 'form': form })

