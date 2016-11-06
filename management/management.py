from models.models import Stp, User, StpSection, Section
def PromoteUser(user_id, sections):
    user = User.get(id=user_id)
    user.state = 'stp_initial'
    user.save()
    stp = Stp.get_or_create(user=user, staff_id=1, is_active=True)[0]
    stp.save()
    [StpSection.get_or_create(stp=stp, section=section, importance=1) for section in sections]

PromoteUser(1, [1,2])