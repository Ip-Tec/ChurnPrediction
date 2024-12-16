import base64
import random
import string
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from flask import session, request

class CaptchaMiddleware:
    def __init__(self, app):
        self.app = app
        app.before_request(self.before_request)

    # Generate a random CAPTCHA text with a max length of 6
    def generate_captcha_text(self, length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    # Create a CAPTCHA image
    def generate_captcha_image(self, text):
        width, height = 150, 50
        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except IOError:
            font = ImageFont.load_default()

        # Add random noise
        for _ in range(random.randint(100, 200)):
            draw.point((random.randint(0, width), random.randint(0, height)), fill=random.choice(["gray", "black", "blue"]))

        # Draw the text
        if not text:
            text = self.generate_captcha_text()
            session['captcha'] = text

        bbox = draw.textbbox((0, 0), text, font=font)  # Get bounding box of the text
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_position = ((width - text_width) // 2, (height - text_height) // 2)
        draw.text(text_position, text, fill=(0, 0, 0), font=font)

        byte_io = BytesIO()
        image.save(byte_io, 'PNG')
        byte_io.seek(0)
        
        captcha_image_base64 = base64.b64encode(byte_io.read()).decode('utf-8')
        return captcha_image_base64

    # Middleware before each request
    def before_request(self):
        if request.endpoint == 'main.login' and request.method == 'GET':
            captcha_text = self.generate_captcha_text()  # Generate random 6-character CAPTCHA text
            session['captcha'] = captcha_text
            captcha_image_base64 = self.generate_captcha_image(captcha_text)  # Use this text for image generation
            # session['captcha_image'] = captcha_image_base64  # Store the base64-encoded CAPTCHA image in session

    # Serve the CAPTCHA image when requested
    def serve_captcha_image(self):
        captcha_image_base64 = session.get('captcha_image')
        if captcha_image_base64:
            return f'<img src="data:image/png;base64,{captcha_image_base64}" alt="captcha">'
        return 'Captcha image not found', 404
