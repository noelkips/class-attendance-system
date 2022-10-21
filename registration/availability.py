from .models import UnitRegistration
# from users.models import UserProfile


def check_availability(unit, start_date,end_date ):
    available_units = []
    register_list = UnitRegistration.objects.filter(unit=unit)
    # for student in user_list:
    #     user_year=student.year
    #     user_semester=student.semester
    for registering in register_list:
         if registering.start_date > end_date or registering.end_date < start_date:
            # if registering.user.semester == registering.unit.semester:
            available_units.append(True)
         else:
            available_units.append(False)
    return all(available_units)
