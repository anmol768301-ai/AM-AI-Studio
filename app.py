import os
from flask import Flask, render_template, request, send_file
from moviepy import VideoFileClip
import moviepy.video.fx as fx

app = Flask(__name__)

# Render ke liye /tmp folder sabse best hai
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

        # Video ko memory-efficient tarike se process karein
        with VideoFileClip(input_path) as clip:
            # Low quality resize taaki server crash na ho
            small_clip = clip.resized(height=360) 
            final_clip = small_clip.with_effects([fx.MultiplySpeed(1.5)])
            
            # Sabse light settings
            final_clip.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac",
                preset="ultrafast",
                logger=None,
                threads=1 # Zyada threads se 502 error aata hai
            )

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        # Files delete karna zaroori hai memory bachane ke liye
        if os.path.exists(input_path): os.remove(input_path)
            
