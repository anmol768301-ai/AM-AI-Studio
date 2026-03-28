import os
from flask import Flask, render_template, request, send_file
from moviepy import VideoFileClip
import moviepy.video.fx as fx

app = Flask(__name__)

# Folders banane ke liye
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    try:
        video_file = request.files['video']
        if video_file:
            input_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
            output_path = os.path.join(UPLOAD_FOLDER, "edited_" + video_file.filename)
            video_file.save(input_path)

            # Naya aur Sahi Tarika: Speed 1.5x karne ke liye
            clip = VideoFileClip(input_path)
            final_clip = clip.with_effects([fx.MultiplySpeed(1.5)])
            
            # Video save karna (Phone support ke liye settings)
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            
            clip.close()
            final_clip.close()

            return send_file(output_path, as_attachment=True)
    except Exception as e:
        return f"Editing Error: {str(e)}"
    
    return "Error: File nahi mili!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
