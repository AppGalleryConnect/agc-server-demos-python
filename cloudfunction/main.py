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
import os

from agconnect.common_server import AGCClient
from agconnect.common_server import CredentialParser
from agconnect.cloud_function import AGConnectFunction

AGCClient.initialize("real_cli",
                     credential=CredentialParser.to_credential(
                         (os.path.join(os.path.dirname(__file__), '[PATH]/agconnect_credentials.json'))))
agcFunction = AGConnectFunction.get_instance()


async def my_handler_test():
    value = agcFunction.wrap("callback", "$latest")
    value.set_timeout(20000)
    test_str = "test s string"
    res = await value.call(test_str)
    print(f"res: {res.get_value()}")
    buf = memoryview(bytearray(10))
    res3 = await value.call(buf)
    print(f"res2: {res3.get_value()}")


async def my_handler():
    good_res = {'simple': 'example'}
    test_str = "test s string"
    res = await agcFunction.wrap("callback", "$latest").call(test_str)

    print(f"res: {res.get_value()}")
    assert res.get_value() == good_res


loop = asyncio.get_event_loop()
loop.run_until_complete(my_handler_test())
