# from rgb_yuv import rgb_to_yuv
import os

# f5 to run
if __name__ == '__main__':

    option=0
while not option==5:

    print("1. Macroblocks and Motion Vectors")
    print("2. Extract Video and Audio and package into an .mp4")
    print("3. Which broadcasting standards are compatible")
    print("4. Add subtitles")
    print("5. Exit \n")
    option = int(input("Option: "))

    if option == 1:
        print("#Macroblocks and Motion Vectors \n")
        os.system('ffmpeg -flags2 +export_mvs -i video_cut.mp4 -vf codecview=mv=pf+bf+bb video_cut_motion.mp4')

    if option == 2:
        print("#Extract Video and Audio and package into an .mp4 \n")
        os.system('ffmpeg -i video.mp4 -ss 00:00:0.0 -t 00:01:0.0 -an video_cut_1m.mp4')

        os.system('ffmpeg -i video.mp4 -ss 00:00:0.0 -t 00:01:0.0 -vn -acodec mp3 video_cut_1m_mp3.mp3')
        os.system('ffmpeg -i video.mp4 -ss 00:00:0.0 -t 00:01:0.0 -vn -acodec aac -b:a 128k video_cut_1m_aac.aac')

        os.system('ffmpeg -i video_cut_1m.mp4 -i video_cut_1m_mp3.mp3 -i video_cut_1m_aac.aac -map 0 -map 1 -map 2 -c copy final_video.mp4')
        #os.system('ffmpeg -i video_cut_1m.mp4 -i video_cut_1m_mp3.mp3 -i video_cut_1m_aac.aac -map 0 -map 1 -metadata:s:a:0 title="mp3" -map 2 -metadata:s:a:1 title="aac" final_video.mp4')

        #os.system('ffmpeg -i final_video.mp4')
    if option == 3:
        print("#Which broadcasting standards are compatible \n")

        os.system('ffprobe -v error -select_streams v:0 -show_entries stream=codec_name \
            -of default=noprint_wrappers=1:nokey=1 final_video.mp4 >> codecs.txt')

        os.system('ffprobe -v error -select_streams a:0 -show_entries stream=codec_name \
            -of default=noprint_wrappers=1:nokey=1 final_video.mp4 >> codecs.txt')

        os.system('ffprobe -v error -select_streams a:1 -show_entries stream=codec_name \
            -of default=noprint_wrappers=1:nokey=1 final_video.mp4 >> codecs.txt')

        file = open('codecs.txt','r')
        codecs = file.read()
        file.close()
        os.system('rm codecs.txt')

        standards = []
        if ('h264' or 'mpeg2' in codecs) and ('aac' or 'ac3' or 'mp3' in codecs):
            standards.append('DVB')
        if ('h264' or 'mpeg2' in codecs) and ('aac' in codecs):
            standards.append('ISDB')
        if ('h264' or 'mpeg2' in codecs) and ('ac3' in codecs):
            standards.append('ATSC')
        if ('h264' or 'avs' or 'avs+' or 'mpeg2' in codecs) and ('aac' or 'dra' or 'ac3' or 'mp2' or 'mp3' in codecs):
            standards.append('DTMB')

        if(not standards):
            print('ERROR: No standards compatible with the video')
        else:
            print('Video compatible with broadcasting standards: '+str(standards))

    if option == 4:
        print("#Add subtitles \n")
        os.system('wget https://raw.githubusercontent.com/dbarreropl/Video_Encoding_S2/main/subtitles.srt')
        os.system('ffmpeg -i final_video.mp4 -i subtitles.srt -c copy -c:s mov_text final_video_subtitles.mp4')
        os.system('rm subtitles.srt')
