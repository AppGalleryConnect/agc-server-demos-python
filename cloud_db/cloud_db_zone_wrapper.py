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

from datetime import datetime, timedelta, timezone

from agconnect.common_server import AGCClient
from agconnect.common_server import CredentialParser
from agconnect.database_server import AGConnectCloudDBException
from agconnect.database_server import CloudDBZoneConfig
from agconnect.database_server import CloudDBZoneQuery
from agconnect.database_server import AGConnectCloudDB
from agconnect.database_server import TransactionFunction, Transaction
from agconnect.common_server import logger

from book_info import BookInfo


class CloudDbZoneWrapper:

    def __init__(self, client_name, region):
        self.client_name = client_name
        self.region = region
        try:
            zone_name = "QuickStartDemo"
            credential_path = CredentialParser.to_credential(
                "[PATH]/agconnect_credentials.json")
            AGCClient.initialize(self.client_name, credential_path, self.region)
            agc_client = AGCClient.get_instance(self.client_name)
            logger.info(f"name {agc_client.get_name()}")
            AGConnectCloudDB.initialize(agc_client)
            cloud_db_zone_config = CloudDBZoneConfig(zone_name)
            self.cloud_db_zone = AGConnectCloudDB.get_instance(agc_client).open_cloud_db_zone(cloud_db_zone_config)
        except Exception as err:
            logger.error(err)

    async def upsert_book(self, book_info):
        if not self.cloud_db_zone:
            logger.info("CloudDBClient is null, try re-initialize it")
            return
        try:
            resp = await self.cloud_db_zone.execute_upsert(book_info)
            print(resp)
            logger.info(f'The number of upsert books is: {resp}')
        except Exception as err:
            logger.warning(f'upsertInfoBook=> {err}')

    async def delete_book(self, book_info):
        if not self.cloud_db_zone:
            logger.info("CloudDBClient is null, try re-initialize it")
            return
        try:
            resp = await self.cloud_db_zone.execute_delete(book_info)
            logger.info(f'The number of delete books is: {resp}')
        except Exception as err:
            logger.warning(f'deleteInfoBook=> {err}')

    async def delete_all_books(self, book_info):
        if not self.cloud_db_zone:
            logger.info("CloudDBClient is null, try re-initialize it")
            return
        try:
            resp = await self.cloud_db_zone.execute_delete_all(book_info)
            logger.info(f'The number of delete all books is: {resp}')
        except Exception as err:
            logger.warning(f'deleteAllInfoBook=> {err}')

    async def query_all_books(self):
        if not self.cloud_db_zone:
            logger.info("CloudDBClient is null, try re-initialize it")
            return
        try:
            cloud_db_zone_query = CloudDBZoneQuery.where(BookInfo)
            resp = await self.cloud_db_zone.execute_query(cloud_db_zone_query)
            len(resp.get_snapshot_objects())
            logger.info(f'The number of query table is: {len(resp.get_snapshot_objects())}')
        except Exception as err:
            logger.warning(f'queryAllInfo=> {err}')

    async def query_books(self, cloud_db_zone_query):
        if not self.cloud_db_zone:
            logger.info("CloudDBClient is null, try re-initialize it")
            return
        try:
            resp = await self.cloud_db_zone.execute_query(cloud_db_zone_query)
            print(len(resp.get_snapshot_objects()))
            logger.info(f'The number of query table is: {len(resp.get_snapshot_objects())}')
        except Exception as err:
            logger.warning(f'queryAllInfo=> {err}')

    async def query_books_with_order(self):
        if not self.cloud_db_zone:
            logger.info("CloudDBClient is null, try re-initialize it")
            return
        try:
            cloud_db_zone_query = CloudDBZoneQuery.where(BookInfo).order_by_desc("price").limit(3)
            resp = await self.cloud_db_zone.execute_query(cloud_db_zone_query)
            logger.info(f'The number of query table is: {len(resp.get_snapshot_objects())}')

        except Exception as err:
            logger.warning(f'queryAllInfo=> {err}')

    async def query_books_start_at(self):
        obj = BookInfo()
        obj.set_id(5)
        obj.set_book_name("The Red And Black")
        obj.set_price(10.99)
        try:
            cloud_db_zone_query = CloudDBZoneQuery.where(BookInfo).order_by_asc("bookName"). \
                order_by_asc("price").start_at(obj)
            resp = await self.cloud_db_zone.execute_query(cloud_db_zone_query)
            print(len(resp.get_snapshot_objects()))
            logger.info(f'The number of query table is: {len(resp.get_snapshot_objects())}')

        except Exception as err:
            logger.warning(f'queryAllInfo=> {err}')

    async def query_average(self):
        try:
            cloud_db_zone_query = CloudDBZoneQuery.where(BookInfo)
            resp = await self.cloud_db_zone.execute_average_query(cloud_db_zone_query, "price")
            logger.info(f'The average price of all books is: {resp}')
        except Exception as err:
            logger.warning(f'queryAllInfo=> {err}')

    async def delete_over_due_books(self, cloud_db_zone_query):
        try:
            transaction_function_obj = TransactionFunction()

            async def apply(transaction: Transaction):
                try:
                    data = await transaction.execute_query(cloud_db_zone_query)
                    logger.info(f'query entityone num: {str(len(data))}')
                except AGConnectCloudDBException as error:
                    logger.error(error)
                    return False
                return True

            transaction_function_obj.apply = apply
            res = await self.cloud_db_zone.run_transaction(transaction_function=transaction_function_obj)
            print(res)
            logger.info(f"the transaction result: {res}")
        except AGConnectCloudDBException as err:
            logger.error(err.get_error_message())

    @staticmethod
    def get_single_book():
        obj3 = BookInfo()
        obj3.set_id(3)
        obj3.set_book_name("Les Fleurs du mal")
        obj3.set_author("Charles Pierre Baudelaire")
        obj3.set_publisher("Auguste Poulet-Malassis")
        obj3.set_price(30.99)
        date = CloudDbZoneWrapper.timezone_utc()
        obj3.set_publish_time(date)
        return obj3

    @staticmethod
    def get_books_list():
        obj1 = BookInfo()
        obj1.set_id(1)
        obj1.set_book_name("Harry Potter1")
        obj1.set_author("J. K. Rowling")
        obj1.set_publisher("Bloomsbury Publishing (UK)")
        obj1.set_price(80.99)
        date = CloudDbZoneWrapper.timezone_utc()
        obj1.set_publish_time(date)

        obj2 = BookInfo()
        obj2.set_id(2)
        obj2.set_book_name("Murder on the Orient Express")
        obj2.set_author("Agatha Christie")
        obj2.set_publisher("Collins Crime Club")
        obj2.set_price(50.99)
        date = CloudDbZoneWrapper.timezone_utc()
        obj2.set_publish_time(date)

        obj3 = BookInfo()
        obj3.set_id(2)
        obj3.set_book_name("Les Fleurs du mal")
        obj3.set_author("Charles Pierre Baudelaire")
        obj3.set_publisher("Auguste Poulet-Malassis")
        obj3.set_price(30.99)
        date = CloudDbZoneWrapper.timezone_utc()
        obj3.set_publish_time(date)

        obj4 = BookInfo()
        obj4.set_id(2)
        obj4.set_book_name("The Moon and Sixpence")
        obj4.set_author("William Somerset Maugham")
        obj4.set_publisher("Heinemann UK")
        obj4.set_price(40.99)
        date = CloudDbZoneWrapper.timezone_utc()
        obj4.set_publish_time(date)

        obj5 = BookInfo()
        obj5.set_id(2)
        obj5.set_book_name("The Red And Blacks")
        obj5.set_author("Stendhal")
        obj5.set_publisher("A. Levasseur")
        obj5.set_price(10.99)
        date = CloudDbZoneWrapper.timezone_utc()
        obj5.set_publish_time(date)

        obj_list = [obj1, obj2, obj3, obj4, obj5]
        return obj_list

    @staticmethod
    def timezone_utc():
        time = datetime.now(timezone.utc)
        time_obj = time + timedelta(seconds=1 * 10000)
        return time_obj
