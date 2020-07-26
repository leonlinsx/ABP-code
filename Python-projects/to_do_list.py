# jetbrains project
# to do list with menu

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import sys

# create db file
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

# All model classes should inherit from the DeclarativeMeta class that is returned by declarative_base():
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html
Base = declarative_base()

# create table class
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

class ToDo:
    def __init__(self):
        self.choice = None
        self.session = None

    def main(self):
        self.database()
        self.print_menu()
        self.choice = input()
        print("")
        day_of = datetime.today().date()  # only interested in date, not time
        if self.choice == "1":
            self.print_today_tasks(day_of)
        elif self.choice == "2":
            self.print_week_tasks(day_of)
        elif self.choice == "3":
            self.print_all_tasks()
        elif self.choice == "4":
            self.print_missed_tasks(day_of)
        elif self.choice == "5":
            self.add_tasks()
        elif self.choice == "6":
            self.delete_tasks()
        elif self.choice == "0":
            self.exit_menu()

    def database(self):
        # create table
        Base.metadata.create_all(engine)

        # create session
        Session = sessionmaker(bind=engine)
        self.session = Session()
        return True

    def print_menu(self):
        print("")
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")
        return True

    def print_today_tasks(self, day_of):
        # return all rows as list, filtered for date
        rows = self.session.query(Table).filter(Table.deadline == day_of).all()
        print(f"Today {day_of.day} {day_of.strftime('%b')}:")
        if len(rows) >= 1:
            for row in rows:
                print(f"{row.id}. {row.task}")
        else:
            print("Nothing to do!")
        return self.main()  # to keep the while loop going

    def print_week_tasks(self, day_of):
        for i in range(7):
            wk_day_of = day_of + timedelta(days=i)
            rows = self.session.query(Table).filter(Table.deadline == wk_day_of).all()
            print("")
            # get day, date, month
            print(f"{wk_day_of.strftime('%A')} {wk_day_of.day} {wk_day_of.strftime('%b')}:")
            if len(rows) >= 1:
                for row in rows:
                    print(f"{row.id}. {row.task}")
            else:
                print("Nothing to do!")
        return self.main()  # to keep the while loop going

    def print_all_tasks(self):
        # order all available tasks
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        # don't want to use row id, use the count
        if len(rows) >= 1:
            for count, row in enumerate(rows):
                print(f"{count + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        else:
            print("Nothing to do!")
        return self.main()  # to keep the while loop going

    def print_missed_tasks(self, day_of):
        print("Missed tasks:")
        rows = self.session.query(Table).filter(Table.deadline < day_of).all()
        if len(rows) >= 1:
            for count, row in enumerate(rows):
                print(f"{count + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        else:
            print("Nothing is missed!")
        return self.main()  # to keep the while loop going

    def add_tasks(self):
        task_name = input("Enter task\n")
        task_deadline = datetime.strptime(input("Enter deadline\n"), '%Y-%m-%d')
        new_row = Table(task=task_name,
                        deadline=task_deadline)
        self.session.add(new_row)
        self.session.commit()
        print("The task has been added!")
        return self.main()  # to keep the while loop going

    def delete_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print("Chose the number of the task you want to delete:")
        if len(rows) >= 1:
            for count, row in enumerate(rows):
                print(f"{count + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        else:
            print("No tasks to delete!")
        # can use the index within rows, rather than row.id
        del_row = rows[int(input()) - 1]
        self.session.delete(del_row)
        self.session.commit()
        print("The task has been deleted!")
        return self.main()  # to keep the while loop going

    def exit_menu(self):
        print("Bye!")
        sys.exit()

# start to do list
todo = ToDo()
todo.main()



