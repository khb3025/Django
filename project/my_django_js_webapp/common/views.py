from django.shortcuts import render, redirect
import datetime, xlsxwriter, uuid, logging, traceback
from django.conf import settings
from sound.models import Metadata
from django.http import Http404, HttpResponse, JsonResponse, HttpRequest
from django.core.files.storage import FileSystemStorage
from django.core.files import File


log = logging.getLogger(__name__)


def index(request):
    return redirect('/api/login_view')

def go_main(request):
    return render(request, 'main.html')


def sample_page(request):
    return render(request, 'sample.html')

def sample_excel_download(request):

    data_list = list(Metadata.objects.all().values('cre_dt', 'data_set_idx', 'version'))

    excel_header_list = [
        '일자',
        'idx',
        'version'
    ]

    sheet_name = 'sample_list'

    save_path, save_name = excel_download(data_list=data_list, excel_header_list=excel_header_list, sheet_name=sheet_name)

    return JsonResponse({'success': True, 'save_path': save_path, 'file_name': save_name})


# Create your views here.
def excel_download(data_list: list, excel_header_list: list, sheet_name: str) -> str:
    '''공통 excel download

    Args:
        data_list (list): excel로 만들 데이터
        excel_header_list (list): 데이터 column 명 data_list의 컬럼 순서와 맞아야 한다.
        sheet_name (str): file 명, excel sheet 명

    Returns:
        save_path (str): excel파일이 저장된 위치
    '''

    save_name = sheet_name + '_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')) + '.xlsx'
    save_path = settings.EXCEL_URL + save_name
    wb = xlsxwriter.Workbook(save_path)
    ws = wb.add_worksheet(sheet_name)
    
    excel_column_list = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
    *data_column_list, = data_list[0]

    header_format = wb.add_format({
        'border': 1,
        'pattern': 1,
        'bg_color': 'E0E0E0',
    })

    header_column_list = excel_column_list[0:len(excel_header_list)]
    
    for col_order, col_alphabet in enumerate(header_column_list):
        ws.write_string(col_alphabet+'2', excel_header_list[col_order], header_format)

    sheet_row_idx = 3
    
    row_format = wb.add_format({'border': 1})
    max_col_widths = [0] * len(excel_header_list)
    
    for data in data_list:
        for col_order, col_alphabet in enumerate(header_column_list):
            cell_value = str(data[data_column_list[col_order]])
            ws.write_string(col_alphabet+str(sheet_row_idx), cell_value, row_format)
            max_col_widths[col_order] = max(max_col_widths[col_order], len(cell_value))
        sheet_row_idx += 1
    
    for col_order, col_alphabet in enumerate(header_column_list):
        ws.set_column(col_alphabet+':'+col_alphabet, max_col_widths[col_order]+15)  # 엑셀 열 여유공간 15px 추가
   
    wb.close()
    save_path = settings.EXCEL_DOWNLOAD_URL + save_name

    return save_path, save_name


def file_upload(file_reg_gb: str, file: File, file_real_name: str, file_ext: str, file_size: str, target_pk: str, reg_user_no: str):
    '''파일 객체를 받아 서버에 저장한다.

    Args:
        file_reg_gb (str): 파일을 저장시키는 테이블 구분
        file (File): File 객체
        file_real_name (str): file 업로드시, 이름
        file_ext (str): file 확장자
        file_size (str): file 크기
        target_pk (str): 파일을 저장시킬때의 테이블 번호
        reg_user_no (str): 등록 회원 번호

    Returns:
        True or False: 업로드 성공시, True 실패시, False를 반환
    '''

    save_path = settings.UPLOAD_URL


    file_name = str(uuid.uuid4()).replace('-', '')

    try:
        fs = FileSystemStorage(
            location=save_path
        )

        fs.save(file_name + '.' + '', file)

        return True
        
    except Exception as e:
        log.info( traceback.format_exc() )
        log.info('save_path :::::::::: %s', save_path)

        return False
