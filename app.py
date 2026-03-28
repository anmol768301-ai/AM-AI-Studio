import os
from flask import Flask, render_template, request, send_file
from moviepy import VideoFileClip
import moviepy.video.fx as fx

app = Flask(__name__)

# Folder settings
UPLOAD_FOLDER = '/tmp' # Render ke liye /tmp zyada fast aur safe hai

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return "Video file nahi mili!", 400
        
    video_file = request.files['video']
    if video_file.filename == '':
        return "Koi file select nahi ki!", 400

    input_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, "ai_edited_" + video_file.filename)
    
    try:
        # File save karein
        video_file.save(input_path)

        # Video process karein
        with VideoFileClip(input_path) as clip:
            # Speed increase 1.5x (AI Effect)
            final_clip = clip.with_effects([fx.MultiplySpeed(1.5)])
            
            # Low resolution rendering taaki white page na aaye
            final_clip.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac",
                temp_audiofile='/tmp/temp-audio.m4a',
                remove_temp=True,
                preset="ultrafast", # Isse fast processing hogi
                threads=4
            )

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"Editing Error: {str(e)}", 500
    finally:
        # Purani files saaf karein taaki memory full na ho
        if os.path.exists(input_path):
            os.remove(input_path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
