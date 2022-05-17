## O'rnatish

`git clone https://github.com/iamzuxmaster/django-cfg-synaptic.git`

*Linux:*

`virtualenv venv && source venv/bin/activate`

*Windows: GitBashdan:*

`virtualenv venv && source venv/Scripts/activate`

`pip install -r requeirements.txt`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver`

## **Dramatiq ishlash uchun**

Dramatiq konfiguratsiyalari tayyor.

Default Broker: [Dramatiq.Redis](https://dramatiq.io/_modules/dramatiq/brokers/redis.html).

Ishga tushurish: `python manage.py rundramatiq`

default settings:

`DRAMATIQ_BROKER = { "BROKER": "dramatiq.brokers.redis.RedisBroker", "OPTIONS": { "url": "redis://localhost:6379", }, "MIDDLEWARE": [ "dramatiq.middleware.Prometheus", "dramatiq.middleware.AgeLimit", "dramatiq.middleware.TimeLimit", "dramatiq.middleware.Callbacks", "dramatiq.middleware.Retries", "django_dramatiq.middleware.DbConnectionsMiddleware", "django_dramatiq.middleware.AdminMiddleware", ] }`

# Reset email

startapp: reset

models:
**user** = paroli unutlgan user emaili bog'lanadi.
**hash** = vaqtinchalik 32xonali hash code
**complete** = parol tiklangandan kn True ga otadi.
**date_created** = hash qachon jo'natilgani va real vaqtni solishtirish uchun.Vaqt 1soat.

Hozirda reset_password beta test holatida.Email kiritish uchun: `templates/reset/index.html`

Emailga jo'natilgan html kodi: `templates/reset/send_email.html`

Emailga jo'natilgan kodga kirgandan so'ng parrollarni almashtirish uchun: `templates/reset/reset_password.html`

reset.views sinxron ishlaydi.Email tiklashni bosilganda Django Emailga xabar jo'natayotgan vaqt qotib qoladi.Shu sababdan Django vazifani tasks.py (Dramatiq) ga jo'natadi.Kiritilgan Email rostan ham bazadan topilsagina emailga xabar yozadi.Emaillar huddi django-reset-email ga o'xshab nastroyka qilinadi.

`SMTP_SSL = "smtp.gmail.com"` <- emailimiz smpt serveri.[< Qolganlari >](https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html)

`SMTP_PORT = 465 `

`SMTP_LOGIN = "sardorbeksabitovich@gmail.com" ` <- email pochtamiz.Rasmiy apilardan foydalanilgan va parollarni ishonish mumkin.

`SMTP_PASSWORD = "40221533"` <- Email pochtamiz paroli.

# Chat (Alpha)

Chat [python-socketio django-example](https://github.com/miguelgrinberg/python-socketio/tree/main/examples/server/wsgi/django_example) dan foydalangan holda yasalgan.

Chat hozirda alfa test holatida.Va undan faqat account.role == 'developer' dagilar foydalana oladi.


# Django-Ninja

Assosan Telegram Bot yoki shunga o'xshash ochiq Apilar uchun qulay interfeyzli Framework framework default o'rnatilgan.

Api uchun mahsus control.api fayli yaratilgan. To'liq [Dokumentatsiya.](https://django-ninja.rest-framework.com/)
