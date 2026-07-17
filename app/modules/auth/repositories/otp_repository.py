from sqlalchemy import select

from app.models import OTPVerification
from app.models.auth.otp_verification import OTPPurpose
from app.modules.auth.repositories import BaseRepository


class OTPRepository(BaseRepository[OTPVerification]):

    def get_by_email_purpose(
        self,
        email: str,
        purpose: OTPPurpose
    ) -> OTPVerification | None:

        return self.db.scalar(
            select(OTPVerification).where(
                OTPVerification.email == email,
                OTPVerification.purpose == purpose
            )
        )

    def create(
        self,
        otp_verification: OTPVerification,
    ) -> OTPVerification:

        self.db.add(otp_verification)

        return otp_verification

    def delete(
        self,
        otp_verification: OTPVerification,
    ) -> None:

        self.db.delete(otp_verification)