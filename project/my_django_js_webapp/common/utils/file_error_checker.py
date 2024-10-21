import librosa
import os

def file_error_checker(path):
    """
    실험 패키지 버전
    librosa==0.10.2.post1
    
    입력 파라미터 : 파일경로
    예시 : file_error_checker('path/to/sound.wav')

    출력 파라미터 : 에러코드 리스트반환
    예시 : 
        에러가 없을 경우 빈 리스트 반환 
            return []
        에러가 존재 할 경우 해당하는 에러코드 반환
            return ['E131', 'E141']   

    --------- 코드표----------
    데이터 타입  | 코드  | 내용
    -----------------------------
    공통       | E000 | 정상 파일
    소리       | E101 | 소리 포맷 오류 
    소리       | E111 | 소리 길이 짧음(1초 이하)
    소리       | E112 | 소리 길이 김 (10분 이상) 
    소리       | E121 | 소리 볼륨 작음 (-?? DB 이하)        
    소리       | E131 | 소리 샘플 주기(Sample Rate) 9600 미만        
    소리       | E132 | 소리 샘플 주기(Sample Rate) 96000 초과        
    소리       | E141 | 채널 수 에러 (1채널)        
    동영상      | E201 | 동영상 포맷 오류        
    동영상      | E211 | 동영상 길이 소리데이터와 상이
    동영상      | E221 | 동영상 화면 크기 오류        
    동영상      | E222 | 동영상 종횡비 오류 (640x480, 1200x1400)
    빔포밍      | E321 | 빔포밍 크기 오류 (40x30)        
    """
        
    _, ext = os.path.splitext(path)
    errors = []
    
    if ext in ['.wav']: errors += wav_file_error_checker(path)
    elif ext in ['.mp4']: errors += video_file_error_checker(path)

    if len(errors) == 0:
        errors.append('E000')
                
    return errors


def video_file_error_checker(path):
    # 미구현
    return []


def wav_file_error_checker(path):
    errors = []
    try:
        signals, sample_rate = librosa.load(path, sr=None, mono=False)
    except:
        # 소리 파일 에러
        return ['E101']

    # 소리파일 플레이시간
    if len(signals.shape) == 2:
        channel = signals.shape[0]
        duration = signals.shape[1] / sample_rate
    else:
        channel = 1
        duration = signals.shape[0] / sample_rate
    
    if duration < 1.:  errors.append('E111')     # 1초 미만
    elif duration > 600. : errors.append('E112') # 10분(600초) 초과 
    
    rms = (signals ** 2) ** 0.5  # rms 계산   
    if rms.max() < 0.: errors.append('E121')  # rms 최대치로 소리 볼륨 체크
    
    if sample_rate < 9600: errors.append('E131')  # 소리 샘플 주기(sample_rate) 9600 미만
    elif sample_rate > 96000: errors.append('E132')  # 소리 샘플 주기(sample_rate) 96000 초과

    if channel != 1:  errors.append('E141') # 채널 수 에러(1채널이 아님)
    
    return errors