from core.db.db import select_location_by_id, select_category_name, select_quiz_name_by_id


async def generate_quizes(rows):
    general_text = ''
    time_list = []

    for date in rows:
        quiz_date = str(date['quiz_time']).split(' ')[0]
        if not quiz_date in time_list:
            time_list.append(quiz_date)

    for i in time_list:
        month = str(i).split('-')[1]
        day = str(i).split('-')[2]

        dt = await generate_date(month, day)
        general_text += f'\n<b>{dt}</b>\n'
        for row in rows:
            quiz_date = str(row['quiz_time']).split(' ')[0]
            if quiz_date == i:
                location = await select_location_by_id(int(row['location_id']))
                quiz_name = await select_quiz_name_by_id(int(row['quiz_id']))
                quiz_time = str(row["quiz_time"]).split(' ')[1]
                hh = quiz_time.split(':')[0]
                mm = quiz_time.split(':')[1]

                general_text += f'– {quiz_name[0]["name"]} [{row["tag"]}] - {hh}:{mm}, {location[0]["name"]}\n'

    return general_text


async def generate_quiz_by_(rows: dict):
    general_text = ''
    time_list = []

    for date in rows:
        parts = date.split('/')
        time_part = parts[1]
        date = time_part.split(' ')[0]
        if not date in time_list:
            time_list.append(date)

    time_list.sort()

    for i in time_list:
        month = str(i).split('-')[1]
        day = str(i).split('-')[2]
        dt = await generate_date(month, day)
        general_text += f'\n<b>{dt}</b>\n'
        for row in rows:
            parts = row.split('/')
            time_part = parts[1]
            quiz_date = time_part.split(' ')[0]

            if quiz_date == i:
                name = str(str(row).split('/')[0]).split(':')[0]
                title = str(str(row).split('/')[0]).split(':')[1]
                location = str(str(row).split('/')[0]).split(':')[2]
                if 'München' in location:
                    location = 'Munchen'
                hours_minutes = str(str(row).split('/')[1]).split(' ')[1]
                general_text += f'<code>– {name} [{title}] - {hours_minutes}, {location}</code>\n'
    return general_text


async def generate_date(month, day):
    months = {
        '01': 'января',
        '02': 'февраля',
        '03': 'марта',
        '04': 'апреля',
        '05': 'мая',
        '06': 'июня',
        '07': 'июля',
        '08': 'августа',
        '09': 'сентября',
        '10': 'октября',
        '11': 'ноября',
        '12': 'декабря'
    }

    n_m = months[month]

    text = f'{day} {n_m}'

    return text