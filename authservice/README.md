# Python_Server_SDK_AuthService_Demo

## Introduction

Auth Service helps you quickly build a secure and reliable user authentication system for your app by directly
integrating
cloud-based Auth Service capabilities into your app. Auth Service provides an SDK and backend services, supports
multiple
authentication modes, and provides a powerful management console, enabling you to easily develop and manage user
authentication.
The Auth Service SDK supports multiple platforms and programming languages, and allows users to enjoy a consistent
sign-in
experience using the same user identity across various device types. As a serverless service, Auth Service can
automatically
adapt to other serverless services. You can protect user data security in the serverless services
by defining simple security rules.

## Preparing the Environments

* Before using the auth server sdk, your server needs support Python 3.7 or higher.

## Getting Started

Before running the auth server sdk, you need to:

1. If you do not have a HUAWEI Developer account, you need
   to [register an account](https://developer.huawei.com/consumer/en/doc/start/registration-and-verification-0000001053628148)
   and pass identity verification.
2. Use your account to sign in
   to [AppGallery Connect](https://developer.huawei.com/consumer/cn/service/josp/agc/index.html#/), create a project.
3. Go to Project settings > Server SDK, click Create under API client, then click Download credential.
4. Save the downloaded authentication credential file agc-apiclient-xxx-xxx.json to the specified path. The file will be
   used during SDK initialization in [main.py](./authservice/main.py).
5. Install AGC Pyhon Server SDK by following command:
      ```bash
      pip install agconnect
	```
6. Run the following code in terminal in the demo path, and demo will start.
   ```bash
   python main.py
   ```
 
 More about details  
     [Auth-Server-Introduction](https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-Guides/agc-get-started-server-0000001058092593#section1778162811430)

## Sample Code

Sample code: main.py

## Question or issues

If you have questions about how to use AppGallery Connect Demos, try the following options:

* [Stack Overflow](https://stackoverflow.com/) is the best place for any programming questions. Be sure to tag your
  question with `AppGallery`.
* [Huawei Developer Forum](https://forums.developer.huawei.com/forumPortal/en/home) AppGallery Module is great for
  general questions, or seeking recommendations and opinions.

If you run into a bug in our samples, please submit an [issue](https://github.com/AppGalleryConnect/agc-demos/issues) to
the Repository. Even better you can submit a [Pull Request](https://github.com/AppGalleryConnect/agc-demos/pulls) with a
fix.

## License

This quickstart is licensed under the [Apache License, version 2.0](http://www.apache.org/licenses/LICENSE-2.0).