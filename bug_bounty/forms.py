from django.forms import ModelForm
from django import forms
from bug_bounty.models import Company, Program, Reports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Field, HTML

class CompanyModelForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['program', 'slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['company_name'].widget.attrs.update({
            'id': 'companyName',
            'class': 'form-control'
            })
        self.fields['industry'].widget.attrs.update({
            'class': 'select-control form-control',
            'id' : 'industry'
            })
        self.fields['size'].widget.attrs.update({
            'class' : 'form-control select-control',
            'id' : 'companySize'
        })
        self.fields['website'].widget.attrs.update({
            'class': 'form-control',
            'id' : 'website',
            'placeholder': 'https://your-company.com'
        })
        self.fields['headquarter'].widget.attrs.update({
            'class' : 'form-control',
            'id' : "headquarters",
            'placeholder': 'City, Country'
        })


class ProgramModelForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = '__all__'
        widgets = {
            'vulnerability_interest': forms.CheckboxSelectMultiple,
            'program_range' : forms.RadioSelect
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['target_asset'].widget.attrs.update({
            'id': 'targetAssets',
            'class' : 'form-control',
            'placeholder' : """List the applications, websites, APIs, or systems you want tested: \n • https://app.yourcompany.com \n • https://api.yourcompany.com \n • Mobile app: YourApp (iOS/Android)""",
            'rows' : 4
        })
        self.fields['program_type'].widget.attrs.update({
            'class' : 'form-control select-control',
            'id' : 'programType'
        })
        self.fields['timeframe'].widget.attrs.update({
            'class' : 'form-control select-control',
            'id' : 'timeframe'
        })
        self.fields['description_and_goals'].widget.attrs.update({
            'id' : 'editor'
        })
        self.fields['description_and_goals'].widget.attrs.update({
            'id' : 'editor',
            'data-placeholder' : 'Describe your security goals, any specific concerns, compliance requirements, and what you hope to achieve with your bug bounty program.'
        })
        self.fields['compliance_requirement'].widget.attrs.update({
            'class' : 'form-control',
            'rows' : 3,
            'id' : 'compliance',
            'placeholder' : 'e.g., GDPR, HIPAA, SOC 2, PCI DSS, etc.'
        })
        self.fields['request_questions'].widget.attrs.update({
            'class' : 'form-control',
            'rows' : 3,
            'id' : 'specialRequests',
            'placeholder' : "Any specific requirements, questions about our platform, or additional services you're interested in..."
        })

class ReportModelForm(forms.ModelForm):
    class Meta:
        model = Reports
        fields = '__all__'
        # exclude = ['program']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['author'].widget.attrs.update({
            'id' : 'reporterName',
            'class' : 'form-control',
            'required': True
        })
        self.fields['email'].widget.attrs.update({
            'id' : 'email',
            'class' : 'form-control'
        })
        self.fields['phone_number'].widget.attrs.update({
            'id' : 'phone',
            'class' : 'form-control',
            'placeholder' : '+234 xxx xxx xxxx'
        })
        self.fields['company'].widget.attrs.update({
            'id' : 'company',
            'class' : 'form-control',
            'placeholder': 'Optional'
        })
        self.fields['severity_level'].widget.attrs.update({
            'id' : 'severity',
            'class' : 'form-control select-control'
        })
        self.fields['vulnerability_type'].widget.attrs.update({
            'class' : 'form-control select-control',
            'id' : 'category'
        })
        self.fields['vulnerability_title'].widget.attrs.update({
            'class' : 'form-control',
            'id' : 'title',
            'placeholder' : "Provide a clear, descriptive title for the vulnerability"    
        })
        self.fields['affected_url'].widget.attrs.update({
            'class' : 'form-control',
            'id' : 'url',
            'placeholder' : "https://example.wemabank.com/vulnerable-endpoint"
        })
        self.fields['description'].widget.attrs.update({
            'class' : 'form-control',
            'id' : 'description',
            'placeholder' : "Provide a detailed technical description of the vulnerability, including how it works and what makes it exploitable...",
            'rows' : 5
        })
        self.fields['steps_to_reproduce'].widget.attrs.update({
            'class' : 'form-control',
            'id' : 'reproduction',
            'placeholder' : """Provide clear, step-by-step instructions to reproduce the vulnerability; \n 1. Navigate to https://... \n 2. Login with credentials... \n 3. Click on... \n 4. Observe that...""",
            'rows' : 6
        })
        self.fields['business_impact'].widget.attrs.update({
            'class' : 'form-control',
            'id' : 'impact',
            'placeholder' : "Describe the potential impact on Wema Bank's operations, customer data security, financial transactions, etc.",
            'rows' : 4
        })
        self.fields['recommended_mitigation'].widget.attrs.update({
            'class' : 'form-control',
            'id' : 'mitigation',
            'rows' : 3,
            'placeholder' : "Optional: Suggest how this vulnerability could be fixed or mitigated"
        })
        self.fields['tools_and_method'].widget.attrs.update({
            'class' : 'form-control',
            'id' : 'tools',
            'placeholder' : "e.g., Burp Suite, OWASP ZAP, Custom scripts, Manual testing"
        })
        self.fields['discovery_timeline'].widget.attrs.update({
            'class' : 'form-control',
            'id' : 'timeline',
            'placeholder' : "When did you first discover this vulnerability?"
        })
        self.fields['notes'].widget.attrs.update({
            'class' : 'form-control',
            'id' : 'additionalNotes',
            'placeholder' : "Any additional context, related findings, or notes you'd like to share...",
            "rows" : 3
        })