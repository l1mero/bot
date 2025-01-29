import json

from nicegui import ui
from db import users
from db.models.user import User
from bson import json_util

def parse_json(user: dict):
    user['_id'] = str(user['_id'])
    user['date'] = str(user['date'])
    return user


async def users_page():
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'Object ID', 'checkboxSelection': True, 'field': '_id', 'filter': 'agTextColumnFilter', 'floatingFilter': True,
             'sortable': "true"},
            {'headerName': 'Telegram ID', 'field': 'tg_id', 'filter': 'agTextColumnFilter', 'floatingFilter': True,
             'sortable': "true"},
            {'headerName': 'Registration date', 'field': 'date', 'filter': 'agNumberColumnFilter', 'floatingFilter': True,
             'sortable': "true"},
        ],
        'rowData': [parse_json(user) for user in await users.find_all()],
        "pagination": "true",
        "paginationAutoPageSize": "true",
        'rowSelection': 'multiple',
    }).classes('max-h-300').style("min-height: 75vh")