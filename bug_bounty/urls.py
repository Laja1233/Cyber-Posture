from django.urls import path
from bug_bounty import views

app_name="bug_bounty"
urlpatterns = [
    path('landing/', views.bug_bounty_landing, name="bug_bounty_landing"),
    path('registration/', views.bounty_registration, name="bug_bounty_registration"),
    path('submissions/', views.bounty_submissions, name="bug_bounty_submissions"),
    path('submissions/<int:id>/details', views.bounty_submissions_details, name="bug_bounty_submission_details"),
    path('template_document/', views.documents_templates, name="documents_template"),
    path('chat/', views.compliance_ai, name="compliance_ai"),
    path('verify-document/', views.verify_document, name="verify_document"),
    path('resume/', views.backgroud_check, name="resume"),
    path('<int:id>/bug-list/', views.bug_list_bank, name="bug_list_bank"),
]
