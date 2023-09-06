import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendRecoverEmail(sender_email, receiver_email, subject, password, smtpDomain, smtpPort, urlDomain, recoverId):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    html = """\
    <!DOCTYPE html>
        <html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <meta name="x-apple-disable-message-reformatting">
            <title></title>
            <!--[if mso]>
            <noscript>
                <xml>
                    <o:OfficeDocumentSettings>
                        <o:PixelsPerInch>96</o:PixelsPerInch>
                    </o:OfficeDocumentSettings>
                </xml>
            </noscript>
            <![endif]-->
            <style>
                table, td, div, h1, p {font-family: Arial, sans-serif;}
            </style>
        </head>
        <body style="margin:0;padding:0;">
            <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#ffffff;">
                <tr>
                    <td align="center" style="padding:0;">
                        <table role="presentation" style="width:650px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
                            <tr>
                                <td align="center" style="padding:40px 0 30px 0;background:black;">
                                    <img src="https://i.postimg.cc/SNJCG72Y/homepage-Logo.png" width="300" style="height:auto;display:block">
                                </td>
                            </tr>
                            <tr>
                                <td style="padding:36px 30px 42px 30px;">
                                    <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                                        <tr>
                                            <td style="padding:0 0 12px 0;color:#153643;">
                                                <h1 style="font-size:24px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Reset your JustBeat password</h1>
                                                <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">We heard that you lost your JustBeat password.
        <br>
        Don’t worry! You can use the following button to reset your password:</p>
                                                <p style="text-align:center; margin:0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;"><a target="_blank" href="""+urlDomain+"""/createNewPasswordRecover?recoverId="""+recoverId+"""" style="background-color:#28a745 !important;color:#fff;text-decoration:none;position:relative;display:inline-block;font-size:inherit;font-weight:500;line-height:1.5;white-space:nowrap;vertical-align:middle;cursor:pointer;border-radius:.5em;-webkit-appearance:none;transition:background-color .2s cubic-bezier(0.3, 0, 0.5, 1);font-family:-apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif, Color UI !important;padding:.75em 1.5em;border:1px solid #28a745;" class="yiv5573766756btn yiv5573766756btn-primary yiv5573766756btn-large">Reset your password</a></p>
                                            </td>
                                        </tr>				
                                    </table>
                                    <p style="margin:0">If you don’t use this link within 1 hour, it will expire.</p>
        <p style="margin:0">To get a new password reset link, visit: <a href="""+urlDomain+"""/passwordRecover">"""+urlDomain+"""/passwordRecover</a></p>
        <p style="margin-bottom:0px;">Thank you,</p>
        <h4 style="margin:0px;">The JustBeat Team</h4>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
    """

    part = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtpDomain, smtpPort, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )