from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os

# Initialize the Flask app and set the template folder to '../front'
app = Flask(__name__, template_folder='../front')

# Route to display the form (GET request)
@app.route('/')
def index():
    return render_template('index.html')

# Route to generate the certificate (POST request)
@app.route('/generate', methods=['POST'])
def generate_certificate():
    try:
        # Debugging Step 1: Check if form data is received
        print("Form Received:", request.form)
        
        name = request.form.get('name', '').strip()
        print("Extracted Name:", name)
        
        if not name:
            return "Error: Name is required", 400

        # Use absolute paths to avoid issues
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(base_dir, 'template.png')  # Same folder as app.py
        output_folder = os.path.join(base_dir, 'certificates')
        output_path = os.path.join(output_folder, f"{name}_certificate.png")

        # Debugging Step 2: Check if template exists
        if not os.path.exists(template_path):
            print(f"Error: Template not found at {template_path}")
            return "Error: Certificate template missing", 500

        # Ensure certificates directory exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Load the template image
        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)

        # Define the confined frame for the name (adjust as needed)
        max_width = 600  # Maximum width of the frame in pixels
        max_height = 200  # Maximum height of the frame in pixels (for multi-line if needed)
        text_position = (800, 800)  # Starting position (x, y)

        # Font setup
        font_path = "arial"  # Using default system font "arial" (Pillow will look for it in the system)
        initial_font_size = 300 # Starting font size
        font = ImageFont.truetype(font_path, initial_font_size)

        # Function to adjust font size to fit within max_width
        def get_adjusted_font(name, font_path, initial_size, max_width):
            font_size = initial_size
            font = ImageFont.truetype(font_path, font_size)
            text_bbox = draw.textbbox((0, 0), name, font=font)
            text_width = text_bbox[2] - text_bbox[0]  # Right - Left
            text_height = text_bbox[3] - text_bbox[1]  # Bottom - Top
            
            # Reduce font size until it fits within max_width
            while text_width > max_width and font_size > 20:  # Minimum font size of 20
                font_size -= 5  # Decrease font size incrementally
                font = ImageFont.truetype(font_path, font_size)
                text_bbox = draw.textbbox((0, 0), name, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

            return font, text_width, text_height

        # Get adjusted font for the name
        font, text_width, text_height = get_adjusted_font(name, font_path, initial_font_size, max_width)

        # Center the text within the frame (optional)
        x_position = text_position[0] + (max_width - text_width) // 2
        y_position = text_position[1]

        # Draw the name on the certificate
        draw.text((x_position, y_position), name, font=font, fill="black")

        # Save the generated certificate
        img.save(output_path)
        print(f"Certificate Saved: {output_path}")

        # Send the generated certificate to the user
        return send_file(output_path, mimetype='image/png', as_attachment=True, download_name=f"{name}_certificate.png")

    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return f"Internal Server Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)