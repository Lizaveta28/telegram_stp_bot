from models.models import Section, Type, SiteUser


def create_section_struct():
    sec1 = Section(name="Тестовая секция", click_count=0)
    sec1.save()
    sec2 = Section(name="Вложенная секция", click_count=0, parent_section=sec1)
    sec2.save()

    type1 = Type(name="Не работает что-то", click_count=0, section=sec2)
    type1.save()
    type2 = Type(name="Не работает оплата на сайте", click_count=0, parent_type=type1, section=sec2)
    type2.save()

    user = SiteUser(is_superuser=True, username='admin', email='test@test.com')
    user.set_password('admin')
    user.save()