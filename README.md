## Môi trường ảo (Virtual Environment) độc lập
- [x] [virtualenv](https://pypi.org/project/virtualenv/)

### Cài đặt
```angular2html
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Cập nhật requirements.txt
```angular2html
pip freeze > requirements.txt
```

### Thoát môi trường ảo
```angular2html
deactivate
```

## Chạy môi trường ảo
```angular2html
source venv/bin/activate
```

## Tạo file .env và copy nội dung dưới đâys
```angular2html
DEBUG = True
SECRET_KEY = 'django-insecure-%g@5(_f=9b*ty$8ft!ubh&it3%vukt9#x(_8&%w$a7rydyfhl2'
ALLOWED_HOSTS = ['*']

/*Social Google*/
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '562191817247-v64b85etbr1j9dbq0ug0d91cuvm9pi1n.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

/*Social Facebook*/
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''

/*Chỉ dành cho MySQL DATABASE*/
DB_NAME = 'database'
DB_USER = 'root'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_PORT = 'port'
