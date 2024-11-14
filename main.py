from PIL import Image, ImageFont, ImageDraw
import os

class CertificateGenerator:
    def __init__(self, template_path):
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file not found: {template_path}")
        self.template = Image.open(template_path)
        self.WIDTH, self.HEIGHT = self.template.size
        
        
        os.makedirs("out", exist_ok=True)
        
        
        self.REGULAR_FONT = ImageFont.truetype("./font/Arial.ttf", 40)
        self.BOLD_FONT = ImageFont.truetype("./font/Arial_Bold.ttf", 42)
        self.FONT_COLOR = "#5E113D"  
        
    def generate_certificate(self, name, output_dir="out"):
        
        image = self.template.copy()
        draw = ImageDraw.Draw(image)
        
        
        prefix = "This is to certify that "
        suffix = " has successfully attended a talk on "
        talk_title = '"_____________________________"'
        location = " at\nShri Madhwa Vadiraja Institute of Technology and Management, Bantakal"
        date = "on ___________ __, ____."
        
       
        start_y = self.HEIGHT * 0.5
        line_spacing = 52  
        
        
        current_y = start_y
        
        
        prefix_bbox = draw.textbbox((0, 0), prefix, font=self.REGULAR_FONT)
        name_bbox = draw.textbbox((0, 0), name, font=self.BOLD_FONT)
        suffix_bbox = draw.textbbox((0, 0), suffix, font=self.REGULAR_FONT)
        
        total_width = (prefix_bbox[2] + name_bbox[2] + suffix_bbox[2])
        start_x = (self.WIDTH - total_width) / 2
        
        # Draw prefix
        draw.text((start_x, current_y), prefix, font=self.REGULAR_FONT, fill=self.FONT_COLOR)
        current_x = start_x + prefix_bbox[2]
        
        # Draw name in bold
        draw.text((current_x, current_y), name, font=self.BOLD_FONT, fill=self.FONT_COLOR)
        current_x += name_bbox[2]
        
        # Draw suffix
        draw.text((current_x, current_y), suffix, font=self.REGULAR_FONT, fill=self.FONT_COLOR)
        
        # Draw talk title on the same line
        current_y += line_spacing
        talk_bbox = draw.textbbox((0, 0), talk_title, font=self.REGULAR_FONT)
        talk_x = (self.WIDTH - talk_bbox[2]) / 2
        draw.text((talk_x, current_y), talk_title, font=self.REGULAR_FONT, fill=self.FONT_COLOR)
        
        # Draw location
        current_y += line_spacing
        location_bbox = draw.textbbox((0, 0), location, font=self.REGULAR_FONT)
        location_x = (self.WIDTH - location_bbox[2]) / 2
        draw.text((location_x, current_y), location, font=self.REGULAR_FONT, fill=self.FONT_COLOR, align="center")
        
        # Draw date
        current_y += line_spacing * 1.7
        date_bbox = draw.textbbox((0, 0), date, font=self.REGULAR_FONT)
        date_x = (self.WIDTH - date_bbox[2]) / 2
        draw.text((date_x, current_y), date, font=self.REGULAR_FONT, fill=self.FONT_COLOR)
        
        # Save the certificate
        output_path = os.path.join(output_dir, f"{name}_certificate.png")
        image.save(output_path)
        return output_path

    def generate_bulk_certificates(self, names):
        
        generated_files = []
        for name in names:
            try:
                output_path = self.generate_certificate(name)
                generated_files.append(output_path)
                print(f'Generated certificate for: {name}')
            except Exception as e:
                print(f'Error generating certificate for {name}: {str(e)}')
        
        print(f"Successfully generated {len(generated_files)} certificates.")
        return generated_files

def main():
    try:
        with open("names.txt", "r") as file:
            names = [line.strip() for line in file.readlines() if line.strip()]
        
        if not names:
            print("No names found in the text file.")
            return

        generator = CertificateGenerator("template.png")
        generated_files = generator.generate_bulk_certificates(names)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
