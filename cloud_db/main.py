#
# Copyright 2022. Huawei Technologies Co., Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import asyncio
import datetime

from agconnect.common_server import logger
from agconnect.common_server import logging_config
from agconnect.database_server import CloudDBZoneQuery
from cloud_db_zone_wrapper import CloudDbZoneWrapper
from book_info import BookInfo


def start():
    obj_wrapper = CloudDbZoneWrapper("clientDE", "DE")
    book_info_list = obj_wrapper.get_books_list()
    book = obj_wrapper.get_single_book()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(obj_wrapper.delete_all_books(BookInfo))
    loop.run_until_complete(obj_wrapper.upsert_book(book))
    loop.run_until_complete(obj_wrapper.upsert_book(book_info_list))
    loop.run_until_complete(obj_wrapper.query_all_books())

    try:
        cloud_db_zone_query = CloudDBZoneQuery.where(BookInfo).less_than(
            "price", 50)
        res = loop.run_until_complete(obj_wrapper.query_books(cloud_db_zone_query))
        print(res)
    except Exception as err:
        logger.warning(err)

    loop.run_until_complete(obj_wrapper.query_books_with_order())
    loop.run_until_complete(obj_wrapper.query_books_start_at())
    loop.run_until_complete(obj_wrapper.query_average())

    try:
        date_obj = datetime.datetime.now()
        cloud_db_zone_query = CloudDBZoneQuery.where(BookInfo).greater_than_equal_to("publishTime", date_obj)
        loop.run_until_complete(obj_wrapper.delete_over_due_books(cloud_db_zone_query))
    except Exception as err:
        logger.warning(err)

    loop.run_until_complete(obj_wrapper.delete_book(book))
    loop.run_until_complete(obj_wrapper.delete_book(book_info_list))


start()
