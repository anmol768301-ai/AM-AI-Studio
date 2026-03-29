import os
from flask import Flask, render_template, request, send_file
from moviepy import VideoFileClip
import moviepy.video.fx as fx

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return "File nahi mili!", 400
        
    video_file = request.files['video']
    input_path = os.path.join(UPLOAD_FOLDER, "in_" + video_file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, "out_" + video_file.filename)
    
    try:
        video_file.save(input_path)

        # 1 Minute ki video ke liye Smart Processing
        with VideoFileClip(input_path) as clip:
            # Step 1: Resolution thoda kam karein taaki server na phate (480p)
            if clip.height > 480:
                clip = clip.resized(height=480)
            
            # Step 2: AI Speed Effect
            final_clip = clip.with_effects([fx.MultiplySpeed(1.5)])
            
            # Step 3: Fast Rendering Settings
            final_clip.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac",
                preset="ultrafast", # Sabse tez mode
                bitrate="1000k",    # File size chhota rakhne ke liye
                logger=None,
                threads=1
            )

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        if os.path.exists(input_path): os.remove(input_path)
            
