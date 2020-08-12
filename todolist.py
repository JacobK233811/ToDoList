
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f'{self.task}. {self.deadline.day} {self.deadline.strftime("%b")}'


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

start_screen = ['1) Today\'s tasks', "2) Week's tasks", '3) All tasks', '4) Missed tasks', '5) Add task', '6) Delete task', '0) Exit']
i = 0
no_entry = True

today = datetime.today()


def day_tasks(relevant_day=today.date()):
    days_of_the_week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    weekday = days_of_the_week.get(relevant_day.weekday())
    print(f"{weekday} {relevant_day.day} {relevant_day.strftime('%b')}:")
    if no_entry:
        return "Nothing to do!"
    return session.query(Table).filter(Table.deadline == relevant_day).all()


while i < 20:
    i += 1
    for item in start_screen:
        print(item)
    num = input()
    if num == '1':
        print(day_tasks())
        print('\n')
    elif num == '2':
        days_ahead = 0
        while days_ahead < 7:
            chosen_day = today.date() + timedelta(days=days_ahead)
            print(day_tasks(chosen_day))
            days_ahead += 1
            print('\n')
    elif num == '3':
        print('All tasks:')
        for task in session.query(Table).order_by(Table.deadline).all():
            print(task)
        print('\n')
    elif num == '4':
        print('Missed tasks:')
        rows = session.query(Table).filter(Table.deadline < today.date()).all()
        if len(rows) == 0:
            print('Nothing is missed!')
            continue
        for task in session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all():
            print(task)
        print('\n')
    elif num == '5':
        no_entry = False
        task_name = input('Enter task')
        task_date = datetime.strptime(input('Enter deadline'), '%Y-%m-%d')
        new_row = Table(task=task_name, deadline=task_date)
        session.add(new_row)
        session.commit()
        print('The task has been added!\n')
    elif num == '6':
        print('Choose the number of the task you want to delete:')
        rows = session.query(Table).order_by(Table.deadline).all()
        for task in rows:
            print(task)
        index = int(input())
        for i, task in enumerate(rows, 1):
            if i == index:
                specific_row = rows[i-1]
                session.delete(specific_row)
                session.commit()
    elif num == '0':
        print('Bye!')
