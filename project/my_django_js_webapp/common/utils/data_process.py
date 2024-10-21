import soundfile as sf
import librosa
import math
import os

def data_process(src_path, dst_path, **args):
    '''
    실험 패키지 : 
    soundfile==0.12.1
    librosa==0.10.2.post1

    
    데이터 가공작업시 
    원천데이터의 입력경로
    가공완료된 데이터의 출력경로
    무슨 가공을 할건지 현재 자르는 작업만하지만 
    추가될 가능성이 존재하기에 **args로 인자확인

    입력인자
    src_path : 가공작업할 대상 소리파일 경로
    dst_path : 가공작업이 완료되어 저장될 경로
    
    자르는 작업은 'slice'로 시작초, 끝초를 줌
    slice={'start':2.5, 'end':5.5}

    data_process('01_01_1204_231011_0154.wav', 'sliced_wav5.wav', slice={'start':2.5, 'end':5.5})
    
    '''

    _, ext = os.path.splitext(src_path)
    if ext in ['.wav']:
        if 'slice' in args:
            wav_data_slice(src_path, dst_path, args['slice']['start'], args['slice']['end'])


def wav_file_save(dst_path, signal, sample_rate):
    sf.write(dst_path, signal, sample_rate, format='WAV', endian='LITTLE', subtype='PCM_16') 
    return True


def sound_data_slice(signal, sample_rate, start_second, end_second):
    start_index = math.floor(start_second * sample_rate)
    end_index = math.floor(end_second * sample_rate)
    return signal[start_index:end_index]


def wav_data_slice(src_path, dst_path, start_second, end_second):
    signal, sample_rate = librosa.load(src_path, sr=None)
    sliced_signal = sound_data_slice(signal, sample_rate, start_second, end_second)
    wav_file_save(dst_path, sliced_signal, sample_rate)
    