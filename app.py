from flask import Flask, render_template, request, send_file
import os
import imageio_ffmpeg
from moviepy.editor import VideoFileClip

# --- FFMPEG ERROR FIX ---
# Ye hissa MoviePy ko batata hai ki ffmpeg kahan chhupa hai
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
# ------------------------

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return "Video select nahi ki!", 400
    
    file = request.files['video']
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, "ai_edited_" + file.filename)
    
    file.save(input_path)

    try:
        # Video processing shuru
        clip = VideoFileClip(input_path)
        
        # AI Effect: Speed 1.2x karna
        final_clip = clip.speedx(1.2)
        
        # Phone par render karne ke liye settings
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        clip.close()
        return send_file(output_path, as_attachment=True)
        
    except Exception as e:
        return f"Editing Error: {str(e)}", 500

if __name__ == '__main__':
    # Phone ke liye 0.0.0.0 aur port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
