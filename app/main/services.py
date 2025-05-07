from app.models import Parent, Child


def add_children_to_parent(name_children: str, surname_children: str, patronymic_children: str, group_children: str,
                           user_parent: Parent, db_session):
    children = Child(name=name_children,
                     surname=surname_children,
                     patronymic=patronymic_children,
                     group=group_children,
                     parent=user_parent)

    try:
        db_session.add(children)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        return e

    return 'OK'
