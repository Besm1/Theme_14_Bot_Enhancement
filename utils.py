
async def mifflin_san_geor(age, growth, weight, gender):
    '''
    Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5. 1
    Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.
    :param age: - возраст, лет
    :param growth: - рост, см
    :param weight: - вес, кг
    :param gender: - м(ужчина) или ж(енщина)
    :return: - суточная норма калорий, кал
    '''
    try:
        res = (10 * float(weight) * 10 + 6.25 * float(growth)
               - 5 * float(age)
               + (5.1 if gender[0].lower() == 'м' else (-161 if gender[0].lower() == 'ж' else None)))
    except Exception as e:
        res = f'...Упссс! Неправильные данные привели к ошибке: "{e}". Не могу рассчитать...'
    finally:
        return res


