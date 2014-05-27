from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
import models
from django.conf import settings


EMAIL_TEMPLATE = """
    <html><body>
        <h1>You've been invited to a PublicSqr project!</h1>
        <p>
            Visit the url below to join the discussion.
        </p>
        <p>
            <a href="{{domain}}/project/{{proj.id}}/?key={{key}}">http://publicsqr.com/project/{{proj.id}}/?key={{key}}</a>
        </p>
    </body></html>
    """

EMAIL_SUBJECT = "You've been invited to a PublicSqr project"

def invite_people(model_project, li_emails):
    for email in li_emails:
        usr2proj = models.UserToProject.objects.get_or_create(proj=model_project, invitation_email=email)[0]

        t = Template(EMAIL_TEMPLATE)

        c = Context({"proj": model_project, "key": usr2proj.key, "domain": settings.SITE_DOMAIN})
        message = t.render(c)
        msg = EmailMultiAlternatives(EMAIL_SUBJECT, message, "noreply@publicsqr.com", [email,])
        msg.attach_alternative(message, "text/html")
        msg.send()
