import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from card import card,db

card.config.from_object("config.Config")

migrate = Migrate(card,db)
manager = Manager(card)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()