import argparse
import subprocess
import os

SILENCE_THRESHOLD = -50

parser = argparse.ArgumentParser(description='Trim start splash screen from video')
parser.add_argument('--input', type=str, help='input video file path')
parser.add_argument('--output_wav', type=str, help='output audio file path')
parser.add_argument('--output_mp4', type=str, help='output video file path')

# default entrypoint
if __name__ == "__main__":
    args = parser.parse_args()

    f_in = os.path.abspath(args.input)
    f_out_wav = os.path.abspath(args.output_wav)
    f_out_mp4 = os.path.abspath(args.output_mp4)
    
    # Extract trimmed audio from video
    command = f'ffmpeg -v error -stats -i {f_in} -af silenceremove=1:0:{SILENCE_THRESHOLD}dB -ab 160k -acodec pcm_s16le -ar 44100 -vn {f_out_wav}'
    res = subprocess.call(command, shell=True)
    if res != 0:
        exit(res)
    
    # Calculate audio duration difference
    command = f'ffprobe -v error -stats -i {f_in} -show_entries format=duration -of csv="p=0"'
    res = subprocess.check_output(command, shell=True)
    original_duration = float(res.decode('utf-8').strip())

    command = f'ffprobe -v error -stats -i {f_out_wav} -show_entries format=duration -of csv="p=0"'
    res = subprocess.check_output(command, shell=True)
    trimmed_duration = float(res.decode('utf-8').strip())

    duration_diff = original_duration - trimmed_duration
    print(f"Duration difference: {duration_diff}")

    # Trim video
    command = f'ffmpeg -v error -stats -i {f_in} -ss {duration_diff} -c copy {f_out_mp4}'
    res = subprocess.call(command, shell=True)
    exit(res)
    