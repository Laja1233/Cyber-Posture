from django.db import models
from django_quill.fields import QuillField
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from django.utils.text import slugify
from django.core.validators import EmailValidator

# Create your models here.
# Programs for each companies.
# class Vulnerabilities(models.Model):
#     name = models.CharField(blank=False, null=False, )

class Program(models.Model):
    VULNERABILITY_CHOICES = [
        ( 'xss', ' Cross-Site Scripting (XSS)' ),
        ( 'sql-injection', 'SQL Injection'),
        ( 'authentication', 'Authentication Bypass' ),
        ( 'authorization', 'Authorization Issues' ),
        ( 'data-exposure', 'Data Exposure' ),
        ( 'rce', 'Remote Code Execution' )
    ]
    PROGRAM_TYPE_CHOICES = [
        ('', 'Select program type'),
        ('public', 'Public Program (Open to all researchers)'),
        ('private', 'Private Program (Invite-only)'),
        ('hybrid', 'Hybrid (Start private, go public later)')
   ]
    PROGRAM_RANGES_CHOICE = (
        ('5k-15k', '$5,000 - $15,000/year'),
        ('15k-50k', '$15,000 - $50,000/year'),
        ('50k-100k', '$50,000 - $100,000/year'),
        ('100k', '$100,000+/year')
    )
    TIMEFRAME_CHOICES = [
        ('', 'Select timeframe'),
        ('asap', 'ASAP (Within 2 weeks)'),
        ('1-month', 'Within 1 month'),
        ('2-3-months', '2-3 months'),
        ('6-month', '6+ months'),
        ('planning', 'Still planning')
    ]
    # Program's assets and scope
    target_asset = models.TextField(null=False, blank=False, verbose_name=_('Target Assets and URLs'))
    vulnerability_interest = MultiSelectField(choices=VULNERABILITY_CHOICES, max_length=150, null=False, blank=False, verbose_name=_('Vulnerability Types of Interest'))
    # Program Configuration
    program_type = models.CharField(choices=PROGRAM_TYPE_CHOICES, max_length=150, blank=False, null=False, verbose_name=_('Program type'))
    program_range = models.CharField(choices=PROGRAM_RANGES_CHOICE, default='5k-15k',max_length=100, blank=False, null=False, verbose_name=_('Program range'))
    timeframe = models.CharField(choices=TIMEFRAME_CHOICES, max_length=100, blank=False, null=False, verbose_name=_('Program timeframe'))
    description_and_goals = QuillField(blank=True, null= True, verbose_name=_('Description and Goal'))
    compliance_requirement = models.TextField(blank=True, null=True, verbose_name=_('Compliance requirements'))
    request_questions = models.TextField(blank=True, null=True, verbose_name=_("Requests or questions"))
    # company = models.OneToOneField
    def __str__(self):
        return 'Company: "%s" "%s" program ' %(self.company, self.program_type)

    class Meta:
        verbose_name_plural = _('Programs')

# Companies Model / Database
class Company(models.Model):
    INDUSTRY_CHOICES = (
        ('', 'Select your industry'),
        ('fintech', 'Financial Technology'),
        ('healthcare', 'Healthcare'),
        ('ecommerce', 'E-commerce'),
        ('saas', 'Software as a Service'),
        ('gaming', 'Gaming'),
        ('education', 'Education'),
        ('government', 'Government'),
        ('cryptocurrency', 'Cryptocurrency'),
        ('social-media', 'Social Media'),
        ('iot', 'Internet of Things'),
        ('other', 'Other')
    )
    SIZE_CHOICES = (
        ('', 'Select company size'),
        ('startup', 'Startup (1-10 employees)'),
        ('small' , 'Small (11-50 employees)'),
        ('medium', 'Medium (51-200 employees)'),
        ('large', 'Large (201-1000 employees)'),
        ('enterprise', 'Enterprise (1000+ employees)')
    )
    company_name = models.CharField(max_length=150, blank=False, null=False, verbose_name=_('Company name'))
    # Company industry
    industry = models.CharField(choices=INDUSTRY_CHOICES, blank=False, null=False, verbose_name=_('Industry'))
    # Company size
    size = models.CharField(choices=SIZE_CHOICES, blank=False, null=False, verbose_name=_('Company size'))
    # Company website
    website = models.URLField(blank=False, null=False, verbose_name=_('Company website')) 
    # Company headquarter
    headquarter = models.CharField(blank=False, null=False, verbose_name=_('Company headquarter'))
    # Company program
    program = models.OneToOneField(Program, on_delete=models.CASCADE, blank=False, null=False, verbose_name=_('Company Program'), related_name='company')
    slug = models.SlugField(verbose_name=_("Slug URL"))

    class Meta:
        verbose_name_plural = _('Companies')

    def __str__(self):
        return self.company_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.company_name)
        super().save(*args, **kwargs)

class Reports(models.Model):
    VULNERABILITY_SEVERITY_CHOICES = [
        ('', 'Select severity'),
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    VULNERABILITY_TYPE_CHOICES = [
        ('', 'Select vulnerability type'),
        ('rce', 'Remote Code Execution'),
        ('sqli', 'SQL Injection'),
        ('xss', 'Cross-Site Scripting (XSS)'),
        ('csrf', 'Cross-Site Request Forgery'), 
        ('auth', 'Authentication Issues'),
        ('authz', 'Authorization Issues'),
        ('data-exposure', 'Data Exposure'),
        ('session', 'Session Management'),
        ('crypto', 'Cryptographic Issues'),
        ('business-logic', 'Business Logic Flaw'),
        ('other', 'Other')
    ]
    company = models.OneToOneField(Company, on_delete=models.CASCADE,blank=False, null= False, verbose_name=_('Company'))
    # program = models.OneToOneField(Program, on_delete=models.CASCADE, blank=False, null= False, verbose_name=_('Program'))
    author = models.CharField(max_length=150, null= False, blank=False, verbose_name=_('Full Name'))
    email = models.EmailField(max_length=150, blank=False, null=False, validators=[EmailValidator()], verbose_name=_('Email'))
    phone_number = models.CharField(max_length=15, null=False, blank=False, verbose_name=_('Phone Number'))
    severity_level = models.CharField(choices=VULNERABILITY_SEVERITY_CHOICES, blank=False, null=False, verbose_name=_('Severity Level'))
    vulnerability_type = models.CharField(choices=VULNERABILITY_TYPE_CHOICES, blank=False, null=False, verbose_name=_('Vulnerability Type'))
    vulnerability_title = models.CharField(max_length=150, blank=False, null=False, verbose_name=_('Vulnerability Title'))
    affected_url = models.URLField(null=False, blank= False, verbose_name=_('Affected URL/System'))
    description = models.TextField(null= False, blank= False, verbose_name=_('Description'))
    steps_to_reproduce = models.TextField(null= False, blank= False, verbose_name=_('Steps to reproduce'))
    business_impact = models.TextField(null= False, blank= False, verbose_name=_('Business Impact'))
    recommended_mitigation = models.TextField(null= True, blank= True, verbose_name=_('Recommended Mitigation'))
    tools_and_method = models.CharField(null= True, blank= True, verbose_name=_('Tools and Methods used'))
    discovery_timeline = models.CharField(null= True, blank= True, verbose_name=_('Discovery Mitigation'))
    notes = models.TextField(null= True, blank= True, verbose_name=_('Additional Notes'))
    created = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.vulnerability_title} sent by {self.author}'

    class Meta:
        verbose_name_plural = 'Reports'

    