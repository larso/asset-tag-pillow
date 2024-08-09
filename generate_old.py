from PIL import Image, ImageDraw, ImageFont
import random
import datetime

def generate_asset_tag():
    current_year = datetime.datetime.now().year
    random_number = random.randint(100000, 999999)
    return f"AV-{current_year}-{random_number}"

def load_and_prepare_logo(logo_path, target_size):
    image = Image.new('RGB', target_size, color='white')
    draw = ImageDraw.Draw(image)

    try:
        logo = Image.open(logo_path)
        print(f"Logo mode: {logo.mode}, Size: {logo.size}")

        if logo.mode not in ('RGB', 'RGBA'):
            logo = logo.convert('RGBA')
        
        logo = logo.resize(target_size)
        
        # Paste the logo onto the white background
        if logo.mode == 'RGBA':
            image.paste(logo, (0, 0), logo)
        else:
            image.paste(logo, (0, 0))
    except Exception as e:
        print(f"Error loading logo: {e}")
        # Draw a placeholder if logo can't be loaded
        draw.rectangle([0, 0, target_size[0], target_size[1]], outline="black", width=2)
        draw.text((10, target_size[1]//2), "Logo", fill="black")

    return image

def create_asset_tag_image(logo_path):
    # Create a new image with a white background
    img_width, img_height = 300, 400
    image = Image.new('RGB', (img_width, img_height), color='white')
    
    # Load and prepare the logo
    logo_size = (img_width, img_width)
    logo_image = load_and_prepare_logo(logo_path, logo_size)
    
    # Paste the logo image at the top of our main image
    image.paste(logo_image, (0, 0))
    
    # Create a draw object
    draw = ImageDraw.Draw(image)
    
    # Draw a horizontal line
    line_y = img_width + 20
    draw.line([(50, line_y), (img_width - 50, line_y)], fill="black", width=2)
    
    # Load a font
    font_size = 36
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Generate the asset tag
    asset_tag = generate_asset_tag()
    
    # Calculate text position
    left, top, right, bottom = font.getbbox(asset_tag)
    text_width = right - left
    text_height = bottom - top
    text_x = (img_width - text_width) // 2
    text_y = line_y + 20
    
    # Draw the asset tag text
    draw.text((text_x, text_y), asset_tag, font=font, fill='black')
    
    # Save the image
    image.save('asset_tag.png')
    print("Asset tag image created: asset_tag.png")

# Path to your logo file
logo_path = './logo.png'

# Create the asset tag image
create_asset_tag_image(logo_path)