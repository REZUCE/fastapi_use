# Файл для регистрации всех моделей
from app.users.models import Users
from app.events.models import Events
from app.infrastructure.models_relations import user_event_table

# Список всех моделей, который можно использовать в Alembic и других местах
all_models = [Users, Events, user_event_table]
