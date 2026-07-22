"""
Email service for sending emails to users.

This module provides:
- Email sending functionality using SMTP
- Welcome/registration emails
- Password reset emails
- Error handling for email failures
"""

import logging
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

logger = logging.getLogger(__name__)
load_dotenv()

# Email configuration from environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    plain_text_content: Optional[str] = None,
) -> bool:
    """
    Send an email using SMTP.

    Args:
        to_email: Recipient email address
        subject: Email subject line
        html_content: Email body in HTML format
        plain_text_content: Optional plain text fallback

    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = SENDER_EMAIL
        message["To"] = to_email

        # Add plain text part (fallback)
        if plain_text_content:
            message.attach(MIMEText(plain_text_content, "plain"))

        # Add HTML part
        message.attach(MIMEText(html_content, "html"))

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)

        logger.info(f"Email sent successfully to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP authentication failed: {str(e)}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error while sending email: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while sending email: {str(e)}")
        return False


def send_welcome_email(user_email: str, user_name: Optional[str] = None) -> bool:
    """
    Send a welcome email to newly registered users.

    Args:
        user_email: User's email address
        user_name: User's name (optional, uses email if not provided)

    Returns:
        True if email sent successfully, False otherwise
    """
    name = user_name or user_email.split("@")[0]

    subject = "Welcome to Flight Booking!"

    plain_text = f"""
    Welcome to Flight Booking, {name}!

    Your account has been successfully created.
    You can now log in and start booking flights.

    Best regards,
    Flight Booking Team
    """

    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto;">
                <h2 style="color: #0066cc;">Welcome to Flight Booking!</h2>
                <p>Hello <strong>{name}</strong>,</p>

                <p>Your account has been successfully created. You can now log in to your account and start booking flights.</p>

                <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Account Details:</strong></p>
                    <p>Email: {user_email}</p>
                </div>

                <p>If you have any questions or need assistance, please don't hesitate to contact our support team.</p>

                <p>Happy flying!</p>

                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <footer style="font-size: 12px; color: #666;">
                    <p>Flight Booking Team</p>
                    <p>This is an automated email. Please do not reply to this message.</p>
                </footer>
            </div>
        </body>
    </html>
    """

    return send_email(user_email, subject, html_content, plain_text)


def send_password_reset_email(
    user_email: str, reset_token: str, reset_link: str
) -> bool:
    """
    Send a password reset email to users.

    Args:
        user_email: User's email address
        reset_token: Password reset token
        reset_link: Full URL for password reset link

    Returns:
        True if email sent successfully, False otherwise
    """
    subject = "Password Reset Request - Flight Booking"

    plain_text = f"""
    Password Reset Request

    Click the link below to reset your password:
    {reset_link}

    This link will expire in 24 hours.

    If you didn't request this, please ignore this email.
    """

    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto;">
                <h2 style="color: #0066cc;">Password Reset Request</h2>
                <p>We received a request to reset your password.</p>

                <p style="margin: 30px 0;">
                    <a href="{reset_link}"
                       style="display: inline-block; padding: 10px 20px; background-color: #0066cc;
                              color: white; text-decoration: none; border-radius: 5px;">
                        Reset Your Password
                    </a>
                </p>

                <p style="color: #666; font-size: 12px;">
                    Or copy this link: <br>
                    <code>{reset_link}</code>
                </p>

                <p style="color: #d9534f; margin: 30px 0;">
                    <strong>Note:</strong> This link will expire in 24 hours.
                </p>

                <p>If you didn't request this password reset, please ignore this email.</p>

                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <footer style="font-size: 12px; color: #666;">
                    <p>Flight Booking Team</p>
                </footer>
            </div>
        </body>
    </html>
    """

    return send_email(user_email, subject, html_content, plain_text)


def send_email_confirmation(user_email: str, confirmation_link: str) -> bool:
    """
    Send an email confirmation link to users.

    Args:
        user_email: User's email address
        confirmation_link: Full URL for email confirmation

    Returns:
        True if email sent successfully, False otherwise
    """
    subject = "Confirm Your Email - Flight Booking"

    plain_text = f"""
    Email Confirmation

    Please click the link below to confirm your email address:
    {confirmation_link}

    Thank you!
    """

    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto;">
                <h2 style="color: #0066cc;">Confirm Your Email</h2>
                <p>Thank you for registering with Flight Booking!</p>

                <p>Please click the button below to confirm your email address:</p>

                <p style="margin: 30px 0;">
                    <a href="{confirmation_link}"
                       style="display: inline-block; padding: 10px 20px; background-color: #0066cc;
                              color: white; text-decoration: none; border-radius: 5px;">
                        Confirm Email
                    </a>
                </p>

                <p style="color: #666;">
                    If you didn't create this account, please ignore this email.
                </p>

                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <footer style="font-size: 12px; color: #666;">
                    <p>Flight Booking Team</p>
                </footer>
            </div>
        </body>
    </html>
    """

    return send_email(user_email, subject, html_content, plain_text)
