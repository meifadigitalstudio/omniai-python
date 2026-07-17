from pathlib import Path

from fastapi_mail import (
    ConnectionConfig,
    FastMail,
    MessageSchema,
    MessageType,
)
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core import settings
from app.thirdparty.mail import EmailSchema


BASE_DIR = Path(__file__).resolve().parent

TEMPLATE_DIR = BASE_DIR / "templates"

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


conf = ConnectionConfig(

    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,

    MAIL_FROM=settings.MAIL_FROM,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,

    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,

    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,

    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


class EmailService:

    def __init__(self):

        self.mail = FastMail(conf)

    @property
    def MAIL_CC_LIST(self) -> list[str]:

        if not self.MAIL_CC:
            return []

        return [
            x.strip()
            for x in self.MAIL_CC.split(",")
            if x.strip()
        ]


    @property
    def MAIL_BCC_LIST(self) -> list[str]:

        if not self.MAIL_BCC:
            return []

        return [
            x.strip()
            for x in self.MAIL_BCC.split(",")
            if x.strip()
        ]
        
    async def send(
        self,
        email: EmailSchema,
    ):

        template = env.get_template(
            email.template_name
        )

        html = template.render(
            **email.context
        )

        message = MessageSchema(
            subject=email.subject,
            recipients=email.to,
            cc=settings.MAIL_CC_LIST,
            bcc=settings.MAIL_BCC_LIST,
            body=html,
            subtype=MessageType.html,
            attachments=email.attachments or [],
        )

        await self.mail.send_message(message)