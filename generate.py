from PIL import Image, ImageDraw, ImageFont
import segno
import random
import datetime
import io
import logging

url = "https://asset-tag.arkivverket.no/asset"

def generate_asset_id() -> str:
    current_year = datetime.datetime.now().year
    random_number = random.randint(1000, 9999)
    return f"{current_year}-{random_number}"


def load_and_prepare_logo(logo_path: str, target_height: int) -> Image:
    try:
        logo = Image.open(logo_path)
        logging.debug(f"Input logo: {logo.mode}, Size: {logo.size}")
        if logo.mode not in ('RGB', 'RGBA'):
            logo = logo.convert('RGBA')
        
        aspect_ratio = logo.width / logo.height
        new_width = int(target_height * aspect_ratio)
        logo = logo.resize((new_width, target_height))
        logging.debug(f"Prepared logo: {logo.mode}, Size: {logo.size}")
        return logo
    except Exception as e:
        print(f"Error loading logo: {e}")
        exit(1)


def create_qr_code(asset_id: str, size: int) -> Image:
    tag = f"{url}/{asset_id}"
    qr = segno.make(tag)
    buffer = io.BytesIO()
    qr.save(buffer, kind='png', border=2)
    buffer.seek(0)
    qr_image = Image.open(buffer)
    qr_image = qr_image.resize((size, size))
    return qr_image


def create_asset_tag(logo_path: str) -> Image:
    
    asset_id = generate_asset_id()
    
    # Set up dimensions
    img_width, img_height = 800, 200
    padding = 20
    mpadding = int(20 * 1.5)
    logo_height = img_height - 2 * padding

    # Create base image
    image = Image.new('RGB', (img_width, img_height), color='white')

    # Load and paste logo
    logo = load_and_prepare_logo(logo_path, logo_height)
    image.paste(logo, (padding, padding), logo)

    # Draw vertical dividing line
    divider_x = logo.width + padding + mpadding
    draw = ImageDraw.Draw(image)
    draw.line([(divider_x, mpadding), (divider_x, img_height - mpadding)], fill='black', width=2)

    # Create and paste QR code
    qr_size = logo_height
    qr_x = divider_x + mpadding
    qr_code = create_qr_code(asset_id, logo_height)
    image.paste(qr_code, (qr_x, padding))

    # Create an asset id text. Rotate it 90deg
    text_x = qr_x + qr_code.width + int(padding/3)
    font_size = 28
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    txt_bbox = font.getbbox(asset_id)
    img_txt = Image.new('RGB', (txt_bbox[2],txt_bbox[3]), color="white")
    draw_txt = ImageDraw.Draw(img_txt)
    draw_txt.text((0,0), asset_id, font=font, fill='black')
    img_rotate = img_txt.rotate(90, expand=1)
    #img_rotate.save("debug_text.png")
    
    # Paste rotated text into image at correct height
    text_y = int((img_height - img_rotate.height) / 2)
    image.paste(img_rotate, (text_x, text_y))

    # Crop image, then return it
    img_end = text_x + img_rotate.width + padding
    return image.crop((0, 0, img_end, image.height))

# Usage
logo_path = './logo.png'  # Replace with your logo path
asset_tag = create_asset_tag(logo_path)
asset_tag.save('asset_tag.png')
print(f"Asset tag created")
