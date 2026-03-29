import os
from flask import Flask, render_template, request, send_file
from moviepy import VideoFileClip
import moviepy.video.fx as fx

app = Flask(__name__)

# Render ke liye sabse safe temporary folder
UPLOAD_FOLDER = '/tmp'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return "File nahi mili!", 400
        
    video_file = request.files['video']
    input_path = os.path.join(UPLOAD_FOLDER, "input_" + video_file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, "edited_" + video_file.filename)
    
    try:
        video_file.save(input_path)

        # Smart Processing for 1-minute videos
        with VideoFileClip(input_path) as clip:
            # Resolution fix: Naye version mein .h use hota hai
            if clip.h > 480:
                clip = clip.resized(height=480)
            
            # AI Speed Effect (1.5x)
            final_clip = clip.with_effects([fx.MultiplySpeed(1.5)])
            
            # Safe Rendering Settings
            final_clip.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac",
                preset="ultrafast",
                logger=None,
                threads=1,
                bitrate="1500k" # Quality aur size ka balance
            )

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        # Taki humein asli galti pata chale
        return f"Editing Error: {str(e)}", 500
    finally:
        # Memory saaf karna zaroori hai
        if os.path.exists(input_path): os.remove(input_path)
            
