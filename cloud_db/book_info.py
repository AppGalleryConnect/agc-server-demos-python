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

class BookInfo:
    id = None
    bookName = None
    author = None
    price = None
    publisher = None
    publishTime = None
    shadowFlag = None

    @staticmethod
    def get_field_type_map():
        field_type_map = {"id": "Integer", "bookName": "String", "author": "String", "price": "Double",
                          "publisher": "String", "publishTime": "Date", "shadowFlag": "Boolean"}
        return field_type_map

    @staticmethod
    def get_class_name():
        return "BookInfo"

    @staticmethod
    def get_primary_key_list():
        primary_key_list = ["id"]
        return primary_key_list

    @staticmethod
    def get_index_list():
        index_list = ["bookName,price,id", "bookName"]
        return index_list

    @staticmethod
    def get_encrypted_field_list():
        encrypted_field_list = []
        return encrypted_field_list

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_book_name(self, book_name):
        self.bookName = book_name

    def get_book_name(self):
        return self.bookName

    def set_author(self, author):
        self.author = author

    def get_author(self):
        return self.author

    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price

    def set_publisher(self, publisher):
        self.publisher = publisher

    def get_publisher(self):
        return self.publisher

    def set_shadow_flag(self, shadow_flag):
        self.shadowFlag = shadow_flag

    def set_publish_time(self, publish_time):
        self.publishTime = publish_time

    def get_publish_time(self):
        return self.publishTime
